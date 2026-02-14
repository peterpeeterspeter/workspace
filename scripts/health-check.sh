#!/bin/bash

# Content Health Check Script
# Usage: ./health-check.sh <post_id>

WP_SITE_URL="https://crashcasino.io/wp-json"
WP_USERNAME="peter"
WP_APP_PASSWORD="3vRhtTs2khfdLtTiDFqkdeXI"

POST_ID=$1

if [ -z "$POST_ID" ]; then
  echo "Usage: $0 <post_id>"
  exit 1
fi

# Fetch post data
POST_DATA=$(curl -s -u "${WP_USERNAME}:${WP_APP_PASSWORD}" "${WP_SITE_URL}/wp/v2/posts/${POST_ID}")

# Extract fields
TITLE=$(echo "$POST_DATA" | jq -r '.title.rendered // ""')
CONTENT=$(echo "$POST_DATA" | jq -r '.content.rendered // ""')
EXCERPT=$(echo "$POST_DATA" | jq -r '.excerpt.rendered // ""' | sed 's/<[^>]*>//g' | xargs)
FEATURED_MEDIA=$(echo "$POST_DATA" | jq -r '.featured_media // 0')

# Strip HTML for word count
CONTENT_TEXT=$(echo "$CONTENT" | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | tr -s ' ')
WORD_COUNT=$(echo "$CONTENT_TEXT" | wc -w | awk '{print $1}')
TITLE_LENGTH=${#TITLE}

# Check for H2 headings
H2_COUNT=$(echo "$CONTENT" | grep -o '<h2' | wc -l)

# Check for images
IMG_COUNT=$(echo "$CONTENT" | grep -o '<img' | wc -l)

# Check for images with alt text
IMG_WITH_ALT=$(echo "$CONTENT" | grep -oP 'alt="[^"]*"' | wc -l)

# Check for internal links
INTERNAL_LINKS=$(echo "$CONTENT" | grep -o 'href="https://crashcasino.io' | wc -l)

# Calculate score
SCORE=0
MAX_SCORE=100

# Word count (20 points)
if [ "$WORD_COUNT" -ge 1000 ]; then
  SCORE=$((SCORE + 20))
  WORD_STATUS="✅ Excellent ($WORD_COUNT words)"
elif [ "$WORD_COUNT" -ge 500 ]; then
  SCORE=$((SCORE + 15))
  WORD_STATUS="🟡 Good ($WORD_COUNT words)"
elif [ "$WORD_COUNT" -ge 300 ]; then
  SCORE=$((SCORE + 10))
  WORD_STATUS="⚠️  Minimal ($WORD_COUNT words)"
else
  WORD_STATUS="❌ Too short ($WORD_COUNT words)"
fi

# Title length (10 points)
if [ "$TITLE_LENGTH" -ge 50 ] && [ "$TITLE_LENGTH" -le 60 ]; then
  SCORE=$((SCORE + 10))
  TITLE_STATUS="✅ Perfect ($TITLE_LENGTH chars)"
elif [ "$TITLE_LENGTH" -ge 40 ] && [ "$TITLE_LENGTH" -le 70 ]; then
  SCORE=$((SCORE + 7))
  TITLE_STATUS="🟡 Good ($TITLE_LENGTH chars)"
else
  TITLE_STATUS="⚠️  $TITLE_LENGTH chars (target: 50-60)"
fi

# Excerpt (15 points)
if [ -n "$EXCERPT" ] && [ "$EXCERPT" != "none" ]; then
  SCORE=$((SCORE + 15))
  EXCERPT_STATUS="✅ Present (${#EXCERPT} chars)"
else
  EXCERPT_STATUS="❌ Missing"
fi

# Featured image (15 points)
if [ "$FEATURED_MEDIA" -gt 0 ]; then
  SCORE=$((SCORE + 15))
  MEDIA_STATUS="✅ Set (ID: $FEATURED_MEDIA)"
else
  MEDIA_STATUS="❌ Not set"
fi

# H2 headings (10 points)
if [ "$H2_COUNT" -ge 3 ]; then
  SCORE=$((SCORE + 10))
  H2_STATUS="✅ $H2_COUNT H2 headings"
elif [ "$H2_COUNT" -ge 1 ]; then
  SCORE=$((SCORE + 5))
  H2_STATUS="🟡 $H2_COUNT H2 heading (need more)"
else
  H2_STATUS="❌ No H2 headings"
fi

# Images (10 points)
if [ "$IMG_COUNT" -ge 3 ]; then
  SCORE=$((SCORE + 10))
  IMG_STATUS="✅ $IMG_COUNT images"
elif [ "$IMG_COUNT" -ge 1 ]; then
  SCORE=$((SCORE + 5))
  IMG_STATUS="🟡 $IMG_COUNT image (add more)"
else
  IMG_STATUS="⚠️  No images"
fi

# Alt text (10 points)
if [ "$IMG_WITH_ALT" -ge "$IMG_COUNT" ] && [ "$IMG_COUNT" -gt 0 ]; then
  SCORE=$((SCORE + 10))
  ALT_STATUS="✅ All images have alt text"
elif [ "$IMG_WITH_ALT" -gt 0 ]; then
  SCORE=$((SCORE + 5))
  ALT_STATUS="🟡 $IMG_WITH_ALT/$IMG_COUNT have alt text"
else
  ALT_STATUS="⚠️  Missing alt text"
fi

# Internal links (10 points)
if [ "$INTERNAL_LINKS" -ge 3 ]; then
  SCORE=$((SCORE + 10))
  LINK_STATUS="✅ $INTERNAL_LINKS internal links"
elif [ "$INTERNAL_LINKS" -ge 1 ]; then
  SCORE=$((SCORE + 5))
  LINK_STATUS="🟡 $INTERNAL_LINKS internal link (add more)"
else
  LINK_STATUS="❌ No internal links"
fi

# Print report
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           CONTENT HEALTH SCORE REPORT                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📄 Post: $TITLE"
echo "🔗 ID: $POST_ID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 ANALYSIS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Word Count:      $WORD_STATUS"
echo "Title Length:    $TITLE_STATUS"
echo "Excerpt:         $EXCERPT_STATUS"
echo "Featured Image:  $MEDIA_STATUS"
echo "H2 Headings:     $H2_STATUS"
echo "Images:          $IMG_STATUS"
echo "Alt Text:        $ALT_STATUS"
echo "Internal Links:  $LINK_STATUS"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 FINAL SCORE: $SCORE/$MAX_SCORE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$SCORE" -ge 80 ]; then
  echo "🟢 EXCELLENT - Ready to publish!"
elif [ "$SCORE" -ge 60 ]; then
  echo "🟡 GOOD - Minor improvements recommended"
elif [ "$SCORE" -ge 40 ]; then
  echo "🟠 FAIR - Needs some work"
else
  echo "🔴 POOR - Major improvements needed"
fi

echo ""
