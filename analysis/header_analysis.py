<<<<<<< HEAD
import re
from collections import Counter
from email.utils import parseaddr


class HeaderAnalyzer:
    def __init__(self, headers: dict):
        """
        headers: dictionary of parsed email headers
        """
        self.headers = headers
        self.score = 0
        self.reasons = []

    # -------------------------
    # Utility functions
    # -------------------------

    def _get_domain(self, email_address):
        if not email_address or "@" not in email_address:
            return None
        return email_address.split("@")[-1].lower()

    def _extract_email(self, header_value):
        _, email_addr = parseaddr(header_value)
        return email_addr.lower() if email_addr else None

    # -------------------------
    # Header checks
    # -------------------------

    def check_from_reply_to_mismatch(self):
        from_addr = self._extract_email(self.headers.get("From", ""))
        reply_to = self._extract_email(self.headers.get("Reply-To", ""))

        if from_addr and reply_to:
            if self._get_domain(from_addr) != self._get_domain(reply_to):
                self.score += 5
                self.reasons.append(
                    "Mismatch between From and Reply-To domains"
                )

    def check_return_path_mismatch(self):
        from_addr = self._extract_email(self.headers.get("From", ""))
        return_path = self._extract_email(self.headers.get("Return-Path", ""))

        if from_addr and return_path:
            if self._get_domain(from_addr) != self._get_domain(return_path):
                self.score += 5
                self.reasons.append(
                    "Return-Path domain does not match From domain"
                )

    def check_display_name_spoofing(self):
        from_header = self.headers.get("From", "")
        display_name, email_addr = parseaddr(from_header)

        suspicious_keywords = ["paypal", "bank", "support", "security", "admin"]

        if display_name and email_addr:
            display_name_lower = display_name.lower()
            domain = self._get_domain(email_addr)

            if any(k in display_name_lower for k in suspicious_keywords):
                if domain and domain.endswith(("gmail.com", "yahoo.com", "outlook.com")):
                    self.score += 4
                    self.reasons.append(
                        "Possible display name spoofing using brand keywords"
                    )

    def check_message_id_domain(self):
        message_id = self.headers.get("Message-ID", "")
        from_addr = self._extract_email(self.headers.get("From", ""))

        if message_id and from_addr:
            msg_domain_match = re.search(r"@([^>]+)", message_id)
            if msg_domain_match:
                msg_domain = msg_domain_match.group(1).lower()
                from_domain = self._get_domain(from_addr)

                if from_domain and msg_domain != from_domain:
                    self.score += 3
                    self.reasons.append(
                        "Message-ID domain does not match sender domain"
                    )

    def check_missing_or_duplicate_headers(self):
        required_headers = ["From", "To", "Date", "Message-ID"]
        missing = [h for h in required_headers if h not in self.headers]

        if missing:
            self.score += 3
            self.reasons.append(
                f"Missing required headers: {', '.join(missing)}"
            )

        header_counts = Counter(self.headers.keys())
        duplicates = [h for h, c in header_counts.items() if c > 1]

        if duplicates:
            self.score += 3
            self.reasons.append(
                f"Duplicate headers detected: {', '.join(duplicates)}"
            )

    # -------------------------
    # Main analysis entry
    # -------------------------

    def analyze(self):
        self.check_from_reply_to_mismatch()
        self.check_return_path_mismatch()
        self.check_display_name_spoofing()
        self.check_message_id_domain()
        self.check_missing_or_duplicate_headers()

        verdict = "PASS"
        if self.score >= 12:
            verdict = "FAIL"
        elif self.score >= 6:
            verdict = "SUSPICIOUS"

        return {
            "phase": "Header Analysis",
            "score": self.score,
            "verdict": verdict,
            "reasons": self.reasons
        }
=======
import re
from collections import Counter
from email.utils import parseaddr


class HeaderAnalyzer:
    def __init__(self, headers: dict):
        """
        headers: dictionary of parsed email headers
        """
        self.headers = headers
        self.score = 0
        self.reasons = []

    # -------------------------
    # Utility functions
    # -------------------------

    def _get_domain(self, email_address):
        if not email_address or "@" not in email_address:
            return None
        return email_address.split("@")[-1].lower()

    def _extract_email(self, header_value):
        _, email_addr = parseaddr(header_value)
        return email_addr.lower() if email_addr else None

    # -------------------------
    # Header checks
    # -------------------------

    def check_from_reply_to_mismatch(self):
        from_addr = self._extract_email(self.headers.get("From", ""))
        reply_to = self._extract_email(self.headers.get("Reply-To", ""))

        if from_addr and reply_to:
            if self._get_domain(from_addr) != self._get_domain(reply_to):
                self.score += 5
                self.reasons.append(
                    "Mismatch between From and Reply-To domains"
                )

    def check_return_path_mismatch(self):
        from_addr = self._extract_email(self.headers.get("From", ""))
        return_path = self._extract_email(self.headers.get("Return-Path", ""))

        if from_addr and return_path:
            if self._get_domain(from_addr) != self._get_domain(return_path):
                self.score += 5
                self.reasons.append(
                    "Return-Path domain does not match From domain"
                )

    def check_display_name_spoofing(self):
        from_header = self.headers.get("From", "")
        display_name, email_addr = parseaddr(from_header)

        suspicious_keywords = ["paypal", "bank", "support", "security", "admin"]

        if display_name and email_addr:
            display_name_lower = display_name.lower()
            domain = self._get_domain(email_addr)

            if any(k in display_name_lower for k in suspicious_keywords):
                if domain and domain.endswith(("gmail.com", "yahoo.com", "outlook.com")):
                    self.score += 4
                    self.reasons.append(
                        "Possible display name spoofing using brand keywords"
                    )

    def check_message_id_domain(self):
        message_id = self.headers.get("Message-ID", "")
        from_addr = self._extract_email(self.headers.get("From", ""))

        if message_id and from_addr:
            msg_domain_match = re.search(r"@([^>]+)", message_id)
            if msg_domain_match:
                msg_domain = msg_domain_match.group(1).lower()
                from_domain = self._get_domain(from_addr)

                if from_domain and msg_domain != from_domain:
                    self.score += 3
                    self.reasons.append(
                        "Message-ID domain does not match sender domain"
                    )

    def check_missing_or_duplicate_headers(self):
        required_headers = ["From", "To", "Date", "Message-ID"]
        missing = [h for h in required_headers if h not in self.headers]

        if missing:
            self.score += 3
            self.reasons.append(
                f"Missing required headers: {', '.join(missing)}"
            )

        header_counts = Counter(self.headers.keys())
        duplicates = [h for h, c in header_counts.items() if c > 1]

        if duplicates:
            self.score += 3
            self.reasons.append(
                f"Duplicate headers detected: {', '.join(duplicates)}"
            )

    # -------------------------
    # Main analysis entry
    # -------------------------

    def analyze(self):
        self.check_from_reply_to_mismatch()
        self.check_return_path_mismatch()
        self.check_display_name_spoofing()
        self.check_message_id_domain()
        self.check_missing_or_duplicate_headers()

        verdict = "PASS"
        if self.score >= 12:
            verdict = "FAIL"
        elif self.score >= 6:
            verdict = "SUSPICIOUS"

        return {
            "phase": "Header Analysis",
            "score": self.score,
            "verdict": verdict,
            "reasons": self.reasons
        }
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
