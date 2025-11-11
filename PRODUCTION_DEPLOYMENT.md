# RackSum Production Deployment Guide

This guide covers deploying RackSum in a production environment using systemd and Gunicorn with Uvicorn workers.

## Table of Contents

- [Quick Start](#quick-start)
- [Manual Deployment](#manual-deployment)
- [Configuration](#configuration)
- [Systemd Service Management](#systemd-service-management)
- [Nginx Reverse Proxy](#nginx-reverse-proxy)
- [SSL/TLS Setup](#ssltls-setup)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Automated Deployment

For a quick production deployment on a systemd-based Linux system:

```bash
# Clone or copy the repository to your server
git clone https://github.com/yourusername/racksum.git
cd racksum

# Run the automated deployment script
sudo ./deploy_production.sh
```

The script will:
- Install to `/opt/racksum`
- Create a systemd service
- Set up the database
- Configure file permissions
- Create an admin user

After deployment:

```bash
# Edit configuration
sudo nano /opt/racksum/.env

# Start the service
sudo systemctl start racksum

# Check status
sudo systemctl status racksum

# View logs
sudo journalctl -u racksum -f
```

## Manual Deployment

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm
- systemd (for service management)
- nginx or Apache (recommended for reverse proxy)
- MySQL or PostgreSQL (recommended for production)

### Step 1: Prepare the System

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx

# For MySQL (optional but recommended)
sudo apt install -y mysql-server
```

### Step 2: Create Deployment Directory

```bash
# Create installation directory
sudo mkdir -p /opt/racksum

# Set ownership (replace with your deployment user)
sudo chown $USER:$USER /opt/racksum

# Copy application files
cp -r /path/to/racksum/* /opt/racksum/
cd /opt/racksum
```

### Step 3: Set Up Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit configuration
nano .env
```

**Important .env settings for production:**

```bash
# Set to production mode
ENVIRONMENT=production

# Server configuration
SERVER_PORT=8000
BIND_ADDRESS=0.0.0.0
GUNICORN_WORKERS=4  # 2-4 x CPU cores

# Database (recommended: MySQL)
DB_ENGINE=mysql
DB_NAME=racksum
DB_USER=racksum_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# WebAuthn (adjust for your domain)
WEBAUTHN_RP_ID=yourdomain.com
WEBAUTHN_RP_NAME=RackSum
WEBAUTHN_ORIGIN=https://yourdomain.com

# Enable authentication
REQUIRE_AUTH=true

# Sentry (optional)
SENTRY_DSN=your_sentry_dsn_here
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

### Step 4: Build Frontend

```bash
# Install Node.js dependencies
npm install --production

# Build Vue.js application
npm run build
```

### Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn
```

### Step 6: Configure Django

```bash
cd backend

# Run migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Create superuser
python manage.py createsuperuser
```

### Step 7: Install Systemd Service

```bash
# Copy service file (adjust paths if needed)
sudo cp /opt/racksum/racksum.service /etc/systemd/system/

# Edit service file to match your setup
sudo nano /etc/systemd/system/racksum.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable racksum

# Start service
sudo systemctl start racksum

# Check status
sudo systemctl status racksum
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | development | Set to 'production' for production mode |
| `SERVER_PORT` | 8000 | Port to listen on |
| `BIND_ADDRESS` | 127.0.0.1 | Bind address (use 0.0.0.0 for all interfaces) |
| `GUNICORN_WORKERS` | auto | Number of Gunicorn workers (recommended: 2-4 x CPU cores) |
| `DB_ENGINE` | sqlite | Database engine (sqlite, mysql, postgresql) |
| `REQUIRE_AUTH` | false | Enable/disable authentication |
| `SENTRY_DSN` | (empty) | Sentry error tracking DSN |

### Gunicorn Configuration

The `gunicorn.conf.py` file contains production-ready settings:

- **Workers**: Auto-calculated based on CPU cores
- **Worker Class**: Uvicorn workers for async support
- **Timeouts**: 120s request timeout, 30s graceful shutdown
- **Connections**: Max 1000 worker connections
- **Logging**: JSON-formatted logs to stdout/stderr

To customize:

```python
# Edit gunicorn.conf.py
nano /opt/racksum/gunicorn.conf.py
```

## Systemd Service Management

### Basic Commands

```bash
# Start service
sudo systemctl start racksum

# Stop service
sudo systemctl stop racksum

# Restart service
sudo systemctl restart racksum

# Reload configuration (graceful)
sudo systemctl reload racksum

# Check status
sudo systemctl status racksum

# Enable on boot
sudo systemctl enable racksum

# Disable on boot
sudo systemctl disable racksum
```

### View Logs

```bash
# Follow logs in real-time
sudo journalctl -u racksum -f

# View last 100 lines
sudo journalctl -u racksum -n 100

# View logs since yesterday
sudo journalctl -u racksum --since yesterday

# View logs with priority
sudo journalctl -u racksum -p err
```

## Nginx Reverse Proxy

### Basic Configuration

Create `/etc/nginx/sites-available/racksum`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Client max body size
    client_max_body_size 50M;

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (for future real-time features)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (served directly by nginx)
    location /static/ {
        alias /opt/racksum/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /opt/racksum/backend/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
}
```

Enable the site:

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/racksum /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## SSL/TLS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

## Monitoring and Logging

### Application Logs

```bash
# Real-time logs
sudo journalctl -u racksum -f

# Error logs only
sudo journalctl -u racksum -p err -f

# JSON-formatted logs
sudo journalctl -u racksum -o json-pretty
```

### System Monitoring

```bash
# Check service status
sudo systemctl status racksum

# Check resource usage
sudo systemctl status racksum --no-pager -l

# View worker processes
ps aux | grep gunicorn
```

### Sentry Integration

Configure Sentry for error tracking and performance monitoring:

```bash
# In .env file
SENTRY_DSN=your_sentry_dsn_here
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status racksum

# View full logs
sudo journalctl -u racksum -n 100 --no-pager

# Check configuration
source /opt/racksum/venv/bin/activate
cd /opt/racksum/backend
python manage.py check
```

### Permission Errors

```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/racksum

# Fix permissions
sudo chmod -R 755 /opt/racksum
sudo chmod 600 /opt/racksum/.env
```

### Database Connection Issues

```bash
# Test database connection
cd /opt/racksum/backend
source ../venv/bin/activate
python manage.py dbshell

# Check migrations
python manage.py showmigrations
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Worker Crashes

```bash
# Check logs
sudo journalctl -u racksum -p err

# Restart service
sudo systemctl restart racksum

# Adjust worker count in .env
GUNICORN_WORKERS=2  # Reduce if running out of memory
```

## Performance Tuning

### Database Optimization

For MySQL:

```sql
-- Optimize tables
OPTIMIZE TABLE devices, racks, rack_devices;

-- Add indexes for frequently queried fields
CREATE INDEX idx_device_category ON devices(category);
CREATE INDEX idx_rack_site ON racks(site_id);
```

### Gunicorn Workers

```bash
# Calculate optimal workers
# Formula: (2 x CPU cores) + 1

# Check CPU count
nproc

# Example for 4 cores:
GUNICORN_WORKERS=9  # (2 x 4) + 1
```

### Static File Caching

Ensure nginx is serving static files with proper caching headers (see nginx config above).

## Backup and Recovery

### Database Backup

```bash
# MySQL backup
mysqldump -u racksum_user -p racksum > backup_$(date +%Y%m%d).sql

# Restore
mysql -u racksum_user -p racksum < backup_20231115.sql
```

### Application Backup

```bash
# Backup entire application
sudo tar -czf racksum_backup_$(date +%Y%m%d).tar.gz /opt/racksum

# Restore
sudo tar -xzf racksum_backup_20231115.tar.gz -C /
```

## Security Checklist

- [ ] Change default admin password
- [ ] Use HTTPS/TLS
- [ ] Configure firewall (ufw/iptables)
- [ ] Enable authentication (`REQUIRE_AUTH=true`)
- [ ] Use strong database passwords
- [ ] Regular security updates
- [ ] Configure Sentry for error tracking
- [ ] Set up database backups
- [ ] Restrict SSH access
- [ ] Enable fail2ban
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular log review

## Support

For issues or questions:
- GitHub Issues: https://github.com/yourusername/racksum/issues
- Documentation: https://github.com/yourusername/racksum/wiki
