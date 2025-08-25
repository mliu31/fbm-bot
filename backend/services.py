from backend.notifications import send_email
from backend.scrape_fbm import get_listings
from backend.db import fetch_unemailed_listings, insert_listings_batch
from tabulate import tabulate

def scrape_service(url, keyword):
    listings = get_listings(url, keyword)
    insert_listings_batch(listings)
    return {"inserted": len(listings)}

def listings_service():
    rows, headers = fetch_unemailed_listings()
    return {"headers": headers, "rows": rows}

def notify_service():
    def remove_emojis(text):
        """Remove non-alphanumeric characters (including emojis) from text"""
        import string
        allowed_chars = string.ascii_letters + string.digits + string.whitespace + ".,!?@#$%&*()-_+=:;\"'<>/\\|[]{}()"
        return ''.join(char for char in str(text) if char in allowed_chars)

    listings, headers = fetch_unemailed_listings()
    if not listings:
        return {"msg": "no new listings"}

    formatted = [(f"${l['price']:,}", remove_emojis(l['title']), remove_emojis(l['location']), l['url']) for l in listings]

    table = tabulate(formatted, headers=headers, tablefmt="html", numalign="left", stralign="left")
    subject = f"[fbm-bot] {len(listings)} new listings"
    send_email(subject, table)
    
    print(tabulate(formatted, headers=headers, tablefmt="simple", numalign="left", stralign="left"))

    return {"sent": len(listings)}