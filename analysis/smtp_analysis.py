def analyze_received_headers(headers):
    received = headers.get("Received", "")
    hops = received.count("Received")

    score = 0
    reasons = []

    if hops > 5:
        score += 3
        reasons.append("Unusual number of SMTP hops")

    return score, reasons
