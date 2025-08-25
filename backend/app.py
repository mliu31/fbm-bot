from scrape_fbm import get_listings, show_head
from send_email import send_email_new_listings
from datetime import datetime

def main():
    config = {
        'main_keyword': 'cannondale',
        'query': 'cannondale caadx 105 51cm',
        'min_price': 300,
        'max_price': 1000,
        'location': 'memphis',
        'delimiter': '%20'
    }
    
    # Extract configuration values
    main_keyword = config['main_keyword']
    query = config['query']
    min_price = config['min_price']
    max_price = config['max_price']
    location = config['location']
    delimiter = config['delimiter']

    query_url = query.replace(" ", delimiter)
    # Build the Facebook Marketplace URL
    url = f"https://www.facebook.com/marketplace/{location}/search/?query={query_url}&minPrice={min_price}&maxPrice={max_price}"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Time: {current_time}")
    print(f"Searching for {query} bikes in {location}...")
    print(f"Price range: ${min_price} - ${max_price}")
    print(f"URL: {url}")
    print("="*80)
    
    # Get listings from Facebook Marketplace
    get_listings(url, main_keyword)
    print("Fetched listings")
    # show_head()
    
    # Send email for new listings
    send_email_new_listings()

if __name__ == "__main__":
    main()