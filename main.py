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

def main():
    mail = connect(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, "ALL")
    for email_id in data[0].split():
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        headers, body, attachments = parse_email(raw_email)

        header_result = HeaderAnalyzer(headers).analyze()
        smtp_score, _ = analyze_received_headers(headers)
        auth_score, _ = analyze_authentication(headers)
        ip_score, _ = analyze_sender_ip(headers)
        content_score, _ = analyze_content(body)
        url_score, _ = analyze_urls(body)
        attach_score, _ = analyze_attachments(attachments)

        total_score = (
            header_result["score"] + smtp_score + auth_score +
            ip_score + content_score + url_score + attach_score
        )

        verdict = classify(total_score)

        print(f"Email {email_id.decode()} → {verdict}")

if __name__ == "__main__":
    main()
