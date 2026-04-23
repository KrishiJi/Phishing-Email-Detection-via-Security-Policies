<<<<<<< HEAD
from config.settings import PHISHING_THRESHOLD, SUSPICIOUS_THRESHOLD

def classify(total_score):
    if total_score >= PHISHING_THRESHOLD:
        return "PHISHING"
    elif total_score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"
    return "LEGITIMATE"
=======
from config.settings import PHISHING_THRESHOLD, SUSPICIOUS_THRESHOLD

def classify(total_score):
    if total_score >= PHISHING_THRESHOLD:
        return "PHISHING"
    elif total_score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"
    return "LEGITIMATE"
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
