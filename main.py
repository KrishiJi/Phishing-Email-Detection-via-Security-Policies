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

def main():
    mail = connect(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, "ALL")
    emails = data[0].split()[::-1][:3]

    for email_id in emails:
        email_id_str = email_id.decode()

        logger = setup_logger(email_id_str)

        logger.info("===== STARTING ANALYSIS =====")
    
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        msg, headers, body, attachments = parse_email(raw_email)
        logger.info("Email parsed successfully")

        header_result = HeaderAnalyzer(headers).analyze()
        logger.info(f"Header Score: {header_result['score']}")

        smtp_score, smtp_reasons, _ = analyze_received_headers(msg)
        logger.info(f"SMTP Score: {smtp_score}")
        
        auth_score, auth_reasons,_ = analyze_authentication(headers)
        logger.info(f"Auth Score: {auth_score}")
        
        ip_score, ip_reasons,_ = analyze_sender_ip(headers)
        logger.info(f"IP Score: {auth_score}")    
        
        content_score, content_reasons,_ = analyze_content(body)
        logger.info(f"Content Score: {auth_score}")    
        
        url_score, url_reasons, _ = analyze_urls(body)
        logger.info(f"URL Score: {auth_score}")    
        
        attach_score, attach_reasons, _ = analyze_attachments(attachments)
        logger.info(f"Attachment Score: {auth_score}")    
        
        typo_score, typo_reasons,_ = analyze_typosquatting(headers, body)
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
            "email_id": email_id.decode(),
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
        print(f"📧 Email ID: {results['email_id']}")
        print(f"📌 Subject : {results['subject']}")
        print(f"📊 Score   : {report['final_score']}")
        print(f"🚨 Verdict : {report['classification']}")

        print("\n🔍 Module Breakdown:")
        for k, v in results["breakdown"].items():
            print(f"  {k.upper():15} : {v}")

        print("\n⚠️ Reasons:")
        if report["details"]:
            for r in report["details"]:
                print(f"  - {r}")
        else:
            print("  No suspicious indicators.")

        print("="*60)



if __name__ == "__main__":
    main()
