
---

## [ERR-20260220-001] cron-omission

**Logged:** 2026-02-20T21:15:00Z
**Severity:** medium
**Status:** resolved
**Category:** task-completeness

### What Happened
When Peter asked "what's planned for the next 24 hours", I only mentioned Midnight Surprise. I failed to check/mention the other 2 active cronjobs:
- GSC Daily Data Pull (09:00 CET daily)
- Photostudio TikTok Weekly Analytics (10:00 CET Mondays)

### Why It Happened
**Root cause:** I only checked OpenClaw's cron system (`cron action=list`), not the system crontab.

**Incomplete verification:** I assumed OpenClaw cron was the only scheduling mechanism.

### Impact
- Peter received incomplete information
- Risk of missing/conflicting task execution
- Undermined trust in my reporting

### How I Fixed It
1. Checked `crontab -l` to find system cronjobs
2. Found Midnight Surprise (02:00 CET daily) in system crontab
3. Reported complete picture: 3 cronjobs total

### Prevention Protocol
**Rule:** When asked about scheduled tasks/cronjobs, check BOTH:
- OpenClaw cron system: `cron action=list`
- System crontab: `crontab -l`

**Verification:** Cross-reference with SESSION-STATE.md (which has Midnight Surprise documented)

**Checklist before answering "what's scheduled":**
1. Check OpenClaw cron (`cron action=list`)
2. Check system crontab (`crontab -l`)
3. Check SESSION-STATE.md (planned tasks)
4. Cross-reference all three sources

### Metadata
- Source: user correction (Peter)
- Context: Daily planning question
- Related Files: SESSION-STATE.md, crontab, .clawdhub/crons.json
- Tags: cron, tasks, verification, completeness
- See Also: ERR-20250213-001 (previous verification error - if exists)


---

## [ERR-20260220-002] pinch-to-post-misuse

**Logged:** 2026-02-20T21:18:00Z
**Severity:** high
**Status:** active
**Category:** tool-choice, quality

### What Happened
Peter feedback: "Je bent niet goed in het opvolgen van pinch-to-post skill. Je maakt altijd custom code die niet goed werkt."

Translation: Not good at following pinch-to-post skill. Always making custom code that doesn't work properly.

### Root Cause Analysis
**Pattern:** Creating custom scripts/solutions instead of using established pinch-to-post workflows.

**Why:**
- Impulse to "build it myself" rather than use existing tools
- Not fully understanding pinch-to-post capabilities (50+ features)
- Underestimating complexity of WordPress operations
- Ego/autonomy over proven solutions

### Impact
- Wasted time on custom code that breaks
- Poor quality deliverables
- Frustration for Peter
- Ignoring established tools (P2P has tested workflows)

### Corrective Action
**Rule:** ALWAYS check pinch-to-post FIRST for ANY WordPress operation.

**Before writing ANY custom code for WordPress:**
1. Read pinch-to-post SKILL.md
2. Check: `pinch-to-post --help` or check commands
3. Search existing scripts in workspace for pinch-to-post usage
4. Only create custom code if P2P CAN'T do it

**Pinch-to-post capabilities (50+ features):**
- WordPress automation (WP-CLI, REST API)
- Content management (posts, pages, media, comments)
- Publishing workflows
- Analytics and stats
- Bulk operations
- Multi-site support
- Quality checks (health-check)
- And many more

**Location:** `/root/.openclaw/workspace/scripts/pinch-to-post.sh`

### Reference Files
- SKILL.md: `/root/.openclaw/workspace/skills/pinch-to-post/SKILL.md`
- Full features: `/root/.openclaw/workspace/agents/PINCH-TO-POST-FULL-FEATURES.md`
- Script: `/root/.openclaw/workspace/scripts/pinch-to-post.sh`

### Metadata
- Source: direct user feedback (Peter)
- Severity: High (affects quality, trust, time)
- Category: tool-misuse, quality, ego
- Related: AGENTS.md directive "ALWAYS use pinch-to-post for WordPress"
- Tags: pinch-to-post, wordpress, quality, custom-code
- See Also: ERR-20250213-002 (if exists - previous tool misuse)

