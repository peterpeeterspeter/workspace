#!/bin/bash
#
# Portfolio Review - Review and optimize all projects
# Sundays - Strategic overview and prioritization
#

set -e

DATE=$1
OUTPUT_DIR=$2
OUTPUT_FILE="$OUTPUT_DIR/portfolio-review-$DATE.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "💼 PORTFOLIO REVIEW - $DATE"

cat > "$OUTPUT_FILE" << 'EOF'
# 💼 Portfolio Review
*Weekly strategic overview*

**Date:** {DATE}
**Week Number:** {WEEK}

---

## 📊 Portfolio Overview

### Active Projects (Ranked by Priority)

1. **Photostudio.io** ⭐⭐⭐⭐⭐
   - **Status:** [Active/Paused/Launching]
   - **This Week's Progress:** [Summary]
   - **Blockers:** [Any issues]
   - **Next Week Focus:** [Priorities]
   - **ROI Assessment:** [High/Medium/Low]

2. **Outilo** ⭐⭐⭐⭐
   - **Status:** [Status]
   - **This Week's Progress:** [Summary]
   - **Blockers:** [Any issues]
   - **Next Week Focus:** [Priorities]
   - **ROI Assessment:** [High/Medium/Low]

3. **Hobbysalon** ⭐⭐⭐
   - **Status:** [Status]
   - **This Week's Progress:** [Summary]
   - **Blockers:** [Any issues]
   - **Next Week Focus:** [Priorities]
   - **ROI Assessment:** [High/Medium/Low]

4. **DeBadkamer.com** ⭐⭐⭐
   - **Status:** [Status]
   - **This Week's Progress:** [Summary]
   - **Blockers:** [Any issues]
   - **Next Week Focus:** [Priorities]
   - **ROI Assessment:** [High/Medium/Low]

5. **Apertura.ai** ⭐⭐
   - **Status:** [Status]
   - **This Week's Progress:** [Summary]
   - **Blockers:** [Any issues]
   - **Next Week Focus:** [Priorities]
   - **ROI Assessment:** [High/Medium/Low]

---

## 🎯 Portfolio Optimization

### Shifts to Consider

**Move Resources FROM:**
- [Low ROI projects]
- [Blocked projects]

**Move Resources TO:**
- [High ROI opportunities]
- [Quick wins]

### Kill or Pause?

**Projects to Consider:**
- [Underperformers]
- [Projects no longer aligned with goals]

---

## 💡 Key Insights

**What's Working:**
- [Success patterns to replicate]

**What's Not:**
- [Issues to address]

**New Opportunities:**
- [Fresh ideas worth pursuing]

---

## 🚀 Next Week's Priorities

**Top 3 Must-Dos:**
1. [Priority #1]
2. [Priority #2]
3. [Priority #3]

**If Time Permits:**
1. [Nice-to-have #1]
2. [Nice-to-have #2]

---

## 📈 Portfolio Health Score

**Overall:** [Score/100]

**Breakdown:**
- Innovation: [Score]
- Execution: [Score]
- ROI: [Score]
- Strategic Fit: [Score]

---

EOF

WEEK=$(date +%U)
sed -i "s/{DATE}/$DATE/g" "$OUTPUT_FILE"
sed -i "s/{WEEK}/$WEEK/g" "$OUTPUT_FILE"

log "✅ Portfolio review template created: $OUTPUT_FILE"

echo "$OUTPUT_FILE"
