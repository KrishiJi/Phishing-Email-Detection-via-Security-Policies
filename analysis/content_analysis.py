<<<<<<< HEAD
import re
from config.constants import SUSPICIOUS_KEYWORDS

def analyze_content(body):
    score = 0
    reasons = []

    body_lower = body.lower()

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in body_lower:
            score += 1

    if score > 5:
        reasons.append("Phishing-like language detected")

    return score, reasons
=======
import re
from config.constants import SUSPICIOUS_KEYWORDS

def analyze_content(body):
    score = 0
    reasons = []

    body_lower = body.lower()

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in body_lower:
            score += 1

    if score > 5:
        reasons.append("Phishing-like language detected")

    return score, reasons
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
