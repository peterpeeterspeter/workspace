#!/bin/bash
# 🦞 Pinch-to-Post: Comment Moderation
# Approves good comments, marks spam, deletes trash

GATEWAY="/root/.openclaw/workspace/scripts/publish-gateway.sh"

echo "=== Comment Moderation: $(date) ==="
echo ""

sites=("crashcasino" "crashgame" "freecrash" "cryptocrash")

total_approved=0
total_spam=0

for site in "${sites[@]}"; do
  echo "## Moderating: $site"

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

  # Get pending comments
  comments=$(curl -s "${url}/wp/v2/comments?status=hold&per_page=100" -u "${user}:${pass}")

  count=$(echo "$comments" | jq 'length')
  echo "Found $count pending comments"

  # Moderate each comment
  echo "$comments" | jq -r '.[] | @json' | while read -r comment; do
    id=$(echo "$comment" | jq -r '.id')
    content=$(echo "$comment" | jq -r '.content.rendered' | sed 's/<[^>]*>//g')
    author=$(echo "$comment" | jq -r '.author_name')

    # Simple spam detection
    if echo "$content" | grep -qiE "casino|gambling|bet|slot|poker|lottery|viagra|crypto"; then
      # Mark as spam
      curl -s -X POST "${url}/wp/v2/comments/${id}" -u "${user}:${pass}" \
        -H "Content-Type: application/json" -d '{"status": "spam"}' > /dev/null
      echo "  ❌ SPAM: $author - ${content:0:50}..."
      total_spam=$((total_spam + 1))
    else
      # Approve
      curl -s -X POST "${url}/wp/v2/comments/${id}" -u "${user}:${pass}" \
        -H "Content-Type: application/json" -d '{"status": "approved"}' > /dev/null
      echo "  ✅ APPROVED: $author - ${content:0:50}..."
      total_approved=$((total_approved + 1))
    fi
  done

  echo ""
done

echo "=== Moderation Complete ==="
echo "Approved: $total_approved"
echo "Marked spam: $total_spam"
