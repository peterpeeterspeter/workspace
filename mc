#!/bin/bash
#
# Mission Control CLI Wrapper
# Adds bin directory to PATH and provides easy access to all CLI tools
#

WORKSPACE="/root/.openclaw/workspace"
BIN_DIR="$WORKSPACE/bin"

# Add bin directory to PATH if not already there
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    export PATH="$BIN_DIR:$PATH"
fi

# Show help if no arguments
if [ $# -eq 0 ]; then
    cat << 'EOF'
Mission Control CLI - Phase 2

Available Commands:

Task Management:
  mc-task list [--status STATUS] [--assignee AGENT]
  mc-task show <id>
  mc-task create <title> [--assignee AGENT] [--priority LEVEL] [--description TEXT] [--handoff AGENT] [--tags TAGS]
  mc-task update <id> [--status STATUS] [--progress N] [--handoff AGENT]
  mc-task assign <id> --to AGENT

Activity Feed:
  mc-activity list [--limit N] [--agent AGENT]
  mc-activity log 'message' [--agent AGENT] [--task TASK_ID] [--type TYPE]
  mc-activity watch

Agent Management:
  mc-agent list
  mc-agent status <id>
  mc-agent update <id> [--status STATUS] [--task TASK_ID]

Examples:
  mc-task list --status in_progress
  mc-task create 'SERP Analysis' --assignee fury --priority high --handoff vision
  mc-task update task-123456 --status done --progress 100
  mc-activity log 'Starting SERP analysis' --agent fury --task task-123456
  mc-agent status vision

Database: /root/.openclaw/workspace/mission-control.db.json
EOF
    exit 0
fi

# Execute the requested command
exec "$@"
