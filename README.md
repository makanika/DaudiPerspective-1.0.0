# Daudi's Perspective Blog

A Flask-based blog application preserving the original design and styling while adding dynamic functionality.

## Features

- **Preserved Design**: Maintains the exact original styling with Lora and Lato fonts, warm color scheme, and subtle checkered background
- **Dynamic Content**: Articles stored in JSON format for easy management
- **Individual Article Pages**: Each article has its own URL
- **Responsive Design**: Works on all device sizes
- **SEO Friendly**: Proper meta tags and semantic HTML
- **Weekly Updates**: Built-in system for adding new articles
- **Digital Ocean Ready**: Configured for production deployment

## Project Structure

\`\`\`
blog/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── Procfile             # For deployment
├── runtime.txt          # Python version
├── templates/
│   ├── base.html        # Base template with original styling
│   ├── index.html       # Main blog page
│   └── article.html     # Individual article page
├── static/
│   └── images/          # Article images
├── data/
│   └── articles.json    # Article content and metadata
├── utils/
│   ├── article_updater.py    # Weekly update utility
│   └── create_placeholders.py # Image placeholder generator
└── deployment/
    ├── deploy.sh        # Deployment script
    ├── gunicorn.conf.py # Gunicorn configuration
    └── nginx.conf       # Nginx configuration
\`\`\`

## Quick Start

### Local Development

1. **Install Dependencies**
   \`\`\`bash
   cd blog
   pip install -r requirements.txt
   \`\`\`

2. **Create Placeholder Images**
   \`\`\`bash
   python utils/create_placeholders.py
   \`\`\`

3. **Run the Application**
   \`\`\`bash
   python app.py
   \`\`\`

4. **Visit** http://localhost:5000

### Production Deployment (Digital Ocean)

1. **Prepare Your Droplet**
   - Create a Ubuntu 20.04+ droplet
   - Point your domain to the droplet's IP

2. **Upload Your Code**
   \`\`\`bash
   scp -r blog/ user@your-server:/var/www/
   \`\`\`

3. **Run Deployment Script**
   \`\`\`bash
   ssh user@your-server
   cd /var/www/blog
   chmod +x deployment/deploy.sh
   sudo ./deployment/deploy.sh
   \`\`\`

4. **Configure Domain**
   - Update `deployment/nginx.conf` with your domain
   - Restart nginx: `sudo systemctl restart nginx`

## Article Management

### Current Articles (All dated July 14, 2025)

1. **Networks**: "The Internet in Africa is Just a Connection to Europe"
2. **Automotive**: "The Soul of the Machine" 
3. **Aviation**: "The Simple Genius of the Turbofan"
4. **Linux**: "My Operating System is a Land Cruiser"
5. **Python**: "The Language That Speaks to Machines"
6. **Embedded**: "The Hidden Genius All Around Us"

### Adding New Articles

1. **Using the Article Updater**
   \`\`\`bash
   # See current articles
   python utils/article_updater.py list
   
   # Create a sample article template
   python utils/article_updater.py sample > new_article.json
   
   # Edit the JSON file with your content
   # Then add it to the blog
   python utils/article_updater.py add new_article.json
   \`\`\`

2. **Manual JSON Format**
   \`\`\`json
   {
     "id": "unique-article-id",
     "title": "Article Title",
     "category": "Category",
     "date": "Month Day, Year",
     "image": "image-filename.jpg",
     "content": [
       "First paragraph...",
       "Second paragraph...",
       "etc..."
     ]
   }
   \`\`\`

### Weekly Updates

Set up a cron job for weekly article reminders:
\`\`\`bash
# Edit crontab
crontab -e

# Add this line for Monday 9 AM reminders
0 9 * * 1 cd /var/www/blog && python utils/article_updater.py list >> /var/log/weekly_update.log 2>&1
\`\`\`

## Image Management

### Current Placeholder Images

The blog includes placeholder images for all articles. To replace with real images:

1. **Download Images**
   - Use Unsplash, Pexels, or other free stock photo sites
   - Recommended search terms:
     - Networks: "fiber optic cables", "network infrastructure"
     - Automotive: "Toyota Land Cruiser", "off-road vehicle"
     - Aviation: "jet engine", "turbofan engine"
     - Linux: "Ubuntu desktop", "terminal screen"
     - Python: "microcontroller", "ESP32", "programming"
     - Embedded: "circuit board", "electronics"

2. **Prepare Images**
   - Resize to 1200x600 pixels
   - Optimize for web (JPEG, 80-90% quality)
   - Name according to articles.json

3. **Upload**
   \`\`\`bash
   scp image.jpg user@server:/var/www/blog/static/images/
   \`\`\`

## Customization

### Styling
- All original CSS is preserved in `templates/base.html`
- Colors: Warm off-white background (#FDFDFB), brown headings (#5C554F)
- Fonts: Lora (serif) for body, Lato (sans-serif) for headings
- Subtle checkered background pattern maintained

### Configuration
- Edit `.env` for environment variables
- Modify `config.py` for Flask settings
- Update `data/articles.json` for content

### Navigation
- Categories automatically link to article sections
- Individual article URLs: `/article/article-id`
- Home page shows all articles in order

## Security & Performance

- **Environment Variables**: Sensitive data in `.env`
- **Static Files**: Served efficiently by Nginx
- **Process Management**: Supervised by systemd
- **Logging**: Comprehensive error and access logs
- **Firewall**: UFW configured for security

## Monitoring

### Check Application Status
\`\`\`bash
# Application status
sudo supervisorctl status daudi_blog

# View logs
sudo tail -f /var/log/gunicorn/daudi_blog.log

# Nginx status
sudo systemctl status nginx
\`\`\`

### Health Check
Visit `/health` endpoint for application status.

## SSL Certificate (Optional)

After deployment, secure with Let's Encrypt:
\`\`\`bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
\`\`\`

## Backup

### Database (JSON)
\`\`\`bash
# Backup articles
cp /var/www/blog/data/articles.json ~/backup/articles_$(date +%Y%m%d).json
\`\`\`

### Images
\`\`\`bash
# Backup images
tar -czf ~/backup/images_$(date +%Y%m%d).tar.gz /var/www/blog/static/images/
\`\`\`

## Troubleshooting

### Common Issues

1. **Application Won't Start**
   - Check logs: `sudo tail -f /var/log/gunicorn/daudi_blog.log`
   - Verify permissions: `sudo chown -R www-data:www-data /var/www/blog`

2. **Images Not Loading**
   - Check file permissions: `chmod 644 static/images/*`
   - Verify Nginx configuration

3. **Articles Not Updating**
   - Validate JSON syntax: `python -m json.tool data/articles.json`
   - Restart application: `sudo supervisorctl restart daudi_blog`

### Support

For issues or questions:
1. Check the logs first
2. Verify configuration files
3. Test locally before deploying
4. Ensure all dependencies are installed

## License

This blog application preserves the original design and content structure while adding modern web application functionality.
