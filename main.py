from backend.services import notify_service, scrape_service
from config import SEARCH
from datetime import datetime

def main():
    print(f"{datetime.now()} - Searching {SEARCH['query']} in {SEARCH['location']}")

    result = scrape_service()
    print(f"Inserted {result['inserted']} listings")

    notif = notify_service()
    print(notif)

if __name__ == "__main__":
    main()