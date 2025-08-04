# Deployment Guide for Daudi's Blog

This guide will help you deploy the blog to Digital Ocean and set up weekly article management.

## Prerequisites

- Digital Ocean account
- Domain name (optional but recommended)
- SSH access to your server
- Basic command line knowledge

## Step 1: Create Digital Ocean Droplet

1. **Create Droplet**
   - Choose Ubuntu 20.04 LTS or newer
   - Select appropriate size (Basic $5/month is sufficient)
   - Add your SSH key
   - Choose a datacenter region close to your audience

2. **Initial Server Setup**
   ```bash
   # Connect to your server
   ssh root@your-server-ip
   
   # Update system
   apt update && apt upgrade -y
   
   # Create a non-root user (optional but recommended)
   adduser daudi
   usermod -aG sudo daudi
   
   # Switch to new user
   su - daudi
   ```

## Step 2: Upload Your Blog

1. **Prepare Local Files**
   ```bash
   # On your local machine, compress the blog
   cd /path/to/your/blog
   tar -czf daudi-blog.tar.gz blog/
   ```

2. **Upload to Server**
   ```bash
   # Upload the compressed file
   scp daudi-blog.tar.gz daudi@your-server-ip:~/
   
   # Connect to server and extract
   ssh daudi@your-server-ip
   tar -xzf daudi-blog.tar.gz
   sudo mv blog /var/www/daudi_blog
   sudo chown -R daudi:daudi /var/www/daudi_blog
   ```

## Step 3: Run Deployment Script

```bash
cd /var/www/daudi_blog
chmod +x deployment/deploy.sh
sudo ./deployment/deploy.sh
```

The deployment script will:
- Install system dependencies (Python, Nginx, Supervisor)
- Set up Python virtual environment
- Install Python packages
- Configure Gunicorn
- Set up Nginx
- Configure firewall
- Start services

## Step 4: Configure Domain (Optional)

1. **Update DNS**
   - Point your domain's A record to your server's IP
   - Wait for DNS propagation (up to 24 hours)

2. **Update Nginx Configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/daudi_blog
   
   # Replace 'your-domain.com' with your actual domain
   # Save and exit
   
   sudo nginx -t  # Test configuration
   sudo systemctl reload nginx
   ```

## Step 5: Set Up SSL (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## Step 6: Configure Weekly Updates

1. **Set Up Cron Job**
   ```bash
   crontab -e
   
   # Add this line for Monday 9 AM reminders
   0 9 * * 1 cd /var/www/daudi_blog && python utils/weekly_scheduler.py log
   
   # Optional: Check daily and send alerts if overdue
   0 18 * * * cd /var/www/daudi_blog && python utils/weekly_scheduler.py check || echo "Blog needs update!" | mail -s "Blog Update Needed" your-email@example.com
   ```

2. **Test Weekly Scheduler**
   ```bash
   cd /var/www/daudi_blog
   python utils/weekly_scheduler.py stats
   python utils/weekly_scheduler.py remind
   ```

## Step 7: Add Real Images

1. **Download Images**
   - Use Unsplash, Pexels, or other free stock photo sites
   - Search for relevant terms for each article category

2. **Prepare Images**
   ```bash
   # Resize images to 1200x600 (you can use ImageMagick)
   sudo apt install imagemagick
   convert original-image.jpg -resize 1200x600^ -gravity center -extent 1200x600 resized-image.jpg
   ```

3. **Upload Images**
   ```bash
   # Upload to server
   scp *.jpg daudi@your-server-ip:/var/www/daudi_blog/static/images/
   
   # Set proper permissions
   sudo chown www-data:www-data /var/www/daudi_blog/static/images/*
   sudo chmod 644 /var/www/daudi_blog/static/images/*
   ```

## Step 8: Verify Deployment

1. **Check Services**
   ```bash
   # Check application status
   sudo supervisorctl status daudi_blog
   
   # Check Nginx
   sudo systemctl status nginx
   
   # View application logs
   sudo tail -f /var/log/gunicorn/daudi_blog.log
   ```

2. **Test Website**
   - Visit your domain or server IP
   - Check all article links work
   - Verify images load correctly
   - Test responsive design on mobile

3. **Health Check**
   - Visit `/health` endpoint
   - Should return JSON with status and article count

## Managing Articles

### Adding New Articles

1. **Create Article JSON**
   ```bash
   cd /var/www/daudi_blog
   python utils/article_updater.py sample > new_article.json
   ```

2. **Edit Article Content**
   ```bash
   nano new_article.json
   # Edit the content, title, category, etc.
   ```

3. **Add to Blog**
   ```bash
   python utils/article_updater.py add new_article.json
   ```

4. **Restart Application**
   ```bash
   sudo supervisorctl restart daudi_blog
   ```

### Weekly Workflow

1. **Monday Morning**: Check reminder log
   ```bash
   tail -f /var/log/blog_reminders.log
   ```

2. **Write Article**: Use your preferred editor

3. **Add to Blog**: Use article updater utility

4. **Verify**: Check website and test links

## Backup Strategy

### Automated Backup Script

```bash
#!/bin/bash
# Save as /home/daudi/backup_blog.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/daudi/backups"
BLOG_DIR="/var/www/daudi_blog"

mkdir -p $BACKUP_DIR

# Backup articles
cp $BLOG_DIR/data/articles.json $BACKUP_DIR/articles_$DATE.json

# Backup images
tar -czf $BACKUP_DIR/images_$DATE.tar.gz $BLOG_DIR/static/images/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Set Up Automated Backups

```bash
chmod +x /home/daudi/backup_blog.sh

# Add to crontab for daily backups at 2 AM
crontab -e
0 2 * * * /home/daudi/backup_blog.sh >> /var/log/blog_backup.log 2>&1
```

## Monitoring and Maintenance

### Log Monitoring

```bash
# Application logs
sudo tail -f /var/log/gunicorn/daudi_blog.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u nginx -f
```

### Performance Monitoring

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
htop

# Check network connections
netstat -tulpn | grep :80
```

### Security Updates

```bash
# Update system packages monthly
sudo apt update && sudo apt upgrade -y

# Update Python packages quarterly
cd /var/www/daudi_blog
source venv/bin/activate
pip list --outdated
pip install --upgrade package-name
```

## Troubleshooting

### Common Issues

1. **Site Not Loading**
   ```bash
   # Check Nginx status
   sudo systemctl status nginx
   
   # Check application status
   sudo supervisorctl status daudi_blog
   
   # Check firewall
   sudo ufw status
   ```

2. **Images Not Loading**
   ```bash
   # Check file permissions
   ls -la /var/www/daudi_blog/static/images/
   
   # Fix permissions if needed
   sudo chown -R www-data:www-data /var/www/daudi_blog/static/
   sudo chmod -R 644 /var/www/daudi_blog/static/images/
   ```

3. **Articles Not Updating**
   ```bash
   # Check JSON syntax
   python -m json.tool /var/www/daudi_blog/data/articles.json
   
   # Restart application
   sudo supervisorctl restart daudi_blog
   ```

### Getting Help

1. **Check Logs First**: Always start with the logs
2. **Test Locally**: Reproduce issues in development
3. **Verify Configuration**: Check all config files
4. **Search Documentation**: Review Flask and Nginx docs

## Performance Optimization

### Enable Gzip Compression

Add to Nginx configuration:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

### Cache Static Files

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Monitor Performance

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor in real-time
htop           # CPU and memory
iotop          # Disk I/O
nethogs        # Network usage
```

## Scaling Considerations

As your blog grows, consider:

1. **CDN**: Use CloudFlare for global content delivery
2. **Database**: Migrate from JSON to PostgreSQL for better performance
3. **Caching**: Implement Redis for article caching
4. **Load Balancing**: Multiple application servers behind a load balancer
5. **Monitoring**: Professional monitoring with tools like New Relic or DataDog

## Success Checklist

- [ ] Server created and configured
- [ ] Blog deployed and running
- [ ] Domain configured (if applicable)
- [ ] SSL certificate installed
- [ ] Weekly update system configured
- [ ] Real images uploaded
- [ ] Backup system in place
- [ ] Monitoring configured
- [ ] First new article published
- [ ] Performance optimized

Congratulations! Your blog is now live and ready for weekly updates.