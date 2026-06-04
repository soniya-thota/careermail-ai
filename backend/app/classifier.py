def classify_email(subject, sender, content):
    text = f"{subject} {sender} {content}".lower()

    # Non-job emails
    if (
        "sheerid" in text
        or "verification services powered by sheerid" in text
        or "student verification" in text
        or "security alert" in text
        or "account recovered" in text
        or "password reset" in text
        or "google account" in text
        or "newsletters-noreply@linkedin.com" in text
        or "accepted your invitation" in text
        or "explore their network" in text
        or "connections, experience" in text
        or "via linkedin <newsletters-noreply@linkedin.com>" in text
    ):
        return "Not Job Related"

    # Rejections
    if (
        "not selected" in text
        or "unfortunately" in text
        or "we regret to inform you" in text
        or "regret to inform" in text
        or "move forward with other candidates" in text
        or "moving forward with other candidates" in text
        or "not moving forward" in text
        or "will not be moving forward" in text
        or "will not move forward" in text
        or "position has been filled" in text
        or "after careful consideration" in text
        or "your application was not selected" in text
        or "we have decided not to move forward" in text
    ):
        return "Rejection"
    
    
    # Interviews
    if (
        "interview" in text
        or "schedule a call" in text
        or "schedule an interview" in text
        or "interview invitation" in text
        or "phone screen" in text
        or "technical interview" in text
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
        or "take home assignment" in text
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
        or "technical recruiter" in text
        or "talent acquisition" in text
        or "talent team" in text
        or "staffing" in text
        or "recruiting@" in text
        or "messaged you" in text
        or "new message awaits your response" in text
    ):
        return "Recruiter Message"

    # Applications submitted
    if (
        "successfully submitted" in text
        or "thank you for applying" in text
        or "application received" in text
        or "application submitted" in text
        or "we have received your application" in text
    ):
        return "Application Submitted"

    # Job alerts
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
        or "recommended jobs" in text
        or "job alert" in text
    ):
        return "General Job Email"

    return "Not Job Related"