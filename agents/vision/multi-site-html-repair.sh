#!/bin/bash
# Multi-Site WordPress HTML Repair - Fixes broken HTML on ALL sites
# Repairs broken HTML tags and adds metadata to crashcasino.io, crashgamegambling.com, cryptocrashgambling.com, freecrashgames.com

LOG_FILE="/root/.openclaw/workspace/tasks/logs/multi-site-repair.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== Multi-Site WordPress HTML Repair ===" | tee -a "$LOG_FILE"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Define all sites
declare -A SITES
SITES[crashcasino.io]="https://crashcasino.io|${WORDPRESS_CRASHCASINO_APP_PASSWORD}|Reviews"
SITES[crashgamegambling.com]="https://crashgamegambling.com|${WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD}|Strategy"
SITES[cryptocrashgambling.com]="https://cryptocrashgambling.com|${WORDPRESS_CRYPTOCRASH_APP_PASSWORD}|Bitcoin"
SITES[freecrashgames.com]="https://freecrashgames.com|${WORDPRESS_FREECRASH_APP_PASSWORD}|Bonuses"

# Process each site
TOTAL_REPAIRED=0
TOTAL_FAILED=0

for SITE_KEY in "${!SITES[@]}"; do
  IFS='|' read -r SITE_URL SITE_APP SITE_CATEGORY <<< "${SITES[$SITE_KEY]}"
  
  if [ -z "$SITE_APP" ]; then
    echo "⚠️  Skipping ${SITE_KEY} - No credentials" | tee -a "$LOG_FILE"
    continue
  fi

  echo "" | tee -a "$LOG_FILE"
  echo "========================================" | tee -a "$LOG_FILE"
  echo "Processing: ${SITE_KEY}" | tee -a "$LOG_FILE"
  echo "========================================" | tee -a "$LOG_FILE"
  
  # Get all published posts
  echo "Fetching posts from ${SITE_KEY}..." | tee -a "$LOG_FILE"
  
  POSTS_JSON=$(curl -s "${SITE_URL}/wp-json/wp/v2/posts?per_page=100&status=publish" \
    --user "peter:${SITE_APP}")
  
  if echo "$POSTS_JSON" | jq -e '.[0].id' > /dev/null 2>&1; then
    POST_COUNT=$(echo "$POSTS_JSON" | jq '. | length')
    echo "Found ${POST_COUNT} posts" | tee -a "$LOG_FILE"
  else
    echo "ERROR: Failed to fetch posts" | tee -a "$LOG_FILE"
    ((TOTAL_FAILED++))
    continue
  fi

  # Process each post
  SITE_REPAIRED=0
  SITE_FAILED=0

  for i in $(seq 0 $((POST_COUNT - 1))); do
    POST=$(echo "$POSTS_JSON" | jq ".[$i]")
    POST_ID=$(echo "$POST" | jq -r '.id')
    POST_TITLE=$(echo "$POST" | jq -r '.title.rendered')
    POST_CONTENT=$(echo "$POST" | jq -r '.content.rendered')

    echo "[$((i+1))/${POST_COUNT}] Post ID: ${POST_ID}" | tee -a "$LOG_FILE"
    echo "    Title: ${POST_TITLE}" | tee -a "$LOG_FILE"

    # Check if HTML is broken
    BROKEN=false

    # Check for unclosed h1/h2 tags
    if echo "$POST_CONTENT" | grep -q '<h1[^>]*>[^<]*</p>'; then
      BROKEN=true
    fi

    # Check for tables rendered as text
    if echo "$POST_CONTENT" | grep -q '<p>|[^|]*|[^|]*|</p>'; then
      BROKEN=true
    fi

    # Check for h2 inside p tags
    if echo "$POST_CONTENT" | grep -q '<p><h2'; then
      BROKEN=true
    fi

    if [ "$BROKEN" = false ]; then
      echo "    ✅ HTML looks good, skipping" | tee -a "$LOG_FILE"
      echo "" | tee -a "$LOG_FILE"
      continue
    fi

    echo "    ⚠️  Broken HTML detected, repairing..." | tee -a "$LOG_FILE"

    # Save current content to temp file for reconstruction
    TEMP_MD="/tmp/${SITE_KEY}-post-${POST_ID}.md"
    
    # Reconstruct markdown from broken HTML
    MD_CONTENT=$(echo "$POST_CONTENT" | python3 -c "
import sys
import re
import html

html_content = sys.stdin.read()

# Fix common broken patterns
html_content = re.sub(r'<h1[^>]*>([^<]*)</p>', r'# \1\n', html_content)
html_content = re.sub(r'<h2[^>]*>([^<]*)</p>', r'## \1\n', html_content)
html_content = re.sub(r'<p><h2[^>]*>([^<]*)</p>', r'## \1\n', html_content)
html_content = re.sub(r'<p>\|([^|]+)\|([^|]+)\|([^|]+)\|</p>', r'|\1|\2|\3|', html_content)
html_content = re.sub(r'<p><li[^>]*>([^<]*)</li></p>', r'- \1\n', html_content)
html_content = re.sub(r'<li[^>]*>([^<]*)</li>', r'- \1\n', html_content)
html_content = re.sub(r'<strong>([^<]*)</strong>', r'**\1**', html_content)
html_content = re.sub(r'<em>([^<]*)</em>', r'*\1*', html_content)
html_content = re.sub(r'<a href=\"([^\"]+)\">([^<]*)</a>', r'[\2](\1)', html_content)
html_content = re.sub(r'<p>([^<]*)</p>', r'\1\n', html_content)
html_content = re.sub(r'<[^>]+>', '', html_content)
html_content = re.sub(r'\n{3,}', '\n\n', html_content)
html_content = html.unescape(html_content)

print(html_content)
")

    # Save reconstructed markdown
    echo "# ${POST_TITLE}" > "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    echo "$MD_CONTENT" >> "$TEMP_MD"

    # Convert to proper HTML using fixed converter
    HTML_RESULT=$(python3 /root/.openclaw/workspace/agents/shared/md2html-fixed.py "$TEMP_MD" 2>&1)

    if ! echo "$HTML_RESULT" | jq -e '.html' > /dev/null 2>&1; then
      echo "    ❌ ERROR: Failed to convert to HTML" | tee -a "$LOG_FILE"
      ((SITE_FAILED++))
      rm -f "$TEMP_MD"
      echo "" | tee -a "$LOG_FILE"
      continue
    fi

    # Extract HTML
    PROPER_HTML=$(echo "$HTML_RESULT" | jq -r '.html')
    META_DESC=$(echo "$HTML_RESULT" | jq -r '.metadata.description // empty')

    # Escape for JSON
    ESCAPED_HTML=$(echo "$PROPER_HTML" | jq -Rs .)

    echo "    Updating post ${POST_ID} on ${SITE_KEY}..." | tee -a "$LOG_FILE"

    # Update post
    UPDATE_RESPONSE=$(curl -s -X POST "${SITE_URL}/wp-json/wp/v2/posts/${POST_ID}" \
      --user "peter:${SITE_APP}" \
      -H "Content-Type: application/json" \
      -d "{
        \"content\": ${ESCAPED_HTML},
        \"excerpt\": \"${META_DESC}\"
      }" 2>&1)

    if echo "$UPDATE_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
      echo "    ✅ SUCCESS: HTML repaired on ${SITE_KEY}" | tee -a "$LOG_FILE"
      ((SITE_REPAIRED++))
    else
      echo "    ❌ ERROR: Update failed" | tee -a "$LOG_FILE"
      echo "    ${UPDATE_RESPONSE}" | tee -a "$LOG_FILE"
      ((SITE_FAILED++))
    fi

    # Clean up temp file
    rm -f "$TEMP_MD"
    
    echo "" | tee -a "$LOG_FILE"
    sleep 1
  done

  echo "--- ${SITE_KEY} Summary ---" | tee -a "$LOG_FILE"
  echo "Repaired: ${SITE_REPAIRED}" | tee -a "$LOG_FILE"
  echo "Failed: ${SITE_FAILED}" | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"

  ((TOTAL_REPAIRED += SITE_REPAIRED))
  ((TOTAL_FAILED += SITE_FAILED))
done

# Final summary
echo "========================================" | tee -a "$LOG_FILE"
echo "=== Multi-Site Repair Summary ===" | tee -a "$LOG_FILE"
echo "✅ Total Repaired: ${TOTAL_REPAIRED}" | tee -a "$LOG_FILE"
echo "❌ Total Failed: ${TOTAL_FAILED}" | tee -a "$LOG_FILE"
echo "📊 Total Processed: $((TOTAL_REPAIRED + TOTAL_FAILED))" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ "$TOTAL_REPAIRED" -gt 0 ]; then
  echo "🎉 Multi-site HTML repair complete!" | tee -a "$LOG_FILE"
  exit 0
else
  echo "ℹ️  No repairs needed across all sites" | tee -a "$LOG_FILE"
  exit 0
fi
