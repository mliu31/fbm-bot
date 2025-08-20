from scrape_fbm import get_listings, show_head
from send_email import send_email_new_listings


def main():
    # Configuration
    make = "cannondale"
    model = "caadx"
    min_price = 300
    max_price = 1000
    location = "memphis"
    
    # Build the Facebook Marketplace URL
    url = f"https://www.facebook.com/marketplace/{location}/search/?query={make}%20{model}&minPrice={min_price}&maxPrice={max_price}"
    
    print(f"Searching for {make} {model} bikes in {location}...")
    print(f"Price range: ${min_price} - ${max_price}")
    print(f"URL: {url}")
    
    # Get listings from Facebook Marketplace
    get_listings(url)
    print("Listings fetched")
    
    show_head()
    
    # Send email for new listings
    send_email_new_listings()

if __name__ == "__main__":
    main()