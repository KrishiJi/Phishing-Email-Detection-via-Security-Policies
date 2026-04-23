def label_as_phishing(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Flagged')
