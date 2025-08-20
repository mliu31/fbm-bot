from playwright.sync_api import sync_playwright
import sqlite3

def create_database():
    conn = sqlite3.connect('listings.db')
    cursor = conn.cursor()
    
    # Drop existing table
    # cursor.execute('DROP TABLE IF EXISTS listings')
    
    # Create table for Facebook Marketplace listings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price INTEGER,
            title TEXT,
            location TEXT,
            url TEXT UNIQUE,
            emailed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_listings_batch(listings):
    conn = sqlite3.connect('listings.db')
    cursor = conn.cursor()
    
    # convert price strings to integers
    processed = []
    for price, title, location, url in listings:
        try:
            price_num = int(price.replace('$', '').replace(',', '').strip())
        except ValueError:
            price_num = 0
        processed.append((price_num, title, location, url)) 
    
    cursor.executemany('''
    INSERT INTO listings (price, title, location, url)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(url) DO UPDATE SET
        price=excluded.price,
        emailed=0, -- reset so you can trigger a new email
        created_at=CURRENT_TIMESTAMP
    WHERE excluded.price != listings.price;
''', processed)

    
    conn.commit()
    conn.close()

def show_listings(): 
    conn = sqlite3.connect('listings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM listings')
    listings = cursor.fetchall()
    for listing in listings:
        print(listing)
    conn.close()

# fb marketplace search is not stringent with title 
def filter_listing(price, title, location, href): 
    if "cannondale" in title.lower():  # TODO generalize to any query with no make? 
        return True 
        # TODO 
        # 1. enter url
        # 2. parse description for details
        # 3. OCR on images to extract text (make, model, groupset, disc brakes) TODO cv classifier for cyclocross bike? 
    return False 

def get_listings(url):
    # Create database 
    create_database()
    listings = []
    with sync_playwright() as p:
        # launch browser agent 
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # x out the login info 
        login_locator = page.locator('div[aria-label="Close"]')
        if login_locator:
            login_locator.first.click()

        # find listings (will have attribute role="link")
        links = page.locator('[role="link"]')

        # extract information from each listing/link 
        for i in range(links.count()):
            link_element = links.nth(i)
            text = link_element.inner_text()
            if len(text.split('\n')) <= 1:  # not a listing (e.g., "Log in")
                continue
            href = "facebook.com" + link_element.get_attribute('href')

            if len(text.split('\n')) > 3:  # if price dropped, two prices are listed. keep dropped price only
                price, _, title, location = text.split('\n')
            elif len(text.split('\n')) == 3:
                price, title, location = text.split('\n')
            else:
                print("Error parsing text from listing", text)
                continue

            if filter_listing(price, title, location, href):
                listings.append((price, title, location, href))
        
        insert_listings_batch(listings)    
        browser.close()