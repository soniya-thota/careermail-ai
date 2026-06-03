import re


def extract_company(sender):
    sender = sender.strip()

    # Example:
    # IBM Talent Acquisition <talent@ibm.com>

    if "<" in sender:
        display_name = sender.split("<")[0].strip()

        display_name = re.sub(
            r"(Talent Acquisition|Recruiting|Recruitment|Careers?)",
            "",
            display_name,
            flags=re.IGNORECASE,
        ).strip()

        if display_name:
            return display_name

    # Example:
    # noreply@mail.amazon.jobs

    email_match = re.search(
        r'@([a-zA-Z0-9\-]+)',
        sender
    )

    if email_match:
        company = email_match.group(1)

        return company.capitalize()

    return "Unknown"