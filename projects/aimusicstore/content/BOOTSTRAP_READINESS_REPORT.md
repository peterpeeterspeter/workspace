# Bootstrap Voting Readiness Report

**Generated:** 2026-02-15 09:35 UTC
**Status:** ✅ Ready to proceed with safeguards

---

## Current Database State

### Content Inventory
- **Songs:** 68 total
  - 10 existing (original seed)
  - 58 new (just seeded)
  - Distribution:
    - Electronic: 12
    - Pop: 10
    - Ambient: 8
    - Hip-hop: 8
    - Lo-fi: 7
    - Rock: 7
    - Experimental: 6
    - Other: 10

- **Tools:** 12 total
  - 1 existing (Suno AI)
  - 11 new (just seeded)
  - Distribution:
    - Mubert: 15
    - Soundraw: 14
    - Suno: 12
    - Udio: 17

- **Total Items:** 80 (68 songs + 12 tools)
- **Target Met:** ✅ Yes (50+ minimum requirement)

### Content Quality
- ✅ Platform diversity: Suno, Udio, Mubert, Soundraw represented
- ✅ Genre diversity: 7 genres represented
- ✅ BPM range: 75-150 (good variety)
- ✅ Mood diversity: energetic, chill, upbeat, dark, mellow, etc.
- ✅ Timestamp randomization: Last 30 days (prevents artificial clustering)

---

## Database Constraint Verification (Step 2)

### ✅ Verified
1. **Unique constraint on (agent_id, item_id):** EXISTS
   - Constraint name: `unique_vote_per_agent`
   - Status: ✅ Active and working
   - Prevents duplicate votes per agent per item

2. **Vote model fields:**
   - Current fields: id, agent_id, item_type, item_id, vote, comment, timestamp
   - Missing: `vote_source` field

3. **Agent reputation defaults:**
   - reputation_score: INTEGER, NOT NULL, no default
   - Should default to: 0.5 (bootstrap agents) and 50 (new real agents)

### ⚠️ Issues Found

1. **Missing vote_source field**
   - Vote model lacks field to distinguish bootstrap vs real votes
   - Recommendation: Add `vote_source` ENUM('bootstrap', 'real')
   - Purpose: Enables filtering, transparency, later removal of bootstrap bias

2. **Agent reputation defaults**
   - Bootstrap agents should init at: 0.5 (not 0 or 1.0)
   - Real agents should init at: 50 (neutral score)

---

## Bootstrap Script Safeguards Required (Step 3)

### Current bootstrap-votes.py Issues

1. **Vote weight = 1.0** (should be 0.1)
   - Currently uses full agent reputation for vote weight
   - Should use: 0.1 (10% of normal weight) for bootstrap votes

2. **Votes on 25 items** (should be 30-40%)
   - Currently: Each agent votes on 25 items (fixed number)
   - Should be: 30-40% of total items with preference bias
   - For 80 items: 24-32 votes per agent (randomized)

3. **Timestamp randomization: 0-24 hours** (should be 0-48 hours)
   - Currently: Randomized within last 24 hours
   - Should be: Randomized within last 48 hours

4. **Agent reputation = 0** (should be 0.5)
   - Currently: Bootstrap agents created with reputation 0
   - Should be: 0.5 (real agents can always outrank)

5. **No vote source tracking**
   - Currently: No way to distinguish bootstrap vs real votes
   - Should be: `vote_source = 'bootstrap'` for all bootstrap votes

---

## Required Fixes (Critical Safeguards)

### Fix #1: Add vote_source Field
```sql
ALTER TABLE votes ADD COLUMN vote_source VARCHAR(20) DEFAULT 'real';
```

### Fix #2: Bootstrap Vote Weight = 0.1
```python
# In bootstrap-votes.py, modify vote submission:
cursor.execute(
    """
    INSERT INTO votes (agent_id, item_type, item_id, vote, vote_source, created_at)
    VALUES (%s, %s, %s, %s, 'bootstrap', %s)
    """,
    (agent_id, item_type, item_id, vote, timestamp)
)

# In reputation calculation, check for bootstrap votes:
is_bootstrap = (vote_source == 'bootstrap')
weight = 0.1 if is_bootstrap else agent_reputation_score
```

### Fix #3: Vote on 30-40% of Items (not fixed number)
```python
# For 80 total items, vote on 24-32 items (30-40%)
VOTE_PERCENTAGE_MIN = 0.30
VOTE_PERCENTAGE_MAX = 0.40

total_items = len(all_items)  # Should be 80
votes_per_agent = random.randint(
    int(total_items * VOTE_PERCENTAGE_MIN),
    int(total_items * VOTE_PERCENTAGE_MAX)
)

items_to_vote = random.sample(all_items, votes_per_agent)
```

### Fix #4: Timestamp Randomization 0-48 Hours
```python
# Change from:
# hours_ago = random.randint(0, 24)
# To:
hours_ago = random.randint(0, 48)
```

### Fix #5: Bootstrap Agent Reputation = 0.5
```python
# In create_agents():
cursor.execute(
    """
    INSERT INTO agents (id, name, type, preferences, reputation_score)
    VALUES (%s, %s, %s, %s, 0.5)
    """,
    (agent_id, request.name, request.type, request.preferences)
)
```

---

## Execution Order (Strict)

### ✅ Step 1: Reach ≥50 Tracks
- Status: ✅ COMPLETE
- Result: 80 items total (68 songs + 12 tools)
- Met requirement: 50+ minimum ✓

### 🔄 Step 2: Verify DB Constraints
- Status: ✅ VERIFIED
- Unique constraint: EXISTS ✓
- vote_source field: MISSING (need to add)
- Reputation defaults: NEEDS UPDATE

### ⏳ Step 3: Patch Bootstrap Script
- Status: ⏳ PENDING
- Fixes required:
  1. Add vote_source field to database
  2. Fix bootstrap vote weight to 0.1
  3. Change vote distribution to 30-40% of items
  4. Extend timestamp randomization to 0-48 hours
  5. Set bootstrap agent reputation to 0.5

### ⏳ Step 4: Run Bootstrap Votes
- Status: ⏳ BLOCKED (depends on Step 3)
- Safeguards must be in place before running

### ⏳ Step 5: Recompute Rankings
- Status: ⏳ BLOCKED (depends on Step 4)
- Invalidate ranking cache after bootstrap
- Recalculate weighted scores with new vote weights

---

## Recommendations

### Immediate Actions
1. **Add vote_source field to Vote model**
   ```python
   # In api/models.py, Vote class:
   vote_source = Column(String(20), default="real", nullable=False)
   ```

2. **Update bootstrap-votes.py with all 5 safeguards**
   - Vote weight = 0.1
   - Vote on 30-40% of items
   - Timestamp 0-48 hours ago
   - Agent reputation = 0.5
   - Set vote_source = 'bootstrap'

3. **Test bootstrap with small subset**
   - Before full run, test with 2-3 agents, 10-20 votes
   - Verify unique constraint working
   - Verify vote weights calculated correctly
   - Verify timestamp randomization

### After Bootstrap
1. **Monitor weighted scores**
   - Bootstrap items should NOT dominate rankings
   - New items should have chance to rank high
   - Real agents should be able to change rankings

2. **Vote source transparency**
   - Show "bootstrap votes excluded" toggle in dashboard
   - Display bootstrap vote count per item
   - Allow filtering by vote source

3. **Remove bootstrap effect when platform grows**
   - Gradually reduce bootstrap vote weight over time
   - Or exclude bootstrap votes from calculations once 100+ real votes exist

---

## Stop Condition

**Bootstrap voting is ready when:**
- ✅ 60+ tracks exist (CURRENT: 80 items ✓)
- ✅ 5+ genres represented (CURRENT: 7 genres ✓)
- ✅ Creation timestamps are randomized (CURRENT: Last 30 days ✓)
- ✅ DB uniqueness constraint confirmed (CURRENT: ✓)
- ⏳ vote_source field added (PENDING)
- ⏳ All 5 safeguards applied to bootstrap-votes.py (PENDING)

**Proceed to bootstrap voting only when ALL conditions met.**

---

**Current Status:** ✅ Content ready, ⚠️ Safeguards needed
**Next Action:** Apply 5 critical safeguards to bootstrap-votes.py
**Time Estimate:** 30 minutes to apply all fixes

---

**Report End**
