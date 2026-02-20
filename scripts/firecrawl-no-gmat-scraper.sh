#!/bin/bash
# Firecrawl-powered scraper for no-GMAT MBA programs
# API Key: fc-728da301284d4082a2c6b4069bf29f06

API_KEY="fc-728da301284d4082a2c6b4069bf29f06"
OUTPUT_DIR="/root/.openclaw/workspace/research"
CSV_FILE="$OUTPUT_DIR/onlinembaprograms-no-gmat-firecrawl.csv"
SUMMARY_FILE="$OUTPUT_DIR/onlinembaprograms-no-gmat-firecrawl-summary.md"

# Create CSV header
echo "school_name,program_name,tuition_total,format,duration,accreditation,gmat_requirement,gmat_waiver_details,program_url,source_url,date_scraped" > "$CSV_FILE"

# URLs to scrape (no-GMAT focused)
URLS=(
    "https://www.onlinemba.com"
    "https://www.onlinemba.com/gmat-requirements/"
    "https://www.onlinemba.com/guides/no-gmat/"
    "https://www.onlinemba.com/rankings/best-online-mba/"
    "https://www.mbaguide.org"
    "https://www.geteducated.com"
)

echo "# No-GMAT MBA Programs - Firecrawl Research" > "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "**Date:** $(date)" >> "$SUMMARY_FILE"
echo "**Method:** Firecrawl API v1" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Scraping Progress" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

total_urls=${#URLS[@]}
current=0

for url in "${URLS[@]}"; do
    ((current++))
    echo "[$current/$total_urls] Scraping: $url"

    echo "### [$current/$total_urls] $url" >> "$SUMMARY_FILE"
    echo "**Status:** Scraping..." >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # Scrape URL
    response=$(curl -s -X POST https://api.firecrawl.dev/v1/scrape \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{\"url\": \"$url\"}")

    # Check if successful
    if echo "$response" | jq -e '.success == true' > /dev/null 2>&1; then
        # Extract markdown
        markdown=$(echo "$response" | jq -r '.data.markdown' 2>/dev/null)

        if [ -n "$markdown" ]; then
            # Save markdown to separate file
            safe_name=$(echo "$url" | sed 's|https://||' | sed 's|/|-|g' | sed 's|\.|-|g')
            markdown_file="$OUTPUT_DIR/firecrawl-${safe_name}.md"
            echo "$markdown" > "$markdown_file"

            # Update summary
            echo "**Status:** ✅ Success" >> "$SUMMARY_FILE"
            echo "**Markdown saved:** \`$markdown_file\` ($(wc -c < "$markdown_file") bytes)" >> "$SUMMARY_FILE"
            echo "" >> "$SUMMARY_FILE"

            # Count programs mentioned
            program_count=$(echo "$markdown" | grep -i "university\|school\|college" | wc -l)
            echo "**Programs mentioned:** ~$program_count" >> "$SUMMARY_FILE"
            echo "" >> "$SUMMARY_FILE"
        else
            echo "**Status:** ❌ No markdown data" >> "$SUMMARY_FILE"
            echo "" >> "$SUMMARY_FILE"
        fi
    else
        error=$(echo "$response" | jq -r '.error' 2>/dev/null || echo "Unknown error")
        echo "**Status:** ❌ Failed - $error" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
    fi

    # Rate limiting - wait between requests
    sleep 2
done

echo "## Summary" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "- **Total URLs scraped:** $total_urls" >> "$SUMMARY_FILE"
echo "- **Output CSV:** \`$CSV_FILE\`" >> "$SUMMARY_FILE"
echo "- **Markdown files:** \`$OUTPUT_DIR/firecrawl-*.md\`" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Next Steps" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "1. Review markdown files for program details" >> "$SUMMARY_FILE"
echo "2. Extract no-GMAT programs from content" >> "$SUMMARY_FILE"
echo "3. Populate CSV with verified program data" >> "$SUMMARY_FILE"
echo "4. Create final summary report" >> "$SUMMARY_FILE"

echo ""
echo "✅ Scraping complete!"
echo "📄 Summary: $SUMMARY_FILE"
echo "📊 CSV: $CSV_FILE"
echo "📁 Markdown files: $OUTPUT_DIR/firecrawl-*.md"
