# Multi-Agent System Plan for Crash Casino Affiliate Business

**Based on:** Mission Control architecture by @pbteja1998
**Adapted for:** Crash casino affiliate sites (4 sites)
**Coordinator:** Carlottta (already active)

---

## Executive Summary

Build a team of AI agents that work together like a real team to manage your crash casino affiliate business. Each agent has a specialized role, shared memory, coordinated workflows, and accountability through task tracking.

**Start Small:** 2-3 agents, scale to 6-8 over time
**Timeline:** Phase 1 (1 week), Phase 2 (2-3 weeks), Phase 3 (ongoing)

---

## Phase 1: Foundation (Week 1) - START HERE

### Agent 1: Carlottta (Coordinator) ✅ Already Active
- **Session Key:** `agent:coordinator:main`
- **Role:** Squad lead, delegation, monitoring, communication
- **Tools:** pinch-to-post (full access), memory system, file access
- **Status:** Active, has elite memory enabled

### Agent 2: Vision (SEO & Content Strategist) - NEW
**Session Key:** `agent:seo:main`

**Responsibilities:**
- Keyword research for crash gambling niche
- Content calendar planning
- SEO audit and optimization
- Competitor analysis
- Brief creation for content writers

**SOUL.md Personality:**
```markdown
# Vision - SEO & Content Strategist

## Who You Are
You are Vision, the SEO strategist for crash casino affiliate sites. You think in keywords, search intent, and topical authority.

## Your Expertise
- Keyword research (volume, difficulty, intent)
- Content gap analysis
- On-page SEO optimization
- Competitor keyword targeting
- Content brief creation

## Your Voice
Data-driven. Strategic. Specific. Cite sources. Provide confidence levels.

## What You Care About
- Search volume over guesswork
- User intent matching
- Topical authority building
- ROI on content investment
```

**Tools:**
- web_search (Brave Search API)
- web_fetch (page analysis)
- SEO tools (via pinch-to-post)
- Memory system (recall past research)

**Heartbeat Schedule:** Every 15 minutes at :02 past the hour

**Cron Setup:**
```bash
openclaw cron add \
  --name "vision-seo-heartbeat" \
  --cron "2,17,32,47 * * * *" \
  --session "isolated" \
  --message "Read HEARTBEAT.md and follow it. Check for SEO tasks, keyword research requests, content calendar updates."
```

### Agent 3: Fury (Technical & Research Analyst) - NEW
**Session Key:** `agent:research:main`

**Responsibilities:**
- Competitor research (casino offerings, bonuses, features)
- Technical SEO audits
- Affiliate program research
- Market trend analysis
- Data verification and fact-checking

**SOUL.md Personality:**
```markdown
# Fury - Research & Technical Analyst

## Who You Are
You are Fury, the researcher who always provides receipts. Every claim comes with sources, confidence levels, and verification.

## Your Expertise
- Deep competitive research
- Casino review verification
- Affiliate program analysis
- Technical SEO audits
- Data collection and validation

## Your Voice
Evidence-based. Skeptical. Thorough. "According to [source]" not "I think." Cite everything.

## What You Care About
- Accuracy over speed
- Primary sources over secondary
- Verification before publication
- Documenting methodology
```

**Tools:**
- web_search, web_fetch
- image analysis (casino screenshots)
- Memory system (research database)
- Browser automation (via browser tool)

**Heartbeat Schedule:** Every 15 minutes at :04 past the hour

---

## Shared Infrastructure

### 1. Shared Workspace
```
/root/.openclaw/workspace/
├── SESSION-STATE.md          # Active working memory (WAL protocol)
├── MEMORY.md                 # Long-term curated memory
├── AGENTS.md                 # All agents read this
├── HEARTBEAT.md              # Heartbeat instructions
├── tasks/                    # Task tracking (use simple JSON to start)
│   ├── inbox.json
│   ├── in-progress.json
│   ├── review.json
│   └── done.json
├── research/                 # Shared research database
│   ├── competitors/
│   ├── keywords/
│   └── affiliate-programs/
├── content-calendar.md       # Publishing schedule
└── memory/
    ├── 2026-02-04.md
    └── ...
```

### 2. Task System (Phase 1 - Simple JSON Files)

**Before building full Mission Control UI, start with file-based tracking:**

**tasks/inbox.json**
```json
[
  {
    "id": "task-2026-02-04-001",
    "title": "Research BC.Game alternative for crash games",
    "description": "Find crypto casinos that offer crash games similar to BC.Game",
    "status": "inbox",
    "assignee": "agent:research:main",
    "priority": "high",
    "created": "2026-02-04T16:00:00Z",
    "tags": ["research", "competitor"]
  }
]
```

**Carlottta can manage these via pinch-to-post or direct file operations.**

### 3. Memory System (Already Enabled) ✅
- SESSION-STATE.md - Hot RAM (active context)
- MEMORY.md - Long-term curated wisdom
- memory/YYYY-MM-DD.md - Daily logs
- WAL protocol active (write BEFORE responding)

### 4. Communication Methods

**Direct Session Messaging:**
```bash
# Carlottta can message Vision
sessions_send --session "agent:seo:main" --message "New keyword opportunity: crash game strategies"

# Carlottta can message Fury
sessions_send --session "agent:research:main" --message "Need competitor analysis on Cybet vs Stake"
```

**Task Comments (File-based for Phase 1):**
```json
{
  "taskId": "task-2026-02-04-001",
  "comments": [
    {
      "agent": "agent:research:main",
      "message": "Found 3 alternatives: Cybet, Betzrd, TrustDice",
      "timestamp": "2026-02-04T16:30:00Z"
    }
  ]
}
```

---

## Phase 2: Expand & Optimize (Weeks 2-3)

### Agent 4: Loki (Content Writer) - NEW
**Session Key:** `agent:writer:main`

**Responsibilities:**
- Write crash gambling articles
- Create casino reviews
- Draft comparison pages
- Follow SEO briefs from Vision
- Use research from Fury

**SOUL.md Excerpt:**
```markdown
## Who You Are
You are Loki, a content writer who crafts words with precision. Pro-Oxford comma. Anti-passive voice.

## Your Voice
Engaging. Clear. Specific. Every sentence earns its place. No fluff.
```

**Tools:** pinch-to-post (publish), memory system, web_search (verification)

**Heartbeat:** :06 past every 15 minutes

### Agent 5: Quill (Affiliate & Partnership Manager) - NEW
**Session Key:** `agent:affiliate:main`

**Responsibilities:**
- Monitor affiliate program performance
- Research new affiliate opportunities
- Verify affiliate links are working
- Track EPC and conversion rates
- Negotiate better deals (prepare scripts for Peter)

**Tools:** pinch-to-post (link audits), memory system, web research

**Heartbeat:** :08 past every 15 minutes

### Upgrade Task System

**Move from JSON files to proper database:**

**Option A: Convex (recommended - matches Mission Control)**
- Real-time updates
- TypeScript-native
- Generous free tier
- Full Mission Control replica

**Option B: Notion API**
- You already use Notion
- Good UI out of the box
- Integrates with existing workflow

**Option C: Airtable**
- Easy to set up
- Good for multi-agent coordination
- Affordable

### Implement Notification System

**@Mentions:**
- Agents read tasks/research files every heartbeat
- When @Vision appears, Vision takes action
- Simple text-based parsing

**Thread Subscriptions:**
- Track who commented on what task
- Add them to notification list for that task
- File-based: `tasks/task-id/subscribers.json`

---

## Phase 3: Advanced Features (Ongoing)

### Agent 6: Wanda (Designer) - NEW
**Session Key:** `agent:designer:main`

**Responsibilities:**
- Create featured images for articles
- Design comparison graphics
- Infographic creation
- Brand assets for social media

**Tools:** DALL-E/Midjourney integration, image editing

### Agent 7: Pepper (Social Media Manager) - NEW
**Session Key:** `agent:social:main`

**Responsibilities:**
- Distribute content across social platforms
- Engage with community
- Monitor brand mentions
- Build audience

**Tools:** social media APIs, pinch-to-post (for WordPress → social)

### Daily Standup Automation

**Cron Job: 11:30 PM CET daily**
```bash
openclaw cron add \
  --name "daily-standup" \
  --cron "30 23 * * *" \
  --session "isolated" \
  --message "Read all agent daily logs. Check tasks files. Compile standup. Send to Peter via Telegram."
```

**Standup Format:**
```markdown
📊 DAILY STANDUP — [Date]

✅ COMPLETED TODAY
• Agent: [Task completed]
• Agent: [Task completed]

🔄 IN PROGRESS
• Agent: [Task] ([Status])

🚫 BLOCKED
• Agent: [Task] - [Reason]

📝 KEY DECISIONS
• [Decision made]

💡 INSIGHTS
• [Interesting finding]
```

---

## Agent Coordination Workflows

### Workflow 1: Content Production Pipeline

**Trigger:** New keyword opportunity identified

1. **Vision** (SEO Strategist)
   - Research keyword (volume, difficulty, intent)
   - Create content brief
   - Assign to writer

2. **Fury** (Research Analyst)
   - Research competitors targeting this keyword
   - Gather data points, stats, quotes
   - Verify casino information

3. **Loki** (Content Writer)
   - Write article following Vision's brief
   - Incorporate Fury's research
   - Add affiliate links (via pinch-to-post)

4. **Carlottta** (Coordinator)
   - Quality check (health-check via pinch-to-post)
   - Publish when ready (score 80+)
   - Update content calendar

**Time:** 2-3 days from keyword to published article

### Workflow 2: Affiliate Link Monitoring

**Trigger:** Weekly audit needed

1. **Quill** (Affiliate Manager)
   - Run affiliate audit via pinch-to-post
   - Check for broken links
   - Monitor EPC performance

2. **Fury** (Research Analyst)
   - Research new affiliate programs
   - Compare commission rates
   - Prepare recommendations

3. **Carlottta** (Coordinator)
   - Review findings
   - Approve changes
   - Update via pinch-to-post

### Workflow 3: Competitor Monitoring

**Trigger:** New competitor identified

1. **Vision** (SEO Strategist)
   - Identify competitor keywords
   - Analyze their content strategy
   - Find gaps we can exploit

2. **Fury** (Research Analyst)
   - Deep dive on competitor offerings
   - Test competitor products
   - Document strengths/weaknesses

3. **Carlottta** (Coordinator)
   - Review intelligence
   - Update strategy
   - Assign content tasks

---

## Implementation Steps (This Week)

### Day 1: Setup Vision & Fury
1. Create SOUL.md for Vision (SEO strategist)
2. Create SOUL.md for Fury (Research analyst)
3. Set up heartbeat crons for both
4. Create shared workspace structure
5. Test session messaging between agents

### Day 2: First Tasks
1. Assign Vision: "Keyword research for crash game strategies"
2. Assign Fury: "Competitor analysis on Top 5 crash casinos"
3. Carlottta monitors coordination

### Day 3-5: Iterate & Improve
1. Review agent outputs
2. Refine SOUL.md personalities
3. Adjust heartbeat schedules
4. Document lessons learned
5. Plan Phase 2 expansion

---

## Success Metrics

**Week 1 Target:**
- 2 new agents active (Vision, Fury)
- 5 tasks completed by agent team
- Daily heartbeat system working
- Memory system actively used

**Week 2-3 Target:**
- 5 total agents active (add Loki, Quill)
- Task tracking system upgraded (Convex or Notion)
- Notification system working
- 20+ tasks completed by agents

**Month 1 Target:**
- 7+ agents active
- Full Mission Control replica (if desired)
- Content production pipeline running
- 50+ tasks completed autonomously

---

## Cost Optimization

**Use Cheaper Models for Routine Work:**
- Heartbeats: Use faster/cheaper model (GLM-4.7 is already efficient)
- Research: Can use mid-tier model
- Creative writing: Use best model (Claude/GPT-4)

**Stagger Heartbeats:**
- Don't wake all agents at once
- Spread across 15-minute window
- Reduces API costs significantly

---

## Key Differences from Mission Control

**What We're Doing Differently:**

1. **Start Smaller:** 2-3 agents first, not 10
2. **Use Pinch-to-Post:** Leverage existing WordPress automation
3. **Simpler Task System:** Start with JSON files, upgrade to Convex later
4. **Elite Memory:** Already have 6-layer memory system
5. **No Custom UI Initially:** Use Telegram + file-based tracking
6. **Focus on ROI:** Every agent must drive revenue or save time

---

## Required Tools & Setup

**Already Have:**
- ✅ OpenClaw installed
- ✅ pinch-to-post skill active
- ✅ Elite memory system enabled
- ✅ Carlottta (coordinator) active
- ✅ Telegram integration

**Need to Add:**
- SOUL.md files for each new agent
- AGENTS.md (operational manual)
- HEARTBEAT.md (heartbeat instructions)
- Task tracking system (start with JSON files)
- Heartbeat crons for each agent

**Optional (Phase 2+):**
- Convex deployment (for real-time task system)
- Notion/Airtable integration
- Custom Mission Control UI (React frontend)

---

## Next Steps

**Immediate (Today):**
1. Create Vision's SOUL.md
2. Create Fury's SOUL.md
3. Set up first heartbeat cron
4. Test agent coordination

**This Week:**
1. Launch Vision and Fury
2. Complete 5 test tasks
3. Document what works
4. Plan Loki and Quill setup

**Next 2 Weeks:**
1. Add Loki (writer) and Quill (affiliate)
2. Upgrade task system
3. Implement notifications
4. Scale content production

---

**The Goal:** Build a team of AI agents that runs your crash casino affiliate business while you focus on strategy and growth.

**Starting Point:** 3 agents (Carlottta + Vision + Fury)
**End State:** 7+ agents working autonomously like a real team

---

*Plan created: 2026-02-04*
*Based on Mission Control architecture by @pbteja1998*
*Adapted for crash casino affiliate business*
