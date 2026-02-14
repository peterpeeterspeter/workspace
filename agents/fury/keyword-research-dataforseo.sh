#!/bin/bash
# Fury's keyword research script (FULLY INTEGRATED WITH DATAFORSEO)
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
echo "Fury: Keyword Research (FULLY INTEGRATED WITH DATAFORSEO)" >> "$LOG_FILE"
echo "Task: ${TASK_TITLE}" >> "$LOG_FILE"

# Extract keywords from task
if [[ "$TASK_TITLE" =~ .+:\s+(.+) ]]; then
  KEYWORDS="${BASH_REMATCH[1]}"
else
  echo "ERROR: Could not extract keywords from task title" >> "$LOG_FILE"
  exit 1
fi

echo "Keywords to research: ${KEYWORDS}" >> "$LOG_FILE"

# Use DataForSEO skill (ALREADY CONFIGURED!)
DATAFORSEO_SKILL="/root/.openclaw/workspace/skills/seo-dataforseo"

if [ ! -d "$DATAFORSEO_SKILL" ]; then
  echo "ERROR: DataForSEO skill not found" >> "$LOG_FILE"
  exit 1
fi

# Create output directory
OUTPUT_DIR="/root/.openclaw/workspace/tasks/keyword-research/${TASK_ID}"
mkdir -p "$OUTPUT_DIR"

cd "$DATAFORSEO_SKILL/scripts"

# Convert keywords to array
IFS=',' read -ra KEYWORD_ARRAY <<< "$KEYWORDS"

RESEARCH_COUNT=0

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)

  echo "" >> "$LOG_FILE"
  echo "Researching keyword: ${keyword}" >> "$LOG_FILE"

  # Run DataForSEO keyword research using Python API
  echo "Calling DataForSEO API..." >> "$LOG_FILE"

  RESULT=$(python3 -c "
import sys
sys.path.insert(0, '.')
from main import keyword_research
result = keyword_research('${keyword}')
print(result)
" 2>&1)

  # Save result
  OUTPUT_FILE="${OUTPUT_DIR}/${keyword// /_}_dataforseo_research.json"
  echo "$RESULT" >> "$OUTPUT_FILE"

  echo "DataForSEO research saved: ${OUTPUT_FILE}" >> "$LOG_FILE"

  # Also save as readable text
  TEXT_FILE="${OUTPUT_DIR}/${keyword// /_}_summary.txt"
  echo "Keyword: ${keyword}" >> "$TEXT_FILE"
  echo "Source: DataForSEO API" >> "$TEXT_FILE"
  echo "Date: $(date)" >> "$TEXT_FILE"
  echo "" >> "$TEXT_FILE"
  echo "$RESULT" >> "$TEXT_FILE"

  ((RESEARCH_COUNT++))
done

# Create markdown summary
SUMMARY_MD="${OUTPUT_DIR}/Keyword_Research_Summary.md"

cat > "$SUMMARY_MD" << EOF
# DataForSEO Keyword Research Summary

**Task:** ${TASK_TITLE}
**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Researched By:** Fury 🔍
**Data Source:** DataForSEO API

## Keywords Analyzed: ${RESEARCH_COUNT}

EOF

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "- ${keyword}" >> "$SUMMARY_MD"
done

echo "" >> "$SUMMARY_MD"
echo "## Detailed Reports" >> "$SUMMARY_MD"

for keyword in "${KEYWORD_ARRAY[@]}"; do
  keyword=$(echo "$keyword" | xargs)
  echo "" >> "$SUMMARY_MD"
  echo "### ${keyword}" >> "$SUMMARY_MD"
  echo "- Full data: \`${keyword// /_}_dataforseo_research.json\`" >> "$SUMMARY_MD"
  echo "- Summary: \`${keyword// /_}_summary.txt\`" >> "$SUMMARY_MD"
done

echo "Keyword research summary: ${SUMMARY_MD}" >> "$LOG_FILE"
echo "Total keywords researched: ${RESEARCH_COUNT}" >> "$LOG_FILE"

echo "DataForSEO keyword research complete" >> "$LOG_FILE"
exit 0
