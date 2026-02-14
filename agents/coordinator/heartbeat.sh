#!/bin/bash
# Carlottta's Heartbeat - ACTUALLY RUNS ENHANCED WORKFLOW
# This script is the entry point for cron jobs

# Log heartbeat
LOG_FILE="/root/.openclaw/workspace/agents/coordinator/heartbeat.log"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') === Carlottta Heartbeat ===" >> "$LOG_FILE"

# Run daily operations (ALWAYS)
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "=== Checking Agent Activities ===" >> "$LOG_FILE"

# Check other agents' logs
for agent_log in /root/.openclaw/workspace/agents/*/heartbeat.log; do
  if [ -f "$agent_log" ]; then
    AGENT_NAME=$(echo "$agent_log" | sed 's|.*/\([^/]*\)/heartbeat.log|\1|')
    LAST_RUN=$(tail -3 "$agent_log" | grep "===" | tail -1)
    echo "[$AGENT_NAME] $LAST_RUN" >> "$LOG_FILE"
  fi
done

# Check WORKING.md for blockers
if [ -f "/root/.openclaw/workspace/WORKING.md" ]; then
  echo "" >> "$LOG_FILE"
  grep -i "blocked\|blocker\|issue" /root/.openclaw/workspace/WORKING.md | head -5 >> "$LOG_FILE" || echo "No blockers found" >> "$LOG_FILE"
fi

tail -10 "$LOG_FILE"
