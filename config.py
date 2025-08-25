# backend/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ----------------------------
# Credentials / secrets
# ----------------------------
CREDENTIALS = {
    'gmail_address': os.getenv('GMAIL'),
    'gmail_app_password': os.getenv('GMAIL_APP_PWD')
}

# ----------------------------
# Search parameters
# ----------------------------
SEARCH = {
    'keyword': 'cannondale',
    'query': 'cannondale caadx 105 51cm',
    'min_price': 300,
    'max_price': 1000,
    'location': 'memphis',  # all options (wopen incognito): https://www.facebook.com/marketplace/directory/US/?_se_imp=0oey5sMRMSl7wluQZ&_rdr
    'delimiter': '%20'
}

# ----------------------------
# Database configuration
# ----------------------------
BASE_DIR = Path(__file__).parent
DB = {
    'path': BASE_DIR / 'backend/listings.db'
}

# ----------------------------
# Runtime / environment flags
# ----------------------------
RUNTIME = {
    'headless': True, # Playwright, open browser as agent explores
    # 'log_level': 'INFO'
}

# ----------------------------
# Email / notification settings
# ----------------------------
EMAIL_SETTINGS = {
    'sender': CREDENTIALS['gmail_address'],
    'receiver': CREDENTIALS['gmail_address'],
    'smtp_port': 465
}
