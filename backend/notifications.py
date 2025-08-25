from email.message import EmailMessage
import smtplib
from tabulate import tabulate
from config import CREDENTIALS, EMAIL_SETTINGS
from db import fetch_unemailed_listings


def remove_emojis(text):
    """Remove non-alphanumeric characters (including emojis) from text"""
    import string
    allowed_chars = string.ascii_letters + string.digits + string.whitespace + ".,!?@#$%&*()-_+=:;\"'<>/\\|[]{}()"
    return ''.join(char for char in str(text) if char in allowed_chars)

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

def notify_newlistings():
    listings, headers = fetch_unemailed_listings()
    if not listings:
        print("No new listings")
        return

    formatted = []
    for l in listings:
        line = (f"${l['price']:,}", remove_emojis(l['title']), remove_emojis(l['location']), l['url'])
        formatted.append(line)

    # table = tabulate(formatted, headers=headers, tablefmt='simple')
    table = tabulate(formatted, headers=headers, tablefmt="html", numalign="left", stralign="left")
    subject = f"[fbm-bot] {len(listings)} new listings"
    send_email(subject, table)
    print(tabulate(formatted, headers=headers, tablefmt="simple", numalign="left", stralign="left"))

