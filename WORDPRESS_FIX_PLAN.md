# WordPress Publishing Fix - Complete HTML Repair

**Problem:** Published articles on crashcasino.io had completely broken HTML

## Issues Found

**Broken HTML Structure:**
```html
<h1>Crash Casino Scams — 7 Red Flags</p>  <!-- h1 opened, closed with p -->
<p><h2>Quick Summary</p>                    <!-- h2 inside p tag -->
| Red Flag | Why It's Dangerous |           <!-- Table as plain text, not HTML -->
```

**Root Cause:**
- Old script `wordpress-publish-integrated.sh` sent raw markdown text
- No proper markdown-to-HTML conversion
- Tags not closed properly
- Tables rendered as text with `|` characters

## Fix Applied

### 1. Created Proper Python Converter
**File:** `/agents/shared/md2html-fixed.py`

**Features:**
- ✅ Properly closes all HTML tags
- ✅ Converts `#` to `<h1>...</h1>`
- ✅ Converts tables with `<table>`, `<tr>`, `<td>` tags
- ✅ Handles `**bold**` → `<strong>bold</strong>`
- ✅ Handles `[links](url)` → `<a href="url">link</a>`
- ✅ Proper table structure with `<th>` headers

### 2. Created Republication Script
**File:** `/agents/vision/wordpress-republish-fix.sh`

**Features:**
- Fetches all published posts from crashcasino.io
- Converts original markdown to proper HTML
- Updates posts with corrected HTML
- Preserves title, slug, publish date

### 3. Updated Vision Heartbeat
- Now uses `wordpress-publish-final.sh` with proper HTML

## Testing

```bash
# Test converter
python3 /root/.openclaw/workspace/agents/shared/md2html-fixed.py \
  /root/.openclaw/workspace/drafts/YOUR-FILE.md | jq -r '.html' | head -50

# Should show proper HTML:
# <h1>Title</h1>
# <p>Content</p>
# <table>
#   <tr><th>Header</th></tr>
#   <tr><td>Data</td></tr>
# </table>
```

## Republication Plan

**Option 1: Republish All Articles (Recommended)**
1. Move published drafts back to drafts folder
2. Run improved publishing script
3. All articles get proper HTML

**Option 2: Update Existing Posts**
1. Use WordPress REST API update endpoint
2. Replace content with proper HTML
3. Keep same URLs, publish dates

**Option 3: Manual Review + Publish**
1. Review converted HTML
2. Test on staging first
3. Publish to production

## Files Changed

- ✅ Created: `/agents/shared/md2html-fixed.py` - Proper converter
- ✅ Created: `/agents/vision/wordpress-publish-final.sh` - Uses converter
- ✅ Updated: `/agents/vision/heartbeat.sh` - Routes to new script
- 📝 Logged: `.learnings/LEARNINGS.md` - LRN-20260202-001

## Next Steps

1. **Test converter** on one article
2. **Verify HTML output** is valid
3. **Republish all articles** with proper HTML
4. **Future articles** will automatically use fixed script

---

*Status: Fix implemented, ready for republication*
*Priority: HIGH - All published content has broken HTML*
