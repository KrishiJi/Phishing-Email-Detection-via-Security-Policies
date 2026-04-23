import re
from config.settings import ORGANIZATION_DOMAIN
from utils.helpers import *

# -------------------------------
# Main SMTP Analysis Function
# -------------------------------

def analyze_received_headers(headers):
    score = 0
    reasons = []
    hop_details = []

    # Get all Received headers
    received_headers = headers.get_all("Received", [])

    hops = len(received_headers)

    # -------------------------------
    # Determine Internal vs External
    # -------------------------------

    from_header = headers.get("From", "")
    from_domain = extract_email_domain(from_header)

    # Origin = last Received header
    origin_hop = received_headers[-1] if received_headers else ""
    origin_domain = extract_domain(origin_hop)

    is_internal = (
        from_domain == ORGANIZATION_DOMAIN or
        ORGANIZATION_DOMAIN in origin_domain
    )

    # -------------------------------
    # Basic Hop Count Check
    # -------------------------------

    if hops > 5:
        score += 3
        reasons.append("Unusual number of SMTP hops")

    # -------------------------------
    # Per-Hop Analysis
    # -------------------------------

    for i, hop in enumerate(received_headers):
        ip = extract_ip(hop)
        domain = extract_domain(hop)

        hop_score = 0
        hop_reasons = []

        # Private IP (only if external)
        if ip and is_private_ip(ip) and not is_internal:
            hop_score += 2
            hop_reasons.append(f"Private IP in external email (hop {i+1}): {ip}")

        # Suspicious domain
        if domain.lower() in ["unknown", "localhost"]:
            hop_score += 2
            hop_reasons.append(f"Suspicious domain in hop {i+1}: {domain}")

        # Missing IP
        if not ip:
            hop_score += 1
            hop_reasons.append(f"No IP found in hop {i+1}")
        
        hop_details.append({
            "hop": i + 1,
            "ip": ip,
            "domain": domain,
            "hop_score": hop_score,
            "hop_reasons": hop_reasons
        })
        
        # ---- Aggregate Score ----
        score += hop_score
        reasons.extend([f"Hop {i+1}: {r}" for r in hop_reasons])

    # -------------------------------
    # Return Result
    # -------------------------------

    return score, reasons, hop_details

'''
def analyze_received_headers(headers):
    received = headers.get("Received", "")
    hops = received.count("Received")

    score = 0
    reasons = []

    if hops > 5:
        score += 3
        reasons.append("Unusual number of SMTP hops")

    return score, reasons
'''