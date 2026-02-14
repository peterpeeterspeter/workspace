# HTML Publishing Comparison: Current vs Pinch-to-Post

**Created:** 2026-02-03
**Status:** ACTION REQUIRED - Migration needed

---

## Problem Statement

Current implementation uses `md2html-fixed.py` which produces basic HTML but lacks:
- ❌ Gutenberg block comments (WordPress block editor format)
- ❌ Content health checks
- ❌ Proper table handling
- ❌ Link quality assurance

## Current Implementation (POOR)

**File:** `/root/.openclaw/workspace/agents/shared/md2html-fixed.py`

**What it does:**
- Converts markdown to basic HTML
- Adds `https://` to links without protocol (recent fix)
- Simple regex-based inline processing

**Issues:**
```python
# Current: Basic HTML only
text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
# Output: <a href="https://cybetplay.com">Play</a>
```

**Missing:**
- No Gutenberg block comments
- No content health scoring
- No table validation
- Basic error handling

---

## Pinch-to-Post Implementation (SUPERIOR)

**File:** `/root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh`

**What it does:**
- **markdown_to_gutenberg()** - Full Gutenberg block format
- **create-post-markdown** - Direct markdown publishing
- **content_health_check()** - Quality scoring
- **export-markdown** - Bidirectional conversion

**Gutenberg Block Format:**
```bash
# Pinch-to-Post produces proper WordPress blocks
<!-- wp:heading -->
<h2>Crash Gambling Bonuses</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Here's how to maximize your deposits...</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>Welcome bonuses</li>
  <li>No deposit offers</li>
</ul>
<!-- /wp:list -->
```

**Additional Features:**
1. **Content Health Check:**
   - Word count validation (300+ recommended)
   - Title length check (50-60 chars ideal)
   - Featured image verification
   - Heading structure analysis
   - Image alt text check
   - Internal link detection

2. **Markdown Publishing Command:**
   ```bash
   wp-rest.sh create-post-markdown "Title" content.md publish
   ```

3. **Quality Scoring:**
   - Generates health score (0-100)
   - Identifies specific issues
   - Actionable recommendations

---

## Comparison Table

| Feature | md2html-fixed.py | Pinch-to-Post |
|---------|-----------------|---------------|
| Gutenberg blocks | ❌ No | ✅ Yes |
| Content health check | ❌ No | ✅ Yes (scored) |
| Word count validation | ❌ No | ✅ Yes |
| Title length check | ❌ No | ✅ Yes |
| Alt text verification | ❌ No | ✅ Yes |
| Internal link check | ❌ No | ✅ Yes |
| Markdown → HTML | ✅ Basic | ✅ Gutenberg |
| Error handling | ⚠️ Basic | ✅ Robust |
| WordPress REST API | ❌ No (custom) | ✅ Built-in |
| Export to markdown | ❌ No | ✅ Yes |
| Multi-site support | ❌ No | ✅ Yes |

---

## Migration Plan

### Phase 1: Update Publishing Scripts (IMMEDIATE)

**Current workflow:**
```bash
python3 /root/.openclaw/workspace/agents/shared/md2html-fixed.py "$draft_file"
```

**New workflow:**
```bash
/root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh create-post-markdown "$title" "$draft_file" "publish"
```

### Phase 2: Update WordPress Publishing Scripts

**Files to update:**
- `/root/.openclaw/workspace/agents/vision/wordpress-publish-universal.sh`
- `/root/.openclaw/workspace/agents/vision/wordpress-publish-final.sh`
- `/root/.openclaw/workspace/agents/vision/wordpress-publish-improved.sh`

**Change:**
```bash
# OLD
HTML_RESULT=$(python3 /root/.openclaw/workspace/agents/shared/md2html-fixed.py "$draft_file")

# NEW
CONTENT=$(/root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh --site "$SITE" create-post-markdown "$TITLE" "$draft_file")
```

### Phase 3: Add Content Health Checks

**After publishing:**
```bash
# Check content health
/root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh --site "$SITE" content-health-check "$POST_ID"
```

### Phase 4: Deprecate Old Scripts

**Archive (not delete yet):**
- `/root/.openclaw/workspace/agents/shared/md2html-fixed.py` → `/root/.openclaw/workspace/archive/`
- Keep for backup/reference

---

## Benefits of Migration

### 1. Better WordPress Integration
- Gutenberg blocks are WordPress native format
- Better block editor compatibility
- Future-proofs for WordPress updates

### 2. Quality Assurance
- Automatic content health scoring
- Catches issues before publishing
- Actionable feedback

### 3. Simplified Workflow
- One command instead of Python + curl
- Built-in WordPress REST API handling
- Multi-site support out of the box

### 4. Error Handling
- Proper error messages
- Graceful failures
- Debug mode available

### 5. Consistency
- Same skill used for all WordPress operations
- Tested, maintained codebase
- Community improvements

---

## Action Items

### Immediate (Today)
- [ ] Test pinch-to-post `create-post-markdown` with 1 draft
- [ ] Verify Gutenberg block output
- [ ] Compare published result vs current method

### Short-term (This Week)
- [ ] Update all publishing scripts to use pinch-to-post
- [ ] Add content health checks to workflow
- [ ] Train Vision agent on new workflow

### Medium-term (Next Sprint)
- [ ] Archive old md2html-fixed.py
- [ ] Update documentation (AGENTS.md, WORKING.md)
- [ ] Log learning to .learnings/

---

## Testing Checklist

Before full migration:

- [ ] Publish test article with pinch-to-post
- [ ] Verify Gutenberg blocks are correct
- [ ] Check all formatting (tables, lists, links)
- [ ] Run content health check
- [ ] Verify affiliate links work
- [ ] Confirm schema markup still applies
- [ ] Test on all 4 sites

---

## Rollback Plan

If issues arise:
1. Keep md2html-fixed.py in archive
2. Can revert in <5 minutes
3. No data loss (WordPress posts are source of truth)

---

## Estimated Impact

**Time to migrate:** 2-3 hours
**Risk:** Low (tested skill, rollback available)
**Benefit:** High (better quality, WordPress best practices)

---

**Learning Logged:** LRN-20260203-003 (migrate_to_pinch_to_post_html_publishing)
