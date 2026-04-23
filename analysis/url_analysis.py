import re
from urllib.parse import urlparse
from utils.virustotal import check_url


def analyze_urls(body):
    score = 0
    reasons = []

    urls = re.findall(r"https?://[^\s]+", body)

    suspicious_keywords = [
        "login", "verify", "account", "update",
        "secure", "bank", "signin", "confirm"
    ]

    shorteners = [
        "bit.ly", "tinyurl.com", "t.co", "goo.gl"
    ]

    for url in urls:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # -----------------------------
        # 1. HTTP (Weak Signal)
        # -----------------------------
        if parsed.scheme == "http":
            score += 1
            reasons.append(f"{url}: Uses HTTP (unencrypted connection)")

        # -----------------------------
        # 2. Suspicious Structure
        # -----------------------------
        if domain.count('.') > 3:
            score += 2
            reasons.append(f"{url}: Suspicious URL structure")
        
        # -----------------------------
        # 3. IP-based URL
        # -----------------------------
        if re.match(r"\d{1,3}(\.\d{1,3}){3}", domain):
            score += 4
            reasons.append(f"{url}: Uses IP address instead of domain")

        # -----------------------------
        # 4. URL Shortener
        # -----------------------------
        if any(short in domain for short in shorteners):
            score += 3
            reasons.append(f"{url}: Uses URL shortening service")
        
        # -----------------------------
        # 5. Suspicious Keywords
        # -----------------------------
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            score += 2
            reasons.append(f"{url}: Contains phishing-related keywords")
        
        # -----------------------------
        # 6. '@' Obfuscation Trick
        # -----------------------------
        if "@" in url:
            score += 3
            reasons.append(f"{url}: Contains '@' symbol (URL obfuscation)")
        
        # -----------------------------
        # 7. VirusTotal Check
        # -----------------------------
        vt_result = check_url(url)

        if vt_result and vt_result["malicious"] > 0:
            score += 6
            reasons.append(f"{url}: Malicious URL detected (VirusTotal)")

    return score, reasons