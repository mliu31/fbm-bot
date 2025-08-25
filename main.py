from backend.services import notify_service, scrape_service
from config import SEARCH
from datetime import datetime

def main():
    query_url = SEARCH['query'].replace(" ", SEARCH['delimiter'])
    url = f"https://www.facebook.com/marketplace/{SEARCH['location']}/search/?query={query_url}&minPrice={SEARCH['min_price']}&maxPrice={SEARCH['max_price']}"
    
    print(f"{datetime.now()} - Searching {SEARCH['query']} in {SEARCH['location']}")
    result = scrape_service(url, SEARCH['keyword'])
    print(f"Inserted {result['inserted']} listings")

    notif = notify_service()
    print(notif)



if __name__ == "__main__":
    main()