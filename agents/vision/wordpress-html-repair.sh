#!/bin/bash
# Direct HTML Fix - Updates published posts with proper HTML structure
# Repairs broken HTML tags without needing original markdown files

PUBLISHED_DIR="/root/.openclaw/workspace/drafts/published"
LOG_FILE="/root/.openclaw/workspace/tasks/logs/html-repair-fix.log"

mkdir -p "$PUBLISHED_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== WordPress HTML Repair ===" | tee -a "$LOG_FILE"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# WordPress credentials
WP_URL="https://crashcasino.io"
WP_USER="peter"
WP_APP="3vRhtTs2khfdLtTiDFqkdeXI"

# Get all published posts
echo "Fetching published posts..." | tee -a "$LOG_FILE"
POSTS_JSON=$(curl -s "${WP_URL}/wp-json/wp/v2/posts?per_page=100&status=publish" \
  --user "${WP_USER}:${WP_APP}")

POST_COUNT=$(echo "$POSTS_JSON" | jq '. | length')
echo "Found ${POST_COUNT} posts to check" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

REPAIRED_COUNT=0
FAILED_COUNT=0

# Process each post
for i in $(seq 0 $((POST_COUNT - 1))); do
  POST=$(echo "$POSTS_JSON" | jq ".[$i]")
  POST_ID=$(echo "$POST" | jq -r '.id')
  POST_TITLE=$(echo "$POST" | jq -r '.title.rendered')
  POST_CONTENT=$(echo "$POST" | jq -r '.content.rendered')

  echo "[$((i+1))/${POST_COUNT}] Post ID: ${POST_ID}" | tee -a "$LOG_FILE"
  echo "    Title: ${POST_TITLE}" | tee -a "$LOG_FILE"

  # Check if HTML is broken
  # Look for common broken patterns
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

  # Save current content to file for reconstruction
  TEMP_MD="$PUBLISHED_DIR/post-${POST_ID}.md"
  
  # Reconstruct markdown from broken HTML
  # Convert broken HTML patterns back to markdown
  MD_CONTENT=$(echo "$POST_CONTENT" | python3 -c "
import sys
import re
import html

html_content = sys.stdin.read()

# Fix common broken patterns
# 1. Convert <h1>text</p> to # text
html_content = re.sub(r'<h1[^>]*>([^<]*)</p>', r'# \1\n', html_content)

# 2. Convert <h2>text</p> to ## text
html_content = re.sub(r'<h2[^>]*>([^<]*)</p>', r'## \1\n', html_content)

# 3. Convert <p><h2>text</p> to ## text
html_content = re.sub(r'<p><h2[^>]*>([^<]*)</p>', r'## \1\n', html_content)

# 4. Convert <p>| tables to markdown tables
html_content = re.sub(r'<p>\|([^|]+)\|([^|]+)\|([^|]+)\|</p>', r'|\1|\2|\3|', html_content)

# 5. Convert <p><li> to - list items
html_content = re.sub(r'<p><li[^>]*>([^<]*)</li></p>', r'- \1\n', html_content)
html_content = re.sub(r'<li[^>]*>([^<]*)</li>', r'- \1\n', html_content)

# 6. Convert <strong> to **
html_content = re.sub(r'<strong>([^<]*)</strong>', r'**\1**', html_content)

# 7. Convert <em> to *
html_content = re.sub(r'<em>([^<]*)</em>', r'*\1*', html_content)

# 8. Convert <a href> to markdown links
html_content = re.sub(r'<a href=\"([^\"]+)\">([^<]*)</a>', r'[\2](\1)', html_content)

# 9. Remove remaining HTML tags but keep content
html_content = re.sub(r'<p>([^<]*)</p>', r'\1\n', html_content)
html_content = re.sub(r'<[^>]+>', '', html_content)

# 10. Clean up multiple newlines
html_content = re.sub(r'\n{3,}', '\n\n', html_content)

# 11. Decode HTML entities
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
    ((FAILED_COUNT++))
    rm -f "$TEMP_MD"
    echo "" | tee -a "$LOG_FILE"
    continue
  fi

  # Extract HTML
  PROPER_HTML=$(echo "$HTML_RESULT" | jq -r '.html')

  # Escape for JSON
  ESCAPED_HTML=$(echo "$PROPER_HTML" | jq -Rs .)

  echo "    Updating post ${POST_ID}..." | tee -a "$LOG_FILE"

  # Update post
  UPDATE_RESPONSE=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts/${POST_ID}" \
    --user "${WP_USER}:${WP_APP}" \
    -H "Content-Type: application/json" \
    -d "{
      \"content\": ${ESCAPED_HTML}
    }" 2>&1)

  if echo "$UPDATE_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
    echo "    ✅ SUCCESS: HTML repaired and updated" | tee -a "$LOG_FILE"
    ((REPAIRED_COUNT++))
  else
    echo "    ❌ ERROR: Update failed" | tee -a "$LOG_FILE"
    echo "    ${UPDATE_RESPONSE}" | tee -a "$LOG_FILE"
    ((FAILED_COUNT++))
  fi

  # Clean up temp file
  rm -f "$TEMP_MD"
  
  echo "" | tee -a "$LOG_FILE"
  sleep 1
done

# Summary
echo "=== Repair Summary ===" | tee -a "$LOG_FILE"
echo "✅ Repaired: ${REPAIRED_COUNT}" | tee -a "$LOG_FILE"
echo "❌ Failed: ${FAILED_COUNT}" | tee -a "$LOG_FILE"
echo "📊 Total processed: $((REPAIRED_COUNT + FAILED_COUNT))" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ "$REPAIRED_COUNT" -gt 0 ]; then
  echo "🎉 HTML repair complete! ${REPAIRED_COUNT} articles fixed." | tee -a "$LOG_FILE"
  exit 0
else
  echo "⚠️  No articles needed repair" | tee -a "$LOG_FILE"
  exit 0
fi
