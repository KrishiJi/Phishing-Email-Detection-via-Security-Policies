import re

def analyze_sender_ip(headers):
    score = 0
    reasons = []

    received = headers.get("Received", "")
    ip_match = re.search(r"\[([\d\.]+)\]", received)

    if ip_match:
        ip = ip_match.group(1)
        if ip.startswith(("10.", "192.168.", "172.")):
            score += 3
            reasons.append("Private IP used in public email")

    return score, reasons
