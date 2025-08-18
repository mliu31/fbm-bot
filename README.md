# Facebook Marketplace Bot

A Playwright-based bot that automates Facebook Marketplace searches and sends email notifications for new listings.

## MVP Features

✅ **Playwright script** → logs into fb, opens saved search url, scrapes titles/prices/links, dumps to json  
✅ **Basic filters** → regex for keywords, price range, location  
✅ **Notification** → send email with new matches  
✅ **Scheduler** → run every 5–10 min (cron if local/server, background loop if always-on agent)  

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Environment

Copy the example config file and fill in your details:

```bash
cp config.env.example .env
```

Edit `.env` with your credentials:

```env
# Facebook Login Credentials
FB_EMAIL=your_email@example.com
FB_PASSWORD=your_password

# Search Configuration
SEARCH_URL=https://www.facebook.com/marketplace/search/
DEFAULT_LOCATION=San Francisco, CA
MIN_PRICE=0
MAX_PRICE=1000

# Notification Settings
NOTIFICATION_EMAIL=your_notification_email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username@gmail.com
SMTP_PASSWORD=your_app_password

# Search Keywords (comma-separated)
SEARCH_KEYWORDS=bike,cannondale bike,cannondale caad bike,cannondale caad10,cannondale caad11,cannondale caad12,cannondale caad13

# Search interval in minutes
SEARCH_INTERVAL_MINUTES=10
```

### 3. Test the Bot

Run the test suite to verify everything works:

```bash
python test_bot.py
```

### 4. Start the Bot

Run the scheduler to start monitoring:

```bash
python scheduler.py
```

## Usage

### Individual Components

#### Test Login
```bash
python login.py
```

#### Test Marketplace Search
```bash
python enter_fbm.py
```

#### Test Scraping
```bash
python fbm_query.py
```

#### Manage Search Queries
```bash
python save_query.py
```

### Configuration Options

#### Search Keywords
Set multiple keywords in `.env`:
```env
SEARCH_KEYWORDS=bike,cannondale bike,cannondale caad bike,cannondale caad10,cannondale caad11,cannondale caad12,cannondale caad13
```

#### Price Range
```env
MIN_PRICE=0
MAX_PRICE=1000
```

#### Location
```env
DEFAULT_LOCATION=San Francisco, CA
```

#### Search Interval
```env
SEARCH_INTERVAL_MINUTES=10
```

## How It Works

1. **Login**: Uses Playwright to log into Facebook with your credentials
2. **Search**: Navigates to Marketplace and searches for each keyword
3. **Scrape**: Extracts listing data (title, price, location, link, image)
4. **Filter**: Applies price and keyword filters
5. **Deduplicate**: Remembers previously seen listings to avoid duplicates
6. **Notify**: Sends email notifications for new listings
7. **Schedule**: Runs automatically at specified intervals

## File Structure

```
fbm-bot/
├── login.py              # Facebook login functionality
├── enter_fbm.py          # Marketplace navigation and search
├── fbm_query.py          # Listing scraping and filtering
├── notification.py       # Email notification system
├── scheduler.py          # Main bot with scheduling
├── save_query.py         # Query management utility
├── test_bot.py           # Test suite
├── requirements.txt      # Python dependencies
├── config.env.example    # Configuration template
└── README.md            # This file
```

## Email Setup

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in your `.env` file

## Troubleshooting

### Common Issues

1. **Login fails**: Check your Facebook credentials and ensure 2FA is properly configured
2. **No listings found**: Verify search keywords and location settings
3. **Email not sent**: Check SMTP settings and app password
4. **Playwright errors**: Run `playwright install chromium` to install browsers

### Debug Mode

Set `headless=False` in `login.py` to see the browser in action:

```python
self.browser = p.chromium.launch(headless=False)  # Set to True for production
```

## Future Enhancements

From the roadmap:
- [ ] Spec parsing (regex → AI later)
- [ ] Scoring/relevance
- [ ] Cooldowns, daily digest
- [ ] Sustainability impact calc

## Security Notes

- Never commit your `.env` file to version control
- Use app passwords for email, not your main password
- Consider running on a dedicated server for 24/7 operation

## License

This project is for educational purposes. Please respect Facebook's terms of service.



<!-- 
want playwright browser to open existing chrome profile (don't want to login each time bc fb would flag as bot)
but don't want to use existing chrome profile exactly bc might have race condition and/or corrupt this profile 

copy existing profile 
mac: 
cp -r ~/Library/Application\ Support/Google/Chrome/Default ~/Library/Application\ Support/Google/Chrome/playwright-fb

linux: 
cp -r ~/.config/google-chrome/Default ~/.config/google-chrome/playwright-fb

windows: 
Copy-Item "$env:LOCALAPPDATA\Google\Chrome\User Data\Default" "$env:LOCALAPPDATA\Google\Chrome\User Data\playwright-fb" -Recurse

now only need to login to playwright profile once 
 -->