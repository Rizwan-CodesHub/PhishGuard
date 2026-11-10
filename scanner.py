
import re
from urllib.parse import urlparse

def scan_url(url):

    if not url or not url.strip():
        return {
            "score": 0,
            "risk": "Invalid URL",
            "reasons": ["Please enter a website URL."],
            "recommendation": "Enter a valid URL to scan."
        }

    url = url.strip()

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.hostname

        if not domain or "." not in domain:
            raise ValueError("Invalid domain")

    except ValueError:
        return {
            "score": 0,
            "risk": "Invalid URL",
            "reasons": ["The entered URL is not valid."],
            "recommendation": "Check the URL and try again."
        }

    score = 0
    reasons = []

    # 1. Check HTTPS
    if parsed.scheme != "https":
        score += 15
        reasons.append("Website does not use HTTPS.")

    # 2. Check IP address in URL
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        score += 25
        reasons.append("Website uses an IP address instead of a domain name.")

    # 3. Check suspicious keywords
    keywords = [
        "login", "verify", "update", "secure",
        "account", "banking", "password",
        "free", "claim", "prize", "urgent"
    ]

    found_keywords = [
        word for word in keywords
        if word in url.lower()
    ]

    if found_keywords:
        score += min(len(found_keywords) * 5, 20)
        reasons.append(
            "Suspicious keywords found: " + ", ".join(found_keywords)
        )

    # 4. Check URL length
    if len(url) > 75:
        score += 10
        reasons.append("URL is unusually long.")

    # 5. Check @ symbol
    if "@" in url:
        score += 20
        reasons.append("URL contains an @ symbol.")

    # 6. Check multiple subdomains
    if len(domain.split(".")) > 3:
        score += 15
        reasons.append("URL contains multiple subdomains.")

    # 7. Check hyphens in domain
    if "-" in domain:
        score += 10
        reasons.append("Domain contains hyphens.")

    # 8. Check suspicious file extensions
    if parsed.path.lower().endswith(
        (".exe", ".zip", ".scr", ".bat")
    ):
        score += 15
        reasons.append("URL points to a potentially risky file.")

    score = min(score, 100)

    # Determine risk level
    if score < 25:
        risk = "LOW RISK"
        recommendation = "No major warning signs were detected. Still verify the website before sharing information."

    elif score < 50:
        risk = "MEDIUM RISK"
        recommendation = "Be careful. Verify the website's authenticity before proceeding."

    else:
        risk = "HIGH RISK"
        recommendation = "Avoid entering personal information. Verify the website through an official source."

    if not reasons:
        reasons.append("No suspicious patterns detected by the basic scanner.")

    return {
        "score": score,
        "risk": risk,
        "reasons": reasons,
        "recommendation": recommendation
    }
