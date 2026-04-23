from config.constants import HIGH_RISK_EXTENSIONS, ARCHIVE_EXTENSIONS, MACRO_EXTENSIONS
from utils.virustotal import check_file_hash
import hashlib
import math
import zipfile
import os
import re



def get_file_hash(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_extension(filename):
    return os.path.splitext(filename.lower())[1]

def suspicious_keywords(filename):
    keywords = [
        "invoice",
        "payment",
        "urgent",
        "salary",
        "bank",
        "update",
        "verify",
        "password"
    ]

    name = filename.lower()

    return any(word in name for word in keywords)

def calculate_entropy(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    if not data:
        return 0

    freq = {}
    for byte in data:
        freq[byte] = freq.get(byte, 0) + 1

    entropy = 0
    for count in freq.values():
        p = count / len(data)
        entropy -= p * math.log2(p)

    return entropy


def has_double_extension(filename):
    return bool(re.search(r'\.[a-zA-Z0-9]{1,5}\.[a-zA-Z0-9]{1,5}$', filename))

# -------------------------------------------------
# ZIP Analysis
# -------------------------------------------------

def analyze_zip(filepath):
    score = 0
    reasons = []

    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            names = z.namelist()

            for name in names:
                ext = get_extension(name)

                if ext in HIGH_RISK_EXTENSIONS:
                    score += 5
                    reasons.append(
                        f"ZIP contains executable/script file: {name}"
                    )

            # Password protected check
            encrypted = any(info.flag_bits & 0x1 for info in z.infolist())

            if encrypted:
                score += 3
                reasons.append("Password-protected ZIP archive")

    except:
        score += 2
        reasons.append("Corrupted or unreadable ZIP archive")

    return score, reasons


# -------------------------------------------------
# PDF Analysis
# -------------------------------------------------

def analyze_pdf(filepath):
    score = 0
    reasons = []

    try:
        with open(filepath, "rb") as f:
            content = f.read().decode(errors="ignore")

        suspicious_keywords = [
            "/JavaScript",
            "/JS",
            "/OpenAction",
            "/Launch",
            "/EmbeddedFile"
        ]

        for keyword in suspicious_keywords:
            if keyword in content:
                score += 3
                reasons.append(f"PDF contains {keyword}")

    except:
        pass

    return score, reasons


# --------------------------------------------
# Single Attachment Analyzer
# --------------------------------------------

def analyze_single_attachment(filename):
    score = 0
    reasons = []

    ext = get_extension(filename)

    # ---------------------------------
    # Double Extension
    # ---------------------------------
    if has_double_extension(filename):
        score += 4
        reasons.append("Double extension filename trick")

    # ---------------------------------
    # Dangerous Executable Types
    # ---------------------------------
    if ext in HIGH_RISK_EXTENSIONS:
        score += 6
        reasons.append(f"High-risk executable/script file: {ext}")

    # ---------------------------------
    # Macro Documents
    # ---------------------------------
    if ext in MACRO_EXTENSIONS:
        score += 5
        reasons.append("Macro-enabled Office document")

    # ---------------------------------
    # Archives
    # ---------------------------------
    if ext in ARCHIVE_EXTENSIONS:
        score += 2
        reasons.append("Compressed archive attachment")

    # ---------------------------------
    # Suspicious Filename Lure
    # ---------------------------------
    if suspicious_keywords(filename):
        score += 2
        reasons.append("Social engineering lure filename")

    return score, reasons


    
def analyze_attachments(attachments):
    total_score = 0
    all_reasons = []
    details = []

    for file in attachments:
        score, reasons = analyze_single_attachment(file)

        file_hash = get_file_hash(file)
        vt_result = check_file_hash(file_hash)

        if vt_result and vt_result["malicious"] > 0:
            score += 6
            reasons.append(f"Malicious attachment detected: {file}")

        total_score += score

        details.append({
            "file": file,
            "score": score,
            "reasons": reasons
        })

        for r in reasons:
            all_reasons.append(f"{file}: {r}")

    return total_score, all_reasons, details

