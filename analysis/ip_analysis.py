<<<<<<< HEAD
import re
from utils.virustotal import check_ip

def analyze_sender_ip(headers):
    score = 0
    reasons = []

    received = headers.get("Received", "")
    ip_match = re.search(r"\[([\d\.]+)\]", received)

    # if ip_match:
    #     ip = ip_match.group(1)
    #     if ip.startswith(("10.", "192.168.", "172.")):
    #         score += 3
    #         reasons.append("Private IP used in public email")
    
    vt_result = []
    if ip_match:
        vt_result = check_ip(ip_match.group(1))

    if vt_result and vt_result["malicious"] > 0:
        score += 5
        reasons.append("Malicious IP (VirusTotal)")

    return score, reasons
=======
import re
from utils.virustotal import check_ip

def analyze_sender_ip(headers):
    score = 0
    reasons = []

    received = headers.get("Received", "")
    ip_match = re.search(r"\[([\d\.]+)\]", received)

    # if ip_match:
    #     ip = ip_match.group(1)
    #     if ip.startswith(("10.", "192.168.", "172.")):
    #         score += 3
    #         reasons.append("Private IP used in public email")
    
    vt_result = []
    if ip_match:
        vt_result = check_ip(ip_match.group(1))

    if vt_result and vt_result["malicious"] > 0:
        score += 5
        reasons.append("Malicious IP (VirusTotal)")

    return score, reasons
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
