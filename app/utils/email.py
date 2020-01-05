from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Optional, List
import smtplib

from app.config import config


def send_email():
            # receiver_email: str,
            #    cc: Optional[List[str]],
            #    bcc: Optional[List[str]],
            #    sender_email: str = "noreply@example.com",
            #    subject='',
            #    body: Optional[List[str]] = None
            #    ):
    """Send an email."""
    smtp_host = config("SMTP_HOST", cast=str, default=False)
    smtp_port = config("SMTP_PORT", cast=str, default=False)
    smtp_username = config("SMTP_USERNAME", cast=str, default=False)
    smtp_password = config("SMTP_PASSWORD", cast=str, default=False)

    sender = 'from@fromdomain.com'
    receivers = ['to@todomain.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    try:
        smtpObj = smtplib.SMTP(smtp_host)
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")
