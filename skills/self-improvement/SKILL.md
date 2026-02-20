# Self-Improving Agent Skill

**Description:** Captures learnings, errors, and corrections to enable continuous improvement.

**Author:** pskoett (via ClawHub)
**Installed:** 2026-02-20
**Version:** 1.0

---

## Purpose

This skill helps the autonomous agent organization continuously improve by:
- Capturing lessons learned from mistakes and corrections
- Documenting better approaches discovered over time
- Building a knowledge base of what works and what doesn't
- Reviewing past learnings before making decisions
- Preventing repetition of errors

---

## When to Use

**Trigger this skill when:**

1. **Operation fails unexpectedly** - A command, API call, or tool fails
2. **User corrects you** - Peter says "No, that's wrong..." or "Actually..."
3. **Capability gap discovered** - Peter requests something you can't do
4. **External failure** - An external API or tool fails
5. **Knowledge outdated** - You realize your information is incorrect
6. **Better approach found** - You discover a more efficient way to do something
7. **Before major tasks** - Review relevant past learnings first

---

## How to Use

### Step 1: Capture the Learning

When a learning event occurs, document it in the appropriate file:

**For daily learnings:**
```bash
/root/.openclaw/workspace/self-review.md
```

**For permanent learnings:**
```bash
/root/.openclaw/workspace/MEMORY.md
```

**For topic-specific learnings:**
```bash
/root/.openclaw/workspace/memory/[topic].md
```

### Step 2: Structure the Entry

Use this template:

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

### Step 3: Review Before Major Tasks

Before starting important work:

```bash
# Search relevant learnings
grep -r "DOMAIN NAMES" /root/.openclaw/workspace/self-review.md
grep -r "COST OPTIMIZATION" /root/.openclaw/workspace/memory/
```

---

## Learning Categories

### Technical Learnings
- API failures and workarounds
- Command pitfalls and solutions
- Tool configuration discoveries
- Cost optimization insights
- Performance improvements

### Process Learnings
- Better workflows discovered
- Communication patterns that work
- Decision-making frameworks
- Prioritization insights
- Efficiency gains

### Domain-Specific Learnings
- Photostudio pipeline optimizations
- DeBadkamer lead gen improvements
- Domain investment criteria
- TikTok content insights
- Technical stack decisions

### Personalization Learnings
- Peter's preferences discovered
- Communication style insights
- Decision-making patterns
- Goals and priorities alignment

---

## Example Learnings

### Example 1: Domain Name Verification

**Context:** Creating documentation for DeBadkamer.com
**Issue:** Documented domain as "debadkker.com" without verification
**Root Cause:** Assumed spelling without asking Peter to confirm
**Solution:** Always verify domain names with user before committing to permanent storage
**Prevention:** Add verification step to any documentation involving proper nouns, URLs, domains
**Impact:** Prevents misinformation in knowledge base
**Tags:** domains, verification, documentation, accuracy

### Example 2: Video Format Discovery

**Context:** Creating TikTok videos for Photostudio
**Issue:** Initial format showed only "after" images - user feedback: "that's not good"
**Root Cause:** Didn't show transformation/anticipation
**Solution:** Before/After format with BEFORE image first creates anticipation and dramatic reveal
**Prevention:** Test content formats with user before full production
**Impact:** Better engagement, clearer value proposition
**Tags:** tiktok, video, format, photostudio, testing

---

## Review Schedule

### Daily Review
- Check `/root/.openclaw/workspace/self-review.md` for recent learnings
- Apply learnings to current work
- Update if better approaches discovered

### Weekly Review
- Consolidate daily learnings into MEMORY.md
- Remove outdated information
- Identify patterns in mistakes
- Update prevention strategies

### Monthly Review
- Archive old daily logs
- Extract permanent wisdom
- Update skill documentation
- Share learnings across agent team

---

## Integration with Workflows

### Before Commands
```bash
# Check if there are learnings about this command
grep -r "COMMAND NAME" /root/.openclaw/workspace/self-review.md
```

### After Failures
```bash
# Document what went wrong
# Add to self-review.md with full analysis
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
- Fewer "user corrections" over time
- Better first-attempt accuracy

**Knowledge base growth:**
- More documented learnings
- Better organization of knowledge
- Faster search/retrieval of relevant info

**Decision quality improvement:**
- Better choices based on past experience
- Fewer preventable mistakes
- More efficient problem-solving

---

## File Locations

**Daily review file:**
```
/root/.openclaw/workspace/self-review.md
```

**Permanent memory:**
```
/root/.openclaw/workspace/MEMORY.md
```

**Topic-specific memory:**
```
/root/.openclaw/workspace/memory/[topic].md
```

**Daily logs:**
```
/root/.openclaw/workspace/memory/YYYY-MM-DD.md
```

---

## Best Practices

1. **Document immediately** - Don't rely on memory
2. **Be specific** - Include context, not just the solution
3. **Root cause analysis** - Understand why, not just what
4. **Think preventively** - How to ensure this doesn't recur
5. **Tag effectively** - Use keywords for future search
6. **Review regularly** - Apply learnings to current work
7. **Share insights** - Distribute learnings across agent team
8. **Update continuously** - Knowledge evolves, keep it current

---

## Integration with Other Skills

This skill works best when combined with:

- **All skills** - Capture learnings from every operation
- **Memory system** - Store learnings for long-term retrieval
- **Coordination** - Share learnings across agent team
- **Decision-making** - Apply past learnings to choices

---

**Remember:** The goal is continuous improvement. Every mistake is a learning opportunity. Every success has lessons to extract. Document it all, review it often, apply it always.

---

*Last Updated:* 2026-02-20
*Maintained by:* Carlottta (Coordinator)
*Purpose:* Enable continuous improvement across autonomous agent organization
