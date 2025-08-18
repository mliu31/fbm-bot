#!/usr/bin/env python3
"""
Simple run script for Facebook Marketplace Bot
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    load_dotenv()
    
    required_vars = [
        'FB_EMAIL',
        'FB_PASSWORD',
        'NOTIFICATION_EMAIL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease copy config.env.example to .env and fill in your details.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def main():
    """Main entry point"""
    print("Facebook Marketplace Bot")
    print("=" * 30)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Import and run scheduler
    try:
        from scheduler import main as scheduler_main
        scheduler_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
