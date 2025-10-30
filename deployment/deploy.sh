#!/bin/bash

# Deployment script for Daudi's Blog on Digital Ocean
# Run this script on your Digital Ocean droplet

set -e  # Exit on any error

echo "🚀 Starting deployment of Daudi's Blog..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# Create application directory
APP_DIR="/var/www/daudi_blog"
echo "📁 Setting up application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or copy application files
echo "📥 Setting up application files..."
# If using git:
# git clone https://github.com/yourusername/daudi-blog.git $APP_DIR
# cd $APP_DIR

# If copying files manually, ensure all files are in $APP_DIR

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating necessary directories..."
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
sudo chown www-data:www-data /var/run/gunicorn

# Set up environment variables
echo "⚙️ Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
EOF
fi

# Set up Supervisor for process management
echo "👮 Setting up Supervisor..."
sudo tee /etc/supervisor/conf.d/daudi_blog.conf > /dev/null << EOF
[program:daudi_blog]
command=$APP_DIR/venv/bin/gunicorn --config $APP_DIR/deployment/gunicorn.conf.py app:app
directory=$APP_DIR
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/gunicorn/daudi_blog.log
EOF

# Set up Nginx
echo "🌐 Setting up Nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/daudi_blog
sudo ln -sf /etc/nginx/sites-available/daudi_blog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Set proper permissions
echo "🔐 Setting file permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Start services
echo "🚀 Starting services..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start daudi_blog
sudo systemctl restart nginx
sudo systemctl enable nginx
sudo systemctl enable supervisor

# Set up firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# Create weekly update cron job
echo "⏰ Setting up weekly article update cron job..."
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd $APP_DIR && python3 utils/article_updater.py list >> /var/log/weekly_update.log 2>&1") | crontab -

echo "✅ Deployment completed successfully!"
echo ""
echo "🌍 Your blog should now be accessible at your domain/IP address"
echo "📊 Check status with: sudo supervisorctl status daudi_blog"
echo "📝 View logs with: sudo tail -f /var/log/gunicorn/daudi_blog.log"
echo ""
echo "🔧 Next steps:"
echo "1. Update your domain name in deployment/nginx.conf"
echo "2. Set up SSL certificate with Let's Encrypt"
echo "3. Add your article images to static/images/"
echo "4. Test the weekly update system"
