import json
import os
from flask import Flask, render_template, abort
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

def load_articles():
    """Load articles from JSON file"""
    try:
        with open('data/articles.json', 'r') as f:
            data = json.load(f)
            return data['articles']
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    """Main blog page with all articles"""
    articles = load_articles()
    return render_template('index.html', articles=articles)

@app.route('/article/<article_id>')
def article(article_id):
    """Individual article page"""
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    
    if not article:
        abort(404)
    
    return render_template('article.html', article=article)

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return {'status': 'healthy', 'articles_count': len(load_articles())}

@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    return render_template('base.html'), 404

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5003)