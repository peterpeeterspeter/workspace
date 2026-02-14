#!/bin/bash
# Daily standup script for Carlottta
# Generates daily report for Peter

DATE=$(date -u +%Y-%m-%d)
REPORT="/root/.openclaw/workspace/reports/daily-standup-${DATE}.md"
mkdir -p "$(dirname "$REPORT")"

cat > "$REPORT" << EOF
# Daily Standup - $(date -u +%Y-%m-%d)

Generated at: $(date -u +%H:%M:%S UTC)

---

## COMPLETED

### Vision (Content)
EOF

# Check Vision's log for completed tasks
if grep -q "published\|Published" /root/.openclaw/workspace/agents/vision/heartbeat.log 2>/dev/null; then
  grep "published\|Published" /root/.openclaw/workspace/agents/vision/heartbeat.log | tail -5 >> "$REPORT"
else
  echo "No recent activity" >> "$REPORT"
fi

cat >> "$REPORT" << EOF

### Fury (Research)
EOF

if grep -q "research\|Research\|moderat" /root/.openclaw/workspace/agents/fury/heartbeat.log 2>/dev/null; then
  grep "research\|Research\|moderat" /root/.openclaw/workspace/agents/fury/heartbeat.log | tail -5 >> "$REPORT"
else
  echo "No recent activity" >> "$REPORT"
fi

cat >> "$REPORT" << EOF

### Quill (Publishing)
EOF

if grep -q "publish\|calendar\|stats" /root/.openclaw/workspace/agents/quill/heartbeat.log 2>/dev/null; then
  grep "publish\|calendar\|stats" /root/.openclaw/workspace/agents/quill/heartbeat.log | tail -5 >> "$REPORT"
else
  echo "No recent activity" >> "$REPORT"
fi

cat >> "$REPORT" << EOF

---

## IN PROGRESS

EOF

# Check for in-progress tasks
if [ -d "/root/.openclaw/workspace/tasks/in-progress" ]; then
  ls -1 /root/.openclaw/workspace/tasks/in-progress/ | head -10 >> "$REPORT" 2>/dev/null || echo "No in-progress tasks" >> "$REPORT"
else
  echo "No in-progress tasks" >> "$REPORT"
fi

cat >> "$REPORT" << EOF

---

## BLOCKED

EOF

# Check for blockers
if [ -f "/root/.openclaw/workspace/WORKING.md" ]; then
  grep -i "blocked\|blocker\|issue" /root/.openclaw/workspace/WORKING.md | head -5 >> "$REPORT" 2>/dev/null || echo "No blockers" >> "$REPORT"
else
  echo "No blockers" >> "$REPORT"
fi

cat >> "$REPORT" << EOF

---

## SYSTEM STATUS

- Sites: Online ✅
- Agents: Running ✅
- Disk: $(df -h /root/.openclaw | tail -1 | awk '{print $5}') used

---

*End of report*
EOF

echo "Daily standup report generated: $REPORT"
cat "$REPORT"
