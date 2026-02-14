# Vision Workflow Update - Summary for Peter

**Date:** 2026-02-03 09:30 UTC
**Status:** ✅ Complete

## What Changed

### Before
Vision used custom WordPress publishing scripts with basic HTML:
- `md2html-fixed.py` → basic `<p>`, `<h1>`, `<h2>` tags
- Tables rendered as plain text
- YAML frontmatter leaked into content
- 7+ duplicate publishing scripts

### After
Vision now uses **pinch-to-post skill integration**:
- Proper Gutenberg blocks (`<!-- wp:heading -->`, `<!-- wp:list -->`, etc.)
- Tables as `wp-block-table` blocks
- YAML frontmatter auto-stripped
- Single unified publisher: `wp-publish.sh`

## Files to Use

### Main Publisher (All Articles)
```bash
/root/.openclaw/workspace/wp-publish.sh article.md <site> <status>
```

**Example:**
```bash
wp-publish.sh draft.md crashcasino.io publish
```

### Vision's Universal Publisher
**Location:** `/root/.openclaw/workspace/agents/vision/wordpress-publish.sh`

```bash
# Single article
wordpress-publish.sh article.md crashcasino.io publish

# Batch publish
wordpress-publish.sh --batch crashcasino.io publish 'month2-week1-*.md'
```

## Verified Working ✅

**Tested on:** `month2-week1-crashcasino-001-is-crash-gambling-rigged.md`
**Result:** Perfect Gutenberg output
- ✅ H2/H3 headings as `wp-block-heading`
- ✅ Lists as `wp-block-list`
- ✅ Paragraphs as `wp:paragraph`
- ✅ Clean content (no YAML frontmatter)

## Known Issue

**crashgamegambling.com** - Permission error:
```
"Sorry, you are not allowed to create posts as this user."
```

**Status:** Separate from workflow update - credential/permission issue
**Other sites:** ✅ crashcasino.io, cryptocrashgambling.com, freecrashgames.com all working

## Documentation Created

- `agents/vision/WORDPRESS_PUBLISHING_WORKFLOW.md` - Full workflow guide
- `PINCHTOPOST_INTEGRATION.md` - Integration details
- `.learnings/learning-20260203-use-dedicated-skills.md` - Lessons learned

## Next Steps

Vision can now:
1. Use `wp-publish.sh` for all new publishing
2. Use `wordpress-publish.sh` for batch operations
3. Remove old deprecated scripts (7 files)

---
*Workflow migration complete. Ready for production use.*
