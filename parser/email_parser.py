<<<<<<< HEAD
import email
import os
import uuid

# -------------------------------------------------
# Ensure attachments folder exists
# -------------------------------------------------

ATTACHMENT_DIR = "attachments"
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

# -------------------------------------------------
# Duplicate-safe filename generator
# -------------------------------------------------

def generate_unique_filename(filename):
    base, ext = os.path.splitext(filename)

    unique_id = str(uuid.uuid4())[:8]

    return f"{base}_{unique_id}{ext}"

def parse_email(raw_email):
    msg = email.message_from_bytes(raw_email)
    headers = dict(msg.items())
    # body = ""

    # if msg.is_multipart():
    #     for part in msg.walk():
    #         if part.get_content_type() == "text/plain":
    #             body += part.get_payload(decode=True).decode(errors="ignore")
    # else:
    #     body = msg.get_payload(decode=True).decode(errors="ignore")

    # attachments = []
    # for part in msg.walk():
    #     if part.get_filename():
    #         attachments.append(part.get_filename())

    body = ""
    attachments = []

    # -----------------------------------------
    # Extract body + attachments
    # -----------------------------------------
    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            # ---------------------------------
            # Plain text body
            # ---------------------------------
            if content_type == "text/plain" and "attachment" not in disposition.lower():
                payload = part.get_payload(decode=True)

                if payload:
                    body += payload.decode(errors="ignore")

            # ---------------------------------
            # Attachment
            # ---------------------------------
            filename = part.get_filename()

            if filename:
                payload = part.get_payload(decode=True)

                if payload:
                    safe_name = generate_unique_filename(filename)
                    filepath = os.path.join(ATTACHMENT_DIR, safe_name)

                    with open(filepath, "wb") as f:
                        f.write(payload)

                    attachments.append(filepath)

    else:
        payload = msg.get_payload(decode=True)

        if payload:
            body = payload.decode(errors="ignore")

    return msg, headers, body, attachments
=======
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
>>>>>>> c5df351399b66f378090fa9d86ad08b85a9527ef
