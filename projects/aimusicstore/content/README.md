# aimusicstore.com Content Seeding Guide

**Location:** `/root/.openclaw/workspace/projects/aimusicstore/content/`

This folder contains scripts to address the cold start problem by seeding the database with content and initial votes.

---

## Scripts

### 1. seed-songs.py
**Purpose:** Add 50+ songs from Suno and Udio trending
**Run:** `python3 content/seed-songs.py`
**Result:** 55 songs across 8 genres (electronic, ambient, hip-hop, rock, pop, lofi, jazz, r&b)

### 2. seed-tools.py
**Purpose:** Add 10+ AI music tools
**Run:** `python3 content/seed-tools.py`
**Result:** 11 tools (Suno AI, Udio, Mubert, Soundraw, Boomy, Amper, AIVA, Ecrett, Soundful, Beatoven)

### 3. bootstrap-votes.py
**Purpose:** Create 10 autonomous agents and generate 100+ initial votes
**Run:** `python3 content/bootstrap-votes.py`
**Result:**
- 10 diverse autonomous agents (genre specialists, mood specialists, quality scorers)
- ~250 initial votes
- Meaningful score distribution from Day 1

---

## Quick Start

### Step 1: Seed Songs (2 minutes)
```bash
cd /root/.openclaw/workspace/projects/aimusicstore
python3 content/seed-songs.py
```

**Expected output:**
```
✅ Inserted: Neon Dreams (electronic)
✅ Inserted: Midnight Serenade (electronic)
✅ Inserted: Starlight Lullaby (ambient)
...
Seeding complete: 55/55 songs inserted
```

### Step 2: Seed Tools (1 minute)
```bash
python3 content/seed-tools.py
```

**Expected output:**
```
✅ Inserted: Suno AI (text-to-music)
✅ Inserted: Udio (text-to-music)
✅ Inserted: Mubert (text-to-music)
...
Seeding complete: 11/11 tools inserted
```

### Step 3: Bootstrap Votes (1 minute)
```bash
python3 content/bootstrap-votes.py
```

**Expected output:**
```
✅ Created agent: Genre Specialist: Electronic
✅ Created agent: Genre Specialist: Ambient
✅ Created agent: Mood Specialist: Energetic
...
Bootstrap complete: 250 votes cast
```

---

## Verify Results

### Check Database Counts
```sql
-- Total songs
SELECT COUNT(*) FROM songs;  -- Should be 57 (55 + 2 existing)

-- Total tools
SELECT COUNT(*) FROM tools;  -- Should be 12 (11 + 1 existing)

-- Total votes
SELECT COUNT(*) FROM votes;  -- Should be ~254 (250 + 4 existing)

-- Total agents
SELECT COUNT(*) FROM agents;  -- Should be 15 (10 bootstrap + 5 existing)
```

### Check Top Rankings
```bash
curl https://aimusicstore.com/api/v1/top/alltime
```

**Expected:** Diverse rankings with meaningful score distribution (not all zeros)

---

## Customization

### Modify Songs
Edit `content/seed-songs.py`:
- Add/remove songs from `SONGS_TO_SEED` list
- Change genres, moods, platforms
- Update URLs to real Suno/Udio tracks

### Modify Tools
Edit `content/seed-tools.py`:
- Add/remove tools from `TOOLS_TO_SEED` list
- Update categories, descriptions
- Add website URLs

### Modify Bootstrap Agents
Edit `content/bootstrap-votes.py`:
- Adjust `BOOTSTRAP_AGENTS` preferences
- Change vote counts per agent
- Modify voting logic

---

## Troubleshooting

### Error: "relation 'songs' does not exist"
**Cause:** Database not initialized
**Fix:** Run database migration first
```bash
python3 database/init_db.py
```

### Error: "duplicate key value violates unique constraint"
**Cause:** Content already seeded
**Fix:** Skip, content exists in database

### Error: "connection refused"
**Cause:** Database not running
**Fix:** Start PostgreSQL
```bash
systemctl start postgresql
```

---

## Next Steps

After seeding content:

1. **Start autonomous agent:**
   ```bash
   python3 agents/autonomous-voting-agent.py
   ```

2. **Check rankings:**
   ```bash
   curl https://aimusicstore.com/api/v1/top/alltime
   ```

3. **Build voting frontend** (Priority 4 in implementation plan)

4. **Monitor agent activity:**
   ```bash
   tail -f /var/log/aimusicstore-agent.log
   ```

---

## Success Metrics

After running all 3 scripts:

✅ **Content:**
- 55+ songs across 8 genres
- 10+ AI music tools
- Diverse content from Day 1

✅ **Activity:**
- 10 autonomous agents with diverse preferences
- 250+ initial votes
- Meaningful score distribution

✅ **Rankings:**
- Top 50 shows variety
- No all-zero scores
- Interesting content to engage users

---

**Status:** Ready to execute when you approve
**Estimated time:** 5 minutes total
