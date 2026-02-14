#!/bin/bash
# CrashCasino Article Improvement Plan
# Uses pinch-to-post to analyze and improve all articles

echo "=== CrashCasino.io Article Analysis ==="
echo ""
echo "Checking all published articles and drafts..."
echo ""

# Array of all post IDs
POST_IDS=(838 837 836 835 834 833)

# Analysis results
declare -A SCORES
declare -A ISSUES

echo "## Health Check Results"
echo ""

for id in "${POST_IDS[@]}"; do
  echo "### Article $id"

  # Get health score
  HEALTH_CHECK=$(/root/.openclaw/workspace/scripts/publish-gateway.sh check $id crashcasino 2>&1)

  # Extract score
  if echo "$HEALTH_CHECK" | grep -q "Health Score:"; then
    SCORE=$(echo "$HEALTH_CHECK" | grep "Health Score:" | sed 's/.*Health Score: \([0-9]*\)\/.*/\1/')
    SCORES[$id]=$SCORE

    echo "Score: $SCORE/100"

    if [ "$SCORE" -lt 80 ]; then
      echo "Status: ❌ Needs improvement"

      # Extract issues
      ISSUES[$id]=$(echo "$HEALTH_CHECK" | grep -A 10 "Required fixes:")
      echo "$ISSUES[$id]" | grep "^  -" | sed 's/^  - /    - /'
    else
      echo "Status: ✅ Good"
    fi
  else
    echo "Status: ⚠️ Could not check"
    SCORES[$id]="N/A"
  fi

  echo ""
done

echo ""
echo "## Summary"
echo ""

TOTAL=${#POST_IDS[@]}
BELOW_80=0
ABOVE_80=0

for id in "${POST_IDS[@]}"; do
  SCORE=${SCORES[$id]}
  if [ "$SCORE" != "N/A" ] && [ "$SCORE" -lt 80 ]; then
    ((BELOW_80++))
  elif [ "$SCORE" != "N/A" ]; then
    ((ABOVE_80++))
  fi
done

echo "Total articles checked: $TOTAL"
echo "Need improvement (below 80): $BELOW_80"
echo "Good (80+): $ABOVE_80"
echo ""

echo "## Improvement Recommendations"
echo ""

for id in "${POST_IDS[@]}"; do
  SCORE=${SCORES[$id]}

  if [ "$SCORE" != "N/A" ] && [ "$SCORE" -lt 80 ]; then
    echo "### Article $id (Score: $SCORE/100)"

    # Get post details
    DETAILS=$(curl -s "https://crashcasino.io/wp-json/wp/v2/posts/$id" -u "peter:3vRhtTs2khfdLtTiDFqkdeXI")

    TITLE=$(echo "$DETAILS" | jq -r '.title.rendered')
    WORD_COUNT=$(echo "$DETAILS" | jq -r '.content.rendered' | wc -w)
    HAS_FEATURED=$(echo "$DETAILS" | jq -r '.featured_media')
    HAS_META=$(echo "$DETAILS" | jq -r '.meta._yoast_wpseo_metadesc // "empty"')

    echo "Title: $TITLE"
    echo "Words: $WORD_COUNT"
    echo "Featured image: $HAS_FEATURED"
    echo "Meta description: $HAS_META"

    echo ""
    echo "Required actions:"
    echo "  1. Add meta description (150-160 chars)"
    echo "  2. Set focus keyword"
    echo "  3. Add featured image"
    echo "  4. Add images to content"

    echo ""
  fi
done

echo "## Automated Fixes with Pinch-to-Post"
echo ""

echo "### Adding Meta Descriptions"
echo ""
echo "For each article, generate meta description using this formula:"
echo ""
echo "Example for article 838:"
cat << 'META'
Title: How We Rate Crash Casinos: Full Transparency on Our Review Process

Meta Description:
"Discover how we rate crash casinos in 2026. Full transparency on our 9 crash-specific criteria, testing process, and affiliate disclosure. (155 chars)"

Focus Keyword: "rate crash casinos"
META

echo ""
echo "### Adding Featured Images"
echo ""
echo "Use media upload command:"
echo 'pinch-to-post media-upload crashcasino /path/to/image.jpg "Alt text" "Caption" POST_ID'
echo ""

echo "### Adding Images to Content"
echo ""
echo "For each article, add 2-3 relevant screenshots showing:"
echo "- Crash game interfaces"
echo "- Casino platforms"
echo "- Example gameplay"
echo ""

echo "## Next Steps"
echo ""
echo "1. Generate meta descriptions for all articles"
echo "2. Set focus keywords for all articles"
echo "3. Upload featured images"
echo "4. Add content images"
echo "5. Re-check health scores"
echo "6. Publish articles with 80+ scores"
echo ""

echo "Scripts to use:"
echo "  - pinch-to-post health-check crashcasino POST_ID"
echo "  - pinch-to-post media-upload crashcasino image.jpg \"Alt\" \"Caption\" POST_ID"
echo "  - pinch-to-post publish crashcasino POST_ID (after fixes)"
