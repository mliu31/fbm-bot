from email.message import EmailMessage
import smtplib
from config import CREDENTIALS, EMAIL_SETTINGS

def send_email(subject, body):
    # create message
    msg = EmailMessage()
    msg['From'] = EMAIL_SETTINGS['sender']
    msg['To'] = EMAIL_SETTINGS['sender']
    msg['Subject'] = subject
    msg.add_alternative(body, subtype='html')

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', EMAIL_SETTINGS['smtp_port']) as s:
        s.login(CREDENTIALS['gmail_address'], CREDENTIALS['gmail_app_password'])
        s.send_message(msg)

    print("Sent email with new/updated listings")
