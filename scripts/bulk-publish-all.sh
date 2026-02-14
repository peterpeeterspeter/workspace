#!/bin/bash
# 🦞 Pinch-to-Post: Bulk Publish All Drafts
# Publishes all draft articles that meet quality threshold (80+)

GATEWAY="/root/.openclaw/workspace/scripts/publish-gateway.sh"
DRAFT_DIR="/root/.openclaw/workspace/drafts"
LOG="/root/.openclaw/workspace/logs/bulk-publish.log"

echo "=== Bulk Publish Started: $(date) ===" | tee -a "$LOG"

total=0
published=0
blocked=0
failed=0

# Find all draft files
for draft in "$DRAFT_DIR"/*.md; do
  [ ! -f "$draft" ] && continue

  total=$((total + 1))
  draft_name=$(basename "$draft" .md)
  echo "" | tee -a "$LOG"
  echo "[$total] Processing: $draft_name" | tee -a "$LOG"

  # Determine site from filename
  if [[ "$draft_name" == *"crashgame"* ]]; then
    site="crashgame"
  elif [[ "$draft_name" == *"freecrash"* ]]; then
    site="freecrash"
  elif [[ "$draft_name" == *"cryptocrash"* ]]; then
    site="cryptocrash"
  else
    site="crashcasino"
  fi

  # Create draft via WordPress
  title=$(grep -m1 "^# " "$draft" | sed 's/^# //')
  content=$(cat "$draft")

  # Get credentials
  case $site in
    crashcasino)
      url="https://crashcasino.io/wp-json"
      user="peter"
      pass="3vRhtTs2khfdLtTiDFqkdeXI"
      ;;
    crashgame)
      url="https://crashgamegambling.com/wp-json"
      user="peter"
      pass="MioX SygN Xaz6 pK9o RUiK tBMF"
      ;;
    freecrash)
      url="https://freecrashgames.com/wp-json"
      user="peter"
      pass="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      ;;
    cryptocrash)
      url="https://cryptocrashgambling.com/wp-json"
      user="peter"
      pass="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      ;;
  esac

  # Create draft
  response=$(curl -s -X POST "${url}/wp/v2/posts" \
    -u "${user}:${pass}" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"${title}\", \"content\": \"${content}\", \"status\": \"draft\"}")

  post_id=$(echo "$response" | jq -r '.id // empty')

  if [ -z "$post_id" ] || [ "$post_id" = "null" ]; then
    echo "❌ Failed to create draft" | tee -a "$LOG"
    failed=$((failed + 1))
    continue
  fi

  echo "Draft created: #$post_id" | tee -a "$LOG"

  # Run health check
  health=$("$GATEWAY" check "$post_id" "$site" 2>&1)
  score=$(echo "$health" | grep "Health Score:" | sed 's/.*Health Score: //' | sed 's/\/100.*//')

  if [ "$score" -ge 80 ]; then
    # Publish
    result=$("$GATEWAY" publish "$post_id" "$site" 2>&1)
    if echo "$result" | grep -q "published successfully"; then
      echo "✅ Published: #$post_id (score: $score)" | tee -a "$LOG"
      published=$((published + 1))
      mv "$draft" "$DRAFT_DIR/published/"
    else
      echo "❌ Publish failed: #$post_id" | tee -a "$LOG"
      failed=$((failed + 1))
    fi
  else
    echo "⚠️  Blocked: #$post_id (score: $score, needs 80+)" | tee -a "$LOG"
    blocked=$((blocked + 1))
  fi
done

echo "" | tee -a "$LOG"
echo "=== Bulk Publish Complete ===" | tee -a "$LOG"
echo "Total: $total" | tee -a "$LOG"
echo "Published: $published" | tee -a "$LOG"
echo "Blocked: $blocked" | tee -a "$LOG"
echo "Failed: $failed" | tee -a "$LOG"
