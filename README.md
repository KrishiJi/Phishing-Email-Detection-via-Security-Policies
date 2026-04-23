# 📧 Phishing Email Detection System

## 🚀 Overview

The **Phishing Email Detection System** is a comprehensive security solution designed to identify malicious emails using a combination of **rule-based analysis, heuristic techniques, and threat intelligence integration**.

The system analyzes emails across multiple dimensions such as **headers, SMTP paths, content, URLs, attachments, and domain spoofing techniques**, and assigns a **risk score** to classify emails as:

* ✅ Legitimate
* ⚠️ Suspicious
* 🚨 Phishing

---

## ❗ Problem Statement

Phishing attacks are one of the most common and dangerous cybersecurity threats. Attackers use techniques like:

* Email spoofing
* Typosquatting (e.g., *arnazon → amazon*)
* Malicious links and attachments
* Social engineering

Traditional filters often fail to detect **advanced or zero-day phishing attacks**.

👉 This project aims to build a **multi-layered detection system** that improves accuracy by combining multiple analysis techniques.

---

## 💡 Solution

This system performs **multi-module analysis** on emails and aggregates the results using a **risk scoring engine**.

Key highlights:

* 🔍 Multi-layered detection approach
* 🌐 Integration with VirusTotal for threat intelligence
* 🧠 Heuristic + behavioral analysis
* 📊 Explainable results with detailed reasoning

---

## 🧱 System Architecture

The system follows a modular pipeline:

```
Email Input (IMAP / .eml files)
        ↓
Email Parser
        ↓
Analysis Modules
  ├── Header Analysis
  ├── SMTP Analysis
  ├── Authentication Analysis
  ├── IP Analysis
  ├── Content Analysis
  ├── URL Analysis
  ├── Attachment Analysis
  └── Typosquatting Detection
        ↓
Risk Engine (Scoring + Classification)
        ↓
Report Generator + Logger
        ↓
Final Output
```

---

## ⚙️ Features

* 📥 Email retrieval via IMAP
* 📄 Local `.eml` file testing support
* 🧠 Intelligent phishing detection
* 🔗 URL and IP reputation checking (VirusTotal)
* 📎 Attachment risk analysis
* 🕵️ Typosquatting detection (brand impersonation)
* 📊 Risk scoring and classification
* 🧾 Detailed explainable reports

---

## 🧩 Modules Explained

### 1. 📌 Email Parser

* Extracts:

  * Headers
  * Body
  * Attachments
* Handles multipart emails

---

### 2. 📨 Header Analysis

* Checks for missing or suspicious headers:

  * `Message-ID`, `Date`, etc.

---

### 3. 🌐 SMTP Analysis

* Analyzes `Received` headers
* Tracks email hops
* Detects unusual routing patterns

---

### 4. 🔐 Authentication Analysis

* Verifies:

  * SPF
  * DKIM
  * DMARC
* Identifies spoofed senders

---

### 5. 🌍 IP Analysis

* Extracts sender IP
* Checks against **VirusTotal**
* Flags:

  * Malicious IPs
  * Suspicious/private IP usage

---

### 6. 🧠 Content Analysis

* Detects:

  * Urgency phrases
  * Threat language
  * Social engineering patterns

---

### 7. 🔗 URL Analysis

* Detects:

  * HTTP (unencrypted links)
  * IP-based URLs
  * URL shorteners
  * Phishing keywords
  * Obfuscation (`@`, etc.)
* Verifies URLs via **VirusTotal**

---

### 8. 📎 Attachment Analysis

* Detects:

  * Dangerous file types (`.exe`, scripts)
  * Double extensions (`.pdf.exe`)
  * Suspicious filenames
* Uses hashing + VirusTotal lookup

---

### 9. 🕵️ Typosquatting Detection

* Detects:

  * Domain similarity (e.g., `arnazon → amazon`)
  * Brand misuse
  * Obfuscation tricks (`rn → m`, `0 → o`)
* Uses a curated **trusted domains dataset**

---

### 10. ⚖️ Risk Engine

* Aggregates scores from all modules
* Classifies email:

| Score Range | Verdict    |
| ----------- | ---------- |
| 0–9         | Legitimate |
| 10-15       | Suspicious |
| 15+         | Phishing   |

---

### 11. 🧾 Report Generator

* Produces structured output:

  * Final score
  * Verdict
  * Detailed reasons

---

### 12. 📜 Logger

* Logs analysis results for debugging and auditing

---

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:**

  * `imaplib` (email retrieval)
  * `email` (parsing)
  * `re`, `difflib`, `hashlib`
* **APIs:**

  * VirusTotal API

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/phishing-email-detector.git
cd phishing-email-detector
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Update your credentials in `settings.py`:

```python
EMAIL_ACCOUNT = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
VIRUSTOTAL_API_KEY = "your_api_key"
```

---

## ▶️ Usage

### 🔹 1. Run on Live Emails (IMAP)

```bash
python main.py
```

---

### 🔹 2. Run on Test Emails (.eml)

```bash
python test.py
```

---

## 📊 Sample Output

```
📌 Subject : Amazon Account Verification Required
📊 Score   : 15
🚨 Verdict : PHISHING

🔍 Module Breakdown:
  HEADER          : 3
  SMTP            : 0
  AUTHENTICATION  : 0
  IP              : 0
  CONTENT         : 3
  URL             : 3
  ATTACHMENT      : 0
  TYPOSQUATTING   : 6

⚠️ Reasons:
  - Missing required headers: Date, Message-ID
  - http://arnazon-security-check.com/login: Uses HTTP (unencrypted connection)
  - http://arnazon-security-check.com/login: Contains phishing-related keywords
  - URL: arnazon-security-check.com: Uses obfuscation techniques (rn→m, 0→o, etc.)
  - URL: arnazon-security-check.com: Hyphenated domain often used in phishing
  - URL: arnazon-security-check.com: Misuses brand keyword 'amazon'
```

---

## 🔮 Future Enhancements

* 🤖 Machine Learning-based classification
* 📊 Confidence score (probability-based output)
* 🌐 Web dashboard / UI
* 📬 Server-side deployment (mail gateway integration)
* 🧪 Sandboxed dynamic attachment analysis
* 🌍 Domain age & WHOIS verification

---

## 📚 References

* VirusTotal API Documentation
* RFC 5322 (Email Format Standard)
* OWASP Phishing Guidelines

---

## 👨‍💻 Author

Developed as part of a cybersecurity project focusing on **phishing detection and email security**.

---

## ⭐ Final Note

This project demonstrates how combining **multiple lightweight security techniques** can create a powerful and explainable phishing detection system.

---
