import time
from config import RUNTIME
from playwright.sync_api import sync_playwright, TimeoutError
from playwright._impl._errors import TargetClosedError
from urllib.parse import urljoin


def get_listings(url, keyword):
    """
    Returns list of dicts: [{'price': int, 'title': str, 'location': str, 'url': str}, ...]
    """
    listings = []

    # fb marketplace search is not stringent with title 
    def filter_listing(price, title, location, href, keyword): 
        if keyword.lower() in title.lower():  
            return True 
            # TODO 
            # 1. agent visits url
            # 2. parse description for details
            # 3. OCR on images to extract text (make, model, groupset, disc brakes) TODO cv classifier for cyclocross bike? 
        return False 

    
    with sync_playwright() as p:
        # launch browser agent 
        browser = p.chromium.launch(headless=RUNTIME['headless'])  

        try: 
            page = browser.new_page()
            
            try:
                page.goto(url)
                # print("visited page:", page.title())
            except TimeoutError: 
                print("Timed out visiting ", url)

            time.sleep(3)

            # dismiss login popup if present
            login_locator = page.locator('div[aria-label="Close"]')
            if login_locator.is_visible():
                login_locator.first.click()

            time.sleep(3)

            # find listings 
            links = page.locator('[role="link"]')
            for i in range(links.count()):
                elem = links.nth(i)
                text = elem.inner_text()

                if len(text.split('\n')) < 3:  # not a listing (e.g., "Log in")
                    continue
                if len(text.split('\n')) > 3:  # if price dropped, two prices are listed. keep dropped price only
                    price, _, title, location = text.split('\n')
                else: 
                    price, title, location = text.split('\n')

                href = urljoin(page.url, elem.get_attribute('href'))
                
                # convert price to int 
                try:
                    price_int = int(price.replace('$', '').replace(',', '').strip())
                except ValueError:
                    price_int = 0

                if filter_listing(price_int, title, keyword, href, keyword):
                    listings.append({'price': price_int, 'title': title, 'location': location, 'url': href})
            
        except TargetClosedError:
            print("Browser/page died during navigation; retrying would recreate context.")
        finally:
            browser.close()
    return listings 