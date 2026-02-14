#!/bin/bash
# Fury's SERP analysis script (INTEGRATED WITH PERPLEXITY SKILL)
# Uses Perplexity AI for competitor research and SERP analysis

TASK_ID=$1
TASK_TITLE=$2
TASK_DESCRIPTION=$3

# Source skills integration
source /root/.openclaw/workspace/agents/shared/skills-integration.sh

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "Fury: SERP Analysis (INTEGRATED WITH PERPLEXITY)" >> "$LOG_FILE"
echo "Task: ${TASK_TITLE}" >> "$LOG_FILE"

# Extract keywords from task title or description
# Try title first: "SERP Analysis for: crash gambling, crash casino bonus"
if [[ "$TASK_TITLE" =~ .+:\s+(.+) ]]; then
  KEYWORDS="${BASH_REMATCH[1]}"
else
  # Try description: "Analyze keywords for 5 articles: crash casino bonus, crypto vs fiat..."
  if [[ "$TASK_TITLE" =~ [Ss][Ee][Rr][Pp] ]] && [ -n "$TASK_DESCRIPTION" ]; then
    # Extract keywords from description (look for list after colon)
    if [[ "$TASK_DESCRIPTION" =~ .+:\s+(.+) ]]; then
      KEYWORDS="${BASH_REMATCH[1]}"
    else
      KEYWORDS="$TASK_DESCRIPTION"
    fi
  else
    echo "ERROR: Could not extract keywords from task" >> "$LOG_FILE"
    echo "Title: $TASK_TITLE" >> "$LOG_FILE"
    echo "Description: $TASK_DESCRIPTION" >> "$LOG_FILE"
    exit 1
  fi
fi

echo "Keywords to analyze: ${KEYWORDS}" >> "$LOG_FILE"

# Use Perplexity skill for research
PERPLEXITY_SKILL="/root/.openclaw/workspace/skills/perplexity"

if [ ! -d "$PERPLEXITY_SKILL" ]; then
  echo "ERROR: Perplexity skill not found" >> "$LOG_FILE"
  exit 1
fi

# Create output directory for research
OUTPUT_DIR="/root/.openclaw/workspace/tasks/research/${TASK_ID}"
mkdir -p "$OUTPUT_DIR"

echo "Starting Perplexity research..." >> "$LOG_FILE"

# Convert comma-separated keywords to array
IFS=',' read -ra KEYWORD_ARRAY <<< "$KEYWORDS"

for keyword in "${KEYWORD_ARRAY[@]}"; do
  # Trim whitespace
  keyword=$(echo "$keyword" | xargs)

  echo "" >> "$LOG_FILE"
  echo "Researching keyword: ${keyword}" >> "$LOG_FILE"

  # Use Perplexity to research
  # Query format: "Top ranking articles for [keyword], their content strategy, and SEO opportunities"
  PERPLEXITY_QUERY="Top 10 ranking articles for '${keyword}', their word count, backlink profile estimate, content gaps, and SEO opportunities"

  echo "Query: ${PERPLEXITY_QUERY}" >> "$LOG_FILE"

  # Run Perplexity search
  cd "$PERPLEXITY_SKILL"
  RESULT=$(node scripts/search.mjs "$PERPLEXITY_QUERY" 2>&1)

  # Save result to file
  OUTPUT_FILE="${OUTPUT_DIR}/${keyword// /_}_serp_analysis.txt"
  echo "$RESULT" >> "$OUTPUT_FILE"

  echo "SERP analysis saved to: ${OUTPUT_FILE}" >> "$LOG_FILE"

  # Extract key insights (basic parsing)
  echo "Extracting key insights..." >> "$LOG_FILE"

  # Look for ranking URLs
  echo "$RESULT" | grep -oP 'https?://[^\s)+"' | head -10 >> "${OUTPUT_DIR}/${keyword// /_}_urls.txt"

  echo "Completed keyword: ${keyword}" >> "$LOG_FILE"
done

# Create summary report
echo "" >> "$LOG_FILE"
echo "=== SERP Analysis Complete ===" >> "$LOG_FILE"
echo "Total keywords analyzed: ${#KEYWORD_ARRAY[@]}" >> "$LOG_FILE"
echo "Results saved to: ${OUTPUT_DIR}" >> "$LOG_FILE"

# Generate summary markdown
SUMMARY_MD="${OUTPUT_DIR}/SERP_Analysis_Summary.md"
cat > "$SUMMARY_MD" << EOF
# SERP Analysis Summary

**Task:** ${TASK_TITLE}
**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Analyzed By:** Fury 🔍

## Keywords Analyzed

EOF

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "- ${keyword}" >> "$SUMMARY_MD"
done

echo "" >> "$SUMMARY_MD"
echo "## Detailed Analysis Files" >> "$SUMMARY_MD"

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "" >> "$SUMMARY_MD"
  echo "### ${keyword}" >> "$SUMMARY_MD"
  echo "- Full analysis: \`${keyword// /_}_serp_analysis.txt\`" >> "$SUMMARY_MD"
  echo "- Top URLs: \`${keyword// /_}_urls.txt\`" >> "$SUMMARY_MD"
done

echo "SERP analysis summary created: ${SUMMARY_MD}" >> "$LOG_FILE"

echo "SERP analysis complete" >> "$LOG_FILE"
exit 0
