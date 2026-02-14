#!/bin/bash

# Article Health Analysis Script
# Uses pinch-to-post configured sites to analyze published articles

SITES=(
  "crashcasino:https://crashcasino.io/wp-json"
  "crashgame:https://crashgamegambling.com/wp-json"
  "freecrash:https://freecrashgames.com/wp-json"
  "cryptocrash:https://cryptocrashgambling.com/wp-json"
)

echo "=== 🦞 Pinch-to-Post Article Health Analysis ==="
echo "Analyzing recent published articles across all sites..."
echo ""

for site_entry in "${SITES[@]}"; do
  IFS=':' read -r site_name site_url <<< "$site_entry"

  echo "## 📍 Site: $site_name ($site_url)"
  echo ""

  # Get credentials from config (using crashcasino as example)
  if [ "$site_name" = "crashcasino" ]; then
    USER="peter"
    PASS="3vRhtTs2khfdLtTiDFqkdeXI"
  elif [ "$site_name" = "crashgame" ]; then
    USER="peter"
    PASS="MioX SygN Xaz6 pK9o RUiK tBMF"
  elif [ "$site_name" = "freecrash" ]; then
    USER="peter"
    PASS="F8Mg yZXM qJy4 jQvp BMeZ FoMG"
  elif [ "$site_name" = "cryptocrash" ]; then
    USER="peter"
    PASS="R3kQ 6vRA UwYd x7Cn KEtT Pk83"
  fi

  # Get recent published posts
  posts=$(curl -s "${site_url}/wp/v2/posts?per_page=10&status=publish" \
    -u "$USER:$PASS" 2>/dev/null)

  if [ $? -ne 0 ] || [ -z "$posts" ]; then
    echo "❌ Failed to fetch posts"
    echo ""
    continue
  fi

  # Analyze each post
  echo "$posts" | jq -r '.[] | @json' | while read -r post; do
    id=$(echo "$post" | jq -r '.id')
    title=$(echo "$post" | jq -r '.title.rendered' | sed 's/<[^>]*>//g')
    link=$(echo "$post" | jq -r '.link')
    content=$(echo "$post" | jq -r '.content.rendered')
    excerpt=$(echo "$post" | jq -r '.excerpt.rendered')
    featured_media=$(echo "$post" | jq -r '.featured_media')
    yoast_title=$(echo "$post" | jq -r '.meta._yoast_wpseo_title // "null"')
    yoast_desc=$(echo "$post" | jq -r '.meta._yoast_wpseo_metadesc // "null"')
    yoast_focuskw=$(echo "$post" | jq -r '.meta._yoast_wpseo_focuskw // "null"')

    # Word count
    word_count=$(echo "$content" | sed 's/<[^>]*>//g' | wc -w)
    word_count=$((word_count + 0))  # Ensure it's a number

    # Check for images in content
    image_count=$(echo "$content" | grep -o '<img' | wc -l)
    image_count=$((image_count + 0))

    # Check for internal links (basic check)
    internal_links=$(echo "$content" | grep -o 'href="https://[^"]*"' | grep -v 'href="https://www.crashcasino.io' | wc -l)
    internal_links=$((internal_links + 0))

    # Check for headings
    h2_count=$(echo "$content" | grep -o '<h2' | wc -l)
    h2_count=$((h2_count + 0))

    # Calculate health score
    score=0
    issues=()

    # Word count check (300+ recommended)
    if [ "$word_count" -ge 300 ]; then
      score=$((score + 20))
    else
      issues+=("Word count: $word_count (300+ recommended)")
    fi

    # Title length check
    title_len=${#title}
    if [ "$title_len" -ge 50 ] && [ "$title_len" -le 60 ]; then
      score=$((score + 15))
    elif [ "$title_len" -gt 0 ]; then
      score=$((score + 10))
    else
      issues+=("Missing title")
    fi

    # Excerpt/Meta description check
    if [ "$yoast_desc" != "null" ] && [ ! -z "$yoast_desc" ]; then
      score=$((score + 15))
    else
      issues+=("Missing meta description")
    fi

    # Featured image check
    if [ "$featured_media" -gt 0 ]; then
      score=$((score + 10))
    else
      issues+=("No featured image")
    fi

    # Heading structure check
    if [ "$h2_count" -ge 2 ]; then
      score=$((score + 15))
    else
      issues+=("Insufficient H2 headings ($h2_count found, 2+ recommended)")
    fi

    # Images check
    if [ "$image_count" -ge 1 ]; then
      score=$((score + 10))
    else
      issues+=("No images in content")
    fi

    # Focus keyword check
    if [ "$yoast_focuskw" != "null" ] && [ ! -z "$yoast_focuskw" ]; then
      score=$((score + 15))
    else
      issues+=("No focus keyword set")
    fi

    # Output results
    echo "### $title"
    echo "ID: $id | Score: ${score}/100"
    echo "Link: $link"

    if [ ${#issues[@]} -eq 0 ]; then
      echo "✅ Excellent! No issues found."
    else
      echo "⚠️  Issues:"
      for issue in "${issues[@]}"; do
        echo "   - $issue"
      done
    fi

    echo ""
  done

  echo "---"
  echo ""
done

echo "=== Analysis Complete ==="
