#!/bin/bash
# 🦞 Pinch-to-Post: Content Calendar Viewer
# Shows publishing schedule across all sites

YEAR=${1:-$(date +%Y)}
MONTH=${2:-$(date +%m)}

echo "=== Content Calendar: $YEAR-$MONTH ==="
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

  # Get published posts
  echo "📗 Published:"
  curl -s "${url}/wp/v2/posts?after=${YEAR}-${MONTH}-01T00:00:00&before=${YEAR}-${MONTH}-31T23:59:59&per_page=100&status=publish" \
    -u "${user}:${pass}" | jq -r '.[] | "  \(.date | split(".")[] | split("T")[] | .[0:10]) - \(.title.rendered)"' | head -5

  # Get scheduled posts
  echo "📅 Scheduled:"
  curl -s "${url}/wp/v2/posts?after=${YEAR}-${MONTH}-01T00:00:00&before=${YEAR}-${MONTH}-31T23:59:59&per_page=100&status=future" \
    -u "${user}:${pass}" | jq -r '.[] | "  \(.date | split(".")[] | split("T")[] | .[0:10]) - \(.title.rendered)"' | head -5

  # Get drafts
  echo "📝 Drafts:"
  curl -s "${url}/wp/v2/posts?per_page=10&status=draft" \
    -u "${user}:${pass}" | jq -r '.[] | "  #\(.id) - \(.title.rendered)"' | head -5

  echo ""
done

echo "=== End of Calendar ==="
