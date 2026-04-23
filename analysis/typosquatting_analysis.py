import re
from difflib import SequenceMatcher


# -------------------------------------------------
# Load Trusted Domains
# -------------------------------------------------

def load_trusted_domains():
    try:
        with open("data/trusted_domains.txt", "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []


KNOWN_DOMAINS = load_trusted_domains()


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def normalize_domain(domain):
    domain = domain.lower()

    replacements = {
        "0": "o",
        "1": "l",
        "3": "e",
        "5": "s",
        "7": "t",
        "@": "a"
    }

    for old, new in replacements.items():
        domain = domain.replace(old, new)

    domain = domain.replace("rn", "m")
    domain = domain.replace("vv", "w")

    return domain

def get_base_domain(domain):
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2]  # amazon from amazon.com
    return domain

def extract_domain_from_email(value):
    match = re.search(r'@([A-Za-z0-9.-]+\.[A-Za-z]{2,})', value)
    return match.group(1).lower() if match else None


def extract_domains_from_urls(text):
    return re.findall(r'https?://([A-Za-z0-9.-]+\.[A-Za-z]{2,})', text)


# -------------------------------------------------
# Core Detection Logic
# -------------------------------------------------

def check_domain(domain):
    score = 0
    reasons = []

    suspicious_tlds = ["xyz", "ru", "tk", "ml", "ga", "cf"]

    original = domain.lower()
    base_original = get_base_domain(original)
    normalized_original = normalize_domain(base_original)

    # -----------------------------
    # TLD Check
    # -----------------------------
    tld = original.split(".")[-1]
    if tld in suspicious_tlds:
        score += 2
        reasons.append(f"{domain}: Suspicious TLD used (.{tld})")

    # -----------------------------
    # Hyphen Abuse
    # -----------------------------
    if "-" in original:
        score += 1
        reasons.append(f"{domain}: Hyphenated domain often used in phishing")

    # -----------------------------
    # Excessive Subdomains
    # -----------------------------
    if original.count(".") > 3:
        score += 1
        reasons.append(f"{domain}: Excessive subdomain usage")

    # -----------------------------
    # Compare with Trusted Domains
    # -----------------------------
    best_score = 0
    best_reasons = []
    for legit in KNOWN_DOMAINS:
        temp_score = 0
        temp_reasons = []

        legit_base = get_base_domain(legit)
        normalized_legit = normalize_domain(legit_base)

        # Skip exact match
        if base_original == legit_base:
            continue

        # -----------------------------
        # Similarity Detection
        # -----------------------------
        sim = similarity(normalized_original, normalized_legit)

        if sim >= 0.75 and abs(len(base_original) - len(legit_base)) <= 3:
            temp_score += 5
            temp_reasons.append(
                f"{domain}: Closely resembles trusted domain {legit}"
            )

        # -----------------------------
        # Brand Misuse
        # -----------------------------
        if normalized_legit in normalized_original:
            temp_score += 3
            temp_reasons.append(
                f"{domain}: Misuses brand keyword '{legit_base}'"
            )

        # -----------------------------
        # Brand Extension Attack
        # -----------------------------
        if len(legit_base) > 3 and legit_base in base_original and base_original != legit_base:
            temp_score += 3
            temp_reasons.append(
                f"{domain}: Extends trusted brand '{legit_base}' with extra words"
            )

        # -----------------------------
        # Subdomain Attack
        # -----------------------------
        if legit in original and not original.endswith(legit):
            temp_score += 4
            temp_reasons.append(
                f"{domain}: Uses deceptive subdomain of {legit}"
            )

        # -----------------------------
        # Obfuscation Detection
        # -----------------------------
        if normalized_original != base_original and similarity(base_original, normalized_original) > 0.7:
            temp_score += 2
            temp_reasons.append(
                f"{domain}: Uses obfuscation techniques (rn→m, 0→o, etc.)"
            )

        if temp_score > best_score:
            best_score = temp_score
            best_reasons = temp_reasons
    
    score += best_score
    reasons.extend(best_reasons)

    return score, reasons


# -------------------------------------------------
# Main Module Function
# -------------------------------------------------

def analyze_typosquatting(headers, body=""):
    total_score = 0
    all_reasons = []

    fields = ["From", "Reply-To", "Return-Path"]

    seen_domains = set()

    # Analyze header email fields
    for field in fields:
        value = headers.get(field, "")
        domain = extract_domain_from_email(value)

        if domain:
            if domain in seen_domains:
                continue
            seen_domains.add(domain)

            score, reasons = check_domain(domain)

            total_score += score
            all_reasons.extend(
                [f"{field}: {reason}" for reason in reasons]
            )

    # Analyze URLs in body
    url_domains = extract_domains_from_urls(body)

    for domain in url_domains:
        if domain in seen_domains:
                continue
        seen_domains.add(domain)

        score, reasons = check_domain(domain)

        total_score += score
        all_reasons.extend(
            [f"URL: {reason}" for reason in reasons]
        )

    # -----------------------------
    # IP-based URL Detection
    # -----------------------------
    ip_urls = re.findall(r'https?://(\d{1,3}(?:\.\d{1,3}){3})', body)

    for ip in ip_urls:
        total_score += 3
        all_reasons.append(f"URL uses raw IP address: {ip}")

    # -----------------------------
    # Remove Duplicate Reasons
    # -----------------------------
    all_reasons = list(set(all_reasons))

    return total_score, all_reasons