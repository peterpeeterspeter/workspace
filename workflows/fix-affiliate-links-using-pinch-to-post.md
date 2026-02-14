# Workflow: Fix Affiliate Links Using Pinch-to-Post

## Problem
Affiliate links in published WordPress articles were missing the `https://` protocol, causing them to be treated as relative URLs:
- **Broken:** `<a href="cybetplay.com/tluy6cbpp">`
- **Result:** URL becomes `https://crashcasino.io/post-slug/cybetplay.com/tluy6cbpp` (404 error)

## Root Cause
The `md2html-fixed.py` converter was not adding protocols to URLs that lacked them.

## Solution (Using Pinch-to-Post Skill)

### Step 1: Fix Root Cause
✅ **Already done** - Updated `/root/.openclaw/workspace/agents/shared/md2html-fixed.py`

The `process_inline()` function now automatically adds `https://` to domain-like URLs:
```python
def fix_link(match):
    link_text = match.group(1)
    url = match.group(2)
    if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('/'):
        if '.' in url and ' ' not in url:
            url = 'https://' + url
    return f'<a href="{url}">{link_text}</a>'
```

### Step 2: Fix Published Articles (Using Pinch-to-Post)

For each site that has broken links:

```bash
# 1. Get posts with broken links
POSTS=$(curl -s -u "peter:${APP_PASSWORD}" "${SITE_URL}/wp-json/wp/v2/posts?per_page=100" | jq -r '.[] | select(.content.rendered | contains("href=\"cybetplay.com") or contains("href=\"trustdice.win") or contains("href=\"bitstarz")) | .id')

# 2. For each post, fetch content, fix links, update
for POST_ID in $POSTS; do
  # Fetch current content
  CONTENT=$(curl -s -u "peter:${APP_PASSWORD}" "${SITE_URL}/wp-json/wp/v2/posts/${POST_ID}" | jq -r '.content.rendered')

  # Fix links using Python
  FIXED_CONTENT=$(echo "$CONTENT" | python3 -c "
import sys, re
html = sys.stdin.read()
def fix_href(url):
    if not url.startswith('http') and not url.startswith('/') and '.' in url and ' ' not in url:
        if re.match(r'^[a-z0-9.-]+\.[a-z]{2,}', url):
            return 'https://' + url
    return url
html = re.sub(r'href=\"([^\"]+)\"', lambda m: f'href=\"{fix_href(m.group(1))}\"', html)
print(html, end='')
")

  # Update using pinch-to-post
  ESCAPED_HTML=$(echo "$FIXED_CONTENT" | jq -Rs .)
  curl -s -u "peter:${APP_PASSWORD}" -X POST "${SITE_URL}/wp-json/wp/v2/posts/${POST_ID}" \
    -H "Content-Type: application/json" \
    -d "{\"content\": ${ESCAPED_HTML}}"
done
```

### Step 3: Verify Fix

```bash
# Check a fixed post
curl -s "${SITE_URL}/wp-json/wp/v2/posts/POST_ID" | jq -r '.content.rendered' | grep "href=\"cybetplay.com"
# Should return: <a href="https://cybetplay.com/tluy6cbpp">
```

## Sites Status

| Site | Status | Notes |
|------|--------|-------|
| crashcasino.io | ✅ Fixed (4 posts) | All links have https:// |
| cryptocrashgambling.com | ✅ Clean | No broken links found |
| crashgamegambling.com | ✅ Clean | No broken links found |
| freecrashgames.com | ⚠️ Pending | Need to fix post #51358 |

## Future Prevention

All new articles published via the updated `md2html-fixed.py` will automatically have `https://` added to affiliate links.

## Commands Reference (Pinch-to-Post)

```bash
# List posts
WP_SITE_URL="https://SITE_URL" WP_USERNAME="peter" WP_APP_PASSWORD="PASSWORD" \
  /root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh list-posts 20

# Get post content
WP_SITE_URL="https://SITE_URL" WP_USERNAME="peter" WP_APP_PASSWORD="PASSWORD" \
  /root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh get-post POST_ID

# Update post (example)
WP_SITE_URL="https://SITE_URL" WP_USERNAME="peter" WP_APP_PASSWORD="PASSWORD" \
  /root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh update-post POST_ID content="<p>New HTML content</p>"
```

## Environment Variables Needed

```bash
export CRASHCASINO_APP_PASSWORD="3vRhtTs2khfdLtTiDFqkdeXI"
export CRYPTOCRASH_APP_PASSWORD="bHhPmhNmCxRCrWCKDpRfExDJ"
export CRASHGAME_APP_PASSWORD="dPJmSwdHrZLBYaPTJMxBxAyu"
export FREECRASHGAMES_APP_PASSWORD="kXjRQplGgMdNeUOSCZqKyGHH"
```

---

**Created:** 2026-02-03
**Last Updated:** 2026-02-03
**Status:** Root cause fixed, bulk fixes in progress
