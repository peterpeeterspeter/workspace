# 🦞 Pinch-to-Post Quick Reference

**Status:** ✅ Configured and ready for all agents

## Configured Sites (4)

| Site | URL | Purpose |
|------|-----|---------|
| crashcasino (default) | https://crashcasino.io/wp-json | Main casino site |
| crashgame | https://crashgamegambling.com/wp-json | Gambling guide |
| freecrash | https://freecrashgames.com/wp-json | Free games hub |
| cryptocrash | https://cryptocrashgambling.com/wp-json | Crypto gambling |

## Quick Commands

### Content Creation
```bash
# Create post
./wp-rest.sh create-post "Title" "Content" draft

# Bulk publish drafts
./wp-rest.sh bulk-publish

# Content health check
./wp-rest.sh health-check 123
```

### Multi-Site Operations
```bash
# Switch sites
WP_SITE=crashgame ./wp-rest.sh list-posts

# Cross-post to multiple sites
./wp-rest.sh cross-post "Title" "Content" crashgame,freecrash
```

### SEO & Quality
```bash
# Run health check before publishing
./wp-rest.sh health-check {post_id}

# Add Yoast SEO meta
curl -X POST "${WP_SITE_URL}/wp-json/wp/v2/posts/{id}" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}" \
  -d '{"meta": {"_yoast_wpseo_title": "SEO Title", "_yoast_wpseo_metadesc": "Description"}}'
```

## Agent Integration

When spawning sub-agents, include this context:

```
You have access to pinch-to-post WordPress automation with 4 configured sites:
- crashcasino.io (default)
- crashgamegambling.com
- freecrashgames.com
- cryptocrashgambling.com

Use pinch-to-post for ALL WordPress operations (create, update, publish, health checks).
Reference: ~/.openclaw/workspace/skills/pinch-to-post/SKILL.md
```

## Feature Highlights

✅ **50+ Features** including:
- Posts, pages, media management
- WooCommerce products, orders, inventory
- SEO integration (Yoast, RankMath)
- Content health scoring
- Bulk operations
- Multi-site management
- Social cross-posting
- Markdown to Gutenberg

## Credentials Location

Config: `~/.openclaw/openclaw.json`
Section: `skills.entries.pinch-to-post.env`

**Security:** Never share these credentials or expose them in logs.

## Support

Full documentation: `~/.openclaw/workspace/skills/pinch-to-post/SKILL.md`
Issues or questions: Ask Carlottta 🎭

---

*Last updated: 2026-02-03*
*Standard: All agents use pinch-to-post for WordPress workflows*
