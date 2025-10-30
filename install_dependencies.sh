#!/bin/bash

# Installation script for Daudi's Blog
# This script sets up the Flask blog application

echo "🚀 Setting up Daudi's Blog..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Creating one..."
    python3 -m venv venv
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create placeholder images
echo "🖼️  Creating placeholder images..."
python utils/create_placeholders.py

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p static/css
mkdir -p static/js

# Set up environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env .env.example
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" >> .env
fi

# Make scripts executable
chmod +x deployment/deploy.sh
chmod +x utils/article_updater.py

echo "✅ Setup complete!"
echo ""
echo "🌟 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python app.py"
echo "3. Visit http://localhost:5000"
echo ""
echo "📝 To add new articles:"
echo "   python utils/article_updater.py sample > new_article.json"
echo "   # Edit the JSON file"
echo "   python utils/article_updater.py add new_article.json"
echo ""
echo "🚀 For production deployment:"
echo "   Upload to your server and run: sudo ./deployment/deploy.sh"
