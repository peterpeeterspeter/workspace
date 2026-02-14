# Elite Longterm Memory - Setup Guide

**Status:** ✅ Installed and Ready

**Date:** 2026-02-04

---

## What's Enabled

### Layer 1: HOT RAM ✅ ACTIVE
- **File:** `/root/.openclaw/workspace/SESSION-STATE.md`
- **Purpose:** Active working memory that survives restarts
- **Usage:** Update BEFORE responding to important user inputs

### Layer 2: WARM STORE (LanceDB) - Ready to enable
- **Purpose:** Semantic vector search with auto-recall
- **Requires:** OPENAI_API_KEY (✅ already set)
- **Status:** Dependencies installed, ready to configure

### Layer 3: COLD STORE (Git-Notes) - Optional
- **Purpose:** Structured knowledge graph
- **Status:** Available but not required for basic use

### Layer 4: CURATED ARCHIVE ✅ ACTIVE
- **Files:** 
  - `MEMORY.md` - Long-term curated memory
  - `memory/2026-02-04.md` - Daily logs
- **Purpose:** Human-readable long-term storage

### Layer 5: CLOUD BACKUP - Optional
- **Purpose:** Cross-device sync via SuperMemory
- **Status:** Not configured (optional)

### Layer 6: AUTO-EXTRACTION - Optional
- **Purpose:** Automatic fact extraction
- **Status:** Not configured (optional)

---

## Current Setup (What Works Now)

### 1. SESSION-STATE.md (Hot RAM)
✅ Already created and populated with current context

**Usage:**
- Read on session start: "What was I working on?"
- Write WAL protocol: Update BEFORE responding to important inputs
- Contains: Current task, key context, decisions, pending actions

**Example Update:**
```markdown
## Current Task
Adding featured images to posts

## Recent Decision
User prefers batch operations (10 posts at a time)
```

### 2. MEMORY.md + Daily Logs (Curated Archive)
✅ Already created with today's work

**Structure:**
```
/root/.openclaw/workspace/
├── MEMORY.md              # Curated long-term (the good stuff)
├── SESSION-STATE.md       # Hot RAM (active context)
└── memory/
    ├── 2026-02-04.md      # Daily work log
    └── README.md          # This file
```

**Usage:**
- Daily logs: Record what happened each day
- MEMORY.md: Extract important lessons, decisions, patterns
- Archive monthly: Consolidate daily logs into summaries

---

## How to Use (Daily Workflow)

### Session Start
1. **Read SESSION-STATE.md** → "What was I working on?"
2. **Read memory/YYYY-MM-DD.md** → "What happened yesterday?"
3. **Read MEMORY.md** (if needed) → "What are the long-term patterns?"

### During Session
1. **User gives preference/decision?**
   - Write to SESSION-STATE.md
   - Update memory/YYYY-MM-DD.md with key details

2. **Major accomplishment?**
   - Update SESSION-STATE.md
   - Add to daily log
   - Extract to MEMORY.md if significant

3. **Lesson learned?**
   - Document in daily log
   - Add to MEMORY.md lessons section

### Session End
1. **Update SESSION-STATE.md** with current state
2. **Update daily log** with what was accomplished
3. **Archive important items** to MEMORY.md

---

## WAL Protocol (Critical)

**Write-Ahead Log:** Write BEFORE responding, not after.

| Trigger | Action |
|---------|--------|
| User states preference | Write to SESSION-STATE.md → then respond |
| User makes decision | Write to SESSION-STATE.md → then respond |
| User gives deadline | Write to SESSION-STATE.md → then respond |
| User corrects you | Write to SESSION-STATE.md → then respond |

**Why?** If you crash/compact before saving, context is lost. WAL ensures durability.

---

## Next Steps (Optional Enhancements)

### Enable Semantic Search (LanceDB)
**Benefit:** Auto-recall relevant context without manual searching

**Setup:** 
```bash
# Add to openclaw.json (already done via skill install)
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  }
}
```

**Usage:** Happens automatically via `memory_recall` before responses

### Enable Git-Notes (Knowledge Graph)
**Benefit:** Branch-aware structured memory

**Setup:**
```bash
cd /root/.openclaw
git init  # if not already
/root/.openclaw/workspace/skills/elite-longterm-memory/bin/elite-memory.js init
```

---

## Quick Reference

**Read current context:**
```bash
cat /root/.openclaw/workspace/SESSION-STATE.md
```

**Read today's log:**
```bash
cat /root/.openclaw/workspace/memory/2026-02-04.md
```

**Read long-term memory:**
```bash
cat /root/.openclaw/workspace/MEMORY.md
```

**Update SESSION-STATE.md:**
```markdown
## Current Task
[What you're working on]

## Recent Decision
[User preference or choice made]
```

**Update daily log:**
```markdown
### 2026-02-04 15:00
- Completed: Affiliate link fixes (114 posts)
- Decision: Always use pinch-to-post skill
```

---

## Success Metrics

**Before:**
- Context lost on compaction
- No working memory
- Manual memory search required

**After:**
- ✅ SESSION-STATE.md survives compaction
- ✅ Daily logs track all work
- ✅ MEMORY.md holds long-term wisdom
- ✅ WAL protocol prevents data loss

---

**Current Status:** Basic 4-layer system active (Layers 1, 2, 3, 4)
**Recommendation:** Start using this for a week, then add LanceDB if needed

---

*For advanced features (LanceDB, Git-Notes, Mem0), see SKILL.md in elite-longterm-memory folder*
