from playwright.sync_api import sync_playwright
import sqlite3

def create_database():
    conn = sqlite3.connect('listings.db')
    cursor = conn.cursor()
    # Create table for Facebook Marketplace listings
    cursor.execute('''
        CREATE TABLE listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price INTEGER,
            title TEXT,
            location TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    print("Database table created with INTEGER price column")
    conn.commit()
    conn.close()

def insert_listing(price, title, location, url):
    conn = sqlite3.connect('listings.db')
    cursor = conn.cursor()
    
    # Convert price string to number (remove $ and commas, then convert to integer)
    try:
        # Clean the price string and convert to integer
        price_num = int(price.replace('$', '').replace(',', '').strip())
    except ValueError as e:
        price_num = 0  # Default to 0 if conversion fails
    
    cursor.execute('''
        INSERT INTO listings (price, title, location, url)
        VALUES (?, ?, ?, ?)
    ''', (price_num, title, location, url))
    
    # print(f"Inserted: price={price_num}, title={title}, location={location}, url={url}")
    
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
def prefilter(title):  # TODO generalize to any product? 
    if make in title.lower():
        return True
    return False

def get_listings(url. make):
    # Create database 
    create_database()
    
    with sync_playwright() as p:
        # launch browser agent 
        browser = p.chromium.launch(headless=False)
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

            # Insert into database
            if prefilter(title):
                insert_listing(price, title, location, href)
            
        browser.close()


make = "cannondale"
model = "caadx"
min_price = 300
max_price = 1000

get_listings(f"https://www.facebook.com/marketplace/memphis/search/?query={make}%20{model}&minPrice={min_price}&maxPrice={max_price}",make)
show_listings()