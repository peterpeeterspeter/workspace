#!/bin/bash
# Fix Affiliate Links - Republish articles with corrected HTML
# This script fixes affiliate links that are missing the https:// protocol

LOG_FILE="/root/.openclaw/workspace/tasks/logs/fix-affiliate-links-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== Affiliate Link Fix Script ===" | tee -a "$LOG_FILE"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# WordPress credentials (from existing scripts)
WP_USER="peter"

# Array of sites with their credentials
declare -A SITES=(
  ["crashcasino.io"]="https://crashcasino.io|3vRhtTs2khfdLtTiDFqkdeXI"
  ["cryptocrashgambling.com"]="https://cryptocrashgambling.com|bHhPmhNmCxRCrWCKDpRfExDJ"
  ["crashgamegambling.com"]="https://crashgamegambling.com|dPJmSwdHrZLBYaPTJMxBxAyu"
  ["freecrashgames.com"]="https://freecrashgames.com|kXjRQplGgMdNeUOSCZqKyGHH"
)

TOTAL_FIXED=0
TOTAL_FAILED=0
TOTAL_CHECKED=0

for SITE in "${!SITES[@]}"; do
  IFS='|' read -r WP_URL WP_APP <<< "${SITES[$SITE]}"
  
  echo "=== Processing site: ${SITE} ===" | tee -a "$LOG_FILE"
  echo "URL: ${WP_URL}" | tee -a "$LOG_FILE"
  
  # Fetch all published posts
  echo "Fetching published posts..." | tee -a "$LOG_FILE"
  POSTS_JSON=$(curl -s "${WP_URL}/wp-json/wp/v2/posts?per_page=100&status=publish" \
    --user "${WP_USER}:${WP_APP}" 2>&1)
  
  # Check if request succeeded
  if echo "$POSTS_JSON" | grep -q "code.*rest_cookie_invalid_nonce\|code.*rest_authentication_error" 2>/dev/null; then
    echo "ERROR: Authentication failed for ${SITE}" | tee -a "$LOG_FILE"
    continue
  fi
  
  POST_COUNT=$(echo "$POSTS_JSON" | jq '. | length' 2>/dev/null || echo "0")
  echo "Found ${POST_COUNT} posts" | tee -a "$LOG_FILE"
  
  if [ "$POST_COUNT" -eq 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    continue
  fi
  
  # Check each post for broken affiliate links
  for i in $(seq 0 $((POST_COUNT - 1))); do
    POST=$(echo "$POSTS_JSON" | jq ".[$i]")
    POST_ID=$(echo "$POST" | jq -r '.id')
    POST_TITLE=$(echo "$POST" | jq -r '.title.rendered')
    POST_CONTENT=$(echo "$POST" | jq -r '.content.rendered')
    
    ((TOTAL_CHECKED++))
    
    # Check for broken affiliate links (href without protocol but has domain-like pattern)
    # Pattern: href="domain.com" or href="domain.com/path" (no http:// or https://)
    if echo "$POST_CONTENT" | grep -qE 'href="[a-z0-9][a-z0-9.-]*\.[a-z]{2,}[^/"]*' 2>/dev/null; then
      echo "  Post #${POST_ID}: ${POST_TITLE}" | tee -a "$LOG_FILE"
      echo "    Has broken affiliate links" | tee -a "$LOG_FILE"
      
      # Fix broken affiliate links
      FIXED_CONTENT=$(echo "$POST_CONTENT" | python3 -c "
import sys
import re

html = sys.stdin.read()

# Fix broken affiliate links - add https:// to href values that look like domains
def fix_href(url):
    # Add https:// if URL doesn't have a protocol and looks like a domain
    if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('/') and not url.startswith('#') and '.' in url and ' ' not in url:
        # Basic check for domain-like pattern (contains dots and no spaces)
        if re.match(r'^[a-z0-9.-]+\.[a-z]{2,}', url):
            return 'https://' + url
    return url

# Replace href attributes
html = re.sub(r'href=\"([^\"]+)\"', lambda m: f'href=\"{fix_href(m.group(1))}\"', html)

print(html, end='')
")
      
      # Escape for JSON
      ESCAPED_HTML=$(echo "$FIXED_CONTENT" | jq -Rs .)
      
      # Update post
      UPDATE_RESPONSE=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts/${POST_ID}" \
        --user "${WP_USER}:${WP_APP}" \
        -H "Content-Type: application/json" \
        -d "{\"content\": ${ESCAPED_HTML}}" 2>&1)
      
      if echo "$UPDATE_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
        echo "    ✅ Fixed post #${POST_ID}" | tee -a "$LOG_FILE"
        ((TOTAL_FIXED++))
      else
        echo "    ❌ Failed to fix post #${POST_ID}" | tee -a "$LOG_FILE"
        echo "    Error: $(echo "$UPDATE_RESPONSE" | head -1)" | tee -a "$LOG_FILE"
        ((TOTAL_FAILED++))
      fi
      
      # Rate limiting
      sleep 0.5
    fi
  done
  
  echo "" | tee -a "$LOG_FILE"
done

# Summary
echo "=== Summary ===" | tee -a "$LOG_FILE"
echo "📊 Total posts checked: ${TOTAL_CHECKED}" | tee -a "$LOG_FILE"
echo "✅ Fixed: ${TOTAL_FIXED} posts" | tee -a "$LOG_FILE"
echo "❌ Failed: ${TOTAL_FAILED} posts" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ "$TOTAL_FIXED" -gt 0 ]; then
  echo "🎉 Affiliate link fix complete! ${TOTAL_FIXED} articles updated." | tee -a "$LOG_FILE"
  exit 0
elif [ "$TOTAL_CHECKED" -gt 0 ]; then
  echo "✅ All posts checked - no broken links found!" | tee -a "$LOG_FILE"
  exit 0
else
  echo "⚠️  No posts processed" | tee -a "$LOG_FILE"
  exit 1
fi
