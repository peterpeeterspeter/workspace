#!/bin/bash

# Fix Batch 3 Articles with Pinch-to-Post
# Add SEO metadata and run health checks BEFORE publishing

echo "=== 🦞 Fixing Batch 3 Articles ==="
echo ""

# Article 1: Best Crash Casinos 2026 (crashcasino.io #889)
echo "### 1. Best Crash Casinos 2026 (crashcasino.io #889)"

curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/889" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_title": "Best Crash Casinos 2026: Safe & Verified Sites | CrashCasino.io",
      "_yoast_wpseo_metadesc": "Discover the best crash casinos for 2026. We test real money gameplay, verify fairness, check withdrawals, and rank bonuses. Updated monthly with new sites.",
      "_yoast_wpseo_focuskw": "best crash casinos 2026"
    }
  }' 2>/dev/null | jq -r '.id, .meta._yoast_wpseo_metadesc'

echo "✅ Meta data added"
echo ""

# Check if other posts exist with different IDs
echo "### 2. Looking for USDT Crash Gambling on cryptocrash..."
curl -s "https://cryptocrashgambling.com/wp-json/wp/v2/posts?search=USDT" \
  -u "peter:R3kQ 6vRA UwYd x7Cn KEtT Pk83" | jq -r '.[] | "\(.id) | \(.title.rendered)"'

echo ""
echo "### 3. Looking for How to Play Crash on crashgame..."
curl -s "https://crashgamegambling.com/wp-json/wp/v2/posts?search=How to Play" \
  -u "peter:MioX SygN Xaz6 pK9o RUiK tBMF" | jq -r '.[] | "\(.id) | \(.title.rendered)"'

echo ""
echo "### 4. Looking for Nigeria casinos on freecrash..."
curl -s "https://freecrashgames.com/wp-json/wp/v2/posts?search=Nigeria" \
  -u "peter:F8Mg yZXM qJy4 jQvp BMeZ FoMG" | jq -r '.[] | "\(.id) | \(.title.rendered)"'

echo ""
echo "=== Complete ==="
echo "Next: Add featured images, then run health checks before publishing."
