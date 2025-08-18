#!/usr/bin/env python3
"""
Test script for Facebook Marketplace Bot
Run this to test individual components
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_login():
    """Test Facebook login"""
    print("Testing Facebook login...")
    from login import FacebookLogin
    
    fb_login = FacebookLogin()
    page = fb_login.login()
    
    if page:
        print("✓ Login successful!")
        fb_login.close()
        return True
    else:
        print("✗ Login failed!")
        return False

def test_marketplace():
    """Test marketplace entry and search"""
    print("\nTesting marketplace entry...")
    from login import FacebookLogin
    from enter_fbm import FacebookMarketplace
    
    fb_login = FacebookLogin()
    page = fb_login.login()
    
    if not page:
        print("✗ Cannot test marketplace without login")
        return False
    
    marketplace = FacebookMarketplace(page)
    
    # Test entering marketplace
    if marketplace.enter_marketplace():
        print("✓ Marketplace entry successful!")
        
        # Test search
        if marketplace.search_marketplace("bike", "San Francisco, CA", 0, 1000):
            print("✓ Search successful!")
            fb_login.close()
            return True
        else:
            print("✗ Search failed!")
            fb_login.close()
            return False
    else:
        print("✗ Marketplace entry failed!")
        fb_login.close()
        return False

def test_scraping():
    """Test listing scraping"""
    print("\nTesting listing scraping...")
    from login import FacebookLogin
    from enter_fbm import FacebookMarketplace
    from fbm_query import MarketplaceQuery
    
    fb_login = FacebookLogin()
    page = fb_login.login()
    
    if not page:
        print("✗ Cannot test scraping without login")
        return False
    
    marketplace = FacebookMarketplace(page)
    marketplace.enter_marketplace()
    marketplace.search_marketplace("bike", "San Francisco, CA", 0, 1000)
    
    query = MarketplaceQuery(page)
    listings = query.scrape_listings(max_listings=5)
    
    if listings:
        print(f"✓ Scraped {len(listings)} listings!")
        for listing in listings[:2]:  # Show first 2 listings
            print(f"  - {listing.get('title', 'No title')} - {listing.get('price_text', 'No price')}")
        
        # Test filtering
        filtered = query.filter_listings(keywords=['cannondale'])
        print(f"✓ Filtered to {len(filtered)} Cannondale listings")
        
        fb_login.close()
        return True
    else:
        print("✗ No listings scraped!")
        fb_login.close()
        return False

def test_notification():
    """Test notification system"""
    print("\nTesting notification system...")
    from notification import NotificationSystem
    
    notification = NotificationSystem()
    
    # Test with sample data
    sample_listings = [
        {
            'title': 'Cannondale CAAD10 Road Bike',
            'price': 800.0,
            'price_text': '$800',
            'location': 'San Francisco, CA',
            'link': 'https://www.facebook.com/marketplace/item/123456',
            'image_url': 'https://example.com/bike.jpg'
        }
    ]
    
    # Only send if email is configured
    if os.getenv('SMTP_USERNAME') and os.getenv('SMTP_PASSWORD'):
        if notification.send_email_notification(sample_listings, "Test Notification"):
            print("✓ Email notification sent!")
            return True
        else:
            print("✗ Email notification failed!")
            return False
    else:
        print("⚠ Email not configured - skipping notification test")
        return True

def test_query_manager():
    """Test query manager"""
    print("\nTesting query manager...")
    from save_query import QueryManager
    
    manager = QueryManager("test_queries.json")
    
    # Add test query
    manager.add_query("test bike", "San Francisco, CA", 0, 1000)
    
    # List queries
    active_queries = manager.get_active_queries()
    if active_queries:
        print(f"✓ Query manager working! {len(active_queries)} active queries")
        
        # Clean up test file
        if os.path.exists("test_queries.json"):
            os.remove("test_queries.json")
        return True
    else:
        print("✗ Query manager failed!")
        return False

def main():
    """Run all tests"""
    print("Facebook Marketplace Bot - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Login", test_login),
        ("Marketplace", test_marketplace),
        ("Scraping", test_scraping),
        ("Notification", test_notification),
        ("Query Manager", test_query_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Results:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Bot is ready to use.")
    else:
        print("⚠ Some tests failed. Check configuration and try again.")

if __name__ == "__main__":
    main()
