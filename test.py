import os
from email_client.imap_client import connect
from parser.email_parser import parse_email
from analysis.header_analysis import HeaderAnalyzer
from analysis.smtp_analysis import analyze_received_headers
from analysis.auth_analysis import analyze_authentication
from analysis.ip_analysis import analyze_sender_ip
from analysis.content_analysis import analyze_content
from analysis.url_analysis import analyze_urls
from analysis.attachment_analysis import analyze_attachments
from scoring.risk_engine import classify
from config.settings import EMAIL_ACCOUNT, EMAIL_PASSWORD
from analysis.typosquatting_analysis import analyze_typosquatting
from reporting.report_generator import generate_report
from reporting.logger import setup_logger

from email.header import decode_header
test_folder = "test_emails"

def decode_subject(subject):
    if not subject:
        return "(No Subject)"
        
    decoded_parts = decode_header(subject)
    subject_parts = []

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject_parts.append(part.decode(encoding or "utf-8", errors="ignore"))
        else:
            subject_parts.append(part)

    return "".join(subject_parts)

def test():
    mail = connect(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, "ALL")
    emails = os.listdir(test_folder)

    for email_id in emails:
        path = os.path.join(test_folder, email_id)
        
        logger = setup_logger(email_id)
        logger.info("===== STARTING ANALYSIS =====")

        print("\n" + "="*60)
        print(f"📂 Testing File: {email_id}")
        logger.info(f"Testing File: {email_id}")

        with open(path, "rb") as f:
            raw_email = f.read() 

        msg, headers, body, attachments = parse_email(raw_email)
        logger.info("Email parsed successfully")
        
        header_result = HeaderAnalyzer(headers).analyze()
        logger.info(f"Header Score: {header_result['score']}")

        smtp_score, smtp_reasons, _ = analyze_received_headers(msg)
        logger.info(f"SMTP Score: {smtp_score}")
        
        auth_score, auth_reasons = analyze_authentication(headers)
        logger.info(f"Auth Score: {auth_score}")
        
        ip_score, ip_reasons = analyze_sender_ip(headers)
        logger.info(f"IP Score: {auth_score}")    
        
        content_score, content_reasons = analyze_content(body)
        logger.info(f"Content Score: {auth_score}")    
        
        url_score, url_reasons = analyze_urls(body)
        logger.info(f"URL Score: {auth_score}")    
        
        attach_score, attach_reasons, _ = analyze_attachments(attachments)
        logger.info(f"Attachment Score: {auth_score}")    
        
        typo_score, typo_reasons = analyze_typosquatting(headers, body)
        logger.info(f"Typosquatting Score: {auth_score}")

        total_score = (
            header_result["score"] + smtp_score + auth_score +
            ip_score + content_score + url_score + attach_score + typo_score
        )

        verdict = classify(total_score)
        subject = decode_subject(msg.get("Subject"))
        logger.info(f"Final Score: {total_score}")
        logger.info(f"Verdict: {verdict}")
        logger.info("===== END OF ANALYSIS =====\n")

        all_reasons = (
            header_result["reasons"] +
            smtp_reasons +
            auth_reasons +
            ip_reasons +
            content_reasons +
            url_reasons +
            attach_reasons +
            typo_reasons
        )

        # -----------------------------
        # Build Structured Result
        # -----------------------------
        results = {
            "email_id":email_id,
            "subject": subject,
            "score": total_score,
            "verdict": verdict,
            "reasons": all_reasons,
            "breakdown": {
                "header": header_result["score"],
                "smtp": smtp_score,
                "authentication": auth_score,
                "ip": ip_score,
                "content": content_score,
                "url": url_score,
                "attachment": attach_score,
                "typosquatting": typo_score
            }
        }


        # -----------------------------
        # Generate Report
        # -----------------------------
        report = generate_report(results)

        # -----------------------------
        # Print Report
        # -----------------------------
        print("\n" + "="*60)
        print(f"📌 Subject : {results['subject']}")
        print(f"📊 Score   : {results['score']}")
        print(f"🚨 Verdict : {results['verdict']}")

        print("\n🔍 Module Breakdown:")
        for k, v in results["breakdown"].items():
            print(f"  {k.upper():15} : {v}")

        print("\n⚠️ Reasons:")
        if results["reasons"]:
            for r in results["reasons"]:
                print(f"  - {r}")
        else:
            print("  No suspicious indicators.")

        print("="*60)



if __name__ == "__main__":
    test()
