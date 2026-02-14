#!/bin/bash
# Vision's Heartbeat - ACTUALLY RUNS ENHANCED WORKFLOW
# This script is the entry point for cron jobs

# Log heartbeat
LOG_FILE="/root/.openclaw/workspace/agents/vision/heartbeat.log"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') === Vision Heartbeat ===" >> "$LOG_FILE"

# Run the enhanced workflow (ALWAYS, not just when tasks exist)
/root/.openclaw/workspace/agents/vision/content-production-enhanced.sh heartbeat "Vision Heartbeat" >> "$LOG_FILE" 2>&1

# Get exit code
EXIT_CODE=$?

# If workflow had work to do, it will handle it
# If workflow was idle, that's fine too

echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"

# Only reply HEARTBEAT_OK if truly nothing to do
if [ "$EXIT_CODE" -eq 0 ]; then
  # Check if workflow actually did something
  if grep -q "✅ Vision workflow complete" "$LOG_FILE" 2>/dev/null; then
    # Workflow ran successfully - no need to say HEARTBEAT_OK
    tail -5 "$LOG_FILE"
  else
    echo "HEARTBEAT_OK"
  fi
fi
