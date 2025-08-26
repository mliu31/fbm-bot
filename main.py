from backend.db import init_db, reset_db
from backend.services import notify_service, scrape_service
from config import SEARCH
from datetime import datetime

def main():
    print(f"{datetime.now()} - Searching '{SEARCH['query']}' in '{SEARCH['location']}'")

    # reset_db()
    init_db()

    scraped = scrape_service()
    print(f"Scraped {scraped['scraped']} listings")

    notif = notify_service()
    if notif['sent'] > 0:
        print(f"Emailed {notif['sent']} new listings.")
    else:
        print("0 new listings.")

if __name__ == "__main__":
    main()