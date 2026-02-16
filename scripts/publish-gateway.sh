#!/bin/bash

# 🦞 Pinch-to-Post Publishing Gateway
# MANDATORY quality check before ANY WordPress publishing
# No article publishes below 80/100 score

set -e

# Configuration
PUBLISH_THRESHOLD=80
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../logs"
LOG_FILE="${LOG_DIR}/publish-gateway.log"

# Create logs directory
mkdir -p "$LOG_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging (silent in output)
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Site configuration
get_site_creds() {
  local site=$1
  case $site in
    crashcasino)
      echo "https://crashcasino.io/wp-json peter 3vRhtTs2khfdLtTiDFqkdeXI"
      ;;
    crashgame)
      echo "https://crashgamegambling.com/wp-json peter MioX SygN Xaz6 pK9o RUiK tBMF"
      ;;
    freecrash)
      echo "https://freecrashgames.com/wp-json peter F8Mg yZXM qJy4 jQvp BMeZ FoMG"
      ;;
    cryptocrash)
      echo "https://cryptocrashgambling.com/wp-json peter R3kQ 6vRA UwYd x7Cn KEtT Pk83"
      ;; 
    hobbysalon)
      echo "https://www.hobbysalon.be/wp-json kris yiN7 vXcZ 2U2T t2SM 4DZX 1mKw"
      ;;
    *)
      echo ""
      return 1
      ;;
  esac
}

# Calculate content health score
calculate_health_score() {
  local post_id=$1
  local site_url=$2
  local username=$3
  local password=$4

  log "Calculating health score for post $post_id"

  # Fetch post data
  post_data=$(curl -s -L "${site_url}/wp/v2/posts/${post_id}" -u "${username}:${password}")

  # Validate JSON response
  if [ -z "$post_data" ] || [ "$(echo "$post_data" | jq 'empty')" != "" ] 2>/dev/null; then
    log "ERROR: Invalid or empty JSON response for post $post_id"
    echo "0"
    return 1
  fi

  # Extract data
  title=$(echo "$post_data" | jq -r '.title.rendered // ""' | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g')
  content=$(echo "$post_data" | jq -r '.content.rendered // ""')
  featured_media=$(echo "$post_data" | jq -r '.featured_media // 0')

  # Check for both Yoast and RankMath SEO
  yoast_desc=$(echo "$post_data" | jq -r '.meta._yoast_wpseo_metadesc // "null"')
  yoast_focuskw=$(echo "$post_data" | jq -r '.meta._yoast_wpseo_focuskw // "null"')
  
  # RankMath stores data separately - fetch from RankMath API
  rankmath_data=$(curl -s -L "${site_url}/rankmath/v1/getMeta?pid=${post_id}" -u "${username}:${password}" 2>/dev/null || echo '{}')

  # Validate RankMath JSON if not empty
  if [ "$rankmath_data" != "{}" ] && [ -n "$rankmath_data" ]; then
    if [ "$(echo "$rankmath_data" | jq 'empty' 2>/dev/null)" != "" ]; then
      rankmath_data='{}'
    fi
  fi
  rankmath_desc=$(echo "$rankmath_data" | jq -r '.rankMathDescription // .rank_math_description // "null"')
  rankmath_focuskw=$(echo "$rankmath_data" | jq -r '.rankMathKeyword // .rank_math_focus_keyword // "null"')

  # Use whichever SEO plugin is active
  if [ "$rankmath_desc" != "null" ] && [ ! -z "$rankmath_desc" ] && [ "$rankmath_desc" != "null" ]; then
    seo_desc="$rankmath_desc"
  else
    seo_desc="$yoast_desc"
  fi

  if [ "$rankmath_focuskw" != "null" ] && [ ! -z "$rankmath_focuskw" ] && [ "$rankmath_focuskw" != "null" ]; then
    seo_focuskw="$rankmath_focuskw"
  else
    seo_focuskw="$yoast_focuskw"
  fi

  # Calculate metrics
  word_count=$(echo "$content" | sed 's/<[^>]*>//g' | wc -w)
  word_count=$((word_count + 0))

  title_len=${#title}

  # Count images
  image_count=$(echo "$content" | grep -o '<img' | wc -l || echo 0)
  image_count=$((image_count + 0))

  # Count H2 headings
  h2_count=$(echo "$content" | grep -o '<h2' | wc -l || echo 0)
  h2_count=$((h2_count + 0))

  # Calculate score
  score=0

  # Word count (20 points)
  if [ "$word_count" -ge 300 ]; then
    score=$((score + 20))
  fi

  # Title length (15 points)
  if [ "$title_len" -ge 50 ] && [ "$title_len" -le 60 ]; then
    score=$((score + 15))
  elif [ "$title_len" -gt 0 ]; then
    score=$((score + 10))
  fi

  # Meta description (15 points)
  if [ "$yoast_desc" != "null" ] && [ ! -z "$yoast_desc" ]; then
    score=$((score + 15))
  fi

  # Featured image (10 points)
  if [ "$featured_media" -gt 0 ]; then
    score=$((score + 10))
  fi

  # H2 headings (15 points)
  if [ "$h2_count" -ge 2 ]; then
    score=$((score + 15))
  fi

  # Images in content (10 points)
  if [ "$image_count" -ge 1 ]; then
    score=$((score + 10))
  fi

  # Focus keyword (15 points)
  if [ "$yoast_focuskw" != "null" ] && [ ! -z "$yoast_focuskw" ]; then
    score=$((score + 15))
  fi

  # Output score only (for parsing)
  echo "$score"
}

# Get health report as JSON
get_health_report() {
  local post_id=$1
  local site_url=$2
  local username=$3
  local password=$4

  post_data=$(curl -s -L "${site_url}/wp/v2/posts/${post_id}" -u "${username}:${password}")

  # Validate JSON response
  if [ -z "$post_data" ] || [ "$(echo "$post_data" | jq 'empty' 2>/dev/null)" != "" ]; then
    log "ERROR: Invalid or empty JSON response for post $post_id"
    return 1
  fi

  title=$(echo "$post_data" | jq -r '.title.rendered // ""' | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g')
  content=$(echo "$post_data" | jq -r '.content.rendered // ""')
  featured_media=$(echo "$post_data" | jq -r '.featured_media // 0')
  yoast_desc=$(echo "$post_data" | jq -r '.meta._yoast_wpseo_metadesc // "null"')
  yoast_focuskw=$(echo "$post_data" | jq -r '.meta._yoast_wpseo_focuskw // "null"')

  word_count=$(echo "$content" | sed 's/<[^>]*>//g' | wc -w | tr -d ' ')
  image_count=$(echo "$content" | grep -o '<img' | wc -l | tr -d ' ')
  h2_count=$(echo "$content" | grep -o '<h2' | wc -l | tr -d ' ')

  # Build issues array
  issues_json="[]"

  if [ "$word_count" -lt 300 ]; then
    issues_json=$(echo "$issues_json" | jq --arg x "Word count: $word_count (300+ recommended)" '. + [$x]')
  fi

  if [ "$yoast_desc" = "null" ] || [ -z "$yoast_desc" ]; then
    issues_json=$(echo "$issues_json" | jq '. + ["Missing meta description (SEO critical)"]')
  fi

  if [ "$featured_media" -eq 0 ]; then
    issues_json=$(echo "$issues_json" | jq '. + ["No featured image"]')
  fi

  if [ "$h2_count" -lt 2 ]; then
    issues_json=$(echo "$issues_json" | jq --arg x "Insufficient H2 headings ($h2_count found, 2+ recommended)" '. + [$x]')
  fi

  if [ "$image_count" -eq 0 ]; then
    issues_json=$(echo "$issues_json" | jq '. + ["No images in content"]')
  fi

  if [ "$yoast_focuskw" = "null" ] || [ -z "$yoast_focuskw" ]; then
    issues_json=$(echo "$issues_json" | jq '. + ["No focus keyword set (SEO critical)"]')
  fi

  # Output JSON
  jq -n \
    --arg title "$title" \
    --arg id "$post_id" \
    --argjson score "$(calculate_health_score "$post_id" "$site_url" "$username" "$password")" \
    --argjson issues "$issues_json" \
    '{title: $title, id: $id, score: $score, issues: $issues}'
}

# Display health report
display_health_report() {
  local report_json=$1

  title=$(echo "$report_json" | jq -r '.title')
  post_id=$(echo "$report_json" | jq -r '.id')
  score=$(echo "$report_json" | jq -r '.score')
  issues=$(echo "$report_json" | jq -r '.issues[]')

  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo -e "${BLUE}📊 Content Health Check${NC}"
  echo "═══════════════════════════════════════════════════════"
  echo "Post: $title"
  echo "ID: $post_id"
  echo ""
  echo -e "Health Score: ${score}/100"
  echo ""

  if [ "$score" -ge "$PUBLISH_THRESHOLD" ]; then
    echo -e "${GREEN}✅ READY TO PUBLISH${NC}"
    echo "Article meets quality standards."
    return 0
  else
    echo -e "${RED}❌ NOT READY TO PUBLISH${NC}"
    echo -e "Score must be ${PUBLISH_THRESHOLD}+ to publish."
    echo ""
    echo "Required fixes:"
    echo "$issues" | while read -r issue; do
      echo "  - $issue"
    done
    echo ""
    echo -e "${YELLOW}⚠️  Publishing blocked until issues are resolved.${NC}"
    return 1
  fi
}

# Auto-fix common issues
auto_fix_article() {
  local post_id=$1
  local site_url=$2
  local username=$3
  local password=$4

  log "Attempting auto-fix for post $post_id"

  post_data=$(curl -s -L "${site_url}/wp/v2/posts/${post_id}" -u "${username}:${password}")

  # Validate JSON response
  if [ -z "$post_data" ] || [ "$(echo "$post_data" | jq 'empty' 2>/dev/null)" != "" ]; then
    log "ERROR: Invalid or empty JSON response for post $post_id"
    return 1
  fi

  title=$(echo "$post_data" | jq -r '.title.rendered // ""' | sed 's/<[^>]*>//g')
  content=$(echo "$post_data" | jq -r '.content.rendered // ""')

  # Clean text from HTML
  clean_text=$(echo "$content" | sed 's/<[^>]*>//g' | sed 's/&amp;/\&/g' | sed 's/&nbsp;/ /g' | tr -s ' ')

  # Get first 150 chars for meta description
  meta_desc=$(echo "$clean_text" | head -c 150 | sed 's/ *$//' | sed 's/$/\.../')

  # Extract focus keyword from title (last word usually)
  focus_kw=$(echo "$title" | tr '[:upper:]' '[:lower:]' | rev | cut -d' ' -f1 | rev)

  # Update post with generated meta
  curl -s -L -X POST "${site_url}/wp/v2/posts/${post_id}" \
    -u "${username}:${password}" \
    -H "Content-Type: application/json" \
    -d "{
      \"meta\": {
        \"_yoast_wpseo_metadesc\": \"${meta_desc}\",
        \"_yoast_wpseo_focuskw\": \"${focus_kw}\"
      }
    }" > /dev/null

  log "Auto-fix applied"
}

# Main publish function
publish_article() {
  local post_id=$1
  local site=$2
  local force=${3:-false}

  log "🚀 Publish request: Post #$post_id on $site"

  # Get site credentials
  creds=$(get_site_creds "$site")
  if [ -z "$creds" ]; then
    echo "ERROR: Invalid site: $site"
    return 1
  fi

  read -r site_url username password <<< "$creds"

  # Check if post exists
  post_data=$(curl -s -L "${site_url}/wp/v2/posts/${post_id}" -u "${username}:${password}")

  # Validate JSON response
  if [ -z "$post_data" ] || [ "$(echo "$post_data" | jq 'empty' 2>/dev/null)" != "" ]; then
    echo "ERROR: Invalid or empty JSON response for post #$post_id"
    return 1
  fi

  if [ "$(echo "$post_data" | jq -r '.code // empty')" = "rest_post_invalid_id" ]; then
    echo "ERROR: Post #$post_id not found on $site"
    return 1
  fi

  title=$(echo "$post_data" | jq -r '.title.rendered')
  current_status=$(echo "$post_data" | jq -r '.status')

  log "Post found: $title (status: $current_status)"

  # Skip if already published
  if [ "$current_status" = "publish" ] && [ "$force" != "true" ]; then
    echo "Post already published"
    return 0
  fi

  # Get health report
  health_report=$(get_health_report "$post_id" "$site_url" "$username" "$password")
  score=$(echo "$health_report" | jq -r '.score')

  log "Health score: $score/100"

  # Check if meets threshold
  if [ "$score" -lt "$PUBLISH_THRESHOLD" ] && [ "$force" != "true" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Article below threshold ($score/$PUBLISH_THRESHOLD). Attempting auto-fix...${NC}"
    auto_fix_article "$post_id" "$site_url" "$username" "$password"

    # Recalculate
    health_report=$(get_health_report "$post_id" "$site_url" "$username" "$password")
    score=$(echo "$health_report" | jq -r '.score')
    log "Score after auto-fix: $score/100"
  fi

  # Final check
  if [ "$score" -lt "$PUBLISH_THRESHOLD" ] && [ "$force" != "true" ]; then
    display_health_report "$health_report"
    return 1
  fi

  # Show health report even when forcing
  if [ "$force" = "true" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  FORCE PUBLISH (score: $score/$PUBLISH_THRESHOLD)${NC}"
    display_health_report "$health_report" > /dev/null 2>&1 || true
  fi

  # Publish
  log "Publishing post #$post_id"

  result=$(curl -s -L -X POST "${site_url}/wp/v2/posts/${post_id}" \
    -u "${username}:${password}" \
    -H "Content-Type: application/json" \
    -d '{"status": "publish"}')

  # Validate JSON response
  if [ -z "$result" ] || [ "$(echo "$result" | jq 'empty' 2>/dev/null)" != "" ]; then
    log "ERROR: Invalid or empty JSON response when publishing post #$post_id"
    echo "ERROR: Publishing failed - invalid response"
    return 1
  fi

  new_status=$(echo "$result" | jq -r '.status // empty')

  if [ "$new_status" = "publish" ]; then
    link=$(echo "$result" | jq -r '.link')
    log "✅ Published: $link"
    echo ""
    echo -e "${GREEN}✅ Article published successfully!${NC}"
    echo "Link: $link"
    echo "Score: $score/100"
    return 0
  else
    log "❌ Publish failed"
    echo "ERROR: Publishing failed"
    return 1
  fi
}

# Show help
show_help() {
  cat << EOF
🦞 Pinch-to-Post Publishing Gateway

Mandatory quality checks before WordPress publishing.

USAGE:
  $0 publish <post_id> <site> [force]
  $0 check <post_id> <site>
  $0 help

EXAMPLES:
  # Publish article (must score 80+)
  $0 publish 889 crashcasino

  # Force publish (override score)
  $0 publish 889 crashcasino force

  # Health check only
  $0 check 889 crashcasino

SITES:
  crashcasino    crashcasino.io
  crashgame      crashgamegambling.com
  freecrash      freecrashgames.com
  cryptocrash    cryptocrashgambling.com

THRESHOLD: ${PUBLISH_THRESHOLD}/100 required to publish

EOF
}

# Main
case "${1:-}" in
  publish)
    if [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
      echo "ERROR: Missing arguments"
      show_help
      exit 1
    fi
    publish_article "$2" "$3" "${4:-false}"
    ;;
  check)
    if [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
      echo "ERROR: Missing arguments"
      show_help
      exit 1
    fi

    creds=$(get_site_creds "$3")
    read -r site_url username password <<< "$creds"
    report=$(get_health_report "$2" "$site_url" "$username" "$password")
    display_health_report "$report"
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    echo "ERROR: Unknown command"
    show_help
    exit 1
    ;;
esac
