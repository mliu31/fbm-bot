import time
import schedule
import json
import os
from datetime import datetime
from typing import List, Dict, Set
from dotenv import load_dotenv

from login import FacebookLogin
from enter_fbm import FacebookMarketplace
from fbm_query import MarketplaceQuery
from notification import NotificationSystem

load_dotenv()

class MarketplaceBot:
    def __init__(self):
        self.seen_listings: Set[str] = set()
        self.notification = NotificationSystem()
        self.load_seen_listings()
        
    def load_seen_listings(self):
        """Load previously seen listings from file"""
        try:
            if os.path.exists('seen_listings.json'):
                with open('seen_listings.json', 'r') as f:
                    self.seen_listings = set(json.load(f))
                print(f"Loaded {len(self.seen_listings)} previously seen listings")
        except Exception as e:
            print(f"Error loading seen listings: {e}")
    
    def save_seen_listings(self):
        """Save seen listings to file"""
        try:
            with open('seen_listings.json', 'w') as f:
                json.dump(list(self.seen_listings), f)
        except Exception as e:
            print(f"Error saving seen listings: {e}")
    
    def get_search_keywords(self) -> List[str]:
        """Get search keywords from environment"""
        keywords = os.getenv('SEARCH_KEYWORDS', 'bike')
        return [kw.strip() for kw in keywords.split(',')]
    
    def run_search(self):
        """Run a complete search cycle"""
        print(f"\n=== Starting search cycle at {datetime.now()} ===")
        
        try:
            # Login to Facebook
            fb_login = FacebookLogin()
            page = fb_login.login()
            
            if not page:
                print("Failed to login to Facebook")
                return
            
            # Enter marketplace
            marketplace = FacebookMarketplace(page)
            if not marketplace.enter_marketplace():
                print("Failed to enter marketplace")
                return
            
            # Get search configuration
            keywords = self.get_search_keywords()
            location = os.getenv('DEFAULT_LOCATION', 'San Francisco, CA')
            min_price = int(os.getenv('MIN_PRICE', '0'))
            max_price = int(os.getenv('MAX_PRICE', '1000'))
            
            all_new_listings = []
            
            # Search for each keyword
            for keyword in keywords:
                print(f"Searching for: {keyword}")
                
                # Search marketplace
                marketplace.search_marketplace(keyword, location, min_price, max_price)
                time.sleep(3)
                
                # Scrape listings
                query = MarketplaceQuery(page)
                listings = query.scrape_listings(max_listings=30)
                
                # Filter for new listings
                new_listings = self._get_new_listings(listings)
                
                if new_listings:
                    print(f"Found {len(new_listings)} new listings for '{keyword}'")
                    all_new_listings.extend(new_listings)
                else:
                    print(f"No new listings found for '{keyword}'")
                
                time.sleep(2)
            
            # Send notification if new listings found
            if all_new_listings:
                self.notification.send_email_notification(
                    all_new_listings, 
                    f"Facebook Marketplace ({len(all_new_listings)} new items)"
                )
                print(f"Notification sent for {len(all_new_listings)} new listings")
            else:
                print("No new listings found in this cycle")
            
            # Save seen listings
            self.save_seen_listings()
            
            # Close browser
            fb_login.close()
            
        except Exception as e:
            print(f"Error in search cycle: {e}")
            # Send error notification
            self.notification.send_simple_notification(
                f"Facebook Marketplace Bot encountered an error: {e}",
                "Marketplace Bot Error"
            )
    
    def _get_new_listings(self, listings: List[Dict]) -> List[Dict]:
        """Filter out previously seen listings"""
        new_listings = []
        
        for listing in listings:
            # Create a unique identifier for the listing
            listing_id = f"{listing.get('title', '')}_{listing.get('price', '')}_{listing.get('location', '')}"
            
            if listing_id not in self.seen_listings:
                new_listings.append(listing)
                self.seen_listings.add(listing_id)
        
        return new_listings
    
    def start_scheduler(self, interval_minutes: int = 10):
        """Start the scheduler to run searches at regular intervals"""
        print(f"Starting scheduler - will run every {interval_minutes} minutes")
        
        # Schedule the job
        schedule.every(interval_minutes).minutes.do(self.run_search)
        
        # Run initial search
        self.run_search()
        
        # Keep the scheduler running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print("\nStopping scheduler...")
                break
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)

def main():
    """Main function to run the bot"""
    bot = MarketplaceBot()
    
    # Get interval from environment or use default
    interval = int(os.getenv('SEARCH_INTERVAL_MINUTES', '10'))
    
    print("Facebook Marketplace Bot Starting...")
    print(f"Search interval: {interval} minutes")
    print("Press Ctrl+C to stop")
    
    bot.start_scheduler(interval)

if __name__ == "__main__":
    main()
