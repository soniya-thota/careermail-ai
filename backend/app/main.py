from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from app.auth import oauth
from app.config import settings
from app.classifier import classify_email
from app.company_extractor import extract_company
from app.ai_parser import ai_parse_job_email
from bs4 import BeautifulSoup
import requests
import base64

app = FastAPI(title="CareerMail AI Backend")

FRONTEND_URL = "https://careermail-ai.vercel.app"
GMAIL_MESSAGES_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    same_site="none",
    https_only=True,
)


@app.get("/")
def home():
    return {
        "message": "CareerMail AI backend running",
        "status": "ok",
    }


@app.get("/me")
def me(request: Request):
    headers = get_auth_headers(request)

    return {
        "logged_in": headers is not None
    }


@app.get("/login")
async def login(request: Request):
    redirect_uri = f"{settings.BACKEND_URL}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    access_token = token["access_token"]

    request.session["access_token"] = access_token

    return RedirectResponse(url=f"{FRONTEND_URL}?token={access_token}")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=FRONTEND_URL)


def get_auth_headers(request: Request):
    auth_header = request.headers.get("Authorization")

    if auth_header:
        return {
            "Authorization": auth_header
        }

    access_token = request.session.get("access_token")

    if not access_token:
        return None

    return {
        "Authorization": f"Bearer {access_token}"
    }


def extract_headers(headers_list):
    subject = ""
    sender = ""
    date = ""

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

            if mime_type == "text/plain":
                data = part.get("body", {}).get("data")
                body_text += decode_base64url(data)

            elif mime_type == "text/html":
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

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())

    return text


def get_gmail_message_ids(headers, max_results=100):
    response = requests.get(
        GMAIL_MESSAGES_URL,
        headers=headers,
        params={"maxResults": max_results}
    )

    return response.json().get("messages", [])


def get_gmail_message(headers, message_id, message_format="metadata"):
    response = requests.get(
        f"{GMAIL_MESSAGES_URL}/{message_id}",
        headers=headers,
        params={"format": message_format}
    )

    return response.json(), response.status_code


@app.get("/gmail/emails")
def get_gmail_emails(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    messages = get_gmail_message_ids(headers, max_results=100)
    email_results = []

    for msg in messages:
        msg_id = msg["id"]

        email_data, status_code = get_gmail_message(
            headers,
            msg_id,
            message_format="metadata"
        )

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
            "snippet": snippet
        })

    return {
        "count": len(email_results),
        "emails": email_results
    }


@app.get("/analytics")
def analytics(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    messages = get_gmail_message_ids(headers, max_results=100)

    stats = {
        "Application Submitted": 0,
        "Incomplete Application": 0,
        "Recruiter Message": 0,
        "Interview": 0,
        "Offer": 0,
        "Rejection": 0,
        "Online Assessment": 0,
        "General Job Email": 0,
        "Not Job Related": 0
    }

    for msg in messages:
        msg_id = msg["id"]

        email_data, status_code = get_gmail_message(
            headers,
            msg_id,
            message_format="metadata"
        )

        if status_code != 200:
            continue

        headers_list = email_data.get("payload", {}).get("headers", [])
        subject, sender, date = extract_headers(headers_list)
        snippet = email_data.get("snippet", "")

        category = classify_email(subject, sender, snippet)
        stats[category] = stats.get(category, 0) + 1

    return stats


@app.get("/gmail/full-email/{message_id}")
def get_full_email(message_id: str, request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    email_data, status_code = get_gmail_message(
        headers,
        message_id,
        message_format="full"
    )

    if status_code != 200:
        return {
            "error": "Failed to fetch email",
            "status_code": status_code,
            "gmail_response": email_data
        }

    payload = email_data.get("payload", {})
    headers_list = payload.get("headers", [])

    subject, sender, date = extract_headers(headers_list)

    body = extract_email_body(payload)
    clean_body = clean_html(body)
    snippet = email_data.get("snippet", "")

    parsed = ai_parse_job_email(subject, sender, clean_body or snippet, date)
    company = extract_company(sender)

    return {
        "id": message_id,
        "company": company,
        "from": sender,
        "subject": subject,
        "date": date,
        "category": parsed["category"],
        "status": parsed["status"],
        "next_action": parsed["next_action"],
        "summary": parsed["summary"],
        "snippet": snippet,
        "body_preview": clean_body[:3000]
    }


@app.get("/companies")
def companies(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    messages = get_gmail_message_ids(headers, max_results=100)
    company_stats = {}

    for msg in messages:
        msg_id = msg["id"]

        email_data, status_code = get_gmail_message(
            headers,
            msg_id,
            message_format="metadata"
        )

        if status_code != 200:
            continue

        headers_list = email_data.get("payload", {}).get("headers", [])
        subject, sender, date = extract_headers(headers_list)
        snippet = email_data.get("snippet", "")

        category = classify_email(subject, sender, snippet)

        if category == "Not Job Related":
            continue

        company = extract_company(sender)

        if company not in company_stats:
            company_stats[company] = {
                "total": 0,
                "categories": {}
            }

        company_stats[company]["total"] += 1
        company_stats[company]["categories"][category] = (
            company_stats[company]["categories"].get(category, 0) + 1
        )

    sorted_companies = dict(
        sorted(
            company_stats.items(),
            key=lambda item: item[1]["total"],
            reverse=True
        )
    )

    return sorted_companies


def build_applications(headers):
    messages = get_gmail_message_ids(headers, max_results=100)
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

        email_data, status_code = get_gmail_message(
            headers,
            msg_id,
            message_format="full"
        )

        if status_code != 200:
            continue

        payload = email_data.get("payload", {})
        headers_list = payload.get("headers", [])

        subject, sender, date = extract_headers(headers_list)
        snippet = email_data.get("snippet", "")
        body = extract_email_body(payload)
        clean_body = clean_html(body)

        parsed = ai_parse_job_email(subject, sender, clean_body or snippet, date)

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

        current_status = applications[company]["status"]
        new_status = parsed["status"]

        if priority.get(new_status, 0) > priority.get(current_status, 0):
            applications[company]["status"] = new_status
            applications[company]["category"] = parsed["category"]
            applications[company]["last_email_date"] = date
            applications[company]["next_action"] = parsed["next_action"]
            applications[company]["summary"] = parsed["summary"]

    return list(applications.values())


@app.get("/applications")
def applications(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    app_list = build_applications(headers)

    return {
        "count": len(app_list),
        "applications": app_list
    }


@app.get("/job-insights")
def job_insights(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    app_list = build_applications(headers)

    total = len(app_list)

    recruiter_responses = sum(
        1 for app_item in app_list
        if app_item["status"] in ["Recruiter Replied", "Follow-Up Needed", "Interview", "Online Assessment", "Offer"]
    )

    interviews = sum(1 for app_item in app_list if app_item["status"] == "Interview")
    offers = sum(1 for app_item in app_list if app_item["status"] == "Offer")
    rejections = sum(1 for app_item in app_list if app_item["status"] == "Rejected")
    followups = sum(1 for app_item in app_list if app_item["status"] == "Follow-Up Needed")

    active = sum(
        1 for app_item in app_list
        if app_item["status"] not in ["Rejected", "Offer", "Job Alert", "Not Job Related"]
    )

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
        "Follow-Ups Needed": followups
    }