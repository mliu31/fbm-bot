# Facebook Marketplace Bot 

A Python-based automation bot that scrapes Facebook Marketplace listings based on your search criteria (Playwright), stores them in a local database (sqlite), and sends email notifications for new listings. 

![ohmygodfinally](https://github.com/user-attachments/assets/a669cfa5-c816-4a58-a7f1-16d2ea66ca44)

This software is meant for educational purposes only. Use at your own risk.  

## Requirements
- Python 3.12+
- Google Chrome (for Playwright) or another supported browser

## Setup
1) Create and activate a venv
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source ./.venv/bin/activate # Linux
```

2) Install deps
```bash
pip install -r requirements.txt
python -m playwright install 
```
Note: ```playwright install``` installs the binaries that playwright needs to operate for your os/browser. This is distinct from the pip installed package, which are commands that need binaries to run. 

3) Configure
- Edit `config.py` to set:
  - DB path
  - SEARCH: query, delimiter, location, min_price, max_price, keyword
  - SMTP settings for email

4) Run 
```py main.py``` 

## Project Structure
- `main.py` - Main entry point for the bot
- `api.py` - FastAPI server with endpoints for scraping and emailing
- `config.py` - Configuration settings for search criteria and email
- `backend/` - Core backend modules
  - `scrape_fbm.py` - Facebook Marketplace scraping logic using Playwright
  - `db.py` - Database operations and SQLite setup
  - `services.py` - Logic for processing listings
  - `notifications.py` - Email notification system
  - `listings.db` - SQLite database storing scraped listings


## API (TODO frontend)
### Start server to host 
```bash
uvicorn api:app --reload  # runs on http://localhost:8000
```

### Endpoints
- POST `/scrape` — scrape FBM and insert listings to db 
- GET `/pending_listings` — listings to be emailed
- GET `/all_listings` — all listings in DB
- POST `/send_email` — email new listings

### Test endpoints on Postman 
```bash
POST http://localhost:8000/scrape
GET http://localhost:8000/pending_listings
GET http://localhost:8000/all_listings
post http://localhost:8000/send_email
```

## Notes (Windows)
If Playwright errors under Uvicorn, ensure browsers are installed and restart. The app sets a Windows event loop policy in `api.py`.

## How to Setup Autonomous Execution on Raspberry Pi
1. Open the crontab editor for your user
```bash
crontab -e
``` 
2. Setup daily script at 6:30pm 
```bash 
30 18 * * * cd /home/pi/fbm-bot && /home/pi/fbm-bot/.venv/bin/python main.py >> /home/pi/fbm-bot/cron.log 2>&1
``` 
Format: "minute hour day month weekday command". 

```cd … && … ``` ensures correct working directory

```>> cron.log 2>&1``` logs both stdout and errors

3. Check setup. 

## Challenges & Lessons Learned 
- Bot detection is constant cat-and-mouse
  - FB flags instant clicks/typing
  - Real account login felt unsafe (possible ban) → didn't log in + headless-humanlike pacing
- Keep secrets out of git 
  - Pushed .env → purged history, added to .gitignore
- System software matters
  - Old raspbian blocked deps → clean install fixed it
- Optimize for hardware limits
  - Firefox killed Raspberry Pi’s low RAM 
  - Switched to Chromium + added zram + 1GB swap
## Credits
Inspired by [Michael Reeves](https://www.youtube.com/@MichaelReeves/videos)

Built with help from:
- [Web Scraping Tutorial](https://www.youtube.com/watch?v=nE6m6LERn2U&t=1024s)
- [Email Sending Guide](https://cupofcode.blog/code-email-sending/)
- [Passivebot](https://github.com/passivebot/facebook-marketplace-scraper?tab=readme-ov-file#facebook-marketplace-scraper)
- Cursor/GPT-5/Gemini 2.5 Pro


## 
```cloc . --exclude-dir=.venv```

Number of lines of code = 245 
