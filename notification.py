import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class NotificationSystem:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL')
        
    def send_email_notification(self, new_listings: List[Dict], search_query: str = "Facebook Marketplace"):
        """Send email notification about new listings"""
        if not new_listings:
            print("No new listings to notify about")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.notification_email
            msg['Subject'] = f"New {search_query} Listings Found! ({len(new_listings)} items)"
            
            # Create HTML body
            html_body = self._create_html_email(new_listings, search_query)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"Email notification sent to {self.notification_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
    
    def _create_html_email(self, listings: List[Dict], search_query: str) -> str:
        """Create HTML email body"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .listing {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .title {{ font-weight: bold; font-size: 16px; color: #1877f2; }}
                .price {{ font-size: 18px; color: #42b883; font-weight: bold; }}
                .location {{ color: #666; font-size: 14px; }}
                .link {{ color: #1877f2; text-decoration: none; }}
                .link:hover {{ text-decoration: underline; }}
                .image {{ max-width: 200px; max-height: 150px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h2>New {search_query} Listings Found!</h2>
            <p>Found {len(listings)} new listings that match your criteria.</p>
        """
        
        for listing in listings:
            html += f"""
            <div class="listing">
                <div class="title">{listing.get('title', 'No title')}</div>
                <div class="price">{listing.get('price_text', 'No price')}</div>
                <div class="location">{listing.get('location', 'No location')}</div>
                <div style="margin: 10px 0;">
                    <a href="{listing.get('link', '#')}" class="link" target="_blank">View Listing</a>
                </div>
                {f'<img src="{listing.get("image_url", "")}" class="image" alt="Listing image">' if listing.get('image_url') else ''}
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def send_simple_notification(self, message: str, subject: str = "Facebook Marketplace Bot"):
        """Send a simple text notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.notification_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"Simple notification sent: {subject}")
            return True
            
        except Exception as e:
            print(f"Error sending simple notification: {e}")
            return False

if __name__ == "__main__":
    # Test notification system
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
    
    notification.send_email_notification(sample_listings, "Cannondale Bike")
