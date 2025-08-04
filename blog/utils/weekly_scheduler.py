#!/usr/bin/env python3
"""
Weekly Article Scheduler for Daudi's Blog
This script helps manage weekly article updates and reminders.
"""

import json
import os
import sys
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any

class WeeklyScheduler:
    def __init__(self, articles_file: str = 'data/articles.json'):
        self.articles_file = articles_file
        self.articles_data = self.load_articles()
    
    def load_articles(self) -> Dict[str, Any]:
        """Load articles from JSON file"""
        try:
            with open(self.articles_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"articles": []}
    
    def get_latest_article_date(self) -> datetime:
        """Get the date of the most recent article"""
        if not self.articles_data['articles']:
            return datetime.now() - timedelta(weeks=4)
        
        latest_date = None
        for article in self.articles_data['articles']:
            try:
                article_date = datetime.strptime(article['date'], '%B %d, %Y')
                if latest_date is None or article_date > latest_date:
                    latest_date = article_date
            except ValueError:
                continue
        
        return latest_date or datetime.now() - timedelta(weeks=4)
    
    def days_since_last_article(self) -> int:
        """Calculate days since the last article was published"""
        latest_date = self.get_latest_article_date()
        return (datetime.now() - latest_date).days
    
    def should_remind(self) -> bool:
        """Check if it's time for a weekly reminder"""
        days_since = self.days_since_last_article()
        return days_since >= 7
    
    def generate_article_ideas(self) -> List[str]:
        """Generate article ideas based on existing categories"""
        categories = set()
        for article in self.articles_data['articles']:
            categories.add(article['category'])
        
        ideas = {
            'Networks': [
                'The Future of 5G in Africa',
                'Building Resilient Internet Infrastructure',
                'Mesh Networks for Rural Connectivity',
                'The Role of Satellite Internet in Africa'
            ],
            'Automotive': [
                'Electric Vehicles in African Markets',
                'The Art of Vehicle Maintenance',
                'Off-Road Navigation Without GPS',
                'Sustainable Transportation Solutions'
            ],
            'Aviation': [
                'The Economics of Regional Aviation',
                'Weather Patterns and Flight Safety',
                'Drone Technology in Agriculture',
                'Airport Infrastructure Development'
            ],
            'Linux': [
                'Building Custom Linux Distributions',
                'Server Security Best Practices',
                'Open Source in Education',
                'Container Technology Explained'
            ],
            'Python': [
                'Machine Learning for Beginners',
                'Web Scraping Ethics and Techniques',
                'Building APIs with FastAPI',
                'Data Visualization Best Practices'
            ],
            'Embedded': [
                'IoT Security Fundamentals',
                'Low-Power Design Techniques',
                'Sensor Networks in Agriculture',
                'Real-Time Operating Systems'
            ]
        }
        
        suggestions = []
        for category in categories:
            if category in ideas:
                suggestions.extend([f"{category}: {idea}" for idea in ideas[category][:2]])
        
        return suggestions
    
    def create_reminder_content(self) -> str:
        """Create content for weekly reminder"""
        days_since = self.days_since_last_article()
        latest_date = self.get_latest_article_date()
        article_count = len(self.articles_data['articles'])
        ideas = self.generate_article_ideas()
        
        content = f"""
# Weekly Blog Update Reminder

## Blog Statistics
- Total Articles: {article_count}
- Last Article: {latest_date.strftime('%B %d, %Y')}
- Days Since Last Article: {days_since}

## Status
{'⚠️ Time for a new article!' if self.should_remind() else '✅ Blog is up to date'}

## Article Ideas
{chr(10).join([f'- {idea}' for idea in ideas[:6]])}

## Quick Commands
```bash
# Create new article
python utils/article_updater.py sample > new_article.json

# List current articles
python utils/article_updater.py list

# Add article after editing
python utils/article_updater.py add new_article.json
```

## Article Template
Remember to follow the established style:
- Personal perspective and experience
- Technical depth with practical examples
- Connection to African context where relevant
- "Anti-bloat" philosophy
- Clear, engaging writing

---
Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
"""
        return content
    
    def send_email_reminder(self, to_email: str, smtp_config: Dict[str, str]) -> bool:
        """Send email reminder (optional feature)"""
        try:
            content = self.create_reminder_content()
            
            msg = MIMEMultipart()
            msg['From'] = smtp_config['from_email']
            msg['To'] = to_email
            msg['Subject'] = f"Weekly Blog Reminder - {datetime.now().strftime('%B %d, %Y')}"
            
            msg.attach(MIMEText(content, 'plain'))
            
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def log_reminder(self, log_file: str = '/var/log/blog_reminders.log') -> None:
        """Log reminder to file"""
        try:
            content = self.create_reminder_content()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_file, 'a') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"REMINDER: {timestamp}\n")
                f.write(f"{'='*50}\n")
                f.write(content)
                f.write(f"\n{'='*50}\n\n")
            
            print(f"Reminder logged to {log_file}")
        except Exception as e:
            print(f"Failed to log reminder: {e}")

def main():
    """Main function for command-line usage"""
    scheduler = WeeklyScheduler()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python weekly_scheduler.py check     - Check if reminder needed")
        print("  python weekly_scheduler.py remind    - Generate reminder content")
        print("  python weekly_scheduler.py log       - Log reminder to file")
        print("  python weekly_scheduler.py stats     - Show blog statistics")
        return
    
    command = sys.argv[1]
    
    if command == "check":
        if scheduler.should_remind():
            print("⚠️ Time for a new article!")
            print(f"Days since last article: {scheduler.days_since_last_article()}")
            sys.exit(1)  # Exit with error code for cron job detection
        else:
            print("✅ Blog is up to date")
            sys.exit(0)
    
    elif command == "remind":
        print(scheduler.create_reminder_content())
    
    elif command == "log":
        scheduler.log_reminder()
    
    elif command == "stats":
        days_since = scheduler.days_since_last_article()
        latest_date = scheduler.get_latest_article_date()
        article_count = len(scheduler.articles_data['articles'])
        
        print(f"Blog Statistics:")
        print(f"  Total Articles: {article_count}")
        print(f"  Last Article: {latest_date.strftime('%B %d, %Y')}")
        print(f"  Days Since: {days_since}")
        print(f"  Status: {'⚠️ Needs Update' if scheduler.should_remind() else '✅ Current'}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()