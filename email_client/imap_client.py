import imaplib
import ssl
from config.settings import IMAP_SERVER, IMAP_PORT


def connect(email_user, email_pass):
    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
    mail.login(email_user, email_pass)
    return mail
