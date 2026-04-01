import email


def parse_email(raw_email):
    msg = email.message_from_bytes(raw_email)
    headers = dict(msg.items())
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    attachments = []
    for part in msg.walk():
        if part.get_filename():
            attachments.append(part.get_filename())

    return msg, headers, body, attachments
