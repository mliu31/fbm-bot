import time
from playwright.sync_api import Page, sync_playwright
from human_actions import human_type, human_click

class FacebookMarketplace:
    def __init__(self, page: Page):
        self.page = page
        
    def enter_marketplace(self):
        """Navigate to Facebook Marketplace"""
        try:
            # Navigate to Facebook Marketplace
            self.page.goto('https://www.facebook.com/marketplace/')
            time.sleep(2)
            
            # Wait for marketplace to load
            self.page.wait_for_selector('[data-pagelet="MainFeed"]', timeout=10000)
            print("Successfully entered Facebook Marketplace")
            return True
            
        except Exception as e:
            print(f"Error entering marketplace: {e}")
            return False
    
    def search_marketplace(self, query: str, location: str = None, min_price: int = None, max_price: int = None):
        """Search for items in Facebook Marketplace"""
        try:
            # Type into search box with human-like behavior
            self.page.wait_for_selector('input[placeholder*="Search"]', timeout=5000)
            human_type(self.page, 'input[placeholder*="Search"]', query)
            
            # Press Enter to search
            self.page.keyboard.press('Enter')
            time.sleep(3)
            
            # Apply filters if provided
            if location:
                self._set_location(location)
            
            if min_price is not None or max_price is not None:
                # self._set_price_filter(min_price, max_price)
                pass
            
            print(f"Searching for: {query}")
            return True
            
        except Exception as e:
            print(f"Error searching marketplace: {e}")
            return False
    
    def _set_location(self, location: str):
        """Set location filter"""
        try:
            # Click on the first div with role="button" under seo_filters
            location_selector = '#seo_filters > div[role="button"]:first-child'
            human_click(self.page, location_selector)

            # human_click(self.page, 'input[aria-label*="Location"]')

            time.sleep(1)
            
            # Type location with human-like behavior
            human_type(self.page, 'input[placeholder*="location"]', location, clear_before=True)
            time.sleep(2)
            
            # Select first result
            human_click(self.page, '[role="option"]')
            
        except Exception as e:
            print(f"Error setting location: {e}")
    
    def _set_price_filter(self, min_price: int = None, max_price: int = None):
        """Set price filter"""
        try:
            # Open price filter
            human_click(self.page, 'button[aria-label*="Price"]')
            time.sleep(1)
            
            if min_price is not None:
                human_type(self.page, 'input[placeholder*="Min"]', str(min_price), clear_before=True)
            
            if max_price is not None:
                human_type(self.page, 'input[placeholder*="Max"]', str(max_price), clear_before=True)
            
            # Apply filter
            human_click(self.page, 'button[aria-label="Apply"]')
            
        except Exception as e:
            print(f"Error setting price filter: {e}")

if __name__ == "__main__":
    # Standalone test: open Facebook, navigate to Marketplace, and search (no login)
    with sync_playwright() as p:
        # chrome browser with pre-loaded cookies 
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # windows

        user_data_dir = "C:\\Users\\mgnli\\AppData\\Local\\Google\\Chrome\\User Data\\playwright-fb"

        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",                 # use system chrome
            executable_path=chrome_path,      # override bundled chromium
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            slow_mo=100 # Slows down actions by 50ms to make it easier to watch.
            
        )
            
        page = browser.new_page()
        page.goto('https://www.facebook.com/marketplace')
        time.sleep(2)

        marketplace = FacebookMarketplace(page)
        # marketplace.enter_marketplace()
        marketplace.search_marketplace("bike", "San Francisco, CA", 0, 1000)
        time.sleep(10)

        browser.close()