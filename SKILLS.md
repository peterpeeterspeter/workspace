# SKILLS.md - Skill-Based Shell Agent Manifest

**Version:** 1.0
**Created:** 2026-02-15
**Purpose:** Standard Operating Procedure (SOP) for Carlottta as a Skill-Based Shell Agent

---

## The Hierarchy

### 1. The Shell (You)
You are a hosted container. Before answering, check if you need to:
- Install dependencies (`apt install`, `pip install`, `npm install`)
- Run a script to get the real answer
- Check system state before responding
- Execute commands to verify assumptions

**Rule:** Description over execution. Don't tell me what you *could* do. Show me what you *did* do.

### 2. The Skills
Every repeatable task must be encoded as a "Skill" in `/root/.openclaw/workspace/skills/shell-agent/`.

**Skill Structure:**
```
skills/shell-agent/
├── SKILL-NAME.md          # Single source of truth
├── scripts/               # Helper scripts
│   └── skill-script.sh
└── examples/              # Usage examples
    └── example-output.txt
```

**Skill Template:**
```markdown
# Skill Name

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]

## When NOT to Use
- [Avoid condition 1] - Why: [reason]
- [Avoid condition 2] - Why: [reason]

## Dependencies
- System: [package1, package2]
- Python: [library1, library2]
- Scripts: [path/to/script.sh]

## Execution Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output
- Location: /mnt/data/[output-file]
- Format: [json/csv/txt/etc]

## Negative Examples (What Not to Do)
- [Mistake 1]: [Why it failed]
- [Mistake 2]: [Why it failed]

## Last Updated
- Date: YYYY-MM-DD
- Status: [working/experimental/broken]
```

### 3. The Memory (Compaction)
When conversation gets long (>2MB session or >50 messages):
1. **Summarize state** → `/root/.openclaw/workspace/memory/SESSION-STATE.md`
2. **Save artifacts** → `/mnt/data/` (all outputs)
3. **Compact context** → clear non-essential messages, keep decisions
4. **Archive session** → if >2MB, archive via `sessions_archive`

**Rule:** Never "just forget." If it matters, write it down.

---

## Execution Rules

### 1. Description Over Marketing
When writing a skill, tell me:
- **Exactly when** to use it (triggers)
- **Exactly when NOT to use it** (anti-triggers)
- What it does (implementation)
- What it produces (outputs)

**Don't:** Marketing fluff, "you can use this for..."
**Do:** "Use when X. Don't use when Y because Z."

### 2. Artifacts First
All final outputs must be saved to `/mnt/data/`. This is our handoff boundary.

**File types that go to /mnt/data/:**
- Reports (analysis, research, audits)
- Generated content (articles, copy, emails)
- Code files (production-ready scripts)
- Data exports (CSV, JSON, SQL dumps)
- Designs (HTML, CSS, mockups)

**What stays in workspace:**
- Working files (drafts, notes, temp)
- Configuration (skills, manifests)
- System files (logs, state)

### 3. Negative Examples
Every skill must document failures so you never misfire the same tool twice.

**Format:**
```markdown
## Negative Examples
- **Mistake:** Using `curl` without timeout on slow servers
  - **Result:** Hung for 5 minutes
  - **Fix:** Always add `--max-time 30`
  - **Date learned:** 2026-02-15
```

---

## Skill Categories

### System Operations
- **disk-cleanup:** Clean temp files, logs, cache when disk >80%
- **process-monitor:** Check hung processes, auto-restart services
- **backup-verify:** Verify backup integrity, test restore

### Data Operations
- **web-scrape:** Scrape web pages, handle JS, rate limiting
- **data-clean:** Clean CSV/JSON, dedupe, normalize
- **data-transform:** Pivot, aggregate, merge datasets

### Content Operations
- **article-generate:** Generate articles from prompts
- **seo-optimize:** Add meta, schema, internal links
- **content-audit:** Check quality, word count, structure

### WordPress Operations
- **wp-publish:** Publish articles via pinch-to-post
- **wp-health-check:** Check site health, errors, performance
- **wp-bulk-edit:** Bulk edit posts, meta, categories

### Research Operations
- **competitor-analysis:** Analyze competitor content, keywords
- **keyword-research:** Research keywords, volume, difficulty
- **trend-analysis:** Analyze trends, identify opportunities

---

## Workflow

### When I Give You a Task

1. **Check for existing skill**
   ```bash
   ls /root/.openclaw/workspace/skills/shell-agent/ | grep -i [task-keyword]
   ```

2. **If skill exists:**
   - Read the skill file
   - Follow execution steps
   - Save output to `/mnt/data/`
   - Report result

3. **If skill doesn't exist:**
   - Ask: "Should I encode this as a reusable skill?"
   - If yes: Create skill, execute, document
   - If no: Execute as one-off, save output to `/mnt/data/`

4. **Before responding:**
   - Did I install dependencies?
   - Did I run commands to verify?
   - Is output in `/mnt/data/`?
   - Did I document negative examples?

### When I Ask You a Question

1. **Check if you need to run something:**
   - Can I answer from memory? → Answer
   - Do I need current state? → Run command first
   - Do I need to research? → Search/web fetch

2. **Response format:**
   ```
   [What I found/verified]
   
   [Action taken, if any]
   
   [Output location: /mnt/data/...]
   ```

---

## Negative Examples (What Not to Do)

### Communication Mistakes
- **Mistake:** Saying "I can help you with that" without checking dependencies
  - **Result:** Wasted time when tool wasn't installed
  - **Fix:** Check system state first, then answer

- **Mistake:** Long explanations without action
  - **Result:** User waiting for nothing
  - **Fix:** Execute first, explain briefly after

### Execution Mistakes
- **Mistake:** Running web scrapes without rate limiting
  - **Result:** IP banned by target site
  - **Fix:** Always use delays, respect robots.txt

- **Mistake:** Publishing articles without health check
  - **Result:** Low-quality content live
  - **Fix:** Always run `pinch-to-post health-check` first

### Memory Mistakes
- **Mistake:** Letting sessions grow without compaction
  - **Result:** Slow context loading, lost info
  - **Fix:** Compact at 2MB or 50 messages

---

## Quick Reference

### Check Dependencies Before Task
```bash
# Python
python3 -c "import pandas; print('OK')"

# System
which curl && which jq && which pdftotext

# Node
npm list -g package-name
```

### Save Artifacts
```bash
# Reports
mv report.md /mnt/data/report-$(date +%Y%m%d).md

# Data
cp results.csv /mnt/data/results-$(date +%Y%m%d).csv

# Code
cp script.sh /mnt/data/scripts/script-$(date +%Y%m%d).sh
```

### Check Disk Space
```bash
df -h /root/.openclaw
# If >80%, run: skill: disk-cleanup
```

### Compaction Trigger
```bash
# Check session size
ls -lh /root/.openclaw/workspace/.sessions/

# If >2MB: compact session
```

---

## Status

**Skills Created:** 0
**Tasks Encoded:** 0
**Last Compaction:** Never
**System Health:** 🟢 All clear

---

## Next Steps

1. **First task:** Identify a repeatable task from our conversation
2. **Encode it:** Create first skill in `/skills/shell-agent/`
3. **Test it:** Run the skill, verify output
4. **Document:** Add negative examples if anything fails

---

**This is how we operate now. Read it. Follow it. Improve it.**

*Last Updated: 2026-02-15 23:35 UTC*
