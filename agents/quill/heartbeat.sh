#!/bin/bash
# Quill's Heartbeat - ACTUALLY RUNS ENHANCED WORKFLOW
# This script is the entry point for cron jobs

# Log heartbeat
LOG_FILE="/root/.openclaw/workspace/agents/quill/heartbeat.log"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') === Quill Heartbeat ===" >> "$LOG_FILE"

# Run the enhanced workflow (ALWAYS, not just when tasks exist)
/root/.openclaw/workspace/agents/quill/content-strategy-enhanced.sh heartbeat "Quill Heartbeat" >> "$LOG_FILE" 2>&1

# Get exit code
EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 0 ]; then
  if grep -q "✅ Quill workflow complete" "$LOG_FILE" 2>/dev/null; then
    tail -5 "$LOG_FILE"
  else
    echo "HEARTBEAT_OK"
  fi
fi
