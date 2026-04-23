import imaplib
import ssl
from config.settings import IMAP_SERVER, IMAP_PORT


def connect(email_user, email_pass):
    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
        status, response = mail.login(email_user, email_pass)

        if status == 'OK':
            print("✅ Successfully connected and logged in!")
            return mail
        else:
            print("❌ Login failed:", response)
            return None

    except Exception as e:
        print("❌ Connection error:", str(e))
        return None
