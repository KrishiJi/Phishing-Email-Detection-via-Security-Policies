<<<<<<< HEAD
import re

def safe_lower(text):
    return text.lower() if text else ""

def extract_ip(received_line):
    match = re.search(r"\[?(\d{1,3}(?:\.\d{1,3}){3})\]?", received_line)
    return match.group(1) if match else None


def extract_domain(received_line):
    match = re.search(r"from\s+([^\s]+)", received_line)
    return match.group(1) if match else "unknown"


def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        ip.startswith("172.")
    )


def extract_email_domain(email):
    if "@" in email:
        return email.split("@")[-1].lower()
=======
import re

def safe_lower(text):
    return text.lower() if text else ""

def extract_ip(received_line):
    match = re.search(r"\[?(\d{1,3}(?:\.\d{1,3}){3})\]?", received_line)
    return match.group(1) if match else None


def extract_domain(received_line):
    match = re.search(r"from\s+([^\s]+)", received_line)
    return match.group(1) if match else "unknown"


def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        ip.startswith("172.")
    )


def extract_email_domain(email):
    if "@" in email:
        return email.split("@")[-1].lower()
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
    return ""