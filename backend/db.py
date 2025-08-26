import sqlite3
from config import DB

db = DB['path']

def init_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
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

def reset_db(): 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Drop existing table
    cursor.execute('DROP TABLE IF EXISTS listings')
    print("Dropped listings.db")

    conn.commit()
    conn.close()

def insert_listings_batch(listings):
    """
    listings: list of dicts with keys price(int), title(str), location(str), url(str)
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # convert price strings to integers
    processed = [(l['price'], l['title'], l['location'], l['url']) for l in listings]
    
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

def fetch_unemailed_listings():
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # get unemailed listings sorted by price (lowest to highest)
    cur.execute("SELECT price, title, location, url FROM listings WHERE emailed=0 ORDER BY price ASC")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    # set unemailed listings to emailed 
    cur.execute("UPDATE listings SET emailed=1 WHERE emailed=0")
    
    conn.commit()
    conn.close()

    # convert to list of dicts
    listings = [{'price': r[0], 'title': r[1], 'location': r[2], 'url': r[3]} for r in rows]
    return listings, headers

def show_head(limit=5):
    """Show the first few rows of the database table (like Unix 'head' command)"""
    print("Showing db head")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM listings LIMIT ?', (limit,))
    listings = cursor.fetchall()
    
    print(f"\nFirst {limit} rows of listings table:")
    for listing in enumerate(listings):
        print(listing)
    
    conn.close()

def fetch_all_listings():
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT * FROM listings")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    
    conn.close()
    
    listings = [{'price': r[0], 'title': r[1], 'location': r[2], 'url': r[3]} for r in rows]
    
    return listings, headers