# .learnings/ - Self-Improvement System

**Purpose:** Log learnings, errors, and feature requests for continuous improvement.

---

## 📁 Files

| File | Purpose |
|------|---------|
| `LEARNINGS.md` | Corrections, knowledge gaps, best practices |
| `ERRORS.md` | Command failures, exceptions, bugs |
| `FEATURE_REQUESTS.md` | User-requested capabilities |
| `SKILL.md` | Full documentation of the self-improvement system |

---

## 🚀 Quick Start

### Log Something Now

```bash
# Quick reminder of what to log
./scripts/activator.sh
```

### Review Pending Items

```bash
# Count pending learnings
grep -h "Status\*\*: pending" LEARNINGS.md | wc -l

# List high-priority items
grep -B5 "Priority\*\*: high" LEARNINGS.md | grep "^## \["
```

### Promote to Project Memory

When a learning is broadly applicable:
1. Add to `AGENTS.md` (workflows) or `SOUL.md` (behavior)
2. Update learning: `Status: promoted`
3. Add: `Promoted: AGENTS.md`

---

## 📊 Current Status

**Total Learnings:** 9 entries
**Total Errors:** 0 entries
**Total Features:** 0 entries

**Pending Items:** 9
**Resolved Items:** 0
**Promoted Items:** 0

---

## 🎯 Key Learnings

1. **Locked Architecture Pattern** (LRN-20250213-001) - Lock all architectural elements in AI content generation, vary only style
2. **Viral Hook Formula** (LRN-20250213-002) - [Another person] + [conflict] → showed proof → changed mind
3. **Skill Files Critical** (LRN-20250213-003) - Skill files are the critical component of AI agent systems
4. **Hybrid Workflow** (LRN-20250213-004) - AI does 95%, human does 5%
5. **Batch API** (LRN-20250213-005) - Pre-generate content overnight for 50% cost savings

---

## 🔗 Integration

The `.learnings/` system integrates with:

- **OpenClaw workspace** - Automatic skill loading
- **Agent coordination** - Share learnings across agents
- **Session history** - Reference past learnings in new tasks
- **Midnight Surprise** - Review learnings before autonomous work

---

## 📝 Logging Format

All entries follow this structure:

```markdown
## [TYPE-YYYYMMDD-XXX] category

**Logged:** ISO timestamp
**Priority:** low | medium | high | critical
**Status:** pending | resolved | promoted
**Area:** frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context

### Suggested Action
What to do about it

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX

---
```

---

## 🔄 Promotion Workflow

### When to Promote

- Learning applies across multiple files/features
- Knowledge any agent should know
- Prevents recurring mistakes
- Documents project-specific conventions

### Where to Promote

| Learning Type | Target | Example |
|---------------|--------|---------|
| Behavioral patterns | `SOUL.md` | "Be concise, avoid disclaimers" |
| Workflow improvements | `AGENTS.md` | "Spawn sub-agents for long tasks" |
| Tool gotchas | `TOOLS.md` | "Git push needs auth configured first" |

### How to Promote

1. Distill to concise rule
2. Add to target file
3. Update learning: `Status: promoted`
4. Add: `Promoted: TARGET_FILE`

---

## 📈 Best Practices

1. **Log immediately** - Context is fresh
2. **Be specific** - Future agents need clarity
3. **Link related entries** - `See Also: LRN-XXX`
4. **Promote aggressively** - If in doubt, promote it
5. **Review regularly** - Weekly during active work

---

## 🎓 Examples

See `LEARNINGS.md` for 9 real examples including:
- Locked Architecture Pattern for AI content
- Viral Hook Formula from TikTok testing
- Hybrid AI/human workflow (95/5 split)
- OpenAI Batch API cost savings

---

**Last Updated:** 2026-02-20
**System Version:** 1.1.0
**Documentation:** See `SKILL.md` for complete reference
