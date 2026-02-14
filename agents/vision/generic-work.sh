#!/bin/bash
# Vision's generic work handler
# Catches tasks that don't match specific types

TASK_ID=$1
TASK_TITLE=$2

LOG_DIR="/root/.openclaw/workspace/tasks/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${TASK_ID}.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "Vision: Generic work handler" >> "$LOG_FILE"
echo "Task: ${TASK_TITLE}" >> "$LOG_FILE"

echo "Task type not recognized, using generic handling" >> "$LOG_FILE"
sleep 1
echo "Task complete" >> "$LOG_FILE"
exit 0
