from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from app.auth import oauth
from app.config import settings
from app.classifier import classify_email
from app.company_extractor import extract_company
import requests
import base64

app = FastAPI(title="CareerMail AI Backend")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)


@app.get("/")
def home():
    return {
        "message": "CareerMail AI backend running",
        "status": "ok",
    }


@app.get("/login")
async def login(request: Request):
    redirect_uri = f"{settings.BACKEND_URL}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")

    request.session["access_token"] = token["access_token"]

    return {
        "message": "Login successful",
        "user": user,
        "has_access_token": True,
    }


def get_auth_headers(request: Request):
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


@app.get("/gmail/emails")
def get_gmail_emails(request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    list_response = requests.get(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages",
        headers=headers,
        params={"maxResults": 10}
    )

    messages = list_response.json().get("messages", [])

    email_results = []

    for msg in messages:
        msg_id = msg["id"]

        detail_response = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
            headers=headers,
            params={"format": "metadata"}
        )

        email_data = detail_response.json()
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

    list_response = requests.get(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages",
        headers=headers,
        params={"maxResults": 50}
    )

    messages = list_response.json().get("messages", [])

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

        detail_response = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
            headers=headers,
            params={"format": "metadata"}
        )

        email_data = detail_response.json()
        headers_list = email_data.get("payload", {}).get("headers", [])

        subject, sender, date = extract_headers(headers_list)
        snippet = email_data.get("snippet", "")

        category = classify_email(subject, sender, snippet)

        stats[category] = stats.get(category, 0) + 1

    return stats


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

            elif "parts" in part:
                body_text += extract_email_body(part)

    return body_text


@app.get("/gmail/full-email/{message_id}")
def get_full_email(message_id: str, request: Request):
    headers = get_auth_headers(request)

    if not headers:
        return {"error": "Not logged in. Please visit /login first."}

    response = requests.get(
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}",
        headers=headers,
        params={"format": "full"}
    )

    email_data = response.json()

    if response.status_code != 200:
        return {
            "error": "Failed to fetch email",
            "status_code": response.status_code,
            "gmail_response": email_data
        }

    payload = email_data.get("payload", {})
    headers_list = payload.get("headers", [])

    subject, sender, date = extract_headers(headers_list)

    body = extract_email_body(payload)
    category = classify_email(subject, sender, body)
    company = extract_company(sender)

    return {
        "id": message_id,
        "company": company,
        "from": sender,
        "subject": subject,
        "date": date,
        "category": category,
        "body_preview": body[:3000]
    }