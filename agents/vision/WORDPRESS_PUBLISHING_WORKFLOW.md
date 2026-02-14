# Vision Agent - WordPress Publishing Workflow Update

**Date:** 2026-02-03
**Status:** ✅ Migrated to Pinch-to-Post Integration

## New Publishing Workflow

### Primary Publisher: `wp-publish.sh`
**Location:** `/root/.openclaw/workspace/wp-publish.sh`

**Features:**
- ✅ Uses pinch-to-post skill (not custom code)
- ✅ Proper Gutenberg blocks (`<!-- wp:heading -->`, etc.)
- ✅ YAML frontmatter auto-stripped
- ✅ Tables → Gutenberg `wp-block-table` blocks
- ✅ Multi-site support (crashcasino.io, cryptocrashgambling.com, crashgamegambling.com, freecrashgames.com)
- ✅ Auto-archives published articles

### Usage

#### Single Article
```bash
wp-publish.sh article.md crashcasino.io publish
wp-publish.sh article.md cryptocrashgambling.com draft
```

#### Batch Publishing (Vision's Universal Script)
**Location:** `/root/.openclaw/workspace/agents/vision/wordpress-publish.sh`

```bash
# Single article
wordpress-publish.sh article.md crashcasino.io publish

# Batch publish
wordpress-publish.sh --batch crashcasino.io publish 'month2-week1-*.md'
```

### Migration from Old Workflow

**Old Approach:**
- Custom `md2html-fixed.py` converter
- Basic HTML tags (`<p>`, `<h1>`, `<h2>`)
- Tables rendered as plain text
- YAML frontmatter leaked into content
- Multiple duplicate publishing scripts

**New Approach:**
- Pinch-to-post skill integration
- Proper Gutenberg blocks
- Tables as `wp-block-table` blocks
- YAML frontmatter stripped automatically
- Single unified publisher

## File Changes

### New Files
- `wp-publish.sh` - Main publisher (use this)
- `agents/shared/preprocess_markdown.py` - YAML/table preprocessor
- `agents/shared/md2gutenberg.py` - Gutenberg converter

### Updated Files
- `skills/pinch-to-post/wp-rest.sh` - Fixed `set -e` issue
- `agents/vision/wordpress-publish.sh` - New universal publisher

### Deprecated (Do Not Use)
- `wordpress-publish-improved.sh`
- `wordpress-publish-final.sh`
- `wordpress-publish-gutenberg.sh`
- `wordpress-publish-universal.sh`
- `wordpress-publish-with-metadata.sh`
- `publish-month2-week1-batch2-final.sh`

## Output Quality Comparison

### Before (Custom Implementation)
```html
<h1>Title</h1>
<p>Paragraph</p>
<p>| Col1 | Col2 |</p>  <!-- Tables as plain text -->
```

### After (Pinch-to-Post Integration)
```html
<!-- wp:heading -->
<h1>Title</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Paragraph</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
<figure class="wp-block-table">
<table>...</table>
</figure>
<!-- /wp:table -->
```

## Batch Publishing Templates

### Month 2 Week 1 Batch 2
**Script:** `agents/vision/publish-month2-week1-batch3.sh`

```bash
#!/bin/bash
# 3 articles: Ethereum, Brazil, Bankroll Management
/root/.openclaw/workspace/agents/vision/publish-month2-week1-batch3.sh
```

### Custom Batch
```bash
# All drafts for crashcasino.io
wordpress-publish.sh --batch crashcasino.io publish

# Specific pattern
wordpress-publish.sh --batch crashcasino.io publish 'month2-*.md'
```

## Technical Details

### Preprocessing Pipeline
1. **YAML Stripping:** Removes `---` frontmatter blocks
2. **Table Conversion:** Markdown tables → HTML with `wp-block-table` class
3. **Gutenberg Conversion:** Markdown → `<!-- wp:block -->` format
4. **WordPress REST API:** JSON payload with proper blocks

### Multi-Site Configuration
Uses `WP_SITE_*` environment variables:
- `WP_SITE_CRASHCASINO_URL`
- `WP_SITE_CRASHCASINO_USER`
- `WP_SITE_CRASHCASINO_PASS`

Auto-configured in `wp-publish.sh` - no manual setup needed.

## Troubleshooting

### Issue: "Unknown command: --site=xxx"
**Fix:** Make sure pinch-to-post wp-rest.sh has `set -e` disabled (line 4)

### Issue: YAML frontmatter appearing in content
**Fix:** Verify `preprocess_markdown.py` is being called

### Issue: Tables not rendering
**Fix:** Check that preprocess step converted tables to HTML before Gutenberg conversion

## Testing

Verification command:
```bash
echo "# Test" > /tmp/test.md && wp-publish.sh /tmp/test.md crashcasino.io draft
```

Should output:
```
✅ SUCCESS!
   Post ID: XXX
   Link: https://crashcasino.io/?p=XXX
```

---
*Workflow updated 2026-02-03. All new publishing should use wp-publish.sh.*
