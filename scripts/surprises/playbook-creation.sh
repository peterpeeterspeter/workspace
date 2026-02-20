#!/bin/bash
#
# Playbook Creation - Document and systematize knowledge
# Fridays - Turn experience into repeatable playbooks
#

set -e

DATE=$1
OUTPUT_DIR=$2

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "📖 PLAYBOOK CREATION - $DATE"

OUTPUT_FILE="$OUTPUT_DIR/playbook-$DATE.md"

cat > "$OUTPUT_FILE" << 'EOF'
# 📖 Playbook: [TITLE]
*Converting experience into repeatable systems*

**Created:** {DATE}
**Project/Area:** [To be determined]

---

## 🎯 Purpose

[What this playbook solves]

## 📋 Prerequisites

[What you need before starting]

## 🔄 Process

[Step-by-step instructions]

## ✅ Checklist

[Quality control steps]

## 🚨 Common Pitfalls

[What to avoid]

## 📚 Resources

[Tools, links, references]

---

**Status:** Draft - Ready for review
EOF

sed -i "s/{DATE}/$DATE/g" "$OUTPUT_FILE"

log "✅ Playbook template created: $OUTPUT_FILE"
log "  Note: Actual content needs to be generated"

echo "$OUTPUT_FILE"
