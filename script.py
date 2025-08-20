import asyncio
import smtplib
import sqlite3
from email.mime.text import MIMEText
from playwright.async_api import async_playwright

# ------------ CONFIG ------------
SEARCH_URLS = [
    "https://www.facebook.com/marketplace/memphis/search/?query=cannondale%20caadx&minPrice=300&maxPrice=1000",
    "https://www.facebook.com/marketplace/memphis/search/?query=specialized%20crux&minPrice=300&maxPrice=1000",
]

DB_FILE = "listings.db"

EMAIL_SENDER = "youremail@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "destination@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# --------------------------------


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            title TEXT,
            price TEXT,
            location TEXT,
            url TEXT
        )
    """)
    conn.commit()
    return conn


def send_email_alert(title, price, location, url):
    msg = MIMEText(f"{title}\n{price}\n{location}\n{url}")
    msg["Subject"] = f"NEW FB Bike: {title} - {price}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


async def scrape():
    conn = init_db()
    c = conn.cursor()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        page = await browser.new_page()

        for url in SEARCH_URLS:
            await page.goto(url)
            await page.wait_for_timeout(5000)

            # try to close login popup if it shows up
            try:
                close_btn = await page.query_selector("div[aria-label='Close']")  # fb usually uses this
                if close_btn:
                    await close_btn.click()
                    await page.wait_for_timeout(2000)
            except Exception:
                pass

            items = await page.query_selector_all("a[href*='/marketplace/item/']")
            for item in items:
                href = await item.get_attribute("href")
                if not href:
                    continue
                link = "https://www.facebook.com" + href.split("?")[0]
                id_ = link.split("/")[-1]

                title_el = await item.query_selector("span")
                title = await title_el.inner_text() if title_el else "No title"

                price_el = await item.query_selector("span[dir='auto']")
                price = await price_el.inner_text() if price_el else "?"

                location = "?"

                # check db for duplicates
                c.execute("SELECT 1 FROM listings WHERE id=?", (id_,))
                if not c.fetchone():
                    c.execute(
                        "INSERT INTO listings (id, title, price, location, url) VALUES (?, ?, ?, ?, ?)",
                        (id_, title, price, location, link),
                    )
                    conn.commit()
                    print(f"New listing: {title} - {price} - {location} - {link}")
                    # send_email_alert(title, price, location, link)

        await browser.close()
    conn.close()


if __name__ == "__main__":
    asyncio.run(scrape())
