from backend.notifications import send_email
from backend.scrape_fbm import get_listings
from backend.db import fetch_unemailed_listings, insert_listings_batch, fetch_all_listings, init_db, reset_db
from tabulate import tabulate
from config import SEARCH

def create_db_service():
    try:
        init_db()
        return {"status": "success", "msg": "Database initialized successfully"}
    except Exception as e:
        return {"status": "error", "msg": f"Failed to initialize database: {str(e)}"}

def db_status_service():
    try:
        from backend.db import show_head
        show_head()
        # This will print to console, but we can also return status
        return {"status": "success", "msg": "Database is accessible"}
    except Exception as e:
        return {"status": "error", "msg": f"Database error: {str(e)}"}

def reset_db_service():
    try:
        reset_db()
        init_db()
        return {"status": "success", "msg": "Database reset successfully"}
    except Exception as e:
        return {"status": "error", "msg": f"Failed to reset database: {str(e)}"}

def scrape_service(location, keyword, query, min_price, max_price):
    # query_url = SEARCH['query'].replace(" ", SEARCH['delimiter'])
    url = f"https://www.facebook.com/marketplace/{location}/search/?query={query}&minPrice={min_price}&maxPrice={max_price}"

    print(url)
    listings = get_listings(url, keyword)
    insert_listings_batch(listings)
    return {"scraped": len(listings)}

def pending_listings_service():
    rows, headers = fetch_unemailed_listings()
    return {"headers": headers, "rows": rows}

def all_listings_service(): 
    rows, headers = fetch_all_listings()
    return {"headers": headers, "rows": rows}

def notify_service():
    def remove_emojis(text):
        """Remove non-alphanumeric characters (including emojis) from text"""
        import string
        allowed_chars = string.ascii_letters + string.digits + string.whitespace + ".,!?@#$%&*()-_+=:;\"'<>/\\|[]{}()"
        return ''.join(char for char in str(text) if char in allowed_chars)

    listings, headers = fetch_unemailed_listings()
    if not listings:
        return {"sent": 0}

    formatted = [(f"${l['price']:,}", remove_emojis(l['title']), remove_emojis(l['location']), l['url']) for l in listings]

    table = tabulate(formatted, headers=headers, tablefmt="html", numalign="left", stralign="left")
    subject = f"[fbm-bot] {len(listings)} new listings"
    send_email(subject, table)
    
    print(tabulate(formatted, headers=headers, tablefmt="simple", numalign="left", stralign="left"))

    return {"sent": len(listings)}