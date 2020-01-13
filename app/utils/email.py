from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Optional, List
import smtplib

from jinja2 import Template

from app.settings import TESTING
from app.settings import SMTP_HOST
from app.settings import SMTP_PORT
from app.settings import SMTP_USERNAME
from app.settings import SMTP_PASSWORD

def send_email(to_email: str, subject: str, body: str):
    """Send an email."""
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
    
    if TESTING:
        # Do not send an actual email if unittesting.
        return

    smtpObj = smtplib.SMTP(SMTP_HOST)
    smtpObj.send_message(msg)
