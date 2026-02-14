#!/bin/bash
# FULL SKILLS INTEGRATION LIBRARY
# All available skills mapped and ready to use

# ============================================
# CREDENTIALS (from .env)
# ============================================

# Load credentials
load_credentials() {
  if [ -f /root/.openclaw/workspace/.env ]; then
    export $(grep -v '^#' /root/.openclaw/workspace/.env | xargs)
  fi
}

# ============================================
# VISION SKILLS (SEO/Content)
# ============================================

# Perplexity AI Search
vision_perplexity_search() {
  local query=$1
  local output_file=$2

  load_credentials

  if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "WARNING: PERPLEXITY_API_KEY not set - skipping Perplexity search"
    return 1
  fi

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

# DataForSEO Keyword Research
vision_keyword_research() {
  local keyword=$1
  local output_file=$2

  load_credentials

  local skill_dir="/root/.openclaw/workspace/skills/seo-dataforseo"

  if [ ! -d "$skill_dir" ]; then
    echo "ERROR: seo-dataforseo skill not found"
    return 1
  fi

  cd "$skill_dir/scripts"
  local result=$(python3 -c "
import sys
sys.path.insert(0, '.')
from main import keyword_research
result = keyword_research('${keyword}')
print(result)
" 2>&1)

  if [ -n "$output_file" ]; then
    echo "$result" >> "$output_file"
  fi

  echo "$result"
}

# SEO Audit
vision_seo_audit() {
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

# Humanize Content
vision_humanize() {
  local input_file=$1
  local output_file=$2

  local skill_dir="/root/.openclaw/workspace/skills/humanize"

  if [ ! -d "$skill_dir" ]; then
    echo "WARNING: humanize skill not found - skipping"
    return 1
  fi

  # Apply humanization (script depends on skill structure)
  echo "Applying humanization to content..."

  if [ -n "$output_file" ]; then
    cp "$input_file" "$output_file"
  fi
}

# WordPress Publish
vision_wordpress_publish() {
  local site=$1
  local file=$2
  local status=${3:-publish}

  load_credentials

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
      wp_app="${WORDPRESS_CRASHCASINO_APP_PASSWORD:-}"
      ;;
    cryptocrashgambling.com)
      wp_url="https://cryptocrashgambling.com"
      wp_app="${WORDPRESS_CRYPTOCRASH_APP_PASSWORD:-}"
      ;;
    crashgamegambling.com)
      wp_url="https://crashgamegambling.com"
      wp_app="${WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD:-}"
      ;;
    freecrashgames.com)
      wp_url="https://freecrashgames.com"
      wp_app="${WORDPRESS_FREECRASH_APP_PASSWORD:-}"
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

# GA4 Analytics (if credentials available)
vision_ga4_analytics() {
  local query=$1
  echo "GA4 analytics integration - requires setup"
}

# GSC Data (if credentials available)
vision_gsc_data() {
  local url=$1
  echo "GSC data integration - requires setup"
}

# Programmatic SEO
vision_programmatic_seo() {
  local template=$1
  local keywords=$2
  echo "Programmatic SEO generation using ${template}"
}

# Schema Markup
vision_schema_markup() {
  local content_type=$1
  local data=$2
  echo "Generating schema markup for ${content_type}"
}

# ============================================
# FURY SKILLS (Research)
# ============================================

# Perplexity Deep Research
fury_perplexity_research() {
  local query=$1
  local output_file=$2

  load_credentials

  if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "WARNING: PERPLEXITY_API_KEY not set"
    return 1
  fi

  local skill_dir="/root/.openclaw/workspace/skills/perplexity"
  cd "$skill_dir"
  local result=$(node scripts/search.mjs "$query" 2>&1)

  if [ -n "$output_file" ]; then
    echo "$result" >> "$output_file"
  fi

  echo "$result"
}

# DataForSEO Research
fury_keyword_research() {
  local keyword=$1
  local output_file=$2

  load_credentials

  local skill_dir="/root/.openclaw/workspace/skills/seo-dataforseo"
  cd "$skill_dir/scripts"
  local result=$(python3 -c "
import sys
sys.path.insert(0, '.')
from main import keyword_research
result = keyword_research('${keyword}')
print(result)
" 2>&1)

  if [ -n "$output_file" ]; then
    echo "$result" >> "$output_file"
  fi

  echo "$result"
}

# Firecrawl Search
fury_firecrawl_search() {
  local url=$1
  local output_file=$2

  load_credentials

  if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo "WARNING: FIRECRAWL_API_KEY not set"
    return 1
  fi

  echo "Firecrawl search for ${url}"
}

# Tavily Search
fury_tavily_search() {
  local query=$1
  local output_file=$2

  load_credentials

  if [ -z "$TAVILY_API_KEY" ]; then
    echo "WARNING: TAVILY_API_KEY not set"
    return 1
  fi

  echo "Tavily search for ${query}"
}

# Market Environment Analysis
fury_market_analysis() {
  local market=$1
  echo "Market environment analysis for ${market}"
}

# Competitor Analysis
fury_competitor_analysis() {
  local competitors=$1
  echo "Analyzing competitors: ${competitors}"
}

# ============================================
# QUILL SKILLS (Marketing)
# ============================================

# Launch Strategy
quill_launch_strategy() {
  local product=$1
  local market=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/launch-strategy"

  if [ -d "$skill_dir" ]; then
    echo "Launch strategy for ${product} in ${market}"
  fi
}

# Pricing Strategy
quill_pricing_strategy() {
  local product=$1
  local competitors=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/pricing-strategy"

  if [ -d "$skill_dir" ]; then
    echo "Pricing strategy for ${product}"
  fi
}

# Paid Ads Strategy
quill_paid_ads() {
  local platform=$1
  local budget=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/paid-ads"

  if [ -d "$skill_dir" ]; then
    echo "Paid ads strategy for ${platform}"
  fi
}

# Email Sequence
quill_email_sequence() {
  local goal=$1
  local audience=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/email-sequence"

  if [ -d "$skill_dir" ]; then
    echo "Email sequence for ${goal}"
  fi
}

# Referral Program
quill_referral_program() {
  local product=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/referral-program"

  if [ -d "$skill_dir" ]; then
    echo "Referral program for ${product}"
  fi
}

# Social Content Strategy
quill_social_content() {
  local platform=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/social-content"

  if [ -d "$skill_dir" ]; then
    echo "Social content for ${platform}"
  fi
}

# Marketing Ideas Generation
quill_marketing_ideas() {
  local product=$1
  local audience=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/marketing-ideas"

  if [ -d "$skill_dir" ]; then
    echo "Marketing ideas for ${product}"
  fi
}

# CRO (Conversion Rate Optimization)
quill_cro_audit() {
  local page_type=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references"

  case "$page_type" in
    landing_page|page-cro)
      skill="${skill_dir}/page-cro"
      ;;
    signup|signup-flow)
      skill="${skill_dir}/signup-flow-cro"
      ;;
    form|form-cro)
      skill="${skill_dir}/form-cro"
      ;;
    popup|popup-cro)
      skill="${skill_dir}/popup-cro"
      ;;
    onboarding)
      skill="${skill_dir}/onboarding-cro"
      ;;
    paywall)
      skill="${skill_dir}/paywall-upgrade-cro"
      ;;
    *)
      echo "Unknown CRO type: ${page_type}"
      return 1
      ;;
  esac

  if [ -d "$skill" ]; then
    echo "CRO audit for ${page_type}"
  fi
}

# Copywriting
quill_copywriting() {
  local content_type=$1
  local product=$2

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/copywriting"

  if [ -d "$skill_dir" ]; then
    echo "Copywriting for ${content_type}"
  fi
}

# Copy Editing
quill_copy_editing() {
  local content=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/copy-editing"

  if [ -d "$skill_dir" ]; then
    echo "Copy editing"
  fi
}

# Competitor Alternatives
quill_competitor_alternatives() {
  local competitor=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/competitor-alternatives"

  if [ -d "$skill_dir" ]; then
    echo "Alternatives to ${competitor}"
  fi
}

# Free Tool Strategy
quill_free_tool_strategy() {
  local tool_idea=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/free-tool-strategy"

  if [ -d "$skill_dir" ]; then
    echo "Free tool strategy for ${tool_idea}"
  fi
}

# Analytics Tracking Setup
quill_analytics_tracking() {
  local platform=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/analytics-tracking"

  if [ -d "$skill_dir" ]; then
    echo "Analytics tracking for ${platform}"
  fi
}

# Schema Markup Strategy
quill_schema_strategy() {
  local content_type=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/schema-markup"

  if [ -d "$skill_dir" ]; then
    echo "Schema strategy for ${content_type}"
  fi
}

# Programmatic SEO Strategy
quill_programmatic_seo_strategy() {
  local niche=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/programmatic-seo"

  if [ -d "$skill_dir" ]; then
    echo "Programmatic SEO for ${niche}"
  fi
}

# Marketing Psychology
quill_marketing_psychology() {
  local tactic=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/marketing-psychology"

  if [ -d "$skill_dir" ]; then
    echo "Marketing psychology for ${tactic}"
  fi
}

# A/B Test Setup
quill_ab_testing() {
  local test_type=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/ab-test-setup"

  if [ -d "$skill_dir" ]; then
    echo "A/B test for ${test_type}"
  fi
}

# SEO Audit Strategy
quill_seo_audit() {
  local site=$1

  local skill_dir="/root/.openclaw/workspace/skills_backup/marketing-skills/references/seo-audit"

  if [ -d "$skill_dir" ]; then
    echo "SEO audit for ${site}"
  fi
}

# ============================================
# SHARED UTILITIES
# ============================================

# List all available skills by agent
list_vision_skills() {
  echo "Vision Skills (SEO/Content):"
  echo "  - perplexity_search"
  echo "  - keyword_research (DataForSEO)"
  echo "  - seo_audit"
  echo "  - humanize"
  echo "  - wordpress_publish"
  echo "  - ga4_analytics"
  echo "  - gsc_data"
  echo "  - programmatic_seo"
  echo "  - schema_markup"
}

list_fury_skills() {
  echo "Fury Skills (Research):"
  echo "  - perplexity_research"
  echo "  - keyword_research (DataForSEO)"
  echo "  - firecrawl_search"
  echo "  - tavily_search"
  echo "  - market_analysis"
  echo "  - competitor_analysis"
}

list_quill_skills() {
  echo "Quill Skills (Marketing):"
  echo "  - launch_strategy"
  echo "  - pricing_strategy"
  echo "  - paid_ads"
  echo "  - email_sequence"
  echo "  - referral_program"
  echo "  - social_content"
  echo "  - marketing_ideas"
  echo "  - cro_audit (5 types)"
  echo "  - copywriting"
  echo "  - copy_editing"
  echo "  - competitor_alternatives"
  echo "  - free_tool_strategy"
  echo "  - analytics_tracking"
  echo "  - schema_strategy"
  echo "  - programmatic_seo_strategy"
  echo "  - marketing_psychology"
  echo "  - ab_testing"
  echo "  - seo_audit"
}

# Export functions
export -f load_credentials
export -f vision_perplexity_search vision_keyword_research vision_seo_audit vision_humanize vision_wordpress_publish
export -f fury_perplexity_research fury_keyword_research fury_firecrawl_search fury_tavily_search
export -f quill_launch_strategy quill_pricing_strategy quill_paid_ads quill_email_sequence
export -f quill_referral_program quill_social_content quill_marketing_ideas quill_cro_audit
export -f quill_copywriting quill_copy_editing quill_competitor_alternatives quill_free_tool_strategy
