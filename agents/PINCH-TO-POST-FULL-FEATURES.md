# 🦞 Pinch-to-Post - Full Feature Guide for Agents

**Version:** 3.1.0
**Last Updated:** 2026-02-03

---

## Overview

You have access to **50+ WordPress automation features** via the pinch-to-post system across 4 sites:
- crashcasino.io (default)
- crashgamegambling.com
- freecrashgames.com
- cryptocrashgambling.com

**Master Command:** `/root/.openclaw/workspace/scripts/pinch-to-post.sh`

Run `pinch-to-post help` to see all commands.

---

## Quick Reference

### Publishing
```bash
# Publish single article (with quality gate - 80+ required)
pinch-to-post publish crashcasino 123

# Bulk publish multiple articles
pinch-to-post bulk-publish crashcasino 100-110  # Range
pinch-to-post bulk-publish crashcasino 123 456 789  # Individual IDs

# Cross-post to multiple sites
pinch-to-post cross-post "Title" content.md "crashgame,freecrash,cryptocrash"
```

### Content Management
```bash
# View publishing schedule
pinch-to-post calendar 2026-02              # All sites
pinch-to-post calendar 2026-02 crashcasino  # Specific site

# Get statistics
pinch-to-post stats              # All sites
pinch-to-post stats crashcasino  # Specific site

# Backup content
pinch-to-post backup /root/backups/2026-02-03
pinch-to-post backup /root/backups/2026-02-03 crashcasino
```

### Media & Comments
```bash
# Upload image with alt text
pinch-to-post media-upload crashcasino image.jpg "Crash game screenshot"

# Upload and set as featured image
pinch-to-post media-upload crashcasino image.jpg "Alt text" "Caption" 123

# Moderate comments
pinch-to-post comment-moderate crashcasino show-pending
pinch-to-post comment-moderate crashcasino approve-all
pinch-to-post comment-moderate crashcasino spam-all
pinch-to-post comment-moderate crashcasino spam-suspicious
```

### Social Media
```bash
# Post to social platforms (if configured)
pinch-to-post social-post twitter "New article!" "https://crashcasino.io/post"
pinch-to-post social-post linkedin "Check out our latest post" "URL"
pinch-to-post social-post mastodon "Fresh content dropped" "URL"
```

### Quality Checks
```bash
# Check article health score
pinch-to-post health-check crashcasino 123
```

---

## Daily Workflow

Run daily to stay on top of your sites:

```bash
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh
```

**What it does:**
1. Shows content statistics across all sites
2. Lists pending comments for review
3. Shows today's publishing calendar
4. Provides recommendations

**Run:** Once per day (morning or evening)

---

## Weekly Workflow

Run weekly for maintenance:

```bash
/root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh
```

**What it does:**
1. Creates full content backup
2. Shows this month's calendar
3. Lists draft counts across sites
4. Summarizes pending comments
5. Provides weekly task recommendations

**Run:** Once per week (Monday or Friday)

---

## Agent-Specific Usage

### Vision (SEO/Content)

**Primary Tasks:**
- Create drafts via REST API or direct
- Run health checks before publishing
- Bulk publish when content batches are ready
- Use content calendar for scheduling

**Example Workflow:**
```bash
# 1. Create draft (using REST API or gateway)
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts" \
  -u "peter:PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"title": "Article", "content": "...", "status": "draft"}'

# 2. Check health
pinch-to-post health-check crashcasino 123

# 3. Publish when score is 80+
pinch-to-post publish crashcasino 123

# 4. Bulk publish week's content
pinch-to-post bulk-publish crashcasino 100-120

# 5. Check calendar
pinch-to-post calendar 2026-02 crashcasino
```

### Fury (Editor)

**Primary Tasks:**
- Review drafts and edit content
- Run health checks on edited articles
- Moderate comments (spam/approval)
- Use stats for research insights

**Example Workflow:**
```bash
# 1. Check pending comments
pinch-to-post comment-moderate crashcasino show-pending

# 2. Clean spam
pinch-to-post comment-moderate crashcasino spam-suspicious

# 3. Review article health
pinch-to-post health-check crashcasino 123

# 4. Get stats for research
pinch-to-post stats crashcasino
```

### Quill (Publisher)

**Primary Tasks:**
- Bulk publish batches of content
- Cross-post to multiple sites
- Share content on social media
- Coordinate publishing schedules

**Example Workflow:**
```bash
# 1. View calendar
pinch-to-post calendar 2026-02

# 2. Bulk publish week's content
for site in crashcasino crashgame freecrash cryptocrash; do
  pinch-to-post bulk-publish $site 100-120
done

# 3. Cross-post to multiple sites
pinch-to-post cross-post "Major Update" article.md "crashgame,freecrash"

# 4. Share on social
pinch-to-post social-post twitter "Week 2 content is live!" "https://crashcasino.io"

# 5. Check stats
pinch-to-post stats
```

### Carlottta (Coordinator)

**Primary Tasks:**
- Run daily/weekly workflows
- Monitor stats across sites
- Coordinate between agents
- Handle backups and maintenance

**Example Workflow:**
```bash
# Daily check
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh

# Weekly maintenance
/root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh

# Backup before major changes
pinch-to-post backup /root/backups/pre-publish-$(date +%Y%m%d)
```

---

## Quality Threshold

**All articles must score 80/100 to publish.**

**Health Check Criteria:**
- ✅ Word count (300+ recommended)
- ✅ Meta description present (SEO critical)
- ✅ Focus keyword present (SEO critical)
- ✅ Featured image set
- ✅ H2 headings (2+ recommended)
- ✅ Images in content
- ✅ Title length (50-60 chars optimal)

**If score < 80:**
- Article will NOT publish
- Gateway provides specific feedback
- Fix issues and retry

---

## Multi-Site Management

**Target specific sites:**
```bash
pinch-to-post publish crashcasino 123
pinch-to-post publish crashgame 456
pinch-to-post publish freecrash 789
pinch-to-post publish cryptocrash 101
```

**Cross-post content:**
```bash
pinch-to-post cross-post "Article Title" content.md "crashgame,freecrash,cryptocrash"
```

**Get stats for all sites:**
```bash
pinch-to-post stats
```

---

## Automation & Cron Jobs

**Daily checks (add to cron):**
```bash
0 9 * * * /root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh >> /root/.openclaw/workspace/logs/daily-ops.log 2>&1
```

**Weekly backups (add to cron):**
```bash
0 10 * * 1 /root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh >> /root/.openclaw/workspace/logs/weekly-ops.log 2>&1
```

---

## Error Handling

**If publish fails:**
1. Check health score: `pinch-to-post health-check <site> <id>`
2. Verify post exists: Check WordPress admin
3. Check credentials: `~/.openclaw/openclaw.json`
4. Check site URL: Verify site is accessible

**If health check fails:**
1. Article likely missing meta description or focus keyword
2. Add them manually via WordPress admin or REST API
3. Re-run health check

**If bulk publish skips articles:**
1. Skipped articles have score < 80
2. Fix issues and re-run bulk publish
3. Use `publish` command for individual articles

---

## Best Practices

### Before Publishing:
1. ✅ Always run health check first
2. ✅ Verify meta description and focus keyword are set
3. ✅ Ensure featured image is attached
4. ✅ Check article has proper structure (H2 headings, images)

### Comment Moderation:
1. ✅ Run `show-pending` to review comments
2. ✅ Use `spam-suspicious` to auto-filter spam
3. ✅ Manually approve legitimate comments
4. ✅ Don't `approve-all` without review

### Content Organization:
1. ✅ Use content calendar to plan publishing schedule
2. ✅ Bulk publish batches of related content
3. ✅ Cross-post strategically (don't spam all sites)
4. ✅ Backup before major changes

### Social Media:
1. ✅ Share valuable content, not every post
2. ✅ Customize message for each platform
3. ✅ Include relevant hashtags
4. ✅ Engage with replies

---

## Full Feature List

See `~/.openclaw/workspace/skills/pinch-to-post/SKILL.md` for complete documentation of all 50+ features including:
- WooCommerce features (products, orders, inventory)
- Advanced SEO (Yoast, RankMath)
- Markdown to Gutenberg conversion
- AI-powered workflows
- Custom field management
- Multilingual support
- WP-CLI integration

---

## Troubleshooting

**Command not found:**
```bash
# Add to PATH or use full path
export PATH="/root/.openclaw/workspace/scripts:$PATH"
```

**Permission denied:**
```bash
# Ensure scripts are executable
chmod +x /root/.openclaw/workspace/scripts/pinch-to-post.sh
chmod +x /root/.openclaw/workspace/scripts/pinch-to-post-helpers/*.sh
```

**Credentials error:**
```bash
# Check .env file
cat ~/.openclaw/workspace/.env | grep WP_SITE_
```

**Site not accessible:**
```bash
# Test site connection
curl -I https://crashcasino.io
```

---

## Summary

**You now have full access to all pinch-to-post features.**

**Key commands to remember:**
- `pinch-to-post help` - Show all commands
- `pinch-to-post stats` - Quick status check
- `pinch-to-post publish <site> <id>` - Publish article
- `pinch-to-post bulk-publish <site> <ids>` - Batch publish
- `pinch-to-post calendar <month>` - View schedule
- Daily workflow: `/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh`
- Weekly workflow: `/root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh`

**Use these features proactively** to automate your WordPress workflow and save time.
