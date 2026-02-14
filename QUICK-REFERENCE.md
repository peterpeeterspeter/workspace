# 🦞 Pinch-to-Post Quick Reference

**Version:** 3.1.0 | **Date:** 2026-02-03

---

## Master Command

```bash
/root/.openclaw/workspace/scripts/pinch-to-post.sh <command> [args]
```

Or add to PATH:
```bash
export PATH="/root/.openclaw/workspace/scripts:$PATH"
pinch-to-post <command> [args]
```

---

## Common Commands

### Publishing
```bash
# Publish single article
pinch-to-post publish crashcasino 123

# Bulk publish (range)
pinch-to-post bulk-publish crashcasino 100-110

# Bulk publish (individual)
pinch-to-post bulk-publish crashcasino 123 456 789

# Health check
pinch-to-post health-check crashcasino 123
```

### Content Management
```bash
# View calendar (all sites, this month)
pinch-to-post calendar 2026-02

# View calendar (specific site)
pinch-to-post calendar 2026-02 crashcasino

# Statistics (all sites)
pinch-to-post stats

# Statistics (specific site)
pinch-to-post stats crashcasino

# Backup all sites
pinch-to-post backup /root/backups/2026-02-03

# Backup specific site
pinch-to-post backup /root/backups/2026-02-03 crashcasino
```

### Media & Comments
```bash
# Upload image
pinch-to-post media-upload crashcasino image.jpg "Alt text"

# Upload with caption and featured
pinch-to-post media-upload crashcasino image.jpg "Alt" "Cap" 123

# Show pending comments
pinch-to-post comment-moderate crashcasino show-pending

# Auto-mark spam as spam
pinch-to-post comment-moderate crashcasino spam-suspicious

# Approve all comments
pinch-to-post comment-moderate crashcasino approve-all

# Mark all as spam
pinch-to-post comment-moderate crashcasino spam-all
```

### Multi-Site
```bash
# Cross-post to multiple sites
pinch-to-post cross-post "Title" content.md "crashgame,freecrash,cryptocrash"
```

### Social Media
```bash
# Twitter
pinch-to-post social-post twitter "New post!" "https://crashcasino.io/article"

# LinkedIn
pinch-to-post social-post linkedin "Check this out" "URL"

# Mastodon
pinch-to-post social-post mastodon "Fresh content" "URL"
```

---

## Workflows

### Daily Operations
```bash
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh
```

**What it does:**
- Shows content statistics
- Lists pending comments
- Shows today's calendar
- Provides recommendations

**Run:** Once per day (morning)

### Weekly Operations
```bash
/root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh
```

**What it does:**
- Creates full backup
- Shows monthly calendar
- Lists draft counts
- Summarizes pending comments
- Provides weekly recommendations

**Run:** Once per week (Monday recommended)

---

## Sites

- **crashcasino** - crashcasino.io (default)
- **crashgame** - crashgamegambling.com
- **freecrash** - freecrashgames.com
- **cryptocrash** - cryptocrashgambling.com

---

## Quality Threshold

**All articles must score 80/100 to publish.**

**Health check criteria:**
- ✅ Word count (300+ recommended)
- ✅ Meta description present
- ✅ Focus keyword present
- ✅ Featured image set
- ✅ H2 headings (2+ recommended)
- ✅ Images in content

---

## Agent-Specific Quick Start

### Vision (Content/SEO)
```bash
# 1. Create draft (via REST API or WordPress)
# 2. Check health
pinch-to-post health-check crashcasino 123
# 3. Publish when ready
pinch-to-post publish crashcasino 123
# 4. Bulk publish batch
pinch-to-post bulk-publish crashcasino 100-120
```

### Fury (Research/Edit)
```bash
# 1. Get stats for research
pinch-to-post stats crashcasino
# 2. Moderate comments
pinch-to-post comment-moderate crashcasino show-pending
pinch-to-post comment-moderate crashcasino spam-suspicious
# 3. Review health
pinch-to-post health-check crashcasino 123
```

### Quill (Publisher)
```bash
# 1. View calendar
pinch-to-post calendar 2026-02
# 2. Bulk publish
for site in crashcasino crashgame freecrash cryptocrash; do
  pinch-to-post bulk-publish $site 100-120
done
# 3. Share on social
pinch-to-post social-post twitter "Week 2 content live!" "URL"
# 4. Check stats
pinch-to-post stats
```

### Carlottta (Coordinator)
```bash
# 1. Daily workflow
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh
# 2. Weekly workflow
/root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh
# 3. System overview
pinch-to-post stats
```

---

## Help

```bash
pinch-to-post help
```

Shows all commands with examples.

---

## Full Documentation

**Complete Feature Guide:** `/root/.openclaw/workspace/agents/PINCH-TO-POST-FULL-FEATURES.md`

**Agent SOUL Files:**
- Vision: `/root/.openclaw/workspace/agents/vision/SOUL.md`
- Fury: `/root/.openclaw/workspace/agents/fury/SOUL.md`
- Quill: `/root/.openclaw/workspace/agents/quill/SOUL.md`
- Carlottta: `/root/.openclaw/workspace/SOUL.md`

**Skill Documentation:** `~/.openclaw/workspace/skills/pinch-to-post/SKILL.md`

---

## Troubleshooting

**Command not found?**
```bash
# Use full path
/root/.openclaw/workspace/scripts/pinch-to-post.sh stats
```

**Permission denied?**
```bash
chmod +x /root/.openclaw/workspace/scripts/pinch-to-post.sh
chmod +x /root/.openclaw/workspace/scripts/pinch-to-post-helpers/*.sh
```

**Credentials error?**
```bash
# Check .env file
cat ~/.openclaw/workspace/.env | grep WP_SITE_
```

---

## Summary

**You have 50+ WordPress automation features at your fingertips.**

**Top 5 commands to remember:**
1. `pinch-to-post help` - Show all commands
2. `pinch-to-post stats` - Quick status check
3. `pinch-to-post publish <site> <id>` - Publish article
4. `pinch-to-post bulk-publish <site> <ids>` - Batch publish
5. `pinch-to-post calendar <month>` - View schedule

**Start using them today!** 🚀
