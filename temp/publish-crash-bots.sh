#!/bin/bash
# Publish crash predictor bots article to crashcasino.io

POST_FILE="/root/.openclaw/workspace/temp/crash-predictor-bots-article.md"
SITE="crashcasino"
TITLE="Crash Predictor Bots: Do They Work or Are They a Scam? (2026)"
SLUG="crash-predictor-bots"

# Read content
CONTENT=$(cat "$POST_FILE")

# Escape for JSON
CONTENT_ESCAPED=$(echo "$CONTENT" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | tr -d '\n' | sed 's/\r//g')

# Create post via REST API
curl -s -X POST "https://crashcasino.io/wp-json/wp/v2/posts" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$TITLE\",
    \"content\": \"$CONTENT_ESCAPED\",
    \"status\": \"draft\",
    \"slug\": \"$SLUG\",
    \"meta\": {
      \"_yoast_wpseo_metadesc\": \"Crash predictor bots claim to beat crash games. They do not work. Learn the mathematical truth, security risks, and legitimate alternatives in this comprehensive 2026 guide.\",
      \"_yoast_wpseo_focuskw\": \"crash predictor bots\"
    }
  }"

echo ""
echo "✅ Article published as draft to crashcasino.io"
echo "🔗 URL: https://crashcasino.io/$SLUG/"
echo "📝 Next: Review, add featured image, then publish"
