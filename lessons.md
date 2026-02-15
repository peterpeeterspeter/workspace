# Lessons Learned - Mistakes Documented Once, Never Repeated

**Purpose:** Every mistake documented here prevents it from happening again.
**Updated:** 2026-02-15 00:55 UTC

---

## Memory & Context Management

**Lesson 1: Single MEMORY.md causes context bloat**
- **Problem:** Dumping everything into MEMORY.md makes agent load slow, confused
- **Solution:** Split into focused files (active-tasks.md, lessons.md, projects.md, daily logs)
- **Result:** Faster restart, clearer context, cheaper tokens

**Lesson 2: Daily logs older than 7 days bloat context**
- **Problem:** Keeping all daily logs forever wastes tokens
- **Solution:** Delete daily logs after 7 days (keep insights in lessons.md)
- **Result:** Lean memory, agent loads only relevant context

**Lesson 3: Sessions over 2MB slow down agent**
- **Problem:** Large session files make agent confused and expensive
- **Solution:** Auto-archive sessions >2MB to separate archive folder
- **Result:** Agent stays fast, context remains clear

---

## Agent Coordination

**Lesson 4: Sub-agent results taken for granted**
- **Problem:** Announcing sub-agent work without verification causes 80% of quality issues
- **Solution:** Every sub-agent MUST validate own work; coordinator verifies before announcing
- **Result:** Quality issues dropped from frequent to near-zero

**Lesson 5: Wrong skill selection ~20% of time**
- **Problem:** Agent picks wrong skill because description lacks use cases
- **Solution:** Add "Use when / Don't use when" to every skill description
- **Result:** Correct skill selection first time, less wasted API calls

---

## Model Routing

**Lesson 6: Not every task needs strongest model**
- **Problem:** Using expensive model for file reading wastes money
- **Solution:** Route by task type:
  - File reading, reminders, internal work → fast/cheap model
  - External web content (articles, tweets) → strongest model only
  - Coding tasks → mid-tier with extended thinking
- **Result:** Same quality, 30% lower cost

**Lesson 7: Weaker models vulnerable to prompt injection**
- **Problem:** Fast models on hostile websites can be tricked
- **Solution:** Use strongest model for external content, skip fast models for web scraping
- **Result:** No security issues, better content quality

---

## Heartbeat & Scheduling

**Lesson 8: Heartbeats for quick checks, cron for real work**
- **Problem:** Using heartbeat for batch work wastes tokens and slows response
- **Solution:** Heartbeat = quick health check; cron jobs = actual work
- **Result:** Faster heartbeat, proper work batching

**Lesson 9: Cron jobs need isolated sessions**
- **Problem:** Cron in main session bleeds context, confuses agent
- **Solution:** Each cron runs in isolated session (own context)
- **Result:** No context bleed, focused work

**Lesson 10: HEARTBEAT.md too long → agent skips it**
- **Problem:** Long HEARTBEAT.md makes agent not follow it properly
- **Solution:** Keep HEARTBEAT.md under 20 lines, focus on critical checks only
- **Result:** Heartbeats actually followed, not ignored

---

## Crash Recovery

**Lesson 11: Agent crashes and forgets context**
- **Problem:** Session restart → agent asks "what was I doing?"
- **Solution:** active-tasks.md read FIRST on restart, shows what agent was doing
- **Result:** Zero downtime, agent resumes autonomously

**Lesson 12: Crash recovery not documented**
- **Problem:** Agent didn't know about active-tasks.md, would be confused
- **Solution:** Add to AGENTS.md: "On startup: read active-tasks.md FIRST. Resume autonomously."
- **Result:** Every agent knows crash recovery procedure

---

## Work Quality

**Lesson 13: Generic AI-slop output from personality-less agents**
- **Problem:** Default agent sounds like corporate chatbot, misses edge cases
- **Solution:** Write SOUL.md with personality, communication style, boundaries, opinions allowed
- **Result:** Better engagement, catches edge cases, more natural output

**Lesson 14: Announcing work before verification**
- **Problem:** Telling user "done" without checking causes quality issues
- **Solution:** Sub-agents validate; coordinator verifies before announcing
- **Result:** Quality issues near-zero

---

## GTM & Project Management

**Lesson 15: Research without demand validation**
- **Problem:** Building product without checking if people want it (aidescribe search volume: 10/month)
- **Solution:** Always validate demand (DataForSEO, last30days, direct outreach) before building
- **Result:** Better product-market fit, less wasted effort

---

## Update Policy

**When to add lessons:**
- Immediately after mistake (don't wait)
- Once per mistake (not repeated entries)
- Specific and actionable (not vague)

**Review schedule:**
- Self-review every 4 hours (self-review.md)
- Weekly: Consolidate into patterns
- Monthly: Archive old lessons (keep critical ones)

---

*Last Updated: 2026-02-15 00:55 UTC*
*Total Lessons: 15 documented*
