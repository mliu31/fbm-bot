import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import sqlite3
from tabulate import tabulate

# Load environment variables from .env file
load_dotenv()

# get env vars
sender = os.getenv("GMAIL")
receiver = os.getenv("GMAIL")
password = os.getenv("GMAIL_APP_PWD")

def send_email(subject, body):
    # create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # encrypt connection
        server.login(sender, password)
        server.send_message(msg)

    print("\nEmail sent")

def fetch_new_listings():
    conn = sqlite3.connect("listings.db")
    cur = conn.cursor()
    cur.execute("SELECT price, title, location, url FROM listings WHERE emailed=0")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    num_listings = len(rows)  # Get actual number of listings

    cur.execute("UPDATE listings SET emailed=1 WHERE emailed=0")
    conn.commit()   
    conn.close()

    # Format prices 
    formatted_rows = []
    for row in rows:
        price, title, location, url = row
        formatted_price = f"${price:,}"  # Add $ and commas
        formatted_rows.append((formatted_price, title, location, url))

    table = tabulate(formatted_rows, headers=headers, tablefmt="html", numalign="left", stralign="left")
    return table, num_listings

def send_email_new_listings():
    table, num_listings = fetch_new_listings() 

    if num_listings > 0:
        send_email(f"[fbm-bot] found {num_listings} new listings", table)
    else:
        print("\nNo new listings found--email not sent")