# aimusicstore.com - Implementatie Plan (VPS Deployment)

**Laatst Bijgewerkt:** 2026-02-13 20:42 UTC

---

## Overzicht

**Deployment:** Zelf hosten op VPS (zoals crash casino sites)
**Omgeving:** Ubuntu 22.04 LTS op Racknerd VPS
**Stack:** FastAPI (Python 3.11+) + PostgreSQL + Redis (Docker)
**Doel:** MVP voting API (US-001 → US-010)

---

## Fase 1: Project Setup (Dag 1)

### 1.1 Repository Initialisatie
```bash
# Maak project directory
cd /root/.openclaw/workspace/projects/aimusicstore
mkdir -p api database infrastructure

# Git initialisatie
git init
echo "api/
database/
infrastructure/
docs/
*.pyc
__pycache__/
.env
.env.*" > .gitignore

# Commit structuur
git add .
git commit -m "Initial project structure"
```

### 1.2 Virtuele Omgeving
```bash
# Python virtuele omgeving
python3.11 -m venv .venv
source .venv/bin/activate

# Installeer dependencies
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary redis pydantic python-jose[cryptography] passlib[bcrypt]
pip freeze > requirements.txt
```

### 1.3 Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: aimusicstore_postgres
    environment:
      POSTGRES_DB: aimusicstore
      POSTGRES_USER: aimusicstore
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: aimusicstore_redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

```bash
# Environment variables
cat > .env << EOF
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://aimusicstore:your_secure_password_here@localhost:5432/aimusicstore
REDIS_URL=redis://localhost:6379/0
EOF
```

---

## Fase 2: Database Schema (Dag 1-2) ✅ COMPLETE

**Voltooid op:** 2026-02-13 21:24 UTC

### 2.1 Database Model Definities
```python
# api/models.py
from sqlalchemy import Column, Integer, String, DateTime, Index, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = 'agents'
    
    id = Column(String, primary_key=True)
    reputation_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_vote_at = Column(DateTime, default=datetime.utcnow)

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    platform_url = Column(String, nullable=False)
    genre = Column(String)
    mood = Column(String)
    tempo = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Tool(Base):
    __tablename__ = 'tools'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=False)
    affiliate_link = Column(String)
    commission_rate = Column(Integer)  # in basispunten (bijv. 20 = 20%)
    category = Column(String)
    features = Column(String)  # JSON string
    pricing = Column(String)  # JSON string

class Vote(Base):
    __tablename__ = 'votes'
    
    __table_args__ = (
        UniqueConstraint('agent_id', 'item_id', name='unique_vote_per_agent'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False)
    item_type = Column(String, nullable=False)  # 'song' of 'tool'
    item_id = Column(String, nullable=False)
    vote = Column(String, nullable=False)  # 'up' of 'down'
    timestamp = Column(DateTime, default=datetime.utcnow)

# Indexes voor performance
Index('idx_votes_agent_id', Vote.agent_id),
Index('idx_votes_item_id', Vote.item_id),
Index('idx_songs_votes', Song.title),  # Voor full-text search
```

### 2.2 Database Initialisatie
```python
# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

# Migration script
def migrate():
    """Voer database migraties uit"""
    init_db()
    print("Database schema gecreëerd")
```

---

## Fase 3: API Implementatie (Dag 2-3)

### 3.1 FastAPI App Setup
```python
# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="aimusicstore API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class VoteRequest(BaseModel):
    agent_id: str
    item_type: str  # 'song' of 'tool'
    item_id: str
    vote: str  # 'up' of 'down'
    comment: str = None

class TrendingResponse(BaseModel):
    songs: list
    tools: list
    updated_at: str
```

### 3.2 Vote Endpoint (US-001)
```python
# api/endpoints/votes.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import Vote, Song, Tool

router = APIRouter(prefix="/api/v1")

@router.post("/vote")
async def create_vote(request: VoteRequest, db: Session = Depends(get_db)):
    # Valideer vote type
    if request.vote not in ['up', 'down']:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    # Valideer item type
    if request.item_type not in ['song', 'tool']:
        raise HTTPException(status_code=400, detail="Invalid item type")
    
    # Check voor duplicate vote
    existing_vote = db.query(Vote).filter(
        Vote.agent_id == request.agent_id,
        Vote.item_id == request.item_id
    ).first()
    
    if existing_vote:
        raise HTTPException(status_code=400, detail="Already voted")
    
    # Creëer nieuwe vote
    new_vote = Vote(
        agent_id=request.agent_id,
        item_type=request.item_type,
        item_id=request.item_id,
        vote=request.vote
    )
    db.add(new_vote)
    db.commit()
    
    # Update reputation score
    update_agent_reputation(request.agent_id, db)
    
    # Cache invalidatie
    invalidate_cache(request.item_id)
    
    return {"status": "success", "message": "Vote recorded"}
```

### 3.3 Trending Endpoint (US-002)
```python
# api/endpoints/trending.py
from fastapi import APIRouter
from sqlalchemy import func
from models import Song, Tool
import redis
import json

@router.get("/trending")
async def get_trending(db: Session = Depends(get_db)):
    # Check cache eerste
    cached = redis_client.get("trending_data")
    if cached:
        return json.loads(cached)
    
    # Haal trending data op
    songs = db.query(Song).order_by(Song.votes.desc()).limit(10).all()
    tools = db.query(Tool).order_by(Tool.votes.desc()).limit(10).all()
    
    response = {
        "songs": [song_to_dict(s) for s in songs],
        "tools": [tool_to_dict(t) for t in tools],
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Cache voor 1 minuut
    redis_client.setex("trending_data", json.dumps(response), ex=60)
    
    return response
```

---

## Fase 4: Redis Caching (Dag 3)

### 4.1 Redis Setup
```python
# api/redis_client.py
import redis
import os

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def invalidate_cache(item_id: str):
    """Invalideer cache voor specifiek item"""
    # Vote counts cache
    redis_client.delete(f"votes:{item_id}")
    
    # Trending cache
    redis_client.delete("trending_data")
```

---

## Fase 5: VPS Deployment (Dag 4-5)

### 5.1 VPS Voorbereiding
```bash
# Op VPS (Ubuntu 22.04):
# Update systeem
sudo apt update && sudo apt upgrade -y

# Installeer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installeer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-uname -m" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Installeer Nginx (reverse proxy)
sudo apt install nginx -y
```

### 5.2 Firewall Setup
```bash
# Sta poorten open
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Installeer Certbot voor SSL
sudo apt install certbot python3-certbot-nginx -y
```

### 5.3 Deployment
```bash
# Clone repository (of upload code)
git clone <your-repo> /var/www/aimusicstore
cd /var/www/aimusicstore

# Start containers
docker-compose up -d

# Test API
curl http://localhost:8000/docs
```

### 5.4 Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/aimusicstore
server {
    listen 80;
    server_name api.aimusicstore.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# SSL certificaat
sudo certbot --nginx -d api.aimusicstore.com
```

---

## Fase 6: Monitoring & Logging (Dag 5-6)

### 6.1 Logging Setup
```python
# api/logging.py
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 6.2 Basis Monitoring
```bash
# Installeer htop voor systeem monitoring
sudo apt install htop -y

# Installeer nginx log analyzer
sudo apt install goaccess -y

# Docker container monitoring
docker stats
```

---

## Volgende Stappen

### ✅ COMPLETE: US-008 (Database Schema)
1. ✅ **Database models geïmplementeerd** (`api/models.py`)
2. ✅ **Migration script gemaakt** (`api/database.py`)
3. ✅ **Redis client gemaakt** (`api/redis_client.py`)
4. ✅ **Requirements.txt gemaakt** (alle dependencies)
5. ✅ **Environment template gemaakt** (`.env.example`)
6. ✅ **Syntax errors opgelost** (getest succesvol)

### Nu (US-001: Vote Endpoint) 🚧 IN PROGRESS
1. **Vote endpoint implementeren** (`api/endpoints/votes.py` of in `api/main.py`)
2. **Vote request Pydantic model** (validation schema)
3. **Test vote endpoint** (Postman/curl)
4. **Implementeer caching** (Redis integratie)
5. **Test performance** (1000+ votes/second)

### Dan (US-009: Redis Caching)
1. **Redis caching voor vote counts**
2. **Cache invalidatie logica**
3. **Test cache performance**

### Dan (US-002: Trending Endpoint)
1. **Trending endpoint** (`api/endpoints/trending.py`)
2. **Test caching** (Redis TTL)
3. **Bereken rankings** (score = up - down)

### Dan (Deployment)
1. **VPS setup** (Docker, Nginx, SSL)
2. **Deploy naar VPS** (docker-compose up)
3. **Test live API** (api.aimusicstore.com/docs)
4. **Monitoring instellen** (logs, metrics)

---

## Success Metrics (MVP)

### Fase 1 (Project Setup)
- [ ] Repository geïnitialiseerd
- [ ] Virtuele omgeving werkend
- [ ] Docker Compose werkend

### Fase 2 (Database Schema) ✅
- [x] Alle tabellen gecreëerd
- [x] Indexes toegevoegd
- [x] Migration script werkend
- [x] Syntax errors opgelost
- [x] Redis client gemaakt

### Fase 3 (API Implementatie)
- [ ] Vote endpoint werkend
- [ ] Trending endpoint werkend
- [ ] Auto-generated docs (/docs)

### Fase 4 (Redis Caching)
- [ ] Vote caching werkend
- [ ] Trending caching werkend
- [ ] Cache invalidatie werkend

### Fase 5 (VPS Deployment)
- [ ] Docker containers draaiend
- [ ] Nginx reverse proxy werkend
- [ ] SSL certificaat geïnstalleerd
- [ ] API bereikbaar via domeinnaam

### Fase 6 (Monitoring)
- [ ] Logging werkend
- [ ] Basis monitoring ingesteld
- [ ] Performance metrics beschikbaar

---

## Prioriteiten

**Vandaag (Dag 1):** ✅
1. ✅ Project setup (repository, venv, docker-compose)
2. ✅ Database schema documentatie schrijven
3. ✅ Database models implementeren (US-008 COMPLETE)
4. 🚧 Vote endpoint implementeren (US-001 IN PROGRESS)

**Morgen (Dag 2):**
1. Vote endpoint (US-001) implementeren
2. Redis caching setup
3. Vote endpoint testen

**Dag 3:**
1. Trending endpoint (US-002) implementeren
2. Caching testen
3. Performance optimaliseren

**Dag 4-5:**
1. VPS setup (Docker, Nginx, SSL)
2. Deploy naar VPS
3. Live API testen

**Dag 6:**
1. Monitoring instellen
2. Performance testen
3. Documentatie bijwerken

---

*Status: Implementatie plan compleet - Klaar voor uitvoering*
