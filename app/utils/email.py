from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Optional, List
import smtplib

from jinja2 import Template

from app.config import config


def send_email(
    to_email: str, subject: str, body: str,
):
    """Send an email."""
    smtp_host = config("SMTP_HOST", cast=str, default=False)
    smtp_port = config("SMTP_PORT", cast=str, default=False)
    smtp_username = config("SMTP_USERNAME", cast=str, default=False)
    smtp_password = config("SMTP_PASSWORD", cast=str, default=False)

    msg = MIMEMultipart("alternative")
    # me == the sender's email address
    # you == the recipient's email address
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email

    # Get the contents of the template.
    with open("app/templates/email/empty.html", "r") as template:
        # Parse
        template = Template(template.read())

    # inject the body.
    text = body
    html = template.render(body=body)

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    smtpObj = smtplib.SMTP(smtp_host)
    smtpObj.send_message(msg)
    print("Successfully sent email")
