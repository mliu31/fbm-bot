from scrape_fbm import get_listings, show_head
from send_email import send_email_new_listings


def get_user_configuration():
    """Get configuration from user input"""
    print("Facebook Marketplace Bot Configuration")
    print("=" * 40)
    
    main_keyword = input("Enter main keyword (e.g., 'cannondale'): ").strip()
    if not main_keyword:
        main_keyword = "cannondale"
    
    query = input("Enter full search query (e.g., 'cannondale caadx 105 51cm '): ").strip()
    if not query:
        query = "cannondale caadx 105 51cm"
    
    while True:
        min_price_input = input("Enter minimum price (e.g., 300): $").strip()
        if not min_price_input:
            min_price = 300
            break
        try:
            min_price = int(min_price_input)
            break
        except ValueError:
            print("Please enter a valid number for minimum price.")
    
    while True:
        max_price_input = input("Enter maximum price (e.g., 1000): $").strip()
        if not max_price_input:
            max_price = 1000
            break
        try:
            max_price = int(max_price_input)
            if max_price > min_price:
                break
            else:
                print("Maximum price must be greater than minimum price.")
        except ValueError:
            print("Please enter a valid number for maximum price.")
    
    location = input("Enter location from this list https://www.facebook.com/marketplace/directory/US/ (e.g., 'memphis'): ").strip()
    if not location:
        location = "memphis"
    
    delimiter = "%20"
    
    print("\nConfiguration Summary:")
    print(f"Main keyword: {main_keyword}")
    print(f"Search query: {query}")
    print(f"Price range: ${min_price} - ${max_price}")
    print(f"Location: {location}")
    
    confirm = input("\nProceed with this configuration? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Configuration cancelled.")
        return None
    
    return {
        'main_keyword': main_keyword,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'location': location,
        'delimiter': delimiter
    }


def main():
    # Get user configuration
    config = get_user_configuration()
    if config is None:
        return
    
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
    
    print(f"\nSearching for {query} bikes in {location}...")
    print(f"Price range: ${min_price} - ${max_price}")
    print(f"URL: {url}")
    
    # Get listings from Facebook Marketplace
    get_listings(url, main_keyword)
    print("Listings fetched")
    # show_head()
    
    # Send email for new listings
    send_email_new_listings()

if __name__ == "__main__":
    main()