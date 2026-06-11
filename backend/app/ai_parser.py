from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


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


def ai_parse_job_email(subject, sender, body, date):
    text = f"{subject} {sender} {body}".lower()
    days = days_since(date)

    result = {
        "is_job_related": False,
        "category": "Not Job Related",
        "status": "Not Job Related",
        "next_action": "No action needed",
        "confidence": 0.5,
        "summary": "This email does not appear to be related to job applications.",
        "days_since_last_email": days,
    }

    if any(phrase in text for phrase in [
        "not selected",
        "not moving forward",
        "will not be moving forward",
        "will not move forward",
        "move forward with other candidates",
        "moving forward with other candidates",
        "other candidates",
        "unfortunately",
        "regret to inform",
        "after careful consideration",
        "position has been filled",
        "not be proceeding",
        "will not be proceeding",
        "not proceed with your application",
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
        "offer letter",
        "employment offer",
        "job offer",
        "pleased to offer",
        "we are excited to offer",
        "congratulations on your offer",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Offer",
            "status": "Offer",
            "next_action": "Review offer details",
            "confidence": 0.95,
            "summary": "This email appears to contain an offer or offer-related information.",
        })
        return result

    if any(phrase in text for phrase in [
        "online assessment",
        "coding challenge",
        "hackerrank",
        "codesignal",
        "codility",
        "technical assessment",
        "take home assignment",
        "assessment invitation",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Online Assessment",
            "status": "Online Assessment",
            "next_action": "Complete assessment",
            "confidence": 0.9,
            "summary": "This email appears to be related to an online assessment or coding challenge.",
        })
        return result

    if any(phrase in text for phrase in [
        "schedule an interview",
        "interview invitation",
        "technical interview",
        "phone screen",
        "onsite interview",
        "virtual interview",
        "meet with the hiring team",
        "schedule a call",
        "recruiter call",
        "next round",
    ]):
        result.update({
            "is_job_related": True,
            "category": "Interview",
            "status": "Interview",
            "next_action": "Prepare for interview",
            "confidence": 0.9,
            "summary": "This email appears to be related to an interview, recruiter screen, or next-round discussion.",
        })
        return result

    if any(phrase in text for phrase in [
        "thank you for applying",
        "application received",
        "application submitted",
        "successfully submitted",
        "we have received your application",
        "thanks for your application",
        "thank you for your interest",
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
            "confidence": 0.85,
            "summary": "This email confirms that an application was submitted or received.",
        })
        return result

    if any(phrase in text for phrase in [
        "recruiter",
        "talent acquisition",
        "talent team",
        "recruiting@",
        "sourcer",
        "hiring team",
        "technical sourcer",
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
            "confidence": 0.85,
            "summary": "This email appears to be from a recruiter, sourcer, or hiring team.",
        })
        return result

    if any(phrase in text for phrase in [
        "job alert",
        "jobs near you",
        "apply now",
        "is hiring",
        "glassdoor jobs",
        "indeed",
        "unstop",
        "monster",
        "linkedin jobs",
        "career opportunity",
    ]):
        result.update({
            "is_job_related": True,
            "category": "General Job Email",
            "status": "Job Alert",
            "next_action": "Review if interested",
            "confidence": 0.75,
            "summary": "This email appears to be a job alert or job recommendation.",
        })
        return result

    return result