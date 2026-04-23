from config.settings import PHISHING_THRESHOLD, SUSPICIOUS_THRESHOLD

def classify(total_score):
    if total_score >= PHISHING_THRESHOLD:
        return "PHISHING"
    elif total_score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"
    return "LEGITIMATE"
