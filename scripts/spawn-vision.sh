#!/bin/bash

# Vision Agent Spawn Script
# Spawns Vision as an isolated sub-session for SEO work

SESSION_KEY="agent:seo:main"
WORKSPACE="/root/.openclaw/workspace"
SOUL_FILE="$WORKSPACE/agents/seo/SOUL.md"

# Log location
LOG_DIR="/root/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/vision-spawn.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Vision Spawn Initiated ==="
log "Session Key: $SESSION_KEY"
log "Workspace: $WORKSPACE"

# Check if SOUL.md exists
if [ ! -f "$SOUL_FILE" ]; then
    log "ERROR: SOUL.md not found at $SOUL_FILE"
    exit 1
fi

log "SOUL.md found, loading Vision identity..."

# Check if there are pending Vision tasks
TASKS_DIR="/root/.openclaw/workspace/tasks/in-progress"
PENDING_TASKS=$(ls -1 "$TASKS_DIR"/vision-task*.md 2>/dev/null | wc -l)

# Check for critical tasks
CRITICAL_TASKS=$(grep -l "CRITICAL\|PRIORITY.*HIGH" "$TASKS_DIR"/vision-task*.md 2>/dev/null | wc -l)

# Create the message for Vision
if [ "$CRITICAL_TASKS" -gt 0 ]; then
    MESSAGE="🚨 CRITICAL TASK PRIORITY: You have $CRITICAL_TASKS critical task(s) and $PENDING_TASKS total pending. Check $TASKS_DIR for vision-task*.md files. Start with CRITICAL tasks immediately. Read HEARTBEAT-VISION.md for workflow guidance."
elif [ "$PENDING_TASKS" -gt 0 ]; then
    MESSAGE="You have $PENDING_TASKS pending task(s). Check $TASKS_DIR for vision-task*.md files. Start with the oldest task. Read HEARTBEAT-VISION.md for workflow guidance."
else
    MESSAGE="Read HEARTBEAT-VISION.md if it exists. Follow it strictly. If nothing needs attention, reply HEARTBEAT_OK."
fi

log "Spawning Vision sub-session..."
log "Pending tasks: $PENDING_TASKS"
log "Message: $MESSAGE"

# Spawn Vision as sub-session using OpenClaw
# Using sessions_spawn tool via openclaw command
/root/.local/share/pnpm/openclaw agent \
    --session-id "$SESSION_KEY" \
    --message "$MESSAGE" \
    --thinking low \
    >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
log "Vision spawn completed with exit code: $EXIT_CODE"

if [ $EXIT_CODE -eq 0 ]; then
    log "=== Vision Spawn Successful ==="
else
    log "=== Vision Spawn Failed ==="
fi

exit $EXIT_CODE
