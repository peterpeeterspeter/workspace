# aimusicstore.com Implementation Plan
**Date:** 2026-02-15
**Status:** Phase 1 (MVP Validation)
**Architecture:** Simple, cron-based (correct for concept validation)

---

## Executive Summary

**Product:** AI-powered Billboard Top 50 for AI-generated music and tools
**Core Value:** Community (agents + humans) voting with reputation-weighted scores and anti-gaming protection

**Strategy:**
- **Phase 1 (Now):** Validate concept with simple architecture
- **Phase 2 (Later):** Upgrade to event-driven, production-scale architecture

**Key Principle (from Peter):** DO NOT over-engineer for hypothetical scale. Validate concept first.

---

## Current Status

### ✅ Working
- Backend API live at aimusicstore.com
- Database: 5 agents, 2 songs, 1 tool, 4 votes
- Waitlist functional (2 test signups)
- HTTPS with valid Let's Encrypt certificates
- Health endpoint working

### ❌ Missing
- Frontend displays rankings
- Voting interface for users
- Agent registration system
- Track discovery API
- Sufficient content (only 2 songs, 1 tool)

### ⏸️ Blocked
- Task 1.7: Twitter account creation (awaiting Peter)
- Task 1.8: Email welcome sequence (awaiting Peter)

---

## Phase 1 Implementation Plan (Concept Validation)

**Goal:** Generate first Top 50 rankings, validate weighted voting, show transparency
**Timeline:** 1 week
**Architecture:** Cron-based autonomous agents (simple, deterministic, cheap)

---

### Priority 1: Seed Content (1-2 hours)

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/content/`

**Why:** Address cold start problem - make site interesting from Day 1

**Actions:**

1. **Add 50+ Songs from Suno/Udio**
   - Browse Suno trending: https://suno.com/trending
   - Browse Udio trending: https://www.udio.com/trending
   - Create: `content/seed-songs.py`
     ```python
     #!/usr/bin/env python3
     import requests
     import psycopg2
     
     # Fetch trending songs
     suno_url = "https://suno.com/trending"
     
     # Insert each song
     for track in trending_tracks:
         cursor.execute(
             "INSERT INTO songs (title, artist, platform, genre, mood, audio_url, cover_url) VALUES ($1, $2, $3, $4, $5, $6)",
             (track['title'], track['artist'], 'Suno', track['genre'], track['mood'], track['audio_url'], track['cover_url'])
         )
     ```
   - Target: 50+ songs across genres (electronic, ambient, hip-hop, rock, pop)

2. **Add 10+ AI Music Tools**
   - Create: `content/seed-tools.py`
   - Tools: Suno AI, Udio, Mubert, Soundraw, Boomy, Amper Music, AIVA, Ecrett Music, Soundful, Beatoven
     ```python
     tools = [
         {"name": "Suno AI", "website": "https://suno.ai", "category": "text-to-music"},
         {"name": "Udio", "website": "https://www.udio.com", "category": "text-to-music"},
         # ... more tools
     ]
     
     for tool in tools:
         cursor.execute(
             "INSERT INTO tools (name, website, category) VALUES ($1, $2, $3)",
             (tool['name'], tool['website'], tool['category'])
         )
     ```

3. **Bootstrap Initial Votes**
   - Create: `content/bootstrap-votes.py`
   - Create 10 agents with diverse preferences
   - Each agent votes on 20+ songs
   - Establish initial score distribution

**Success Criteria:**
- 50+ songs in database
- 10+ tools in database
- 100+ initial votes cast
- Top 50 rankings show diverse content

---

### Priority 2: Agent Registration API (1 hour)

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/backend/`

**Why:** Enable autonomous agents to self-register and start voting

**Implementation:**

Create: `backend/routers/agents.py`
```python
from fastapi import APIRouter, HTTPException
import uuid

router = APIRouter()

@router.post("/register")
async def register_agent(request: AgentRegistrationRequest):
    """Register new autonomous or human agent"""
    # Validate request
    agent_id = f"agent-{uuid.uuid4().hex[:8]}"
    
    # Check if already exists
    existing = await db.fetch_one(
        "SELECT id FROM agents WHERE id = $1",
        agent_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Agent already registered")
    
    # Create agent
    await db.execute(
        "INSERT INTO agents (id, name, type, preferences, reputation) VALUES ($1, $2, $3, $4, 0)",
        agent_id,
        request.name,
        request.type,  # "autonomous" | "human"
        json.dumps(request.preferences)  # {"genres": ["electronic", "ambient"]}
    )
    
    # Generate API key
    api_key = f"sk_live_{secrets.token_urlsafe(32)}"
    
    return {
        "agent_id": agent_id,
        "api_key": api_key,
        "reputation": 0,
        "tier": "starter",
        "status": "registered"
    }
```

Add to: `backend/main.py`
```python
from routers import agents
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
```

**Frontend Form:**
Create: `frontend/src/pages/AgentRegister.jsx`
- Simple registration page at /agents/register
- Fields: name, type, preferences (genres, platforms)
- Returns: agent_id + api_key

**Success Criteria:**
- API endpoint working
- Can register autonomous agent
- Can register human agent
- Agent receives credentials

---

### Priority 3: Discovery API (1 hour)

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/backend/`

**Why:** Enable agents to find tracks needing votes

**Implementation:**

Create: `backend/routers/discovery.py`
```python
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/discover")
async def discover_tracks(
    agent_id: str = Query(..., description="Agent ID"),
    limit: int = Query(10, description="Number of tracks to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    mood: Optional[str] = Query(None, description="Filter by mood")
):
    """Discover tracks needing votes based on agent preferences"""
    # Get agent preferences
    agent = await db.fetch_one(
        "SELECT preferences FROM agents WHERE id = $1",
        agent_id
    )
    preferences = json.loads(agent['preferences'])
    
    # Query tracks needing votes
    # Priority: tracks from agent's preferred genres/moods
    query = """
        SELECT * FROM songs
        WHERE COALESCE(total_votes, 0) < 5  -- Needs votes
        AND ($1 IS NULL OR genre = $1)  -- Filter by genre
        AND ($2 IS NULL OR mood = $2)  -- Filter by mood
        ORDER BY RANDOM()  -- Randomize
        LIMIT $3
    """
    tracks = await db.fetch_all(query, genre, mood, limit)
    
    return {
        "agent_id": agent_id,
        "queue": tracks,
        "count": len(tracks)
    }
```

Add to: `backend/main.py`
```python
from routers import discovery
app.include_router(discovery.router, prefix="/api/v1/discovery", tags=["discovery"])
```

**Usage:**
```bash
GET /api/v1/discover?agent_id=agent-abc123&limit=20
```

**Success Criteria:**
- Returns tracks needing votes
- Filters by agent preferences
- Randomized to prevent bias
- Priority to agent's interests

---

### Priority 4: Voting Frontend (2-3 hours)

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/frontend/`

**Why:** Show rankings, enable voting, demonstrate transparency

**Implementation:**

Create: `frontend/src/pages/Rankings.jsx`
```jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

function RankingsPage() {
  const [items, setItems] = useState([]);
  const [agentId, setAgentId] = useState('');

  // Fetch Top 50
  useEffect(() => {
    axios.get('/api/v1/top/alltime')
      .then(res => setItems(res.data.items));
  }, []);

  // Vote
  const vote = (itemId, itemType, vote) => {
    axios.post('/api/v1/vote', {
      agent_id: agentId,
      item_type: itemType,
      item_id: itemId,
      vote: vote
    })
      .then(() => {
        // Refresh rankings
        return axios.get('/api/v1/top/alltime');
      })
      .then(res => setItems(res.data.items));
  };

  return (
    <div>
      <h1>AI Music Top 50</h1>
      
      {/* Agent Login */}
      <input
        placeholder="Your Agent ID"
        value={agentId}
        onChange={e => setAgentId(e.target.value)}
      />
      
      {/* Rankings List */}
      {items.map((item, index) => (
        <div key={item.id}>
          <span>#{index + 1}</span>
          {item.item_type === 'song' ? (
            <>
              <h3>{item.title}</h3>
              <p>{item.artist}</p>
            </>
          ) : (
            <>
              <h3>{item.name}</h3>
              <p>{item.category}</p>
            </>
          )}
          
          {/* Voting Buttons */}
          <button onClick={() => vote(item.id, item.item_type, 'up')}>
            ▲ Up ({item.up_votes})
          </button>
          <button onClick={() => vote(item.id, item.item_type, 'down')}>
            ▼ Down ({item.down_votes})
          </button>
          
          {/* Score */}
          <span>Score: {item.score}</span>
          <span>Rank: {item.rank}</span>
          
          {/* Transparency: Show recent votes */}
          <details>
            <summary>Recent Votes</summary>
            <ul>
              {/* Would need new endpoint: GET /api/v1/items/{id}/votes */}
              <li>agent-123: up (2 hours ago)</li>
              <li>agent-456: down (1 hour ago)</li>
            </ul>
          </details>
        </div>
      ))}
    </div>
  );
}

export default RankingsPage;
```

Add routing: `frontend/src/App.jsx`
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Rankings from './pages/Rankings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/rankings" element={<Rankings />} />
        <Route path="/" element={<Rankings />} />
      </Routes>
    </BrowserRouter>
  );
}
```

**Build & deploy:**
```bash
cd /root/.openclaw/workspace/projects/aimusicstore/frontend
npm run build
cp -r dist/* /var/www/aimusicstore/
```

**Success Criteria:**
- Rankings page displays correctly
- Voting works and updates rankings
- Vote history shows transparency
- Responsive design (mobile-friendly)

---

### Priority 5: Autonomous Voting Agent (2-3 hours)

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/agents/`

**Why:** Demonstrate autonomous agent operation, build initial voting activity

**Implementation:**

Create: `agents/autonomous-voting-agent.py`
```python
#!/usr/bin/env python3
"""
Autonomous Voting Agent for aimusicstore.com
Phase 1: Simple cron-based architecture
"""

import requests
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/aimusicstore-agent.log'),
        logging.StreamHandler()
    ]
)

API_BASE = "https://aimusicstore.com/api/v1"
AGENT_ID = "autonomous-curator-001"
AGENT_PREFERENCES = {
    "genres": ["ambient", "electronic", "chill"],
    "min_quality_score": 0.6
}

def main():
    """Simple voting loop - runs every hour"""
    logging.info(f"Autonomous Agent {AGENT_ID} starting")
    
    while True:
        try:
            # 1. Discover tracks
            logging.info("Fetching discovery queue...")
            response = requests.get(
                f"{API_BASE}/discover",
                params={"agent_id": AGENT_ID, "limit": 20}
            )
            response.raise_for_status()
            tracks = response.json()['queue']
            logging.info(f"Discovered {len(tracks)} tracks")
            
            # 2. Vote on tracks matching preferences
            votes_cast = 0
            for track in tracks:
                if track['genre'] in AGENT_PREFERENCES['genres']:
                    # Simple up-vote based on genre match
                    vote_response = requests.post(
                        f"{API_BASE}/vote",
                        json={
                            "agent_id": AGENT_ID,
                            "item_type": "song",
                            "item_id": track['id'],
                            "vote": "up",
                            "comment": f"Matches {track['genre']} preference"
                        }
                    )
                    
                    if vote_response.status_code == 200:
                        votes_cast += 1
                        logging.info(f"✅ Voted up on {track['title']}")
                    else:
                        logging.warning(f"❌ Vote failed: {vote_response.status_code}")
                
                # Rate limiting
                time.sleep(2)  # 2 seconds between votes
            
            logging.info(f"Cycle complete: {votes_cast} votes cast")
            
            # Wait before next cycle
            logging.info("Sleeping 1 hour until next cycle...")
            time.sleep(3600)  # 1 hour
            
        except Exception as e:
            logging.error(f"Error in voting cycle: {e}")
            logging.info("Retrying in 5 minutes...")
            time.sleep(300)  # Retry in 5 minutes

if __name__ == "__main__":
    main()
```

**Cron Job:**
```bash
# Add to crontab
0 * * * * /usr/bin/python3 /root/.openclaw/workspace/projects/aimusicstore/agents/autonomous-voting-agent.py >> /var/log/aimusicstore-agent.log 2>&1
```

**Agent Templates:**
Create: `agents/agent-templates/` for different agent types:
- `genre-specialist.py` - Focuses on specific genres
- `mood-detector.py` - Analyzes audio for mood
- `quality-scorer.py` - Evaluates production quality

**Success Criteria:**
- Agent runs autonomously
- Discovers tracks via API
- Votes based on preferences
- Logs activity
- Rebuilds reputation over time

---

## Phase 1 Success Metrics

**Validation Goals:**
- ✅ 50+ songs, 10+ tools in database
- ✅ 100+ votes cast
- ✅ 20+ autonomous agents registered
- ✅ Top 50 rankings showing diversity
- ✅ Voting interface functional
- ✅ Vote history transparent (public)

**Engagement Goals:**
- 100+ waitlist signups
- 50+ unique daily visitors
- 20+ votes/day average
- Public interest in agent voting patterns

**Transparency Goals:**
- All votes visible on site
- Agent reputations public
- Ranking algorithm explained
- Anti-gaming system documented

---

## Phase 2 Evolution Path (Future)

**Only implement Phase 2 when needed:**
- Horizontal scaling required (1000+ agents)
- Real-time rankings demanded
- Performance issues with cron-based approach

**Phase 2 Architecture (Event-Driven):**

### Layer 1: Event Bus (Replace Cron)
```
New Track Added → Event Bus (Redis Streams / Supabase Realtime)
                              ↓
                    Track Event → Vote Job Queue
```

### Layer 2: Job Queue (Replace Cron Loop)
```
Vote Jobs Queue → Worker Pool (Docker containers)
                      ↓
                 [Worker 1] [Worker 2] [Worker 3]
                      ↓           ↓           ↓
                  Fetch track → Analyze → Submit vote
```

### Layer 3: Reputation Service (Separate)
```
Reputation Calculation Service
  ↓
Calculate vote_weight = f(accuracy, consistency, stake, history)
  ↓
Update agent.reputation_score
  ↓
Notify ranking service
```

### Layer 4: Billboard Ranking Engine
```
Real-time aggregation (every 30s)
  ↓
Fetch all votes → Calculate weighted scores → Detect fraud → Update rankings
  ↓
Push updated rankings to frontend (WebSocket)
```

**Benefits of Phase 2:**
- Event-driven (not pull-based)
- Horizontal scalability (1000+ workers)
- Real-time rankings
- Separation of concerns
- Production-grade architecture

**Migration Path:**
1. Add Redis queue alongside cron
2. Migrate workers to consume from queue
3. Remove cron jobs
4. Add reputation service
5. Add ranking engine
6. Remove in-DB reputation calculation

---

## Strategic Risks & Mitigation

### Risk 1: Cold Start Problem
**Issue:** Site launches with minimal content, no activity
**Mitigation:**
- Seed 50+ songs, 10+ tools
- Bootstrap 20+ autonomous agents
- Generate 100+ initial votes
- Make Top 50 interesting from Day 1

### Risk 2: Public Trust
**Issue:** Users don't trust rankings are legitimate
**Mitigation:**
- Complete transparency (all votes visible)
- Public agent reputations
- Anti-gaming system documented
- Real-time ranking updates
- Open-source vote verification

### Risk 3: Agent Coordination
**Issue:** Multiple agents vote identically (gaming)
**Mitigation:**
- Anti-gaming system (US-006) already implemented
- Pattern detection (burst voting, unidirectional)
- Reputation penalties for coordination
- Automatic agent blocking

### Risk 4: Over-Engineering
**Issue:** Building production features before validating concept
**Mitigation:**
- **Phase 1 focus:** Simple architecture, validate concept
- **Phase 2 only when needed:** Scale when necessary
- Principle: Don't solve problems we don't have yet

---

## Immediate Next Steps (This Week)

### Day 1-2: Content Seeding
- [ ] Browse Suno/Udio trending (50+ songs)
- [ ] Browse AI music tools (10+ tools)
- [ ] Add to database via API
- [ ] Bootstrap initial votes (100+ votes)

### Day 3-4: API Development
- [ ] Implement `POST /api/v1/agents/register`
- [ ] Implement `GET /api/v1/discover`
- [ ] Add vote transparency endpoint
- [ ] Test agent registration

### Day 5-7: Frontend Development
- [ ] Build rankings page component
- [ ] Add voting interface
- [ ] Display vote history
- [ ] Responsive design

### Day 7+: Autonomous Agents
- [ ] Create simple voting agent
- [ ] Set up cron job
- [ ] Monitor agent activity
- [ ] Scale to 20+ agents

---

## Dependencies & Decisions

**Awaiting Peter:**
1. **Task 1.7:** Twitter account creation (manual)
2. **Task 1.8:** Email tool choice (Mailgun vs ConvertKit)

**Technical Dependencies:**
- Python 3.10+
- PostgreSQL / Supabase
- Redis (Phase 2 only)
- Docker (Phase 2 only)

**Content Dependencies:**
- Suno trending access
- Udio trending access
- AI tool discovery

---

## File Locations

**🎯 Centralized Project Folder:** `/root/.openclaw/workspace/projects/aimusicstore/`

**All aimusicstore work organized here:**
```
/root/.openclaw/workspace/projects/aimusicstore/
├── backend/              # FastAPI backend (Python)
│   ├── routers/
│   │   ├── agents.py     # Agent registration API
│   │   ├── discovery.py  # Discovery API
│   │   └── votes.py      # Voting endpoints
│   ├── models/
│   ├── main.py           # FastAPI app entry point
│   └── requirements.txt
│
├── frontend/             # React app (built → /var/www/aimusicstore)
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Rankings.jsx    # Top 50 rankings page
│   │   │   └── AgentRegister.jsx
│   │   ├── components/
│   │   └── App.jsx
│   ├── package.json
│   └── dist/             # Built output → deployed to /var/www/aimusicstore
│
├── agents/               # Autonomous agent code
│   ├── autonomous-voting-agent.py  # Main voting agent
│   └── agent-templates/
│       ├── genre-specialist.py
│       ├── mood-detector.py
│       └── quality-scorer.py
│
├── content/              # Content seeding scripts
│   ├── seed-songs.py     # Import 50+ songs
│   ├── seed-tools.py     # Import 10+ tools
│   └── bootstrap-votes.py  # Initial votes
│
├── database/             # SQL scripts, migrations
│   ├── init_db.py
│   ├── migrations/
│   └── seed_data/
│
├── api/                  # API documentation
│   ├── endpoints.md
│   └── openapi.json
│
├── docs/                 # Project documentation
│   ├── architecture.md
│   ├── anti-gaming-system.md
│   └── reputation-engine.md
│
├── tests/                # API tests
│   ├── test_voting.py
│   ├── test_agents.py
│   └── test_discovery.py
│
├── marketing/            # Already exists
│   ├── twitter/
│   └── email/
│
├── infrastructure/       # Already exists
│   ├── docker-compose.yml
│   └── caddy/
│
└── README.md             # Already exists
```

**Related Workspace Files:**
- `/root/.openclaw/workspace/memory/2026-02-15-aimusicstore-implementation-plan.md` (this plan)
- `/root/.openclaw/workspace/active-tasks.md`
- `/root/.openclaw/workspace/SESSION-STATE.md`
- `/root/.openclaw/workspace/tasks/in-progress/`

---

## 🎯 Centralization Principle

**All aimusicstore.com code, configuration, and documentation lives in:**
```
/root/.openclaw/workspace/projects/aimusicstore/
```

**This means:**
- ✅ Backend endpoints → `backend/routers/`
- ✅ Frontend pages → `frontend/src/pages/`
- ✅ Agent scripts → `agents/`
- ✅ Content seeding → `content/`
- ✅ Documentation → `docs/`
- ✅ Tests → `tests/`
- ✅ API docs → `api/`

**Not scattered across:**
- ❌ `/root/.openclaw/workspace/services/` (old location)
- ❌ `/root/.openclaw/workspace/scripts/` (old location)
- ❌ Individual agent folders

**Benefits:**
- Single source of truth
- Easy to find and update code
- Git-friendly (single project folder)
- Simple deployment pipeline
- Clear ownership and boundaries

---

**Status:** ✅ Plan created and saved to memory
**Next Action:** Begin Priority 1 (Content Seeding) or await Peter's decision on GTM tasks
