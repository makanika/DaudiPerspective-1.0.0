#!/usr/bin/env python3
"""
Article Updater for Daudi's Blog
This script can be used to add new articles or update existing ones.
Can be run manually or scheduled as a cron job for weekly updates.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ArticleUpdater:
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
    
    def save_articles(self) -> None:
        """Save articles back to JSON file"""
        with open(self.articles_file, 'w') as f:
            json.dump(self.articles_data, f, indent=2)
    
    def add_article(self, article: Dict[str, Any]) -> None:
        """Add a new article"""
        # Ensure required fields
        required_fields = ['id', 'title', 'category', 'content']
        for field in required_fields:
            if field not in article:
                raise ValueError(f"Missing required field: {field}")
        
        # Add date if not provided
        if 'date' not in article:
            article['date'] = datetime.now().strftime('%B %d, %Y')
        
        # Add image placeholder if not provided
        if 'image' not in article:
            article['image'] = f"{article['id']}.jpg"
        
        self.articles_data['articles'].append(article)
        self.save_articles()
        print(f"Added article: {article['title']}")
    
    def update_article(self, article_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing article"""
        for i, article in enumerate(self.articles_data['articles']):
            if article['id'] == article_id:
                self.articles_data['articles'][i].update(updates)
                self.save_articles()
                print(f"Updated article: {article['title']}")
                return True
        return False
    
    def list_articles(self) -> None:
        """List all articles"""
        print("\nCurrent Articles:")
        print("-" * 50)
        for i, article in enumerate(self.articles_data['articles'], 1):
            print(f"{i}. {article['title']} ({article['category']}) - {article['date']}")
    
    def create_sample_article(self) -> Dict[str, Any]:
        """Create a sample article template"""
        return {
            "id": "sample-article",
            "title": "Sample Article Title",
            "category": "Technology",
            "date": datetime.now().strftime('%B %d, %Y'),
            "image": "sample-article.jpg",
            "content": [
                "This is the first paragraph of your article. It should introduce the main topic and grab the reader's attention.",
                "This is the second paragraph. You can continue developing your ideas here.",
                "Add as many paragraphs as needed. Each paragraph should be a separate string in this list."
            ]
        }

def main():
    """Main function for command-line usage"""
    updater = ArticleUpdater()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python article_updater.py list                    - List all articles")
        print("  python article_updater.py sample                  - Show sample article format")
        print("  python article_updater.py add <json_file>         - Add article from JSON file")
        print("  python article_updater.py update <id> <json_file> - Update article")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        updater.list_articles()
    
    elif command == "sample":
        sample = updater.create_sample_article()
        print("\nSample Article Format:")
        print(json.dumps(sample, indent=2))
        print("\nSave this to a JSON file and use 'add' command to add it to the blog.")
    
    elif command == "add" and len(sys.argv) == 3:
        json_file = sys.argv[2]
        try:
            with open(json_file, 'r') as f:
                article = json.load(f)
            updater.add_article(article)
        except Exception as e:
            print(f"Error adding article: {e}")
    
    elif command == "update" and len(sys.argv) == 4:
        article_id = sys.argv[2]
        json_file = sys.argv[3]
        try:
            with open(json_file, 'r') as f:
                updates = json.load(f)
            if updater.update_article(article_id, updates):
                print("Article updated successfully")
            else:
                print(f"Article with ID '{article_id}' not found")
        except Exception as e:
            print(f"Error updating article: {e}")
    
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()