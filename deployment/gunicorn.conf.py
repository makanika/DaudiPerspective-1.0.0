# Gunicorn configuration file for production deployment

# Server socket
# Bind to all network interfaces on port 8000.
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
# The number of worker processes for handling requests.
# A common recommendation is (2 x $num_cores) + 1.
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests to prevent memory leaks.
max_requests = 1000
max_requests_jitter = 100

# Logging
# Define paths for access and error logs.
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "daudi_blog"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/daudi_blog.pid"
# Run Gunicorn as the 'www-data' user and group for security.
user = "www-data"
group = "www-data"
tmp_upload_dir = None
