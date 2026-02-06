import smtplib
from email.message import EmailMessage
import os

SMTP_EMAIL = "yourgmail@gmail.com"
SMTP_PASSWORD = "APP_PASSWORD"

def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(msg)
