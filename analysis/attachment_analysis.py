from config.constants import RISKY_EXTENSIONS
from utils.virustotal import check_file_hash
import hashlib

def get_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()
    
def analyze_attachments(attachments):
    score = 0
    reasons = []

    for file in attachments:
        for ext in RISKY_EXTENSIONS:
            if file.lower().endswith(ext):
                score += 5
                reasons.append(f"Risky attachment detected: {file}")
        
        file_hash = get_file_hash(file)

        vt_result = check_file_hash(file_hash)

        if vt_result and vt_result["malicious"] > 0:
            score += 6
            reasons.append(f"Malicious attachment detected: {file}")

    return score, reasons