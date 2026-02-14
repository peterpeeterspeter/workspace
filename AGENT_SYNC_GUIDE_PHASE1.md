# AGENT SYNC GUIDE - Mission Control Phase 1

**Version:** 2.0 (Enhanced Coordination)
**Last updated:** 2026-02-02 18:05 UTC
**System:** Mission Control Phase 1 - Enhanced Coordination

---

## 🎯 What's New in Phase 1

### New Capabilities:
1. **@Mention System** - Agents can tag each other for attention
2. **Automated Handoffs** - Structured task transitions between agents
3. **Daily Standup** - Automated daily summary at 11 PM CET
4. **Enhanced TASKBOARD** - Better visibility and coordination

### Key Changes:
- TASKBOARD.md → TASKBOARD_ENHANCED.md (new format)
- Manual updates → Semi-automated coordination
- Siloed work → Cross-agent collaboration

---

## 📋 AGENT PROTOCOLS

### Every Agent Must:

**On Wake (Heartbeat):**
1. Check TASKBOARD_ENHANCED.md for @mentions
2. Review AGENT WORKLOAD table
3. Check HANDOFF PROTOCOL section for incoming work
4. Update your status in AGENT WORKLOAD
5. Proceed with assigned tasks or reply HEARTBEAT_OK

**When Starting Work:**
1. Read TASKBOARD_ENHANCED.md completely
2. Identify tasks in ASSIGNED or IN PROGRESS with your name
3. Check HANDOFF PROTOCOL for context
4. Read AGENT COMMUNICATION LOG for recent discussions
5. Update task status to IN PROGRESS if starting work

**When Completing Work:**
1. Update task status in TASKBOARD_ENHANCED.md
2. If ready for next agent → Add to "Handoff to:" field
3. Update your status in AGENT WORKLOAD
4. Add entry to AGENT COMMUNICATION LOG
5. Note: @mention daemon will auto-notify next agent

**When Handing Off:**
1. NEVER hand off incomplete work without noting what's pending
2. ALWAYS specify who you're handing off to
3. ALWAYS link to relevant files/deliverables
4. ALWAYS mention what dependencies are resolved
5. Use HANDOFF PROTOCOL as your guide

---

## 💬 COMMUNICATION PROTOCOLS

### @Mention System

**When to @mention:**
- Assigning a task to someone
- Asking for specific expertise
- Notifying someone of a decision affecting their work
- Requesting review or feedback

**How to @mention:**
- Use format: `@AgentName` (e.g., `@Vision`, `@Fury`)
- Add context in same line or paragraph
- System auto-notifies within 5 minutes

**Example:**
```markdown
- [ ] **SERP Analysis** → @Fury
  - Analyze keywords for Week 2 articles
  - Handoff to: @Vision (for SEO optimization)
```

### Agent Communication Log

**Purpose:** Track all important communications and decisions

**When to Log:**
- After any agent-to-agent handoff
- When making key decisions
- When blockers are identified/resolved
- When task priorities change

**Format:**
```markdown
### 2026-02-02 18:00 UTC
- @Carlottta → @Peter: "Start with Phase 1"
- @Peter → @Carlottta: "Approved"
- @Vision → @Fury: "Week 2 briefs ready, need SERP analysis"
```

---

## 🔄 HANDOFF PROTOCOL

### Standard Handoff Flow:

```
@AgentA (completes work) → updates TASKBOARD → adds "Handoff to: @AgentB"
→ @mention daemon notifies @AgentB → @AgentB acknowledges → starts work
```

### Common Handoff Patterns:

**Research → SEO:**
```
@Fury (Research) → @Vision (SEO)
- Fury provides: Keyword data, competitor analysis, search volume
- Vision receives: SERP analysis, SEO recommendations
```

**SEO → Drafting:**
```
@Vision (SEO) → @Loki (Content Writer)
- Vision provides: Optimized brief, keywords, schema
- Loki receives: Writing guidelines, SEO requirements
```

**Drafting → Review:**
```
@Loki (Writer) → @Vision (Reviewer)
- Loki provides: Draft article, word count, sources
- Vision receives: Content for quality/SEO review
```

**Review → Publishing:**
```
@Vision (Reviewer) → @Carlottta (Publisher)
- Vision provides: Approved content, metadata
- Carlottta receives: Final draft for WordPress
```

### Handoff Checklist:

**Before Handing Off:**
- [ ] Work is complete or clearly marked as partial
- [ ] All relevant files are linked
- [ ] Dependencies are documented
- [ ] Next agent is specified in "Handoff to:"
- [ ] Status is updated in TASKBOARD

**After Receiving Handoff:**
- [ ] Acknowledge receipt (update TASKBOARD)
- [ ] Review incoming work and dependencies
- [ ] Ask questions if context unclear
- [ ] Update task status to IN PROGRESS
- [ ] Log communication in AGENT COMMUNICATION LOG

---

## 📊 TASKBOARD STRUCTURE

### Sections:

**📥 INBOX** - New, unassigned tasks
**📋 ASSIGNED** - Has owner, awaiting start
**🔄 IN PROGRESS** - Active work being done
**✅ REVIEW** - Done, needs approval
**✅ DONE** - Completed
**🚫 BLOCKED** - Stuck, waiting for something

### Task Fields:

Each task includes:
- **Title** - What needs to be done
- **Owner** - `@AgentName` responsible
- **Status** - Current state
- **Priority** - HIGH / MEDIUM / LOW
- **Dependencies** - What must be done first
- **Handoff to** - Who gets it next (with ✅ when complete)
- **File** - Link to detailed brief/document
- **Created/Updated** - Timestamps

---

## 🔔 NOTIFICATION SYSTEM

### Auto-Notify Triggers:

You'll be automatically notified when:
- A task is assigned to you
- Someone @mentions you
- Work is handed off to you
- A task you're subscribed to is updated

### Notification Routing:

- `@Vision` → SEO specialist session
- `@Fury` → Research specialist session
- `@Quill` → Marketing specialist session
- `@Peter` → Direct Telegram (main session)
- `@Carlottta` → Coordinator session

### Checking Notifications:

During heartbeat, check for:
1. @mentions in TASKBOARD_ENHANCED.md
2. Tasks in ASSIGNED with your name
3. Handoffs in IN PROGRESS addressed to you

---

## 📈 DAILY STANDUP

### What It Is:

Automated daily summary at 11 PM CET (10 PM UTC) that includes:
- ✅ Completed tasks today
- 🔄 In-progress work
- 🚫 Blocked items
- 📊 Metrics (articles published, % to goal)

### Why It Matters:

- Visibility into what's getting done
- Accountability for assigned tasks
- Early warning on blockers
- Progress tracking toward goals

### Access:

Standup is automatically:
- Sent to Telegram (main session)
- Logged in `memory/YYYY-MM-DD.md`
- Added to AGENT COMMUNICATION LOG

---

## 🎯 AGENT-SPECIFIC GUIDELINES

### @Vision (SEO/Content)

**Your Responsibilities:**
- SEO analysis and optimization
- Keyword research and targeting
- Content quality review
- Schema markup preparation
- Affiliate link integration

**Handoffs You Make:**
- → @Loki: Optimized briefs ready for drafting
- → @Fury: Need SERP data for new keywords

**Handoffs You Receive:**
- ← @Fury: SERP analysis for SEO strategy
- ← @Loki: Drafts for review

---

### @Fury (Research)

**Your Responsibilities:**
- SERP analysis and competitor research
- Keyword data (volume, CPC, difficulty)
- Market research and customer insights
- Source verification and citation

**Handoffs You Make:**
- → @Vision: SEO-ready keyword research
- → @Quill: Market insights for campaigns

**Handoffs You Receive:**
- ← @Vision: Requests for SERP analysis
- ← @Peter: Strategic research questions

---

### @Quill (Marketing)

**Your Responsibilities:**
- Social media strategy and content
- Promotion planning
- Engagement and growth tactics
- Brand voice consistency

**Handoffs You Make:**
- → @Vision: Content briefs informed by market needs
- → @Fury: Requests for audience research

**Handoffs You Receive:**
- ← @Vision: Published content to promote
- ← @Fury: Audience insights for targeting

---

### @Peter (Human)

**Your Role:**
- Strategic direction
- Approval for key decisions
- Unblocker for stuck tasks
- Quality standards

**When You'll Be @Mentioned:**
- Approval needed (cleanup, major changes)
- Blockers requiring human intervention
- Key decisions (go/no-go on projects)
- Resource allocation (prioritization)

---

## 🛠️ TECHNICAL NOTES

### File Structure:

```
/root/.openclaw/workspace/
├── TASKBOARD_ENHANCED.md       # Main coordination board
├── AGENT_SYNC_GUIDE.md          # This file
├── scripts/
│   ├── mention-daemon.sh        # @mention notification daemon
│   ├── daily-standup.py         # Daily standup generator
│   └── install-phase1-crons.sh  # Cron installation
├── logs/
│   ├── mentions.log             # @mention activity log
│   ├── mention-cron.log         # Daemon execution log
│   └── standup-cron.log         # Standup execution log
└── memory/
    ├── agents/                  # Agent-specific outputs
    └── YYYY-MM-DD.md            # Daily logs + standups
```

### Cron Jobs:

```bash
# @Mention Daemon - Every 5 minutes
*/5 * * * * /root/.openclaw/workspace/scripts/mention-daemon.sh

# Daily Standup - 11 PM CET (10 PM UTC)
0 22 * * * /usr/bin/python3 /root/.openclaw/workspace/scripts/daily-standup.py
```

### Session Keys:

- Vision: `agent:main:cron:*`
- Fury: `agent:main:cron:*`
- Quill: `agent:main:cron:*`
- Peter/Carlottta: `agent:main:main`

---

## 📝 CHECKLISTS

### On Every Wake:

- [ ] Read TASKBOARD_ENHANCED.md
- [ ] Check for @mentions to you
- [ ] Review AGENT WORKLOAD
- [ ] Check HANDOFF PROTOCOL for incoming work
- [ ] Update your status if working
- [ ] Proceed with tasks or HEARTBEAT_OK

### When Starting Work:

- [ ] Task is in ASSIGNED or IN PROGRESS with your name
- [ ] Dependencies are met
- [ ] You have necessary context
- [ ] Update status to IN PROGRESS
- [ ] Log start in AGENT COMMUNICATION LOG

### When Completing Work:

- [ ] Work meets quality standards
- [ ] Files are saved and linked
- [ ] Task status updated
- [ ] Handoff to next agent specified
- [ ] Your status updated in AGENT WORKLOAD

---

## 🚀 BEST PRACTICES

### Coordination:
- Over-communicate context, not under
- Link everything (files, decisions, blockers)
- Update status early and often
- Use @mentions sparingly but effectively

### Handoffs:
- Never leave the next agent guessing
- Document what you tried and what worked
- Flag issues before handing off
- Celebrate wins in AGENT COMMUNICATION LOG

### Quality:
- Your work = your reputation
- If uncertain, ask before proceeding
- Test assumptions before delivering
- Learn from feedback

---

## 🆘 TROUBLESHOOTING

### @Mentions Not Working:
1. Check if mention-daemon.sh is running: `ps aux | grep mention-daemon`
2. Check logs: `tail -f /root/.openclaw/workspace/logs/mentions.log`
3. Verify TASKBOARD_ENHANCED.md has correct format

### Daily Standup Missing:
1. Check if cron is installed: `crontab -l | grep daily-standup`
2. Check logs: `tail -f /root/.openclaw/workspace/logs/standup-cron.log`
3. Verify Python script is executable

### Handoffs Confusing:
1. Read HANDOFF PROTOCOL section carefully
2. Check AGENT COMMUNICATION LOG for context
3. Ask questions via @mention or main session

---

**This guide is living documentation. Update it as protocols evolve.**

*Last updated by: Carlottta*
*Version: 2.0 (Phase 1 Enhanced Coordination)*
