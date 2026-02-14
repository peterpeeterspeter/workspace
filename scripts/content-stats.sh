#!/bin/bash
# 🦞 Pinch-to-Post: Content Stats Reporter
# Shows statistics across all sites

echo "=== Content Statistics: $(date +%Y-%m-%d) ==="
echo ""

sites=("crashcasino" "crashgame" "freecrash" "cryptocrash")

for site in "${sites[@]}"; do
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

  echo "## 📍 $name"

  # Get stats
  publish=$(curl -s "${url}/wp/v2/posts?per_page=1&status=publish" -u "${user}:${pass}" | jq -r '.headers | ."X-WP-Total" // "0"')
  draft=$(curl -s "${url}/wp/v2/posts?per_page=1&status=draft" -u "${user}:${pass}" | jq -r '.headers | ."X-WP-Total" // "0"')

  echo "Posts (publish): $publish"
  echo "Posts (draft): $draft"
  echo ""
done

echo "=== End of Stats ==="
