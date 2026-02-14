# AGENTS.md - aimusicstore.com (AI Music Top 50 Voting API)

**Purpose:** Operational guide for Ralph BUILDING loop — validation commands, test procedures, and learnings.

**Read this:** Every iteration before marking a task complete.

---

## Validation Commands (Backpressure)

**Run these before marking any task complete.**

### Database Schema Validation (US-008)

**Check tables exist:**
```bash
# Via Python
python3 -c "
from database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables:', tables)
assert 'songs' in tables, 'songs table missing'
assert 'tools' in tables, 'tools table missing'
assert 'votes' in tables, 'votes table missing'
assert 'agents' in tables, 'agents table missing'
print('✅ All tables exist')
"

# Via psql (if using direct PostgreSQL)
psql -h localhost -U aimusicstore -d aimusicstore -c "\dt"
```

**Check indexes exist:**
```bash
python3 -c "
from database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
indexes = inspector.get_indexes('votes')
print('Votes indexes:', [idx['name'] for idx in indexes])
"
```

**Test model relationships:**
```bash
python3 -c "
from models import Song, Tool, Vote, Agent
from database import SessionLocal
db = SessionLocal()
print('✅ Models import successfully')
# Test query
song_count = db.query(Song).count()
print(f'Songs in database: {song_count}')
db.close()
"
```

---

### API Endpoint Validation (US-001, US-002, US-003)

**Start FastAPI server:**
```bash
# Development server
cd /root/.openclaw/workspace/projects/aimusicstore
source .venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production server (gunicorn)
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Test vote endpoint (US-001):**
```bash
# Test POST vote
curl -X POST "http://localhost:8000/api/v1/vote" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test-agent-1",
    "item_type": "song",
    "item_id": "song-1",
    "vote": "up",
    "comment": "Test vote"
  }'

# Expected response: {"status": "success", "message": "Vote recorded"}
# Expected HTTP: 200 OK

# Test duplicate vote (should fail)
curl -X POST "http://localhost:8000/api/v1/vote" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test-agent-1",
    "item_type": "song",
    "item_id": "song-1",
    "vote": "up"
  }'

# Expected response: {"detail": "Already voted"}
# Expected HTTP: 400 Bad Request
```

**Test trending endpoint (US-002):**
```bash
# Test GET trending
curl -X GET "http://localhost:8000/api/v1/trending" | python3 -m json.tool

# Expected response:
# {
#   "songs": [...],
#   "tools": [...],
#   "updated_at": "2026-02-13T21:00:00"
# }
# Expected HTTP: 200 OK
```

**Test top 50 endpoint (US-003):**
```bash
# Test GET top daily
curl -X GET "http://localhost:8000/api/v1/top/daily" | python3 -m json.tool

# Expected response: array of 50 items (songs + tools)
# Expected HTTP: 200 OK
```

---

### Redis Caching Validation (US-009)

**Check Redis connection:**
```bash
# From Python
python3 -c "
from api.redis_client import redis_client
try:
    redis_client.ping()
    print('✅ Redis connection successful')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
"

# From redis-cli
redis-cli ping
# Expected: PONG
```

**Test caching:**
```bash
python3 -c "
from api.redis_client import redis_client
import time

# Set test value
redis_client.setex('test_key', 10, 'test_value')
print('Set: test_key = test_value (TTL 10s)')

# Get test value
value = redis_client.get('test_key')
print(f'Get: test_key = {value}')

# Wait for TTL to expire
time.sleep(11)
value_after = redis_client.get('test_key')
print(f'After TTL: test_key = {value_after}')
print('✅ Caching works' if value_after is None else '❌ TTL not working')
"
```

---

### Docker Compose Validation (Deployment)

**Start containers:**
```bash
cd /root/.openclaw/workspace/projects/aimusicstore
docker-compose up -d

# Check containers running
docker ps

# Expected: aimusicstore_postgres and aimusicstore_redis running
```

**Test database connection (via Docker):**
```bash
# Connect to PostgreSQL container
docker exec -it aimusicstore_postgres psql -U aimusicstore -d aimusicstore

# In psql:
SELECT COUNT(*) FROM songs;
SELECT COUNT(*) FROM votes;
\q
```

**Test Redis connection (via Docker):**
```bash
# Connect to Redis container
docker exec -it aimusicstore_redis redis-cli

# In redis-cli:
PING
# Expected: PONG
```

**Stop containers:**
```bash
docker-compose down
```

---

## Performance Benchmarks

**Vote endpoint throughput (US-001):**
```bash
# Install wrk if needed
# sudo apt install wrk -y

# Test 1000 concurrent connections, 10 seconds
wrk -t4 -c1000 -d10s --latency \
  -H "Content-Type: application/json" \
  -s ~/post_vote.txt \
  http://localhost:8000/api/v1/vote

# post_vote.txt content:
# {"agent_id": "load-test-agent", "item_type": "song", "item_id": "song-1", "vote": "up"}

# Target: >1000 requests/second (FastAPI target)
```

**Trending endpoint latency (US-002):**
```bash
# Test response time with cache
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/trending"

# curl-format.txt:
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer:  %{time_pretransfer}\n
# time_starttransfer: %{time_starttransfer}\n
# ----------\n
# time_total:       %{time_total}\n

# Target: <50ms with Redis cache, <500ms without cache
```

---

## Common Issues & Solutions

### Issue: "Module not found: api"
**Solution:**
```bash
cd /root/.openclaw/workspace/projects/aimusicstore
export PYTHONPATH="${PYTHONPATH}:/root/.openclaw/workspace/projects/aimusicstore"
```

### Issue: "Database connection failed"
**Solution:**
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Test connection manually
psql -h localhost -U aimusicstore -d aimusicstore

# If Docker, check container is running
docker ps | grep postgres
```

### Issue: "Redis connection timeout"
**Solution:**
```bash
# Check Redis is running
redis-cli ping
# Or via Docker
docker exec aimusicstore_redis redis-cli ping

# Check REDIS_URL in .env
cat .env | grep REDIS_URL
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn api.main:app --port 8001
```

---

## Learnings Log

**Add discoveries here as you work.**

### Database
- **[DATE]:** [Learning about database schema, migrations, or relationships]
  - Example: "SQLAlchemy requires explicit relationship definitions for foreign keys"

### API
- **[DATE]:** [Learning about FastAPI, routing, error handling]
  - Example: "FastAPI auto-generates OpenAPI docs at /docs endpoint"

### Docker
- **[DATE]:** [Learning about Docker Compose, networking, volumes]
  - Example: "Docker volumes persist database data even after container restart"

### Redis
- **[DATE]:** [Learning about caching, TTL, pub/sub]
  - Example: "Redis setex requires TTL in seconds, not milliseconds"

---

## Environment Variables

**Required in .env file:**
```bash
# Database
DATABASE_URL=postgresql://aimusicstore:your_password@localhost:5432/aimusicstore
POSTGRES_PASSWORD=your_secure_password

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Security (US-010)
SECRET_KEY=your_jwt_secret_key_here
API_RATE_LIMIT_FREE=100
API_RATE_LIMIT_PRO=1000
```

**Never commit .env to git!**

---

## Git Workflow

**Commit standards:**
```bash
# Add files
git add .

# Commit with clear message
git commit -m "feat: implement vote endpoint (US-001)

- Add POST /api/v1/vote endpoint
- Validate agent_id, item_type, item_id, vote
- Check for duplicate votes
- Update agent reputation score
- Invalidate cache on new vote
- Add error handling and tests

Closes #1"
```

**Branch strategy:**
```bash
# Main branch (production)
git checkout main

# Feature branches
git checkout -b feat/database-schema
git checkout -b feat/vote-api
git checkout -b feat/trending-api

# Merge to main when complete
git checkout main
git merge feat/vote-api
git branch -d feat/vote-api
```

---

## Testing Checklist

**Before marking task complete, verify:**

### Database (US-008)
- [ ] All tables created (songs, tools, votes, agents)
- [ ] Indexes present on frequently queried fields
- [ ] Foreign key constraints working
- [ ] Unique constraint on (agent_id, item_id) for votes

### Vote API (US-001)
- [ ] POST /api/v1/vote accepts valid data
- [ ] Returns 200 on success
- [ ] Returns 400 on duplicate vote
- [ ] Returns 400 on invalid vote type (not 'up'/'down')
- [ ] Returns 400 on invalid item type (not 'song'/'tool')
- [ ] Invalidates cache after successful vote

### Redis (US-009)
- [ ] Redis connection successful
- [ ] Vote counts cached with 5-minute TTL
- [ ] Trending data cached with 1-minute TTL
- [ ] Cache invalidated when votes change

### Trending API (US-002)
- [ ] GET /api/v1/trending returns JSON with songs and tools
- [ ] Returns 200 OK
- [ ] Data is sorted by vote count (up - down)
- [ ] Includes updated_at timestamp
- [ ] Uses cache (second request faster)

### Rate Limiting (US-010)
- [ ] Free tier limited to 100 votes/day
- [ ] Returns 429 Too Many Requests when exceeded
- [ ] Includes retry-after header
- [ ] API key authentication works

---

## Quick Reference

**Project location:** `/root/.openclaw/workspace/projects/aimusicstore/`

**Start server:** `uvicorn api.main:app --reload --port 8000`

**Test API docs:** `http://localhost:8000/docs`

**Database URL:** Check `.env` file

**Redis connection:** `redis-cli ping` or `docker exec aimusicstore_redis redis-cli ping`

**Docker Compose:** `docker-compose up -d` (start), `docker-compose down` (stop)

**Python venv:** `source .venv/bin/activate`

**Install dependencies:** `pip install -r requirements.txt`

---

*Last Updated: 2026-02-13 21:17 UTC*
*Mode: BUILDING*
