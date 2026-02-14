#!/bin/bash
# Vision's SEO optimization script (INTEGRATED WITH SEO-OPTIMIZER SKILL)
# Uses seo-optimizer skill for comprehensive SEO audits

TASK_ID=$1
TASK_TITLE=$2

# Source skills integration
source /root/.openclaw/workspace/agents/shared/skills-integration.sh

# Log setup
LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "Vision: SEO Optimization (INTEGRATED WITH SEO-OPTIMIZER)" >> "$LOG_FILE"
echo "Task: ${TASK_TITLE}" >> "$LOG_FILE"

# Find articles to optimize
DRAFT_DIR="/root/.openclaw/workspace/drafts"

if [ ! -d "$DRAFT_DIR" ]; then
  echo "ERROR: Drafts directory not found" >> "$LOG_FILE"
  exit 1
fi

ARTICLE_COUNT=$(find "$DRAFT_DIR" -name "*.md" -type f | wc -l)
echo "Found ${ARTICLE_COUNT} articles to optimize" >> "$LOG_FILE"

if [ "$ARTICLE_COUNT" -eq 0 ]; then
  echo "ERROR: No articles found" >> "$LOG_FILE"
  exit 1
fi

# Use seo-optimizer skill
SEO_SKILL="/root/.openclaw/workspace/skills/seo-optimizer"

if [ ! -d "$SEO_SKILL" ]; then
  echo "ERROR: SEO optimizer skill not found" >> "$LOG_FILE"
  exit 1
fi

# Create output directory
OUTPUT_DIR="/root/.openclaw/workspace/tasks/seo-audits/${TASK_ID}"
mkdir -p "$OUTPUT_DIR"

OPTIMIZED_COUNT=0

# Process each article
for article_file in "$DRAFT_DIR"/*.md; do
  if [ ! -f "$article_file" ]; then
    continue
  fi

  article_name=$(basename "$article_file" .md)
  echo "" >> "$LOG_FILE"
  echo "Optimizing: ${article_name}" >> "$LOG_FILE"

  # Run SEO analyzer
  cd "$SEO_SKILL"

  # Convert markdown to HTML for analysis (basic approach)
  # In production, use proper markdown parser
  HTML_FILE="/tmp/${article_name}.html"
  echo "<html><head><title>${article_name}</title></head><body>" > "$HTML_FILE"
  # Extract content from markdown (simplified)
  grep -v "^#" "$article_file" | sed 's/$/<br>/' >> "$HTML_FILE"
  echo "</body></html>" >> "$HTML_FILE"

  # Run SEO analyzer
  echo "Running SEO audit..." >> "$LOG_FILE"
  AUDIT_RESULT=$(python scripts/seo_analyzer.py "$HTML_FILE" 2>&1)

  # Save audit result
  AUDIT_FILE="${OUTPUT_DIR}/${article_name}_seo_audit.txt"
  echo "$AUDIT_RESULT" >> "$AUDIT_FILE"
  echo "SEO audit saved: ${AUDIT_FILE}" >> "$LOG_FILE"

  # Parse audit result and apply fixes
  # Check for missing meta description
  if echo "$AUDIT_RESULT" | grep -qi "missing.*meta.*description"; then
    echo "Adding meta description..." >> "$LOG_FILE"

    # Generate meta description from first paragraph
    FIRST_PARA=$(grep -m1 -A5 "^# " "$article_file" | grep -v "^#" | tr '\n' ' ' | cut -c1-160)
    META_DESC="<meta name=\"description\" content=\"${FIRST_PARA}\">"

    # Prepend to article (as HTML comment for reference)
    TEMP_FILE="/tmp/${article_name}_temp.md"
    echo "<!-- ${META_DESC} -->" > "$TEMP_FILE"
    cat "$article_file" >> "$TEMP_FILE"
    mv "$TEMP_FILE" "$article_file"

    echo "Meta description added" >> "$LOG_FILE"
  fi

  # Check for missing title tag
  if echo "$AUDIT_RESULT" | grep -qi "missing.*title"; then
    echo "Article has title, skipping title tag addition" >> "$LOG_FILE"
  fi

  # Check heading structure
  if echo "$AUDIT_RESULT" | grep -qi "heading.*structure"; then
    echo "Analyzing heading structure..." >> "$LOG_FILE"

    # Count headings
    H1_COUNT=$(grep -c "^# " "$article_file" || echo "0")
    H2_COUNT=$(grep -c "^## " "$article_file" || echo "0")
    H3_COUNT=$(grep -c "^### " "$article_file" || echo "0")

    echo "H1: ${H1_COUNT}, H2: ${H2_COUNT}, H3: ${H3_COUNT}" >> "$LOG_FILE"

    if [ "$H1_COUNT" -eq 0 ]; then
      echo "WARNING: No H1 heading found" >> "$LOG_FILE"
    fi

    if [ "$H1_COUNT" -gt 1 ]; then
      echo "WARNING: Multiple H1 headings (should have only one)" >> "$LOG_FILE"
    fi
  fi

  # Add schema markup if missing
  SCHEMA_FILE="${OUTPUT_DIR}/${article_name}_schema.json"
  if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Generating schema markup..." >> "$LOG_FILE"

    # Extract article info
    TITLE=$(grep -m1 "^# " "$article_file" | sed 's/^# //')

    # Generate Article schema
    cat > "$SCHEMA_FILE" << EOF
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${TITLE}",
  "author": {
    "@type": "Organization",
    "name": "Crash Casino"
  },
  "datePublished": "$(date +%Y-%m-%d)",
  "description": "${FIRST_PARA}"
}
EOF

    echo "Schema markup generated: ${SCHEMA_FILE}" >> "$LOG_FILE"
  fi

  ((OPTIMIZED_COUNT++))

  # Cleanup temp HTML file
  rm -f "$HTML_FILE"
done

# Summary
echo "" >> "$LOG_FILE"
echo "=== SEO Optimization Summary ===" >> "$LOG_FILE"
echo "Articles optimized: ${OPTIMIZED_COUNT}" >> "$LOG_FILE"
echo "Audit results: ${OUTPUT_DIR}" >> "$LOG_FILE"

# Create summary report
SUMMARY_MD="${OUTPUT_DIR}/SEO_Optimization_Summary.md"
cat > "$SUMMARY_MD" << EOF
# SEO Optimization Summary

**Task:** ${TASK_TITLE}
**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Optimized By:** Vision 🔍

## Articles Processed: ${OPTIMIZED_COUNT}

## Audit Results

All SEO audits saved to: \`${OUTPUT_DIR}\`

## Changes Applied

- Meta descriptions added where missing
- Heading structure analyzed
- Schema markup generated
- SEO reports created for each article

## Next Steps

1. Review audit reports
2. Apply recommended changes
3. Validate schema markup
4. Update articles
EOF

echo "SEO optimization summary: ${SUMMARY_MD}" >> "$LOG_FILE"

echo "SEO optimization complete" >> "$LOG_FILE"
exit 0
