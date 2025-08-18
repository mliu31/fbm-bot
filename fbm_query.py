import json
import time
import re
from typing import List, Dict, Optional
from playwright.sync_api import Page
from datetime import datetime

class MarketplaceQuery:
    def __init__(self, page: Page):
        self.page = page
        self.listings = []
        
    def scrape_listings(self, max_listings: int = 50) -> List[Dict]:
        """Scrape listings from the current marketplace page"""
        try:
            # Wait for listings to load
            self.page.wait_for_selector('[data-testid="marketplace_feed"]', timeout=10000)
            time.sleep(3)
            
            # Scroll to load more listings
            self._scroll_to_load_listings(max_listings)
            
            # Get all listing elements
            listing_elements = self.page.query_selector_all('[data-testid="marketplace_feed"] > div')
            
            scraped_listings = []
            for element in listing_elements[:max_listings]:
                try:
                    listing_data = self._extract_listing_data(element)
                    if listing_data:
                        scraped_listings.append(listing_data)
                except Exception as e:
                    print(f"Error extracting listing data: {e}")
                    continue
            
            self.listings = scraped_listings
            print(f"Scraped {len(scraped_listings)} listings")
            return scraped_listings
            
        except Exception as e:
            print(f"Error scraping listings: {e}")
            return []
    
    def _scroll_to_load_listings(self, max_listings: int):
        """Scroll down to load more listings"""
        current_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 10
        
        while current_count < max_listings and scroll_attempts < max_scroll_attempts:
            # Count current listings
            current_listings = self.page.query_selector_all('[data-testid="marketplace_feed"] > div')
            current_count = len(current_listings)
            
            # Scroll down
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            scroll_attempts += 1
    
    def _extract_listing_data(self, element) -> Optional[Dict]:
        """Extract data from a single listing element"""
        try:
            # Extract title
            title_element = element.query_selector('a[href*="/marketplace/item/"]')
            title = title_element.get_attribute('aria-label') if title_element else "No title"
            
            # Extract link
            link = title_element.get_attribute('href') if title_element else ""
            if link and not link.startswith('http'):
                link = f"https://www.facebook.com{link}"
            
            # Extract price
            price_element = element.query_selector('span[dir="auto"]')
            price_text = price_element.inner_text() if price_element else "No price"
            price = self._extract_price(price_text)
            
            # Extract location
            location_element = element.query_selector('span[dir="auto"]:last-child')
            location = location_element.inner_text() if location_element else "No location"
            
            # Extract image
            img_element = element.query_selector('img')
            image_url = img_element.get_attribute('src') if img_element else ""
            
            return {
                'title': title,
                'price': price,
                'price_text': price_text,
                'location': location,
                'link': link,
                'image_url': image_url,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting listing data: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from price text"""
        try:
            # Remove common price indicators and extract numbers
            price_match = re.search(r'[\$]?([\d,]+)', price_text.replace(',', ''))
            if price_match:
                return float(price_match.group(1))
            return None
        except:
            return None
    
    def filter_listings(self, keywords: List[str] = None, min_price: float = None, 
                       max_price: float = None, location_keywords: List[str] = None) -> List[Dict]:
        """Filter listings based on criteria"""
        filtered_listings = self.listings.copy()
        
        if keywords:
            filtered_listings = [
                listing for listing in filtered_listings
                if any(keyword.lower() in listing['title'].lower() for keyword in keywords)
            ]
        
        if min_price is not None:
            filtered_listings = [
                listing for listing in filtered_listings
                if listing['price'] and listing['price'] >= min_price
            ]
        
        if max_price is not None:
            filtered_listings = [
                listing for listing in filtered_listings
                if listing['price'] and listing['price'] <= max_price
            ]
        
        if location_keywords:
            filtered_listings = [
                listing for listing in filtered_listings
                if any(keyword.lower() in listing['location'].lower() for keyword in location_keywords)
            ]
        
        return filtered_listings
    
    def save_to_json(self, filename: str = None):
        """Save listings to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"marketplace_listings_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.listings, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.listings)} listings to {filename}")
        return filename

if __name__ == "__main__":
    from login import FacebookLogin
    from enter_fbm import FacebookMarketplace
    
    # Test scraping
    fb_login = FacebookLogin()
    page = fb_login.login()
    
    if page:
        marketplace = FacebookMarketplace(page)
        marketplace.enter_marketplace()
        marketplace.search_marketplace("bike", "San Francisco, CA", 0, 1000)
        
        query = MarketplaceQuery(page)
        listings = query.scrape_listings(max_listings=20)
        
        # Filter for Cannondale bikes
        filtered = query.filter_listings(keywords=['cannondale'])
        print(f"Found {len(filtered)} Cannondale listings")
        
        # Save to JSON
        query.save_to_json()
        
        time.sleep(5)
    
    fb_login.close()
