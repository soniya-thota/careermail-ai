from collections import Counter
import base64

import requests
from authlib.integrations.base_client.errors import MismatchingStateError
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.ai_copilot import analyze_resume_match
from app.ai_parser import ai_parse_job_email
from app.auth import oauth
from app.classifier import classify_email
from app.company_extractor import extract_company
from app.config import settings
from app.sample_data import SAMPLE_EMAILS

app = FastAPI(
    title="CareerMail AI Backend",
    description="AI-powered job search intelligence APIs for Gmail recruiting emails, application tracking, and resume-job matching.",
    version="2.0.0",
)

GMAIL_MESSAGES_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

allowed_origins = list({
    "http://localhost:5173",
    "http://localhost:3000",
    settings.FRONTEND_URL,
})

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    # Local HTTP OAuth works reliably with Lax. Hosted HTTPS can use None + Secure.
    same_site="none" if settings.BACKEND_URL.startswith("https") else "lax",
    https_only=settings.BACKEND_URL.startswith("https"),
)


class ResumeMatchRequest(BaseModel):
    resume: str
    job_description: str


class CareerAgentRequest(BaseModel):
    resume: str = ""
    job_description: str = ""
    target_role: str = "AI/ML Engineer"


class EmailClassifyRequest(BaseModel):
    subject: str = ""
    sender: str = ""
    body: str = ""
    date: str = ""


@app.get("/")
def home():
    return {
        "message": "CareerMail AI backend running",
        "status": "ok",
        "version": "2.0.0",
        "demo_mode": settings.DEMO_MODE,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/me")
def me(request: Request):
    headers = get_auth_headers(request)
    return {
        "logged_in": headers is not None,
        "demo_mode": settings.DEMO_MODE,
        "privacy_model": "per-user workspace; Gmail data is fetched with the current user token only",
    }


@app.get("/login")
async def login(request: Request):
    redirect_uri = f"{settings.BACKEND_URL}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except MismatchingStateError:
        # Usually caused by blocked/missing session cookies or mixing localhost and 127.0.0.1.
        request.session.clear()
        return RedirectResponse(url=f"{settings.FRONTEND_URL}?auth_error=oauth_state")
    except Exception:
        request.session.clear()
        return RedirectResponse(url=f"{settings.FRONTEND_URL}?auth_error=oauth_failed")

    access_token = token["access_token"]
    request.session["access_token"] = access_token
    return RedirectResponse(url=f"{settings.FRONTEND_URL}?token={access_token}")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=settings.FRONTEND_URL)


def get_auth_headers(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        return {"Authorization": auth_header}

    access_token = request.session.get("access_token")
    if not access_token:
        return None

    return {"Authorization": f"Bearer {access_token}"}


def should_use_demo(headers):
    return settings.DEMO_MODE and headers is None


def extract_headers(headers_list):
    subject, sender, date = "", "", ""
    for h in headers_list:
        name = h.get("name", "").lower()
        value = h.get("value", "")
        if name == "subject":
            subject = value
        elif name == "from":
            sender = value
        elif name == "date":
            date = value
    return subject, sender, date


def decode_base64url(data):
    if not data:
        return ""
    data += "=" * (-len(data) % 4)
    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode("utf-8", errors="ignore")


def extract_email_body(payload):
    body_text = ""
    if "body" in payload and payload["body"].get("data"):
        return decode_base64url(payload["body"]["data"])

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type in ["text/plain", "text/html"]:
                data = part.get("body", {}).get("data")
                body_text += decode_base64url(data)
            elif "parts" in part:
                body_text += extract_email_body(part)
    return body_text


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["style", "script", "head"]):
        tag.decompose()
    return " ".join(soup.get_text(separator=" ").split())


def get_gmail_message_ids(headers, max_results=None):
    response = requests.get(
        GMAIL_MESSAGES_URL,
        headers=headers,
        params={"maxResults": max_results or settings.GMAIL_MAX_RESULTS},
        timeout=20,
    )
    # Avoid crashing the app when a Google token expires or a user is not authorized.
    if response.status_code in (401, 403):
        return []
    response.raise_for_status()
    return response.json().get("messages", [])


def get_gmail_message(headers, message_id, message_format="metadata"):
    response = requests.get(
        f"{GMAIL_MESSAGES_URL}/{message_id}",
        headers=headers,
        params={"format": message_format},
        timeout=20,
    )
    return response.json(), response.status_code


def get_emails_from_gmail(headers):
    messages = get_gmail_message_ids(headers)
    email_results = []
    for msg in messages:
        msg_id = msg["id"]
        email_data, status_code = get_gmail_message(headers, msg_id, message_format="metadata")
        if status_code != 200:
            continue
        headers_list = email_data.get("payload", {}).get("headers", [])
        subject, sender, date = extract_headers(headers_list)
        snippet = email_data.get("snippet", "")
        category = classify_email(subject, sender, snippet)
        company = extract_company(sender)
        email_results.append({
            "id": msg_id,
            "company": company,
            "from": sender,
            "subject": subject,
            "date": date,
            "category": category,
            "snippet": snippet,
        })
    return email_results


def normalize_application_status(category):
    mapping = {
        "Application Submitted": "Applied",
        "Recruiter Message": "Recruiter Replied",
        "Interview": "Interview",
        "Offer": "Offer",
        "Rejection": "Rejected",
        "Online Assessment": "Online Assessment",
        "Incomplete Application": "Follow-Up Needed",
        "General Job Email": "Job Alert",
    }
    return mapping.get(category, category)


def build_applications_from_emails(emails):
    priority = {
        "Offer": 8,
        "Interview": 7,
        "Online Assessment": 6,
        "Follow-Up Needed": 5,
        "Recruiter Replied": 4,
        "Applied": 3,
        "Rejected": 2,
        "Job Alert": 1,
        "Not Job Related": 0,
    }
    applications = {}
    for email in emails:
        if email.get("category") == "Not Job Related":
            continue
        company = email.get("company", "Unknown")
        status = email.get("status") or normalize_application_status(email.get("category"))
        email_item = {
            "id": email.get("id"),
            "subject": email.get("subject"),
            "from": email.get("from"),
            "date": email.get("date"),
            "category": email.get("category"),
            "status": status,
            "next_action": email.get("next_action") or "Review email and update tracker.",
            "summary": email.get("summary") or email.get("snippet", ""),
            "days_since_last_email": email.get("days_since_last_email"),
        }
        if company not in applications:
            applications[company] = {
                "company": company,
                "status": status,
                "category": email.get("category"),
                "last_email_date": email.get("date"),
                "next_action": email_item["next_action"],
                "summary": email_item["summary"],
                "emails": [email_item],
            }
            continue
        applications[company]["emails"].append(email_item)
        if priority.get(status, 0) > priority.get(applications[company]["status"], 0):
            applications[company].update({
                "status": status,
                "category": email.get("category"),
                "last_email_date": email.get("date"),
                "next_action": email_item["next_action"],
                "summary": email_item["summary"],
            })
    return list(applications.values())


def build_applications(headers):
    if should_use_demo(headers):
        return build_applications_from_emails(SAMPLE_EMAILS)

    messages = get_gmail_message_ids(headers)
    applications = {}
    priority = {
        "Offer": 8,
        "Interview": 7,
        "Online Assessment": 6,
        "Follow-Up Needed": 5,
        "Recruiter Replied": 4,
        "Applied": 3,
        "Rejected": 2,
        "Job Alert": 1,
        "Not Job Related": 0,
    }

    for msg in messages:
        msg_id = msg["id"]
        email_data, status_code = get_gmail_message(headers, msg_id, message_format="full")
        if status_code != 200:
            continue
        payload = email_data.get("payload", {})
        subject, sender, date = extract_headers(payload.get("headers", []))
        snippet = email_data.get("snippet", "")
        body = clean_html(extract_email_body(payload))
        parsed = ai_parse_job_email(subject, sender, body or snippet, date)
        if not parsed["is_job_related"]:
            continue
        company = extract_company(sender)
        email_item = {
            "id": msg_id,
            "subject": subject,
            "from": sender,
            "date": date,
            "category": parsed["category"],
            "status": parsed["status"],
            "next_action": parsed["next_action"],
            "summary": parsed["summary"],
            "days_since_last_email": parsed["days_since_last_email"],
        }
        if company not in applications:
            applications[company] = {
                "company": company,
                "status": parsed["status"],
                "category": parsed["category"],
                "last_email_date": date,
                "next_action": parsed["next_action"],
                "summary": parsed["summary"],
                "emails": [email_item],
            }
            continue
        applications[company]["emails"].append(email_item)
        if priority.get(parsed["status"], 0) > priority.get(applications[company]["status"], 0):
            applications[company].update({
                "status": parsed["status"],
                "category": parsed["category"],
                "last_email_date": date,
                "next_action": parsed["next_action"],
                "summary": parsed["summary"],
            })
    return list(applications.values())


@app.get("/gmail/emails")
def get_gmail_emails(request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        return {"count": len(SAMPLE_EMAILS), "emails": SAMPLE_EMAILS, "demo": True}
    if not headers:
        return {"error": "Not logged in. Please visit /login first."}
    emails = get_emails_from_gmail(headers)
    return {"count": len(emails), "emails": emails, "demo": False}


@app.get("/analytics")
def analytics(request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        emails = SAMPLE_EMAILS
    elif headers:
        emails = get_emails_from_gmail(headers)
    else:
        return {"error": "Not logged in. Please visit /login first."}

    categories = [
        "Application Submitted", "Incomplete Application", "Recruiter Message", "Interview", "Offer", "Rejection", "Online Assessment", "General Job Email", "Not Job Related"
    ]
    stats = {category: 0 for category in categories}
    for email in emails:
        stats[email.get("category", "Not Job Related")] = stats.get(email.get("category", "Not Job Related"), 0) + 1
    return stats


@app.get("/gmail/full-email/{message_id}")
def get_full_email(message_id: str, request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        email = next((item for item in SAMPLE_EMAILS if item["id"] == message_id), None)
        if email:
            return email
        return {"error": "Demo email not found"}
    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    email_data, status_code = get_gmail_message(headers, message_id, message_format="full")
    if status_code != 200:
        return {"error": "Failed to fetch email", "status_code": status_code, "gmail_response": email_data}

    payload = email_data.get("payload", {})
    subject, sender, date = extract_headers(payload.get("headers", []))
    clean_body = clean_html(extract_email_body(payload))
    snippet = email_data.get("snippet", "")
    parsed = ai_parse_job_email(subject, sender, clean_body or snippet, date)
    return {
        "id": message_id,
        "company": extract_company(sender),
        "from": sender,
        "subject": subject,
        "date": date,
        "category": parsed["category"],
        "status": parsed["status"],
        "next_action": parsed["next_action"],
        "summary": parsed["summary"],
        "snippet": snippet,
        "body_preview": clean_body[:3000],
    }


@app.get("/companies")
def companies(request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        emails = SAMPLE_EMAILS
    elif headers:
        emails = get_emails_from_gmail(headers)
    else:
        return {"error": "Not logged in. Please visit /login first."}

    company_stats = {}
    for email in emails:
        if email.get("category") == "Not Job Related":
            continue
        company = email.get("company") or extract_company(email.get("from", ""))
        if company not in company_stats:
            company_stats[company] = {"total": 0, "categories": {}}
        company_stats[company]["total"] += 1
        category = email.get("category", "Unknown")
        company_stats[company]["categories"][category] = company_stats[company]["categories"].get(category, 0) + 1

    return dict(sorted(company_stats.items(), key=lambda item: item[1]["total"], reverse=True))


@app.get("/applications")
def applications(request: Request):
    headers = get_auth_headers(request)
    if not headers and not settings.DEMO_MODE:
        return {"error": "Not logged in. Please visit /login first."}
    app_list = build_applications(headers)
    return {"count": len(app_list), "applications": app_list, "demo": should_use_demo(headers)}


@app.get("/job-insights")
def job_insights(request: Request):
    headers = get_auth_headers(request)
    if not headers and not settings.DEMO_MODE:
        return {"error": "Not logged in. Please visit /login first."}

    app_list = build_applications(headers)
    total = len(app_list)
    recruiter_responses = sum(1 for item in app_list if item["status"] in ["Recruiter Replied", "Follow-Up Needed", "Interview", "Online Assessment", "Offer"])
    interviews = sum(1 for item in app_list if item["status"] == "Interview")
    offers = sum(1 for item in app_list if item["status"] == "Offer")
    rejections = sum(1 for item in app_list if item["status"] == "Rejected")
    followups = sum(1 for item in app_list if item["status"] == "Follow-Up Needed")
    active = sum(1 for item in app_list if item["status"] not in ["Rejected", "Offer", "Job Alert", "Not Job Related"])
    response_rate = round((recruiter_responses / total) * 100, 2) if total else 0
    interview_rate = round((interviews / total) * 100, 2) if total else 0
    return {
        "Applications Tracked": total,
        "Recruiter Responses": recruiter_responses,
        "Response Rate": f"{response_rate}%",
        "Interviews": interviews,
        "Interview Rate": f"{interview_rate}%",
        "Offers": offers,
        "Rejections": rejections,
        "Active Applications": active,
        "Follow-Ups Needed": followups,
    }


@app.get("/recruiters")
def recruiters(request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        emails = SAMPLE_EMAILS
    elif headers:
        emails = get_emails_from_gmail(headers)
    else:
        return {"error": "Not logged in. Please visit /login first."}

    recruiter_rows = []
    for email in emails:
        if email.get("category") in ["Recruiter Message", "Interview", "Online Assessment", "Offer"]:
            recruiter_rows.append({
                "company": email.get("company"),
                "sender": email.get("from"),
                "subject": email.get("subject"),
                "date": email.get("date"),
                "category": email.get("category"),
                "next_action": email.get("next_action", "Review and respond if needed."),
            })
    return {"count": len(recruiter_rows), "recruiters": recruiter_rows}


@app.get("/follow-ups")
def follow_ups(request: Request):
    headers = get_auth_headers(request)
    if not headers and not settings.DEMO_MODE:
        return {"error": "Not logged in. Please visit /login first."}
    app_list = build_applications(headers)
    followup_items = [item for item in app_list if item["status"] in ["Follow-Up Needed", "Recruiter Replied", "Interview", "Online Assessment"]]
    return {"count": len(followup_items), "follow_ups": followup_items}


@app.get("/top-companies")
def top_companies(request: Request):
    headers = get_auth_headers(request)
    if should_use_demo(headers):
        emails = SAMPLE_EMAILS
    elif headers:
        emails = get_emails_from_gmail(headers)
    else:
        return {"error": "Not logged in. Please visit /login first."}

    counts = Counter(email.get("company", "Unknown") for email in emails if email.get("category") != "Not Job Related")
    return {"companies": [{"company": company, "emails": count} for company, count in counts.most_common(10)]}


@app.post("/ai/resume-match")
def resume_match(payload: ResumeMatchRequest):
    return analyze_resume_match(payload.resume, payload.job_description)


@app.post("/ai/classify-email")
def classify_email_preview(payload: EmailClassifyRequest):
    parsed = ai_parse_job_email(payload.subject, payload.sender, payload.body, payload.date)
    return {
        **parsed,
        "company": extract_company(payload.sender),
        "input_preview": {"subject": payload.subject, "sender": payload.sender},
    }


@app.post("/ai/career-agent")
def career_agent(payload: CareerAgentRequest):
    match = analyze_resume_match(payload.resume, payload.job_description) if payload.job_description else None
    target = payload.target_role or (match or {}).get("role_focus", "AI/ML Engineer")
    roadmap = [
        {"step": "1", "title": "Target the right roles", "action": f"Apply to {target}, Applied AI Engineer, AI Software Engineer, and AI Data Engineer roles first."},
        {"step": "2", "title": "Lead with flagship projects", "action": "Show CareerMail AI, RAG Job Assistant, and one ML/CV project at the top of GitHub and resume."},
        {"step": "3", "title": "Prepare interview proof", "action": "Create 3 stories: AI feature, backend/API design, and data pipeline/debugging."},
        {"step": "4", "title": "Close skill gaps", "action": "Practice Python DSA, SQL, LLM/RAG fundamentals, and system design basics weekly."},
    ]
    if match and match.get("missing_skills"):
        roadmap.insert(2, {"step": "Skill gap", "title": "Improve job match", "action": "Add truthful evidence for: " + ", ".join(match["missing_skills"][:5])})
    return {
        "target_role": target,
        "positioning": "AI/ML Engineer with strong software engineering and data engineering foundations",
        "match": match,
        "roadmap": roadmap,
        "portfolio_pitch": "Built CareerMail AI, a multi-user AI job search intelligence platform that connects to Gmail, classifies recruiting emails, tracks applications, analyzes resume-job fit, and generates next actions while keeping each user's data private.",
    }


@app.get("/privacy/design")
def privacy_design():
    return {
        "principle": "Every user gets a private workspace.",
        "rules": [
            "Never store Google tokens in frontend code.",
            "Fetch Gmail data only with the authenticated user's token.",
            "Attach user_id to stored rows if a database is added.",
            "Always filter by current_user.id for emails, resumes, applications, and AI outputs.",
            "Provide logout and delete-data controls before public launch.",
        ],
        "tables": {
            "users": ["id", "email", "name"],
            "emails": ["id", "user_id", "sender", "subject", "category", "summary"],
            "applications": ["id", "user_id", "company", "status", "next_action"],
            "resumes": ["id", "user_id", "extracted_text"],
            "ai_outputs": ["id", "user_id", "type", "result_json"],
        },
    }
