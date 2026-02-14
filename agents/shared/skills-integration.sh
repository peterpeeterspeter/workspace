#!/bin/bash
# Shared skills integration library
# Provides common functions for calling skills

# Perplexity AI search
perplexity_search() {
  local query=$1
  local output_file=$2

  local skill_dir="/root/.openclaw/workspace/skills/perplexity"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: Perplexity skill not found"
    return 1
  fi

  cd "$skill_dir"
  local result=$(node scripts/search.mjs "$query" 2>&1)

  if [ -n "$output_file" ]; then
    echo "$result" >> "$output_file"
  fi

  echo "$result"
}

# SEO optimizer audit
seo_audit() {
  local html_file=$1
  local output_file=$2

  local skill_dir="/root/.openclaw/workspace/skills/seo-optimizer"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: SEO optimizer skill not found"
    return 1
  fi

  cd "$skill_dir"
  local result=$(python scripts/seo_analyzer.py "$html_file" 2>&1)

  if [ -n "$output_file" ]; then
    echo "$result" >> "$output_file"
  fi

  echo "$result"
}

# WordPress publish via pinch-to-post
wordpress_publish() {
  local site=$1
  local file=$2
  local status=${3:-publish}

  local skill_dir="/root/.openclaw/workspace/skills/pinch-to-post"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: pinch-to-post skill not found"
    return 1
  fi

  # Get credentials for site
  local wp_url=""
  local wp_user="peter"
  local wp_app=""

  case "$site" in
    crashcasino.io)
      wp_url="https://crashcasino.io"
      wp_app="${CRASHCASINO_APP_PASSWORD:-}"
      ;;
    cryptocrashgambling.com)
      wp_url="https://cryptocrashgambling.com"
      wp_app="${CRYPTOCRASH_APP_PASSWORD:-}"
      ;;
    crashgamegambling.com)
      wp_url="https://crashgamegambling.com"
      wp_app="${CRASHGAME_APP_PASSWORD:-}"
      ;;
    freecrashgames.com)
      wp_url="https://freecrashgames.com"
      wp_app="${FREECRASHGAMES_APP_PASSWORD:-}"
      ;;
    aviatorcrashgame.com)
      wp_url="https://aviatorcrashgame.com"
      wp_app="${AVIATORCRASH_APP_PASSWORD:-}"
      ;;
    *)
      echo "ERROR: Unknown site ${site}"
      return 1
      ;;
  esac

  if [ -z "$wp_app" ]; then
    echo "ERROR: No WordPress credentials for ${site}"
    return 1
  fi

  # Publish using WordPress REST API
  local title=$(basename "$file" .md)
  local content=$(cat "$file")

  local response=$(curl -s -X POST "${wp_url}/wp-json/wp/v2/posts" \
    --user "${wp_user}:${wp_app}" \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"${title}\",
      \"content\": \"${content}\",
      \"status\": \"${status}\"
    }")

  if echo "$response" | grep -q '"id"'; then
    local post_id=$(echo "$response" | jq -r '.id')
    echo "${post_id}"
    return 0
  else
    echo "ERROR: Failed to publish"
    echo "$response"
    return 1
  fi
}

# Keyword research via DataForSEO
keyword_research() {
  local keyword=$1
  local output_file=$2

  local skill_dir="/root/.openclaw/workspace/skills/seo-dataforseo"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: seo-dataforseo skill not found"
    return 1
  fi

  cd "$skill_dir"
  # Call keyword research script
  # (implementation depends on skill structure)
  echo "Keyword research for: ${keyword}"
}

# Humanize content
humanize_content() {
  local input_file=$1
  local output_file=$2

  local skill_dir="/root/.openclaw/workspace/skills/humanize"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: humanize skill not found"
    return 1
  fi

  # Apply humanization
  # (implementation depends on skill structure)
  echo "Humanizing content..."
}
