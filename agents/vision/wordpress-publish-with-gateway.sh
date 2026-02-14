#!/bin/bash
# WordPress Publishing with Pinch-to-Post Gateway
# MANDATORY quality checks before publishing

TASK_ID=$1
TASK_TITLE=$2

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR}/${TASK_ID}.log"

GATEWAY="/root/.openclaw/workspace/scripts/publish-gateway.sh"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "Vision: WordPress Publishing with Pinch-to-Post Gateway" | tee -a "$LOG_FILE"
echo "Task: ${TASK_TITLE}" | tee -a "$LOG_FILE"

# Find draft articles
DRAFT_DIR="/root/.openclaw/workspace/drafts"

if [ ! -d "$DRAFT_DIR" ]; then
  echo "ERROR: Drafts directory not found: ${DRAFT_DIR}" | tee -a "$LOG_FILE"
  exit 1
fi

DRAFT_COUNT=$(find "$DRAFT_DIR" -name "*.md" -type f | wc -l)
echo "Found ${DRAFT_COUNT} draft articles" | tee -a "$LOG_FILE"

if [ "$DRAFT_COUNT" -eq 0 ]; then
  echo "ERROR: No draft articles found" | tee -a "$LOG_FILE"
  exit 1
fi

PUBLISHED_COUNT=0
FAILED_COUNT=0
BLOCKED_COUNT=0

# Site mapping (from draft filename to site slug)
declare -A SITE_MAP
SITE_MAP["crashcasino"]="crashcasino"
SITE_MAP["crashgame"]="crashgame"
SITE_MAP["freecrash"]="freecrash"
SITE_MAP["cryptocrash"]="cryptocrash"
SITE_MAP["aviatorcrash"]="crashcasino"  # Fallback

# Process each draft
for draft_file in "$DRAFT_DIR"/*.md; do
  if [ ! -f "$draft_file" ]; then
    continue
  fi

  draft_name=$(basename "$draft_file" .md)
  echo "" | tee -a "$LOG_FILE"
  echo "═══════════════════════════════════════════════════════" | tee -a "$LOG_FILE"
  echo "Processing: ${draft_name}" | tee -a "$LOG_FILE"

  # Extract metadata from draft
  TITLE=$(grep -m1 "^# " "$draft_file" | sed 's/^# //')
  META_DESC=$(grep -i "^**Meta Description:**" "$draft_file" | sed 's/\*\*Meta Description:\*\* *//i' | xargs)
  FOCUS_KW=$(grep -i "^**Primary Keyword:**" "$draft_file" | sed 's/\*\*Primary Keyword:\*\* *//i' | xargs)

  # Determine target site from filename
  TARGET_SITE="crashcasino"  # Default

  if [[ "$draft_name" == *"crashgame"* ]]; then
    TARGET_SITE="crashgame"
  elif [[ "$draft_name" == *"freecrash"* ]]; then
    TARGET_SITE="freecrash"
  elif [[ "$draft_name" == *"cryptocrash"* ]]; then
    TARGET_SITE="cryptocrash"
  elif [[ "$draft_name" == *"aviator"* ]]; then
    TARGET_SITE="crashcasino"  # Aviator blocked, use default for now
  fi

  echo "Title: ${TITLE}" | tee -a "$LOG_FILE"
  echo "Site: ${TARGET_SITE}" | tee -a "$LOG_FILE"

  # Step 1: Create draft via REST API
  echo "" | tee -a "$LOG_FILE"
  echo "Step 1: Creating draft post..." | tee -a "$LOG_FILE"

  # Convert markdown to HTML
  HTML_RESULT=$(python3 /root/.openclaw/workspace/agents/shared/md2html-fixed.py "$draft_file" 2>> "$LOG_FILE")

  if ! echo "$HTML_RESULT" | jq -e '.html' > /dev/null 2>&1; then
    echo "❌ ERROR: Failed to convert markdown" | tee -a "$LOG_FILE"
    ((FAILED_COUNT++))
    continue
  fi

  HTML_CONTENT=$(echo "$HTML_RESULT" | jq -r '.html // empty')

  # Get site credentials
  case $TARGET_SITE in
    crashcasino)
      WP_URL="https://crashcasino.io/wp-json"
      WP_USER="peter"
      WP_PASS="3vRhtTs2khfdLtTiDFqkdeXI"
      ;;
    crashgame)
      WP_URL="https://crashgamegambling.com/wp-json"
      WP_USER="peter"
      WP_PASS="MioX SygN Xaz6 pK9o RUiK tBMF"
      ;;
    freecrash)
      WP_URL="https://freecrashgames.com/wp-json"
      WP_USER="peter"
      WP_PASS="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      ;;
    cryptocrash)
      WP_URL="https://cryptocrashgambling.com/wp-json"
      WP_USER="peter"
      WP_PASS="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      ;;
    *)
      echo "❌ ERROR: Unknown site: ${TARGET_SITE}" | tee -a "$LOG_FILE"
      ((FAILED_COUNT++))
      continue
      ;;
  esac

  # Create draft
  POST_RESPONSE=$(curl -s -X POST "${WP_URL}/wp/v2/posts" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{
      \"title": \"${TITLE}\",
      \"content\": ${HTML_CONTENT},
      \"status\": \"draft\",
      \"meta\": {
        \"_yoast_wpseo_title\": \"${TITLE}\",
        \"_yoast_wpseo_metadesc\": \"${META_DESC}\",
        \"_yoast_wpseo_focuskw\": \"${FOCUS_KW}\"
      }
    }" 2>> "$LOG_FILE")

  POST_ID=$(echo "$POST_RESPONSE" | jq -r '.id // empty')

  if [ -z "$POST_ID" ] || [ "$POST_ID" = "null" ]; then
    echo "❌ ERROR: Failed to create draft" | tee -a "$LOG_FILE"
    echo "Response: ${POST_RESPONSE}" | tee -a "$LOG_FILE"
    ((FAILED_COUNT++))
    continue
  fi

  echo "✅ Draft created: Post #${POST_ID}" | tee -a "$LOG_FILE"

  # Step 2: Run health check
  echo "" | tee -a "$LOG_FILE"
  echo "Step 2: Running health check via gateway..." | tee -a "$LOG_FILE"

  HEALTH_CHECK=$("$GATEWAY" check "$POST_ID" "$TARGET_SITE" 2>&1)

  echo "$HEALTH_CHECK" | tee -a "$LOG_FILE"

  # Extract score from health check
  SCORE=$(echo "$HEALTH_CHECK" | grep "Health Score:" | sed 's/.*Health Score: //' | sed 's/\/100.*//')

  if [ -z "$SCORE" ]; then
    echo "⚠️  WARNING: Could not extract score, attempting publish..." | tee -a "$LOG_FILE"
    SCORE=0
  fi

  echo "Score: ${SCORE}/100" | tee -a "$LOG_FILE"

  # Step 3: Publish if score is 80+
  if [ "$SCORE" -ge 80 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "Step 3: Publishing article (score ${SCORE}/100)..." | tee -a "$LOG_FILE"

    PUBLISH_RESULT=$("$GATEWAY" publish "$POST_ID" "$TARGET_SITE" 2>&1)

    if echo "$PUBLISH_RESULT" | grep -q "published successfully"; then
      echo "✅ Article published!" | tee -a "$LOG_FILE"
      LINK=$(echo "$PUBLISH_RESULT" | grep "Link:" | sed 's/.*Link: //')
      echo "Link: ${LINK}" | tee -a "$LOG_FILE"

      # Move draft to published
      mv "$draft_file" "${DRAFT_DIR}/published/${draft_name}.md" 2>/dev/null || \
        mv "$draft_file" "${DRAFT_DIR}/${draft_name}.published.md"

      ((PUBLISHED_COUNT++))
    else
      echo "❌ ERROR: Publish failed" | tee -a "$LOG_FILE"
      echo "$PUBLISH_RESULT" | tee -a "$LOG_FILE"
      ((FAILED_COUNT++))
    fi
  else
    echo "" | tee -a "$LOG_FILE"
    echo "⚠️  Article BLOCKED (score ${SCORE}/100, needs 80+)" | tee -a "$LOG_FILE"
    echo "Draft saved as: ${draft_file}" | tee -a "$LOG_FILE"
    echo "To fix manually, add:" | tee -a "$LOG_FILE"
    echo "  - Meta description (if missing)" | tee -a "$LOG_FILE"
    echo "  - Featured image" | tee -a "$LOG_FILE"
    echo "  - Images in content" | tee -a "$LOG_FILE"
    echo "  - Focus keyword (if missing)" | tee -a "$LOG_FILE"
    echo "  - H2 headings (if less than 2)" | tee -a "$LOG_FILE"
    ((BLOCKED_COUNT++))
  fi

  echo "" | tee -a "$LOG_FILE"
done

# Summary
echo "" | tee -a "$LOG_FILE"
echo "═══════════════════════════════════════════════════════" | tee -a "$LOG_FILE"
echo "Publishing Summary" | tee -a "$LOG_FILE"
echo "═══════════════════════════════════════════════════════" | tee -a "$LOG_FILE"
echo "Total drafts: ${DRAFT_COUNT}" | tee -a "$LOG_FILE"
echo "✅ Published: ${PUBLISHED_COUNT}" | tee -a "$LOG_FILE"
echo "⚠️  Blocked (low quality): ${BLOCKED_COUNT}" | tee -a "$LOG_FILE"
echo "❌ Failed (errors): ${FAILED_COUNT}" | tee -a "$LOG_FILE"
echo "═══════════════════════════════════════════════════════" | tee -a "$LOG_FILE"

if [ "$PUBLISHED_COUNT" -gt 0 ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "🎉 Successfully published ${PUBLISHED_COUNT} articles!" | tee -a "$LOG_FILE"
fi

if [ "$BLOCKED_COUNT" -gt 0 ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "⚠️  ${BLOCKED_COUNT} articles blocked for quality issues." | tee -a "$LOG_FILE"
  echo "Review blocked drafts and fix issues before retrying." | tee -a "$LOG_FILE"
fi

exit 0
