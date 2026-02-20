# Self-Improvement Skill

**Version:** 1.0.0
**Author:** pskoett (via ClawHub)
**Installed:** 2026-02-20

---

## Quick Start

```bash
# Capture a learning
./skills/self-improvement/capture-learning.sh "Domain Name Verification" "accuracy" "Assumed spelling without asking Peter"

# Review recent learnings
cat self-review.md

# Search learnings by topic
grep -r "DOMAIN NAMES" self-review.md
```

---

## What It Does

Captures lessons learned from mistakes, corrections, and discoveries to enable continuous improvement across the autonomous agent organization.

---

## When to Use

Use this skill when:

1. ✅ **Something fails** - Command, API, or tool fails
2. ✅ **Peter corrects you** - "No, that's wrong..." or "Actually..."
3. ✅ **Capability gap** - Peter requests something you can't do
4. ✅ **External failure** - API or tool fails
5. ✅ **Knowledge outdated** - You realize your info is wrong
6. ✅ **Better way found** - Discover a more efficient approach
7. ✅ **Before major tasks** - Review past learnings first

---

## How It Works

### 1. Capture the Learning

**Quick capture:**
```bash
./skills/self-improvement/capture-learning.sh "Title" "category" "Description"
```

**Manual capture:**
Edit `/root/.openclaw/workspace/self-review.md`

### 2. Structure the Entry

```markdown
## [LEARNING TITLE]

**Date:** YYYY-MM-DD HH:MM
**Context:** [What were you trying to do?]
**Issue:** [What went wrong or what did you learn?]
**Root Cause:** [Why did it happen?]
**Solution:** [How was it fixed or what's the better approach?]
**Prevention:** [How to prevent this in the future]
**Impact:** [Why this matters]
**Tags:** [keywords for future search]
```

### 3. Review Before Tasks

```bash
# Search relevant learnings
grep -r "DOMAIN NAMES" self-review.md
grep -r "COST OPTIMIZATION" memory/
```

---

## File Structure

```
/root/.openclaw/workspace/
├── self-review.md              # Daily learnings & corrections
├── MEMORY.md                   # Permanent wisdom
└── memory/
    ├── 2026-02-20.md           # Daily logs
    ├── 2026-02-21.md
    └── ...
```

---

## Learning Categories

**Technical:**
- API failures & workarounds
- Command pitfalls & solutions
- Tool configurations
- Cost optimizations
- Performance improvements

**Process:**
- Better workflows
- Communication patterns
- Decision frameworks
- Prioritization insights
- Efficiency gains

**Domain-Specific:**
- Photostudio optimizations
- DeBadkamer improvements
- Domain investments
- TikTok content
- Technical decisions

**Personalization:**
- Peter's preferences
- Communication style
- Decision patterns
- Goals alignment

---

## Example Learnings

### Example 1: Domain Name Verification

```markdown
## Domain Name Verification Error

**Date:** 2026-02-20 18:45
**Context:** Creating documentation for DeBadkamer.com
**Issue:** Documented domain as "debadkker.com" without verification
**Root Cause:** Assumed spelling without asking Peter to confirm
**Solution:** Always verify domain names with user before committing to permanent storage
**Prevention:** Add verification step to any documentation involving proper nouns, URLs, domains
**Impact:** Prevents misinformation in knowledge base
**Tags:** #domains #verification #documentation #accuracy
```

### Example 2: Video Format Discovery

```markdown
## TikTok Video Format - Before/After Works Better

**Date:** 2026-02-20 16:30
**Context:** Creating TikTok videos for Photostudio
**Issue:** Initial format showed only "after" images - user feedback: "that's not good"
**Root Cause:** Didn't show transformation/anticipation
**Solution:** Before/After format with BEFORE image first creates anticipation and dramatic reveal
**Prevention:** Test content formats with user before full production
**Impact:** Better engagement, clearer value proposition
**Tags:** #tiktok #video #format #photostudio #testing
```

---

## Review Schedule

**Daily:**
- Check `self-review.md` for recent learnings
- Apply learnings to current work

**Weekly:**
- Consolidate daily learnings into MEMORY.md
- Remove outdated information
- Identify patterns in mistakes

**Monthly:**
- Archive old daily logs
- Extract permanent wisdom
- Update skill documentation
- Share learnings across agent team

---

## Integration with Workflows

### Before Commands
```bash
# Check if there are learnings about this command
grep -r "COMMAND NAME" self-review.md
```

### After Failures
```bash
# Document what went wrong
./capture-learning.sh "Failure Title" "category" "Description"
```

### After Successes
```bash
# Document what worked well
# Add to MEMORY.md for future reference
```

### Before Major Decisions
```bash
# Search relevant learnings
# Review past mistakes in this area
# Apply lessons learned
```

---

## Success Metrics

**Reduction in repeated errors:**
- Same mistake shouldn't happen twice
- Fewer user corrections over time
- Better first-attempt accuracy

**Knowledge base growth:**
- More documented learnings
- Better organization
- Faster search/retrieval

**Decision quality:**
- Better choices based on experience
- Fewer preventable mistakes
- More efficient problem-solving

---

## Best Practices

1. ✅ **Document immediately** - Don't rely on memory
2. ✅ **Be specific** - Include context, not just solution
3. ✅ **Root cause analysis** - Understand why, not just what
4. ✅ **Think preventively** - How to ensure this doesn't recur
5. ✅ **Tag effectively** - Use keywords for future search
6. ✅ **Review regularly** - Apply learnings to current work
7. ✅ **Share insights** - Distribute across agent team
8. ✅ **Update continuously** - Knowledge evolves

---

## Helper Script

**Capture a learning quickly:**
```bash
./capture-learning.sh "Title" "category" "Description"
```

**Example:**
```bash
./capture-learning.sh \
  "API Rate Limit Discovered" \
  "technical" \
  "External API limits to 100 req/min, need to add rate limiting"
```

This automatically adds the learning to:
- Daily log (`memory/YYYY-MM-DD.md`)
- Self-review (`self-review.md`)

Then you can fill in the full details later.

---

## Integration with Other Skills

Works best combined with:

- **All skills** - Capture learnings from every operation
- **Memory system** - Store learnings for retrieval
- **Coordination** - Share learnings across agents
- **Decision-making** - Apply past learnings

---

## Remember

> **The goal is continuous improvement. Every mistake is a learning opportunity. Every success has lessons to extract. Document it all, review it often, apply it always.**

---

**Last Updated:** 2026-02-20
**Maintained by:** Carlottta (Coordinator)
**Purpose:** Enable continuous improvement across autonomous agent organization
