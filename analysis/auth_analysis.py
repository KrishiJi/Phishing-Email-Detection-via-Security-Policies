<<<<<<< HEAD
def analyze_authentication(headers):
    score = 0
    reasons = []

    auth = headers.get("Authentication-Results", "")

    if "spf=fail" in auth:
        score += 5
        reasons.append("SPF validation failed")

    if "dkim=fail" in auth:
        score += 5
        reasons.append("DKIM signature validation failed")

    if "dmarc=fail" in auth:
        score += 5
        reasons.append("DMARC policy failed")

    return score, reasons
=======
def analyze_authentication(headers):
    score = 0
    reasons = []

    auth = headers.get("Authentication-Results", "")

    if "spf=fail" in auth:
        score += 5
        reasons.append("SPF validation failed")

    if "dkim=fail" in auth:
        score += 5
        reasons.append("DKIM signature validation failed")

    if "dmarc=fail" in auth:
        score += 5
        reasons.append("DMARC policy failed")

    return score, reasons
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
