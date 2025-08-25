from db import create_database, insert_listings_batch
from scrape_fbm import get_listings
from notifications import notify_newlistings
from config import SEARCH
from datetime import datetime

def main():
    query_url = SEARCH['query'].replace(" ", SEARCH['delimiter'])
    url = f"https://www.facebook.com/marketplace/{SEARCH['location']}/search/?query={query_url}&minPrice={SEARCH['min_price']}&maxPrice={SEARCH['max_price']}"

    print(f"{datetime.now()} Searching {SEARCH['query']} in {SEARCH['location']}")
    listings =  get_listings(url, SEARCH['main_keyword'])
    print(f"Fetched listings\nFound {len(listings)} new listings")

    # update db
    create_database()
    insert_listings_batch(listings)
    
    # send email notifs
    notify_newlistings()

if __name__ == "__main__":
    main()