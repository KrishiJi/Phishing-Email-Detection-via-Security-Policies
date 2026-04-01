import re
from urllib.parse import urlparse
from utils.virustotal import check_url


def analyze_urls(body):
    score = 0
    reasons = []

    urls = re.findall(r"https?://[^\s]+", body)

    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            score += 2
            reasons.append("Non-HTTPS URL detected")

        if parsed.netloc.count('.') > 3:
            score += 2
            reasons.append("Suspicious URL structure")
        
        vt_result = check_url(url)

        if vt_result and vt_result["malicious"] > 0:
            score += 5
            reasons.append(f"Malicious URL detected: {url}")

    return score, reasons