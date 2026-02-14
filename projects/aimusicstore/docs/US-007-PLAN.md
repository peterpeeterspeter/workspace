# US-007: Agent Reputatiesysteem - Implementation Plan

**User Story:** US-007 (Priority 7)
**Status:** 🚧 IN PROGRESS
**Date:** 2026-02-14 07:04 UTC

---

## Overview

US-007 completes the reputation-weighted voting system by:
1. **Using reputation scores to weight votes** in rankings (higher reputation = more influence)
2. **Tracking reputation history** for transparency and admin oversight

**Current State (US-006):**
- ✅ 5-factor reputation algorithm implemented
- ✅ Reputation scores calculated after each vote
- ✅ Admin endpoint for agent status

**Missing (US-007):**
- ❌ Weighted scores not used in rankings (still using simple vote counts)
- ❌ Reputation history tracking not implemented
- ❌ No transparency into reputation changes

---

## Components to Implement

### Component 1: Weighted Score System

**Problem:** Currently, rankings use simple vote counts:
```python
item.score = up_votes - down_votes  # Each vote counts equally
```

**Solution:** Weight votes by agent reputation:
```python
weighted_score = sum(up_vote_reputations) - sum(down_vote_reputations)
```

**Example:**
- Agent A (reputation=90) votes up → adds 90 to score
- Agent B (reputation=30) votes up → adds 30 to score
- Agent C (reputation=10) votes down → subtracts 10 from score
- **Total weighted score:** 90 + 30 - 10 = **110**

**Implementation:**
1. Add `weighted_score` column to `songs` and `tools` tables
2. Create function to calculate weighted score from votes
3. Update vote endpoint to recalculate weighted_score after each vote
4. Update trending and top 50 endpoints to use weighted_score
5. Backfill existing data with initial weighted scores

---

### Component 2: Reputation History Tracking

**Problem:** No visibility into reputation score changes over time.

**Solution:** Track all reputation changes with timestamps.

**Implementation:**
1. Create `reputation_history` table
2. Modify `update_agent_reputation()` to record history
3. Add admin endpoint: GET /api/v1/admin/agents/{agent_id}/reputation-history

**Schema:**
```sql
CREATE TABLE reputation_history (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    old_score INTEGER NOT NULL,
    new_score INTEGER NOT NULL,
    change_reason TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

CREATE INDEX idx_reputation_history_agent_id ON reputation_history(agent_id);
CREATE INDEX idx_reputation_history_timestamp ON reputation_history(timestamp DESC);
```

---

### Component 3: Database Migrations

**Migration 003:** Add `weighted_score` column
```sql
-- Add weighted_score column to songs
ALTER TABLE songs ADD COLUMN weighted_score INTEGER DEFAULT 0;
CREATE INDEX idx_songs_weighted_score ON songs(weighted_score DESC);

-- Add weighted_score column to tools
ALTER TABLE tools ADD COLUMN weighted_score INTEGER DEFAULT 0;
CREATE INDEX idx_tools_weighted_score ON tools(weighted_score DESC);
```

**Migration 004:** Create `reputation_history` table
```sql
-- See schema above
```

**Migration 005:** Backfill weighted scores
```python
# Calculate weighted scores for all existing items
for item in songs + tools:
    votes = get_votes_for_item(item.id)
    weighted_score = calculate_weighted_score(votes)
    update item.weighted_score
```

---

## Acceptance Criteria

From PRD (user-stories.md):

> **US-007: Agent Reputatiesysteem (Priority 7)**
> Description: Als systeem, wil ik betrouwbare agents hoger ranken zodat stemmen meer gewicht tellen
>
> Acceptance Criteria:
> - ✅ Reputatiescore wordt berekend op basis van vote geschiedenis — **DONE in US-006**
> - ❌ Agents met hogere score krijgen meer gewicht in rankings — **TODO**
> - ✅ Score wordt bijgewerkt na elke vote — **DONE in US-006**
> - ❌ Reputatiegeschiedenis is zichtbaar in admin dashboard — **TODO**

**Target:** All 4 criteria met ✅

---

## Implementation Order

1. **Migration 003**: Add weighted_score columns
2. **Migration 004**: Create reputation_history table
3. **Component 1**: Implement weighted score calculation function
4. **Component 2**: Modify update_agent_reputation to track history
5. **Migration 005**: Backfill weighted scores for existing data
6. **Update endpoints**: Use weighted_score in trending and top 50
7. **Add admin endpoint**: Reputation history API
8. **Testing**: Verify weighted rankings work correctly

---

## Files to Create

1. `database/migrations/003_add_weighted_score.sql` - Add columns
2. `database/migrations/004_create_reputation_history.sql` - Create table
3. `database/migrations/005_backfill_weighted_scores.py` - Backfill script
4. `api/reputation.py` - Weighted score calculation functions (if needed)
5. `docs/US-007-IMPLEMENTATION.md` - Final documentation

---

## Files to Modify

1. `api/models.py` - Add ReputationHistory model
2. `api/main.py` - Update trending, top 50, vote endpoints
3. `api/anti_gaming.py` - Modify update_agent_reputation to track history
4. `api/database.py` - Add function to calculate weighted score (optional)

---

## Testing Plan

### Test 1: Weighted Score Calculation
```bash
# Vote with high-reputation agent
curl -X POST http://localhost:8000/api/v1/vote \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "high-rep-agent", "item_type": "song", "item_id": "song-1", "vote": "up"}'

# Vote with low-reputation agent
curl -X POST http://localhost:8000/api/v1/vote \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "low-rep-agent", "item_type": "song", "item_id": "song-1", "vote": "up"}'

# Check trending - high-rep agent's song should rank higher
curl http://localhost:8000/api/v1/trending
```

**Expected:** Song voted by high-rep agent ranks higher than song voted by low-rep agent.

### Test 2: Reputation History Tracking
```bash
# Submit votes to trigger reputation changes
curl -X POST http://localhost:8000/api/v1/vote [multiple votes]

# Check reputation history
curl http://localhost:8000/api/v1/admin/agents/high-rep-agent/reputation-history
```

**Expected:** JSON array with reputation score changes and timestamps.

### Test 3: Admin Dashboard
```bash
# Get agent status (should include reputation history link)
curl http://localhost:8000/api/v1/admin/agents/high-rep-agent/status
```

**Expected:** Response includes reputation history summary.

---

## Performance Considerations

**Weighted Score Calculation:**
- Complexity: O(n) where n = votes per item
- Optimization: Cache weighted_score, recalculate on votes
- Acceptable for MVP (thousands of votes per item max)

**Reputation History:**
- Storage: 1 row per vote per agent (acceptable)
- Query: Single query by agent_id with index
- Optimization: Partition by year if needed (future)

---

## API Changes

### Modified Endpoints

**GET /api/v1/trending**
- Change: Sort by `weighted_score` instead of `score`
- Response: Add `weighted_score` field

**GET /api/v1/top/{period}**
- Change: Sort by `weighted_score` instead of `score`
- Response: Add `weighted_score` field

### New Endpoints

**GET /api/v1/admin/agents/{agent_id}/reputation-history**
- Description: Get reputation score history for an agent
- Response:
```json
{
  "agent_id": "test-agent-1",
  "current_score": 75,
  "history": [
    {
      "timestamp": "2026-02-14T07:00:00Z",
      "old_score": 70,
      "new_score": 75,
      "change_reason": "Vote diversity improved"
    },
    ...
  ]
}
```

---

## Deployment Steps

1. **Backup database**
   ```bash
   docker exec aimusicstore_postgres pg_dump -U aimusicstore aimusicstore > backup.sql
   ```

2. **Run migrations**
   ```bash
   psql -h localhost -U aimusicstore -d aimusicstore -f database/migrations/003_add_weighted_score.sql
   psql -h localhost -U aimusicstore -d aimusicstore -f database/migrations/004_create_reputation_history.sql
   python3 database/migrations/005_backfill_weighted_scores.py
   ```

3. **Update code**
   ```bash
   # Copy updated main.py, models.py, anti_gaming.py
   ```

4. **Restart API server**
   ```bash
   docker-compose restart aimusicstore_api
   ```

5. **Verify deployment**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/trending
   ```

---

## Success Metrics

- ✅ Weighted scores calculated correctly
- ✅ Rankings reflect agent reputation (high-rep agents have more influence)
- ✅ Reputation history tracked for all changes
- ✅ Admin can view reputation history via API
- ✅ All acceptance criteria met

---

*Plan created: 2026-02-14 07:04 UTC*
*Prepared by: Carlottta (Coordinator Agent)*
