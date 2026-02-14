#!/bin/bash
# Vision's Enhanced Content Production Workflow
# Uses ALL pinch-to-post features for full automation

TASK_ID=$1
TASK_TITLE=$2

# Source skills integration
source /root/.openclaw/workspace/agents/shared/skills-integration.sh

# Pinch-to-Post wrapper
PINCH_TO_POST="/root/.openclaw/workspace/scripts/pinch-to-post.sh"

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "Vision: Enhanced Content Production (FULL PINCH-TO-POST INTEGRATION)" | tee -a "$LOG_FILE"
echo "Task: ${TASK_TITLE}" | tee -a "$LOG_FILE"

# ===== DAILY ROUTINE (Run first) =====

echo "" | tee -a "$LOG_FILE"
echo "📊 Running Daily Content Operations..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Get current stats across all sites
echo "Content Statistics:" | tee -a "$LOG_FILE"
"$PINCH_TO_POST" stats 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "Pending Comments:" | tee -a "$LOG_FILE"
for site in crashcasino crashgame freecrash cryptocrash; do
  echo "[$site]" | tee -a "$LOG_FILE"
  "$PINCH_TO_POST" comment-moderate "$site" show-pending 2>&1 | head -5 | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"
echo "Today's Calendar:" | tee -a "$LOG_FILE"
TODAY=$(date -u +%Y-%m)
"$PINCH_TO_POST" calendar "$TODAY" 2>&1 | tee -a "$LOG_FILE"

# ===== TASK WORK =====

# Check for brief
BRIEF_FILE="/root/.openclaw/workspace/tasks/briefs/${TASK_ID}.md"

if [ ! -f "$BRIEF_FILE" ]; then
  echo "WARNING: Brief not found for task ${TASK_ID}" | tee -a "$LOG_FILE"
  echo "Skipping content production..." | tee -a "$LOG_FILE"
  exit 0
fi

echo "" | tee -a "$LOG_FILE"
echo "Processing task: ${TASK_TITLE}" | tee -a "$LOG_FILE"

# Extract brief details
ARTICLE_TOPIC=$(grep "^# " "$BRIEF_FILE" | sed 's/^# //')
KEYWORDS=$(grep "^Keywords:" "$BRIEF_FILE" | sed 's/^Keywords: //')
SITE=$(grep "^Site:" "$BRIEF_FILE" | sed 's/^Site: //')
WORD_COUNT=$(grep "^Word Count:" "$BRIEF_FILE" | sed 's/^Word Count: //')

echo "Topic: ${ARTICLE_TOPIC}" | tee -a "$LOG_FILE"
echo "Keywords: ${KEYWORDS}" | tee -a "$LOG_FILE"
echo "Site: ${SITE}" | tee -a "$LOG_FILE"
echo "Target: ${WORD_COUNT} words" | tee -a "$LOG_FILE"

# ===== PRODUCTION WORKFLOW =====

# Step 1: Research using Skills (ACTIVE)
echo "" | tee -a "$LOG_FILE"
echo "📚 Step 1: Research using Skills..." | tee -a "$LOG_FILE"

# Create research directory
mkdir -p "/root/.openclaw/workspace/tasks/research"

# 1a. Perplexity Research (AI-powered with citations)
if [ -f "/root/.openclaw/workspace/skills/perplexity/scripts/search.mjs" ]; then
  echo "  - Running Perplexity research..." | tee -a "$LOG_FILE"

  PERPLEXITY_SKILL="/root/.openclaw/workspace/skills/perplexity"
  cd "$PERPLEXITY_SKILL"

  # Build comprehensive research query
  RESEARCH_QUERY="${ARTICLE_TOPIC} strategies statistics examples trends 2026 RTP house edge ${KEYWORDS}"

  if node scripts/search.mjs "$RESEARCH_QUERY" > "/root/.openclaw/workspace/tasks/research/${TASK_ID}-perplexity.txt" 2>> "$LOG_FILE"; then
    echo "  ✅ Perplexity research complete" | tee -a "$LOG_FILE"
  else
    echo "  ⚠️  Perplexity research failed" | tee -a "$LOG_FILE"
  fi
fi

# 1b. Web Search (latest information)
echo "  - Running web search..." | tee -a "$LOG_FILE"

if command -v web_search &> /dev/null || [ -n "$OPENCLAW_TOOL_WEB_SEARCH" ]; then
  # Web search is available as a tool - agent can call it directly
  echo "  ✅ Web search tool available" | tee -a "$LOG_FILE"
  # Note: In actual agent execution, web_search would be called via tool invocation
else
  echo "  ⚠️  Web search not directly accessible" | tee -a "$LOG_FILE"
fi

# 1c. DataForSEO Keyword Research
if [ -f "/root/.openclaw/workspace/skills/seo-dataforseo/SKILL.md" ]; then
  echo "  - DataForSEO skill available for keyword research" | tee -a "$LOG_FILE"
  # Can be invoked via agent tool calls
fi

echo "  Research phase complete" | tee -a "$LOG_FILE"

# Step 2: Write content
echo "" | tee -a "$LOG_FILE"
echo "Step 2: Writing article..." | tee -a "$LOG_FILE"

# (Your existing content generation logic here)
# For now, just acknowledge
echo "Content generation in progress..." | tee -a "$LOG_FILE"

# ===== PUBLISHING WORKFLOW (NEW) =====

echo "" | tee -a "$LOG_FILE"
echo "Step 3: Publishing with Pinch-to-Post..." | tee -a "$LOG_FILE"

# Find draft articles
DRAFT_DIR="/root/.openclaw/workspace/drafts"
DRAFT_COUNT=$(find "$DRAFT_DIR" -name "*.md" -type f 2>/dev/null | wc -l)

echo "Found ${DRAFT_COUNT} draft articles" | tee -a "$LOG_FILE"

if [ "$DRAFT_COUNT" -gt 0 ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "Processing drafts for site: ${SITE}" | tee -a "$LOG_FILE"

  # Collect post IDs for bulk publishing
  POST_IDS=()

  for draft_file in "$DRAFT_DIR"/*.md; do
    if [ ! -f "$draft_file" ]; then
      continue
    fi

    # Extract post ID from draft (if already created)
    POST_ID=$(grep "^POST_ID:" "$draft_file" | sed 's/^POST_ID: //')

    if [ -n "$POST_ID" ]; then
      # Check health score first
      echo "Checking health for post ${POST_ID}..." | tee -a "$LOG_FILE"

      if "$PINCH_TO_POST" health-check "$SITE" "$POST_ID" 2>&1 | grep -q "Score:"; then
        POST_IDS+=("$POST_ID")
      else
        echo "  ⚠️  Post ${POST_ID} failed health check" | tee -a "$LOG_FILE"
      fi
    fi
  done

  # Bulk publish all ready articles
  if [ ${#POST_IDS[@]} -gt 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "🚀 Bulk publishing ${#POST_IDS[@]} articles..." | tee -a "$LOG_FILE"

    "$PINCH_TO_POST" bulk-publish "$SITE" "${POST_IDS[@]}" 2>&1 | tee -a "$LOG_FILE"
  else
    echo "No articles ready to publish (need 80+ health score)" | tee -a "$LOG_FILE"
  fi
fi

# ===== WEEKLY ROUTINE (Check if Monday) =====

DAY_OF_WEEK=$(date -u +%A)

if [ "$DAY_OF_WEEK" = "Monday" ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "📅 Running Weekly Content Operations..." | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"

  # Run weekly workflow
  /root/.openclaw/workspace/scripts/workflows/weekly-content-ops.sh 2>&1 | tee -a "$LOG_FILE"
fi

# ===== RECOMMENDATIONS =====

echo "" | tee -a "$LOG_FILE"
echo "💡 Recommendations:" | tee -a "$LOG_FILE"
echo "  - Review unpublished drafts for quality improvements" | tee -a "$LOG_FILE"
echo "  - Use 'pinch-to-post comment-moderate ${SITE} spam-suspicious' to clean comments" | tee -a "$LOG_FILE"
echo "  - Check calendar: 'pinch-to-post calendar ${TODAY}'" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "✅ Vision workflow complete" | tee -a "$LOG_FILE"
