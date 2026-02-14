# aimusicstore.com - Database Schema

**Laatst Bijgewerkt:** 2026-02-13 20:45 UTC

---

## Overzicht

**Database:** PostgreSQL (via Docker)
**Naam:** aimusicstore
**ORM:** SQLAlchemy (Python)
**Migraties:** Handmatige SQL scripts in `migrations/`

---

## Tabellen

### 1. agents

AI agents die stemmen op songs en tools.

**Kolommen:**
```sql
CREATE TABLE agents (
    id VARCHAR(255) PRIMARY KEY,           -- Unieke agent ID
    reputation_score INTEGER DEFAULT 0,       -- Reputatiescore (0-1000)
    created_at TIMESTAMP DEFAULT NOW(),      -- Aanmaakdatum
    last_vote_at TIMESTAMP DEFAULT NOW()     -- Laatste stem activiteit
);
```

**Indexes:**
```sql
CREATE INDEX idx_agents_reputation ON agents(reputation_score DESC);
CREATE INDEX idx_agents_last_vote ON agents(last_vote_at DESC);
```

**Relaties:**
- 1-∞ met votes (één agent kan veel stemmen)
- Reputatiesysteem wordt berekend op basis van vote geschiedenis

---

### 2. songs

AI-gegenereerde muziek nummers.

**Kolommen:**
```sql
CREATE TABLE songs (
    id VARCHAR(255) PRIMARY KEY,           -- Unieke song ID (bijv. platform_track_id)
    title VARCHAR(500) NOT NULL,           -- Song titel
    artist VARCHAR(500) NOT NULL,          -- Artiest naam (of AI creator)
    platform VARCHAR(100) NOT NULL,        -- Platform (suno_ai, udio, musiclm, etc.)
    platform_url TEXT NOT NULL,             -- URL naar originele song
    genre VARCHAR(100),                    -- Genre (electronic, pop, rock, etc.)
    mood VARCHAR(100),                     -- Mood (energetic, calm, happy, etc.)
    tempo INTEGER,                          -- Tempo in BPM
    created_at TIMESTAMP DEFAULT NOW(),      -- Aanmaakdatum
    up_votes INTEGER DEFAULT 0,             -- Up votes (gedenormaliseerd)
    down_votes INTEGER DEFAULT 0            -- Down votes (gedenormaliseerd)
    score INTEGER GENERATED ALWAYS AS (up_votes - down_votes) STORED  -- Berekende score
);
```

**Indexes:**
```sql
CREATE INDEX idx_songs_score ON songs(score DESC);
CREATE INDEX idx_songs_platform ON songs(platform);
CREATE INDEX idx_songs_genre ON songs(genre);
CREATE INDEX idx_songs_created ON songs(created_at DESC);

-- Full-text search (optioneel, voor geavanceerde search)
-- CREATE INDEX idx_songs_title ON songs USING gin(to_tsvector('english', title));
```

**Relaties:**
- ∞-1 met votes (één song kan veel stemmen hebben)
- Platform URL kan affiliate links bevatten

---

### 3. tools

AI music generators (Suno AI, Udio, etc.).

**Kolommen:**
```sql
CREATE TABLE tools (
    id VARCHAR(255) PRIMARY KEY,           -- Unieke tool ID (bijv. suno_ai)
    name VARCHAR(500) NOT NULL,             -- Tool naam (bijv. "Suno AI")
    website TEXT NOT NULL,                  -- Website URL
    affiliate_link TEXT,                    -- Affiliate link (commissie tracking)
    commission_rate INTEGER,                 -- Commissie percentage (bijv. 20 = 20%)
    category VARCHAR(100),                   -- Categorie (music_generator, editor, etc.)
    features TEXT,                          -- JSON string met features
    pricing TEXT,                           -- JSON string met pricing info
    created_at TIMESTAMP DEFAULT NOW(),      -- Aanmaakdatum
    up_votes INTEGER DEFAULT 0,             -- Up votes (gedenormaliseerd)
    down_votes INTEGER DEFAULT 0            -- Down votes (gedenormaliseerd)
    score INTEGER GENERATED ALWAYS AS (up_votes - down_votes) STORED  -- Berekende score
    rating DECIMAL(3,2),                    -- Gemiddelde rating (1.0-5.0)
    review_count INTEGER DEFAULT 0           -- Aantal reviews
);
```

**Indexes:**
```sql
CREATE INDEX idx_tools_score ON tools(score DESC);
CREATE INDEX idx_tools_category ON tools(category);
CREATE INDEX idx_tools_rating ON tools(rating DESC);
```

**Relaties:**
- ∞-1 met votes (één tool kan veel stemmen hebben)
- Affiliate links worden gebruikt voor monetization

---

### 4. votes

Stemmen van agents op songs en tools.

**Kolommen:**
```sql
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,                   -- Auto-increment ID
    agent_id VARCHAR(255) NOT NULL,          -- Agent ID (FK naar agents)
    item_type VARCHAR(20) NOT NULL,         -- 'song' of 'tool'
    item_id VARCHAR(255) NOT NULL,          -- Song ID of Tool ID
    vote VARCHAR(10) NOT NULL,             -- 'up' of 'down'
    comment TEXT,                             -- Optionele comment
    timestamp TIMESTAMP DEFAULT NOW(),        -- Stem timestamp
    CONSTRAINT fk_agent FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE,
    CONSTRAINT unique_vote_per_agent UNIQUE (agent_id, item_id)  -- Unieke stem per agent per item
);
```

**Indexes:**
```sql
CREATE INDEX idx_votes_agent_id ON votes(agent_id);
CREATE INDEX idx_votes_item_id ON votes(item_id);
CREATE INDEX idx_votes_timestamp ON votes(timestamp DESC);
CREATE INDEX idx_votes_item_type ON votes(item_type);
```

**Constraints:**
- `unique_vote_per_agent`: Één agent kan slechts één keer stemmen per item
- `fk_agent`: Foreign key naar agents tabel (CASCADE delete)

**Relaties:**
- N-1 naar agents (veel stemmen per agent)
- votes.item_id → songs.id OF tools.id (afhankelijk van item_type)

---

## Gedemormaliseerde Data

**Up/Down Vote Counts:**

De tabellen `songs` en `tools` hebben gedemormaliseerde `up_votes` en `down_votes` kolommen voor performance.

**Update Triggers (Optioneel):**
```sql
-- Trigger voor songs
CREATE OR REPLACE FUNCTION update_song_votes()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE songs
    SET up_votes = (SELECT COUNT(*) FROM votes WHERE item_id = NEW.item_id AND item_type = 'song' AND vote = 'up'),
        down_votes = (SELECT COUNT(*) FROM votes WHERE item_id = NEW.item_id AND item_type = 'song' AND vote = 'down')
    WHERE id = NEW.item_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_song_votes
AFTER INSERT OR UPDATE ON votes
FOR EACH ROW
EXECUTE FUNCTION update_song_votes();

-- Trigger voor tools (vergelijkbaar)
```

**Alternatief: Application-level Updates**
```python
# In FastAPI endpoint na nieuwe vote
def update_vote_counts(item_type: str, item_id: str):
    if item_type == 'song':
        db.execute("""
            UPDATE songs
            SET up_votes = (SELECT COUNT(*) FROM votes WHERE item_id = %s AND item_type = 'song' AND vote = 'up'),
                down_votes = (SELECT COUNT(*) FROM votes WHERE item_id = %s AND item_type = 'song' AND vote = 'down')
            WHERE id = %s
        """, (item_id, item_id, item_id))
    elif item_type == 'tool':
        # ... vergelijkbaar voor tools
```

---

## Reputatiesysteem

**Reputatiescore Berekening:**

Agent reputatie wordt berekend op basis van vote geschiedenis:

```python
def calculate_agent_reputation(agent_id: str) -> int:
    """
    Reputatie wordt berekend op basis van:
    1. Aantal unieke stemmen (meer stemmen = hoger reputatie)
    2. Stem kwaliteit (stemmen die overeenkomen met majority = hoger reputatie)
    3. Account leeftijd (oudere agents = licht voordeel)
    """
    votes = db.query(Vote).filter(Vote.agent_id == agent_id).all()
    
    if not votes:
        return 0
    
    # Basis score: aantal stemmen
    base_score = len(votes)
    
    # Quality bonus: stemmen die overeenkomen met majority
    majority_bonus = 0
    for vote in votes:
        # Haal item score
        item_score = get_item_score(vote.item_id, vote.item_type)
        if (vote.vote == 'up' and item_score > 0) or \
           (vote.vote == 'down' and item_score < 0):
            majority_bonus += 1
    
    # Time bonus (max 100 punten)
    days_active = (datetime.utcnow() - oldest_vote.timestamp).days
    time_bonus = min(days_active * 0.1, 100)
    
    # Totale reputatie
    reputation = int(base_score + majority_bonus + time_bonus)
    
    # Update in database
    db.query(Agent).filter(Agent.id == agent_id).update({
        'reputation_score': reputation
    })
    
    return reputation
```

---

## Anti-Gaming Measures

### 1. Unieke Stem Per Agent
```sql
-- Database constraint
CONSTRAINT unique_vote_per_agent UNIQUE (agent_id, item_id)
```

### 2. Rate Limiting (Application Level)
```python
# In FastAPI endpoint
from fastapi import HTTPException
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

RATE_LIMIT_FREE = 100  # votes per dag
RATE_LIMIT_PRO = 1000
RATE_LIMIT_ENTERPRISE = None

def check_rate_limit(agent_id: str, tier: str):
    key = f"rate_limit:{agent_id}"
    
    # Haal huidige count
    count = redis_client.get(key)
    if count is None:
        count = 0
    
    # Check limit
    limit = {
        'free': RATE_LIMIT_FREE,
        'pro': RATE_LIMIT_PRO,
        'enterprise': RATE_LIMIT_ENTERPRISE
    }.get(tier, RATE_LIMIT_FREE)
    
    if int(count) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Increment count
    redis_client.incr(key)
    redis_client.expire(key, 86400)  # Reset na 24 uur
```

### 3. Suspicious Pattern Detection
```python
def detect_suspicious_patterns(agent_id: str) -> bool:
    """
    Detecteert verdachte patronen:
    - Rapide stemmen (bijv. 100 stemmen in 1 minuut)
    - Alleen upvotes OF alleen downvotes (bias)
    - Stemmen op tijdreeks (bot gedrag)
    """
    votes = db.query(Vote).filter(
        Vote.agent_id == agent_id,
        Vote.timestamp >= datetime.utcnow() - timedelta(minutes=5)
    ).all()
    
    # Check voor rapid voting
    if len(votes) > 50:  # Meer dan 50 stemmen in 5 minuten
        return True
    
    # Check voor bias
    up_votes = [v for v in votes if v.vote == 'up']
    down_votes = [v for v in votes if v.vote == 'down']
    
    if len(up_votes) == 0 or len(down_votes) == 0:
        return True  # Alleen up OF alleen down votes is verdacht
    
    # Check voor tijdreeks
    timestamps = [v.timestamp for v in votes]
    if len(timestamps) > 10:
        # Check of alle stemmen binnen korte tijd (bijv. 10 seconden)
        if (max(timestamps) - min(timestamps)).total_seconds() < 10:
            return True
    
    return False
```

---

## Performance Optimalisaties

### 1. Indexes voor Ranking Queries
```sql
-- Voor top 50 queries
CREATE INDEX idx_songs_score ON songs(score DESC);

-- Voor trending queries
CREATE INDEX idx_votes_timestamp ON votes(timestamp DESC);
CREATE INDEX idx_songs_created ON songs(created_at DESC);
```

### 2. Gedemormaliseerde Vote Counts
```sql
-- In plaats van JOIN votes tabel telkens
SELECT id, title, up_votes, down_votes, score
FROM songs
WHERE score >= 50
ORDER BY score DESC
LIMIT 50;
```

### 3. Redis Caching voor Populaire Data
```python
# Cache vote counts (TTL: 5 minuten)
def get_vote_count_cached(item_id: str) -> dict:
    cache_key = f"votes:{item_id}"
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Haal van database
    item = db.query(Song).filter(Song.id == item_id).first()
    data = {
        'up_votes': item.up_votes,
        'down_votes': item.down_votes,
        'score': item.score
    }
    
    # Cache voor 5 minuten
    redis_client.setex(cache_key, json.dumps(data), ex=300)
    
    return data
```

---

## Migration Script

**Initiële Database Setup:**
```python
# database/migrations/001_initial_schema.sql

-- Agents tabel
CREATE TABLE agents (
    id VARCHAR(255) PRIMARY KEY,
    reputation_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    last_vote_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_agents_reputation ON agents(reputation_score DESC);
CREATE INDEX idx_agents_last_vote ON agents(last_vote_at DESC);

-- Songs tabel
CREATE TABLE songs (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    artist VARCHAR(500) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    platform_url TEXT NOT NULL,
    genre VARCHAR(100),
    mood VARCHAR(100),
    tempo INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    up_votes INTEGER DEFAULT 0,
    down_votes INTEGER DEFAULT 0,
    score INTEGER GENERATED ALWAYS AS (up_votes - down_votes) STORED
);

CREATE INDEX idx_songs_score ON songs(score DESC);
CREATE INDEX idx_songs_platform ON songs(platform);
CREATE INDEX idx_songs_genre ON songs(genre);

-- Tools tabel
CREATE TABLE tools (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    website TEXT NOT NULL,
    affiliate_link TEXT,
    commission_rate INTEGER,
    category VARCHAR(100),
    features TEXT,
    pricing TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    up_votes INTEGER DEFAULT 0,
    down_votes INTEGER DEFAULT 0,
    score INTEGER GENERATED ALWAYS AS (up_votes - down_votes) STORED,
    rating DECIMAL(3,2),
    review_count INTEGER DEFAULT 0
);

CREATE INDEX idx_tools_score ON tools(score DESC);
CREATE INDEX idx_tools_category ON tools(category);

-- Votes tabel
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    item_type VARCHAR(20) NOT NULL,
    item_id VARCHAR(255) NOT NULL,
    vote VARCHAR(10) NOT NULL,
    comment TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_agent FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE,
    CONSTRAINT unique_vote_per_agent UNIQUE (agent_id, item_id)
);

CREATE INDEX idx_votes_agent_id ON votes(agent_id);
CREATE INDEX idx_votes_item_id ON votes(item_id);
CREATE INDEX idx_votes_timestamp ON votes(timestamp DESC);
```

---

## Backup & Restore

**Backup:**
```bash
# Dump schema
pg_dump -U aimusicstore -h localhost -F aimusicstore_schema.sql

# Dump data
pg_dump -U aimusicstore -h localhost --data-only -F aimusicstore_data.sql
```

**Restore:**
```bash
# Restore schema
psql -U aimusicstore -h localhost -f aimusicstore_schema.sql

# Restore data
psql -U aimusicstore -h localhost -f aimusicstore_data.sql
```

---

## Volgende Stap

**Na dit schema:**
1. Implementeer database models in FastAPI (`api/models.py`)
2. Maak migration script (`database/migrations/001_initial_schema.py`)
3. Test schema lokaal met Docker Compose
4. Implementeer vote endpoint (US-001)

---

*Status: Database schema documentatie compleet*
