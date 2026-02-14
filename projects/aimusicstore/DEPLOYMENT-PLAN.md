# aimusicstore.com Production Deployment Plan

**Date:** 2026-02-14 07:35 UTC
**Goal:** Deploy aimusicstore API to production VPS

---

## Current Infrastructure Status

### ✅ Running Services
- **PostgreSQL:** aimusicstore_postgres (port 5432) - Healthy
- **Redis:** aimusicstore_redis (port 6379) - Healthy
- **Docker:** Active and running

### ❌ Missing Configuration
- **aimusicstore.com DNS:** Nameservers refused query (domain not configured)
- **nginx:** Not installed
- **API Service:** Running in foreground (not managed)
- **SSL Certificate:** Not installed (certbot not present)
- **Firewall:** Need to verify ports 80/443 are open

### ✅ API Application
- **Code:** Complete (v0.3.0, 10/10 user stories)
- **Location:** `/root/.openclaw/workspace/projects/aimusicstore/`
- **Tested:** All endpoints working locally

---

## Deployment Plan

### Phase 1: Web Server Setup (15 min)

**Install and configure nginx:**
```bash
apt update && apt install -y nginx certbot python3-certbot-nginx
```

**Configure nginx reverse proxy:**
- Proxy / → http://localhost:8000
- Handle WebSocket connections (if needed later)
- Static file serving (if needed later)

**Firewall configuration:**
- Allow HTTP (port 80)
- Allow HTTPS (port 443)
- Block direct API port 8000 from public

---

### Phase 2: API Service Setup (10 min)

**Create systemd service:**
```ini
[Unit]
Description=aimusicstore API
After=network.target docker-compose.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/projects/aimusicstore
ExecStart=/usr/bin/python3 -m uvicorn api.main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=10
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
systemctl daemon-reload
systemctl enable aimusicstore-api.service
systemctl start aimusicstore-api.service
systemctl status aimusicstore-api.service
```

---

### Phase 3: SSL Certificate (20 min)

**Prerequisites:**
- Domain DNS must point to this VPS (23.95.148.204)
- Port 80 must be accessible from internet

**Install certificate:**
```bash
certbot --nginx -d aimusicstore.com
```

**Auto-renewal:**
- certbot installs cron job automatically
- Test: `certbot renew --dry-run`

---

### Phase 4: Testing & Verification (15 min)

**Health checks:**
```bash
curl http://localhost:8000/health
curl https://aimusicstore.com/health
curl https://aimusicstore.com/api/v1/trending
```

**API documentation:**
- https://aimusicstore.com/docs (Swagger UI)
- Verify all endpoints accessible

**Smoke tests:**
- Create API key
- Submit test vote
- Verify trending endpoint
- Check weighted scoring
- Test rate limiting

---

## DNS Configuration (CRITICAL ⚠️)

### Current Status
- **Domain:** aimusicstore.com
- **Status:** Nameservers REFUSED query
- **Issue:** Domain not pointing to this VPS

### Required Actions
1. **Log in to domain registrar** (where aimusicstore.com is registered)
2. **Configure nameservers** to point to this VPS's DNS
3. **Add A record:** `aimusicstore.com → 23.95.148.204`
4. **Wait for propagation** (5 min - 48 hours)

### Temporary Option
- **Use IP-based access:** http://23.95.148.204:8000
- **Or use subdomain** if DNS is faster to configure

---

## Security Checklist

### Pre-Deployment
- [ ] Change SECRET_KEY in .env (generate secure random string)
- [ ] Update CORS_ORIGINS to actual domain
- [ ] Set DEBUG=false in .env
- [ ] Configure database backup (automated)
- [ ] Set up log rotation

### Post-Deployment
- [ ] Enable UFW firewall
- [ ] Configure fail2ban (brute force protection)
- [ ] Set up database backups (daily off-site)
- [ ] Configure monitoring (Sentry, etc.)
- [ ] Test rate limiting from external IP

---

## Monitoring Setup

### Application Monitoring
```python
# Add to api/main.py
from prometheus_client import Counter, Histogram, start_http_server

request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def track_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    request_count.inc()
    request_duration.observe(duration)
    return response
```

### Logging
```python
# Configure structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler('logs/api.log', maxBytes=10*1024*1024, backupCount=5)
    ]
)
```

---

## Rollback Plan

If deployment fails:
```bash
# Stop new service
systemctl stop aimusicstore-api.service

# Restore previous (if any)
systemctl start aimusicstore-api-old.service

# Check logs
journalctl -u aimusicstore-api.service -n 50

# Revert nginx changes
nginx -t && systemctl reload nginx
```

---

## Performance Optimization

### nginx Tuning
```nginx
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
gzip on;
gzip_types text/plain application/json;
```

### Application Tuning
```python
# uvicorn config
workers = multiprocessing.cpu_count() * 2 + 1
limit_concurrency = 1000
timeout_keep_alive = 30
```

---

## Cost Estimates

### Monthly (Racknerd VPS)
- VPS: ~€5-10/maand
- Bandwidth: Included (typically)
- SSL: FREE (Let's Encrypt)
- **Total:** ~€5-10/maand

### Scaling Needs
- If >10k requests/day: Consider VPS upgrade
- If >100k requests/day: Load balancer + multiple instances
- Database: PostgreSQL can handle millions of votes

---

## Next Actions

1. **Check domain registrar** - Configure DNS for aimusicstore.com
2. **Install nginx** - Set up reverse proxy
3. **Create systemd service** - Auto-start API on boot
4. **Install SSL certificate** - Enable HTTPS
5. **Test all endpoints** - Smoke testing
6. **Set up monitoring** - Track errors, performance

---

**Ready to deploy when DNS is configured!** 🚀

*Created by: Carlottta (Coordinator Agent)*
*Date: 2026-02-14 07:35 UTC*
