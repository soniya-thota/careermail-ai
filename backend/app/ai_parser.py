from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

NON_JOB_SENDERS = [
    "quora", "digest", "newsletter", "newsletters-noreply", "youtube", "google alerts",
    "amazon.com", "orders", "shipping", "edclub", "maps", "appointment receipt",
    "bank", "statement", "promo", "promotion", "coupon", "sale", "unsubscribe",
    "security alert", "password reset", "verification code", "student verification",
]

NON_JOB_SUBJECTS = [
    "what is it like", "rip", "daily digest", "weekly digest", "newsletter", "receipt",
    "your order", "delivered", "verify your account", "security alert", "new sign-in",
]

JOB_CONTEXT_WORDS = [
    "application", "applied", "candidate", "recruiter", "recruiting", "talent acquisition",
    "interview", "assessment", "job", "role", "position", "offer", "hiring", "resume",
    "career", "workday", "greenhouse", "lever", "ashby", "smartrecruiters", "icims",
]


def parse_email_date(date_str):
    try:
        parsed = parsedate_to_datetime(date_str)
        if parsed and parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return None


def days_since(date_str):
    parsed = parse_email_date(date_str)
    if not parsed:
        return None
    now = datetime.now(timezone.utc)
    return (now - parsed).days


def is_probably_non_job(subject, sender, text):
    subject_l = (subject or "").lower()
    sender_l = (sender or "").lower()
    text_l = (text or "").lower()

    # If it contains clear job context, do not filter too early.
    if any(word in text_l for word in JOB_CONTEXT_WORDS):
        return False

    if any(word in sender_l for word in NON_JOB_SENDERS):
        return True
    if any(word in subject_l for word in NON_JOB_SUBJECTS):
        return True
    return False


def ai_parse_job_email(subject, sender, body, date):
    text = f"{subject} {sender} {body}".lower()
    days = days_since(date)

    result = {
        "is_job_related": False,
        "category": "Not Job Related",
        "status": "Not Job Related",
        "next_action": "No action needed",
        "confidence": 0.75,
        "summary": "This email does not appear to be related to job search activity.",
        "days_since_last_email": days,
    }

    if is_probably_non_job(subject, sender, text):
        return result

    if any(phrase in text for phrase in [
        "not selected", "not moving forward", "will not be moving forward", "will not move forward",
        "move forward with other candidates", "moving forward with other candidates", "other candidates",
        "unfortunately", "regret to inform", "after careful consideration", "position has been filled",
        "not be proceeding", "will not be proceeding", "not proceed with your application",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Rejection",
            "status": "Rejected",
            "next_action": "No action needed",
            "confidence": 0.95,
            "summary": "The company indicated that they are not moving forward with this application.",
        })
        return result

    if any(phrase in text for phrase in [
        "offer letter", "employment offer", "job offer", "pleased to offer", "we are excited to offer",
        "congratulations on your offer",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Offer",
            "status": "Offer",
            "next_action": "Review offer details and respond before the deadline",
            "confidence": 0.95,
            "summary": "This email appears to contain an offer or offer-related information.",
        })
        return result

    if any(phrase in text for phrase in [
        "online assessment", "coding challenge", "hackerrank", "codesignal", "codility",
        "technical assessment", "take home assignment", "assessment invitation",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Online Assessment",
            "status": "Online Assessment",
            "next_action": "Complete assessment and prepare Python, SQL, and DSA",
            "confidence": 0.9,
            "summary": "This email appears to be related to an online assessment or coding challenge.",
        })
        return result

    if any(phrase in text for phrase in [
        "schedule an interview", "interview invitation", "technical interview", "phone screen",
        "onsite interview", "virtual interview", "meet with the hiring team", "schedule a call",
        "recruiter call", "next round",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Interview",
            "status": "Interview",
            "next_action": "Reply with availability and prepare interview stories",
            "confidence": 0.9,
            "summary": "This email appears to be related to an interview, recruiter screen, or next-round discussion.",
        })
        return result

    if any(phrase in text for phrase in [
        "thank you for applying", "application received", "application submitted", "successfully submitted",
        "we have received your application", "thanks for your application", "thank you for your interest",
    ]):
        status = "Applied"
        next_action = "Wait for response"
        if days is not None and days >= 14:
            status = "Follow-Up Needed"
            next_action = "Follow up optional"
        result.update({
            "is_job_related": True,
            "category": "Application Submitted",
            "status": status,
            "next_action": next_action,
            "confidence": 0.88,
            "summary": "This email confirms that an application was submitted or received.",
        })
        return result

    if any(phrase in text for phrase in [
        "recruiter", "talent acquisition", "talent team", "recruiting@", "sourcer", "hiring team",
        "technical sourcer", "share your resume", "current work authorization",
    ]):
        status = "Recruiter Replied"
        next_action = "Monitor conversation"
        if days is not None and days >= 5:
            status = "Follow-Up Needed"
            next_action = "Follow up soon"
        result.update({
            "is_job_related": True,
            "category": "Recruiter Message",
            "status": status,
            "next_action": next_action,
            "confidence": 0.87,
            "summary": "This email appears to be from a recruiter, sourcer, or hiring team.",
        })
        return result

    if any(phrase in text for phrase in [
        "job alert", "jobs near you", "apply now", "is hiring", "glassdoor jobs", "indeed",
        "linkedin jobs", "career opportunity", "new jobs", "recommended jobs",
    ]):
        result.update({
            "is_job_related": True,
            "category": "General Job Email",
            "status": "Job Alert",
            "next_action": "Review if interested",
            "confidence": 0.76,
            "summary": "This email appears to be a job alert or job recommendation.",
        })
        return result

    return result
