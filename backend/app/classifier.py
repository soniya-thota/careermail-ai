def classify_email(subject, sender, content):
    text = f"{subject} {sender} {content}".lower()

    # Rejections
    if (
        "not selected" in text
        or "unfortunately" in text
        or "not moving forward" in text
        or "move forward with other candidates" in text
        or "we regret to inform you" in text
    ):
        return "Rejection"

    # Interviews
    if (
        "interview" in text
        or "schedule a call" in text
        or "schedule an interview" in text
        or "interview invitation" in text
    ):
        return "Interview"

    # Offers
    if (
        "job offer" in text
        or "offer letter" in text
        or "employment offer" in text
        or "we are pleased to offer" in text
    ):
        return "Offer"

    # Assessments
    if (
        "assessment" in text
        or "coding challenge" in text
        or "online assessment" in text
        or "hackerrank" in text
        or "codesignal" in text
        or "technical assessment" in text
    ):
        return "Online Assessment"

    # Incomplete applications
    if (
        "application is incomplete" in text
        or "incomplete application" in text
        or "your application is incomplete" in text
    ):
        return "Incomplete Application"

    # Recruiters
    if (
        "recruiter" in text
        or "talent acquisition" in text
        or "linkedin" in text
        or "recruiting@" in text
    ):
        return "Recruiter Message"

    # Applications submitted
    if (
        "successfully submitted" in text
        or "thank you for applying" in text
        or "application received" in text
        or "application submitted" in text
    ):
        return "Application Submitted"

    # Job alerts and career emails
    if (
        "job application" in text
        or "careers" in text
        or ".jobs" in text
        or "jobs near you" in text
        or "apply now" in text
        or "is hiring" in text
        or "jobs in" in text
        or "dream jobs" in text
        or "hackathons" in text
        or "jobalert" in text
        or "glassdoor jobs" in text
        or "indeed" in text
        or "unstop" in text
    ):
        return "General Job Email"

    return "Not Job Related"