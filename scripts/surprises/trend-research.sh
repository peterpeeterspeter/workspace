#!/bin/bash
#
# Trend Research - Emerging trends and opportunities
# Saturdays - What's coming, how to capitalize
#

set -e

DATE=$1
OUTPUT_DIR=$2
OUTPUT_FILE="$OUTPUT_DIR/trend-research-$DATE.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🔥 TREND RESEARCH - $DATE"

cat > "$OUTPUT_FILE" << 'EOF'
# 🔥 Trend Research Report
*Emerging opportunities for Peter's portfolio*

**Date:** {DATE}

---

## 📸 AI Image Generation Trends

### What's New
- [Latest developments]
- [New tools/techniques]
- [Market shifts]

### Opportunities for Photostudio
- [How to capitalize]
- [Features to consider]
- [Marketing angles]

---

## 🚽 Home Renovation Trends

### Bathroom Design Trends 2026
- [Color trends]
- [Material trends]
- [Smart bathroom tech]

### Opportunities for DeBadkamer
- [Content ideas]
- [Product integrations]
- [Marketing opportunities]

---

## 🌐 Domain Market Trends

### What's Hot
- [Trending niches]
- [Valuation shifts]
- [Auction dynamics]

### Opportunities
- [Domains to watch]
- [Niches to target]

---

EOF

sed -i "s/{DATE}/$DATE/g" "$OUTPUT_FILE"

log "✅ Trend research template created: $OUTPUT_FILE"

echo "$OUTPUT_FILE"
