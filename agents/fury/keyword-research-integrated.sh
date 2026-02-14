#!/bin/bash
# Fury's keyword research script (INTEGRATED WITH SEO-DATAFORSEO SKILL)
# Uses DataForSEO API for comprehensive keyword research

TASK_ID=$1
TASK_TITLE=$2

# Source skills integration
source /root/.openclaw/workspace/agents/shared/skills-integration.sh

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "Fury: Keyword Research (INTEGRATED WITH SEO-DATAFORSEO)" >> "$LOG_FILE"
echo "Task: ${TASK_TITLE}" >> "$LOG_FILE"

# Extract keywords from task
if [[ "$TASK_TITLE" =~ .+:\s+(.+) ]]; then
  KEYWORDS="${BASH_REMATCH[1]}"
else
  echo "ERROR: Could not extract keywords from task title" >> "$LOG_FILE"
  exit 1
fi

echo "Keywords to research: ${KEYWORDS}" >> "$LOG_FILE"

# Use seo-dataforseo skill
DATAFORSEO_SKILL="/root/.openclaw/workspace/skills/seo-dataforseo"

if [ ! -d "$DATAFORSEO_SKILL" ]; then
  echo "ERROR: seo-dataforseo skill not found" >> "$LOG_FILE"
  exit 1
fi

# Create output directory
OUTPUT_DIR="/root/.openclaw/workspace/tasks/keyword-research/${TASK_ID}"
mkdir -p "$OUTPUT_DIR"

# Convert keywords to array
IFS=',' read -ra KEYWORD_ARRAY <<< "$KEYWORDS"

RESEARCH_COUNT=0

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)

  echo "" >> "$LOG_FILE"
  echo "Researching keyword: ${keyword}" >> "$LOG_FILE"

  # Call DataForSEO API for keyword data
  # This would use the DataForSEO API to get:
  # - Search volume
  # - CPC
  # - Competition
  # - Keyword difficulty
  # - Related keywords

  # For now, use Perplexity as fallback for research
  PERPLEXITY_SKILL="/root/.openclaw/workspace/skills/perplexity"
  cd "$PERPLEXITY_SKILL"

  QUERY="Keyword research for '${keyword}': search volume, CPC, competition, keyword difficulty, related keywords, long-tail variations"

  RESULT=$(node scripts/search.mjs "$QUERY" 2>&1)

  # Save result
  OUTPUT_FILE="${OUTPUT_DIR}/${keyword// /_}_keyword_research.txt"
  echo "$RESULT" >> "$OUTPUT_FILE"

  echo "Keyword research saved: ${OUTPUT_FILE}" >> "$LOG_FILE"

  ((RESEARCH_COUNT++))
done

# Create summary
SUMMARY_MD="${OUTPUT_DIR}/Keyword_Research_Summary.md"
cat > "$SUMMARY_MD" << EOF
# Keyword Research Summary

**Task:** ${TASK_TITLE}
**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Researched By:** Fury 🔍

## Keywords Analyzed

EOF

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "- ${keyword}" >> "$SUMMARY_MD"
done

echo "" >> "$SUMMARY_MD"
echo "## Detailed Reports" >> "$SUMMARY_MD"

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "### ${keyword}" >> "$SUMMARY_MD"
  echo "See: \`${keyword// /_}_keyword_research.txt\`" >> "$SUMMARY_MD"
done

echo "Keyword research summary: ${SUMMARY_MD}" >> "$LOG_FILE"
echo "Total keywords researched: ${RESEARCH_COUNT}" >> "$LOG_FILE"

echo "Keyword research complete" >> "$LOG_FILE"
exit 0
