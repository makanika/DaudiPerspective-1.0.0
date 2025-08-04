import json
import os
import math
from flask import Flask, render_template, abort, request
from dotenv import load_dotenv
from operator import itemgetter

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management, loaded from environment variables
# with a default value for development.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-secure-development-secret-key')

# Define the number of articles to display on each paginated page.
ARTICLES_PER_PAGE = 2

def load_articles():
    """
    Loads articles from the 'articles.json' file.
    
    This function reads the JSON file, extracts the list of articles,
    and sorts them in reverse chronological order based on their date.
    This ensures that the newest articles appear first.
    
    Returns:
        list: A sorted list of article dictionaries. Returns an empty list if the file is not found.
    """
    try:
        with open('data/articles.json', 'r') as f:
            data = json.load(f)
            # Sort articles by date in descending order.
            # This assumes the date format is consistent and sortable.
            return sorted(data['articles'], key=itemgetter('date'), reverse=True)
    except FileNotFoundError:
        # If the articles file doesn't exist, return an empty list to avoid errors.
        return []

@app.route('/')
def index():
    """
    Handles the main blog page, displaying a paginated list of articles.
    
    It retrieves the current page number from the URL's query parameters.
    It then calculates which articles to display for that page and determines
    the total number of pages needed.
    """
    all_articles = load_articles()
    
    # Get the current page number from the URL query string (e.g., /?page=2).
    # Defaults to page 1 if not specified.
    page = request.args.get('page', 1, type=int)
    
    # Calculate the starting and ending indices for the articles on the current page.
    start_index = (page - 1) * ARTICLES_PER_PAGE
    end_index = start_index + ARTICLES_PER_PAGE
    
    # Slice the list of all articles to get only the ones for the current page.
    paginated_articles = all_articles[start_index:end_index]
    
    # Calculate the total number of pages required to display all articles.
    total_pages = math.ceil(len(all_articles) / ARTICLES_PER_PAGE)
    
    # Render the index.html template, passing the necessary data to it.
    return render_template(
        'index.html', 
        articles=paginated_articles,
        page=page,
        total_pages=total_pages
    )

@app.route('/article/<article_id>')
def article(article_id):
    """
    Displays a single, full article based on its unique ID.
    
    Args:
        article_id (str): The unique identifier for the article.
    """
    articles = load_articles()
    # Find the article with the matching ID.
    article_data = next((a for a in articles if a['id'] == article_id), None)
    
    # If no article with the given ID is found, return a 404 Not Found error.
    if not article_data:
        abort(404)
    
    # Render the article.html template for the found article.
    return render_template('article.html', article=article_data)

@app.route('/health')
def health_check():
    """
    A simple health check endpoint for monitoring services.
    
    Returns a JSON response indicating the application's status and the number of articles.
    """
    return {'status': 'healthy', 'articles_count': len(load_articles())}

@app.errorhandler(404)
def not_found(error):
    """
    Custom handler for 404 Not Found errors.
    
    Renders the base template with a 404 status code.
    """
    return render_template('base.html'), 404

# This block runs the application in debug mode when the script is executed directly.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
