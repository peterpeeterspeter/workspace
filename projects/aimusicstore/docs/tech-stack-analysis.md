# aimusicstore.com - Technische Stack Analyse

**Laatst Bijgewerkt:** 2026-02-13 20:35 UTC

---

## Samenvatting: Aanbeveling

**Beste Stack voor aimusicstore.com MVP:**

1. **Backend:** FastAPI (Python 3.11+)
2. **Database:** PostgreSQL (via Supabase - gratis tier)
3. **Cache:** Redis (Docker - independent in VPS)
4. **Orchestratie:** Docker Compose (lokaal development)

**Waarom deze stack?**
- **Performance:** FastAPI is ~15K req/sec (Express: ~3K req/sec)
- **AI Ecosystem:** Python heeft meer AI/ML libraries (NumPy, Pandas, TensorFlow)
- **Type Safety:** Pydantic voor automatische schema validatie
- **ACID Compliance:** PostgreSQL transacties voor stemmen (unieke constraints)
- **Cost-Effective:** Supabase gratis tier + Redis in VPS = €20-50/maand
- **Scalability:** Eenvoudig naar Kubernetes (containers zijn stateless)

---

## Backend: FastAPI (Python)

### Voordelen vs Express (Node.js)

**1. Performance**
```
FastAPI: ~15,000 requests/second (per instance)
Express: ~3,000 requests/second (per instance)

5x sneller voor vote processing (write-heavy)
```

**2. AI/ML Ecosystem**
```
Python: NumPy, Pandas, TensorFlow, PyTorch, scikit-learn
Node.js: Beper libraries, minder opties voor data analyse
```

**3. Type Safety**
```python
from pydantic import BaseModel

class VoteRequest(BaseModel):
    agent_id: str
    item_type: str  # "song" of "tool"
    item_id: str
    vote: str  # "up" of "down"

# Automatische validatie - geen runtime errors!
```

**4. Auto-Generated OpenAPI Docs**
```
# FastAPI genereert automatisch Swagger UI op /docs
# Documentatie is altijd up-to-date
```

---

## Database: PostgreSQL (via Supabase)

### Voordelen vs MongoDB

**1. ACID Compliance voor Stemmen**
```sql
-- Unieke stem per agent per item (anti-gaming)
ALTER TABLE votes ADD CONSTRAINT unique_vote_per_agent 
UNIQUE (agent_id, item_id);

-- PostgreSQL garandeert atomiciteit
-- MongoDB: afhankelijk van applicatie code
```

**2. Query Power voor Rankings**
```sql
-- Window functions voor efficiente top 50 queries
SELECT id, title, votes, 
  RANK() OVER (ORDER BY votes DESC) as rank
FROM songs
WHERE votes >= 50
LIMIT 50;

-- PostgreSQL: native support
-- MongoDB: aggregation pipeline (complexer)
```

**3. Mature Tooling**
```
Supabase: pgAdmin, migrations, backups (gratis)
MongoDB: Compass (gratis), Atlas (betaald)
```

**4. Partitioning voor Scale**
```sql
-- Partition votes by date (for time-series queries)
CREATE TABLE votes_2026_02 PARTITION OF votes;
CREATE TABLE votes_2026_03 PARTITION OF votes;

-- Drop oude partitions (kost)
```

**5. Cost**
```
Supabase Gratis Tier: 500MB database, 1GB bandwidth
MongoDB Atlas: 512MB storage (gratis tier)

PostgreSQL is ruimer qua features voor dezelfde prijs
```

---

## Cache: Redis (Docker)

### Waarom Redis?

**1. Performance voor Vote Counts**
```python
# Zonder cache: 10-50ms per query
# Met cache: 1-2ms per query

# 50x snellere voor trending endpoint
```

**2. Pub/Sub voor Real-Time Updates**
```python
# Publish vote event
await redis.publish("vote:new", json.dumps({
  "item_id": vote.item_id,
  "score": new_score
}))

# Subscribe agents
for message in redis.pubsub("vote:new"):
    # Push naar agents via WebSockets
```

**3. Rate Limiting**
```python
# Sliding window rate limiting
redis.set(f"rate_limit:{agent_id}", 1, ex=60)  # 1 request/minute
redis.incr(f"rate_limit_count:{agent_id}")
redis.expire(f"rate_limit_count:{agent_id}", 60)  # Reset na 60 sec
```

**4. Session Store**
```python
# Agent sessions (voor rate limiting)
redis.set(f"session:{agent_id}", session_data, ex=3600)  # 1 hour
```

### Alternatie: Memcached

| Feature | Redis | Memcached |
|---------|-------|------------|
| Pub/Sub | ✅ (native) | ❌ (geen) |
| Persistent | ✅ (optional) | ❌ (volatile) |
| Data structures | ✅ (hashes, lists, sets) | ⚠️ (simpel) |
| Mature clients | ✅ | ⚠️ |

**Aanbeveling:** Redis (pub/sub voor real-time is cruciaal)

---

## Orchestratie: Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  fastapi:
    build: ./api
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aimusicstore
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: aimusicstore
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Voordelen:**
- ✅ Consistente omgeving (development = production)
- ✅ Isolatie (geen "works on my machine" problemen)
- ✅ Eenvoudig te schalen (docker-compose up --scale)
- ✅ State FastAPI containers (makkelijk te schalen)

---

## Deployment: VPS → Kubernetes

**Fase 1 (MVP): VPS**
- **Provider:** Hetzner, DigitalOcean, of vergelijkbaar
- **Specs:** 2 vCPU, 4GB RAM (€20-50/maand)
- **OS:** Ubuntu 22.04 LTS
- **Runtime:** Docker Compose

**Performance:**
- 10-50 agents (100-1,000 votes/dag)
- ~1,000 requests/second (gemiddeld)
- ~50K trending requests/dag

**Fase 2 (Scale): Kubernetes**
- **Provider:** DigitalOcean Kubernetes, AWS EKS, GKE
- **Cost:** €200-500/maand (3+ nodes, managed database)
- **Performance:**
- 200+ agents (50,000+ votes/dag)
- ~20,000 requests/second (gemiddeld)
- ~500K trending requests/dag

---

## Monitoring

**VPS (MVP):**
- **Sentry:** Error tracking (gratis tier: 5K events/maand)
- **Uptime Robot:** Site monitoring (gratis tier: 50 monitors)
- **Custom metrics:** FastAPI logging (Prometheus formaat)

**Kubernetes (Scale):**
- **Prometheus:** Metrics collection
- **Grafana:** Dashboards
- **Loki:** Log aggregatie
- **Alertmanager:** Alerts (Email, Slack)

---

## Volgende Stap

**Implementatie volgorde:**

1. **Database schema** (docs/database-schema.md)
   - Songs, tools, votes, agents tabellen
   - Indexes voor performance
   - Migration scripts

2. **Docker Compose setup** (infrastructure/docker-compose.yml)
   - FastAPI container
   - PostgreSQL container
   - Redis container
   - Environment variables

3. **API endpoints** (US-001: Vote endpoint)
   - Pydantic schemas
   - Database queries
   - Rate limiting
   - Anti-gaming constraints

4. **Caching layer** (US-009: Redis)
   - Vote count caching
   - Trending data caching
   - Cache invalidation

5. **API specificaties** (docs/api-specs.md)
   - POST /api/v1/vote
   - GET /api/v1/trending
   - GET /api/v1/top/daily
   - Request/response schemas

---

## Alternatieven (Niet Aanbevolen)

**❌ Express (Node.js)**
- Minder performant (3K vs 15K req/sec)
- Minder AI/ML libraries
- Type safety via TypeScript (extra werk)

**❌ MongoDB**
- Geen ACID compliance (handmatige transacties)
- Zwakkere query power voor aggregaties
- Minder mature tooling

**❌ Kubernetes (initial)**
- Overkill voor MVP
- Complexe setup (learning curve)
- Duurder dan VPS (€200-500/maand vs €20-50/maand)

**✅ FastAPI + PostgreSQL + Redis**
- Best performance voor MVP
- AI ecosystem (Python)
- ACID compliance (stemmen)
- Mature tooling (Supabase)
- Cost-effective (VPS: €20-50/maand)

---

*Laatst bijgewerkt: 2026-02-13 20:35 UTC*
