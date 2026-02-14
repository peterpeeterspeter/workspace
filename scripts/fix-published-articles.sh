#!/bin/bash
# 🦞 Pinch-to-Post: Fix All Published Articles
# Adds meta descriptions, focus keywords, improves quality of published articles

GATEWAY="/root/.openclaw/workspace/scripts/publish-gateway.sh"
LOG="/root/.openclaw/workspace/logs/fix-published-articles.log"
BACKUP_DIR="/root/.openclaw/workspace/backups/published-articles-$(date +%Y%m%d)"

mkdir -p "$BACKUP_DIR"

echo "=== Fixing Published Articles: $(date) ===" | tee -a "$LOG"
echo "Backup dir: $BACKUP_DIR" | tee -a "$LOG"
echo "" | tee -a "$LOG"

sites=("crashcasino" "crashgame" "freecrash" "cryptocrash")

total_fixed=0
total_failed=0

for site in "${sites[@]}"; do
  echo "## 📍 Site: $site" | tee -a "$LOG"

  # Get credentials
  case $site in
    crashcasino)
      url="https://crashcasino.io/wp-json"
      user="peter"
      pass="3vRhtTs2khfdLtTiDFqkdeXI"
      name="crashcasino.io"
      ;;
    crashgame)
      url="https://crashgamegambling.com/wp-json"
      user="peter"
      pass="MioX SygN Xaz6 pK9o RUiK tBMF"
      name="crashgamegambling.com"
      ;;
    freecrash)
      url="https://freecrashgames.com/wp-json"
      user="peter"
      pass="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      name="freecrashgames.com"
      ;;
    cryptocrash)
      url="https://cryptocrashgambling.com/wp-json"
      user="peter"
      pass="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      name="cryptocrashgambling.com"
      ;;
  esac

  # Get published posts
  posts=$(curl -s "${url}/wp/v2/posts?per_page=100&status=publish" -u "${user}:${pass}")

  count=$(echo "$posts" | jq 'length')
  echo "Found $count published posts" | tee -a "$LOG"

  # Process each post
  echo "$posts" | jq -r '.[] | @json' | while read -r post; do
    id=$(echo "$post" | jq -r '.id')
    title=$(echo "$post" | jq -r '.title.rendered')
    link=$(echo "$post" | jq -r '.link')

    echo "" | tee -a "$LOG"
    echo "Processing #$id: $title" | tee -a "$LOG"

    # Backup current state
    echo "$post" > "$BACKUP_DIR/${site}-${id}.json"

    # Get current metadata
    yoast_desc=$(echo "$post" | jq -r '.meta._yoast_wpseo_metadesc // "null"')
    yoast_focuskw=$(echo "$post" | jq -r '.meta._yoast_wpseo_focuskw // "null"')
    content=$(echo "$post" | jq -r '.content.rendered')

    # Extract first paragraph for meta description
    first_para=$(echo "$content" | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g' | sed 's/&nbsp;/ /g' | tr -s ' ' | cut -c1-155)
    if [ ${#first_para} -gt 100 ]; then
      first_para="${first_para}..."
    fi

    # Extract focus keyword from title
    focus_kw=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | rev | cut -d' ' -f1 | rev)

    # Update post with meta data
    update=$(curl -s -X POST "${url}/wp/v2/posts/${id}" \
      -u "${user}:${pass}" \
      -H "Content-Type: application/json" \
      -d "{
        \"meta\": {
          \"_yoast_wpseo_metadesc\": \"${first_para}\",
          \"_yoast_wpseo_focuskw\": \"${focus_kw}\"
        }
      }")

    # Check if update succeeded
    if [ $? -eq 0 ]; then
      echo "  ✅ Added meta description and focus keyword" | tee -a "$LOG"
      echo "     Meta: ${first_para}" | tee -a "$LOG"
      echo "     Focus: ${focus_kw}" | tee -a "$LOG"
      total_fixed=$((total_fixed + 1))
    else
      echo "  ❌ Failed to update #$id" | tee -a "$LOG"
      total_failed=$((total_failed + 1))
    fi
  done

  echo "" | tee -a "$LOG"
done

echo "=== Summary ===" | tee -a "$LOG"
echo "Fixed: $total_fixed" | tee -a "$LOG"
echo "Failed: $total_failed" | tee -a "$LOG"
echo "Backup: $BACKUP_DIR" | tee -a "$LOG"
