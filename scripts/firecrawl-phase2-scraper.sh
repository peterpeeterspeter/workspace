#!/bin/bash
# Firecrawl scraper - Phase 2: Individual University Program Pages
# Target: 30-50 total no-GMAT MBA programs
# API Key: fc-728da301284d4082a2c6b4069bf29f06

API_KEY="fc-728da301284d4082a2c6b4069bf29f06"
OUTPUT_DIR="/root/.openclaw/workspace/research"
CSV_FILE="$OUTPUT_DIR/onlinembaprograms-no-gmat-expanded.csv"
SUMMARY_FILE="$OUTPUT_DIR/onlinembaprograms-no-gmat-expanded-summary.md"

# Create CSV header with additional fields
echo "school_name,program_name,tuition_total,tuition_per_credit,format,duration,total_credits,accreditation,gmat_requirement,gmat_waiver_details,gre_accepted,application_deadline,class_size,avg_gpa,work_experience_required,program_url,source_url,date_scraped,confidence_score" > "$CSV_FILE"

# University program pages to scrape (known for no-GMAT or likely to have it)
# Phase 2a: Scrape detailed pages for 9 programs we already found
PHASE2A_URLS=(
    "https://onlinemba.unc.edu/program-overview/"
    "https://warrington.ufl.edu/mba/online/curriculum/"
    "https://carey.jhu.edu/programs/mba/online/academics"
    "https://www.usf.edu/business/graduate/mba-online/curriculum"
    "https://michiganross.umich.edu/graduate/cpn/online-mba/curriculum"
    "https://www.marshall.usc.edu/programs/online-mba/curriculum"
)

# Phase 2b: Top state universities (often flexible on GMAT)
PHASE2B_URLS=(
    "https://ischoolonline.berkeley.edu/business/"
    "https://mba.washington.edu/"
    "https://online.ohio.edu/mba/"
    "https://wisconsinbusiness.wisc.edu/"
    "https://online.smu.edu/mba/"
    "https://online.temple.edu/mba/"
    "https://www.cc-seminars.com/OnlineMBA"
    "https://umassglobal.edu/online-programs/mba"
    "https://online.uillinois.edu/mba"
    "https://www.purdueglobal.edu/online-programs/business/mba/"
)

# Phase 2c: Professional/Executive MBAs (often no GMAT for experienced pros)
PHASE2C_URLS=(
    "https://online.pepperdine.edu/mba/"
    "https://www.babson.edu/academics/graduate/online-mba"
    "https://www.uhd.edu/business/online-mba"
    "https://www.csupueblo.edu/online/mba"
    "https://online.fiu.edu/mba/"
    "https://mba.unt.edu/"
    "https://mays.tamu.edu/"
    "https://online.ecu.edu/mba/"
    "https://www.jmu.edu/mba/"
    "https://cbe.BoiseState.edu/online-mba"
)

# Phase 2d: Specialized programs (analytics, healthcare - often no GMAT)
PHASE2D_URLS=(
    "https://learn Bentley.edu/online-mba"
    "https://online.rit.edu/mba"
    "https://www.uah.edu/business/mba/online"
    "https://www.uafs.edu/online-mba"
    "https://online.apu.edu/mba/"
    "https://www.cuhelsinki.fi/"
)

# Combine all URLs
ALL_URLS=("${PHASE2A_URLS[@]}" "${PHASE2B_URLS[@]}" "${PHASE2C_URLS[@]}" "${PHASE2D_URLS[@]}")

echo "# No-GMAT MBA Programs - Expanded Research (Phase 2)" > "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "**Date:** $(date)" >> "$SUMMARY_FILE"
echo "**Target:** 30-50 programs" >> "$SUMMARY_FILE"
echo "**Method:** Firecrawl API v1 - University Program Pages" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Scraping Progress" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

total_urls=${#ALL_URLS[@]}
current=0
success_count=0
programs_found=0

# Create temporary directory for raw markdown
mkdir -p "$OUTPUT_DIR/firecrawl-phase2"

for url in "${ALL_URLS[@]}"; do
    ((current++))
    echo "[$current/$total_urls] Scraping: $url"

    echo "### [$current/$total_urls] $url" >> "$SUMMARY_FILE"
    echo "**Status:** Scraping..." >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # Scrape URL with longer timeout for program pages
    response=$(curl -s -X POST https://api.firecrawl.dev/v1/scrape \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{
            \"url\": \"$url\",
            \"formats\": [\"markdown\"]
        }" \
        --max-time 30)

    # Check if successful
    if echo "$response" | jq -e '.success == true' > /dev/null 2>&1; then
        # Extract markdown
        markdown=$(echo "$response" | jq -r '.data.markdown' 2>/dev/null)

        if [ -n "$markdown" ] && [ "$markdown" != "null" ]; then
            ((success_count++))

            # Save markdown to file
            safe_name=$(echo "$url" | sed 's|https://||' | sed 's|/|-|g' | sed 's|\.|-|g' | cut -c1-50)
            markdown_file="$OUTPUT_DIR/firecrawl-phase2/${safe_name}.md"
            echo "$markdown" > "$markdown_file"

            # Analyze for GMAT requirements
            gmat_status="Unknown"
            waiver_details=""

            # Check for no-GMAT indicators
            if echo "$markdown" | grep -iq "no gmat\|not require gmat\|gmat not required\|without gmat"; then
                gmat_status="Not Required"
                ((programs_found++))
            elif echo "$markdown" | grep -iq "gmat optional\|optional gmat\|gmat waived"; then
                gmat_status="Optional"
                ((programs_found++))
            elif echo "$markdown" | grep -iq "gmat waiver\|waiver.*gmat\|test waiver"; then
                gmat_status="Waiver Available"
                waiver_details=$(echo "$markdown" | grep -i -A 3 "gmat waiver\|waiver.*gmat" | head -4 | tr '\n' ' ' | sed 's/  */ /g')
                ((programs_found++))
            else
                gmat_status="Required"
            fi

            # Extract program name if available
            program_name=$(echo "$markdown" | grep -i "online mba\|master of business" | head -1 | sed 's/^#* *//' | cut -c1-100)

            # Extract tuition if available
            tuition=$(echo "$markdown" | grep -i -E "tuition.*\$|cost.*\$|per credit.*\$" | head -1 | sed 's/  */ /g')

            # Update summary
            echo "**Status:** ✅ Success" >> "$SUMMARY_FILE"
            echo "**GMAT:** $gmat_status" >> "$SUMMARY_FILE"
            if [ -n "$waiver_details" ]; then
                echo "**Waiver:** $waiver_details" >> "$SUMMARY_FILE"
            fi
            echo "**Program:** $program_name" >> "$SUMMARY_FILE"
            echo "**Markdown:** \`$(basename $markdown_file)\` ($(wc -c < "$markdown_file") bytes)" >> "$SUMMARY_FILE"
            echo "" >> "$SUMMARY_FILE"

            # Add to CSV if no-GMAT found
            if [[ "$gmat_status" =~ "(Not Required|Optional|Waiver Available)" ]]; then
                # Extract school name from URL
                school_name=$(echo "$url" | sed 's|https://||' | sed 's|/.*||' | sed 's|online\.||' | sed 's|www\.||')

                echo "$school_name,\"$program_name\",\"$tuition\",\"\",\"Online\",\"\",\"\",\"\",\"$gmat_status\",\"$waiver_details\",\"\",\"\",\"\",\"\",\"\",\"$url\",\"$(date)\",85" >> "$CSV_FILE"
            fi
        else
            echo "**Status:** ⚠️ No markdown data" >> "$SUMMARY_FILE"
            echo "" >> "$SUMMARY_FILE"
        fi
    else
        error=$(echo "$response" | jq -r '.error' 2>/dev/null || echo "Unknown error")
        echo "**Status:** ❌ Failed - $error" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
    fi

    # Rate limiting - wait between requests (be respectful)
    sleep 2
done

echo "## Summary" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "- **Total URLs attempted:** $total_urls" >> "$SUMMARY_FILE"
echo "- **Successful scrapes:** $success_count" >> "$SUMMARY_FILE"
echo "- **No-GMAT programs found:** $programs_found" >> "$SUMMARY_FILE"
echo "- **Success rate:** $(awk "BEGIN {printf \"%.1f\", ($success_count/$total_urls)*100}")%" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Output Files" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "- **CSV:** \`$CSV_FILE\`" >> "$SUMMARY_FILE"
echo "- **Markdown files:** \`$OUTPUT_DIR/firecrawl-phase2/*.md\`" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Next Steps" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "1. Review CSV for data quality" >> "$SUMMARY_FILE"
echo "2. Merge with Phase 1 data (9 programs)" >> "$SUMMARY_FILE"
echo "3. Manual verification of high-value programs" >> "$SUMMARY_FILE"
echo "4. Create comparison tables for content" >> "$SUMMARY_FILE"

echo ""
echo "✅ Phase 2 scraping complete!"
echo "📊 Summary: $SUMMARY_FILE"
echo "📄 CSV: $CSV_FILE"
echo "📁 Markdown: $OUTPUT_DIR/firecrawl-phase2/*.md"
echo ""
echo "📈 Results:"
echo "   - URLs attempted: $total_urls"
echo "   - Successful: $success_count"
echo "   - No-GMAT programs: $programs_found"
