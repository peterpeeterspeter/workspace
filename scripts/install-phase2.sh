#!/bin/bash
#
# Mission Control Phase 2 - Installation Script
# Sets up task database, CLI tools, and enhanced notification daemon
#

echo "=========================================="
echo "Mission Control Phase 2 - Installation"
echo "=========================================="
echo ""

WORKSPACE="/root/.openclaw/workspace"
BIN_DIR="$WORKSPACE/bin"
DB="$WORKSPACE/mission-control.db.json"
LOG_DIR="$WORKSPACE/logs"

# 1. Create bin directory
echo "📁 Creating bin directory..."
mkdir -p "$BIN_DIR"
mkdir -p "$LOG_DIR"
echo "✓ Bin directory created: $BIN_DIR"
echo ""

# 2. Make CLI tools executable
echo "🔧 Making CLI tools executable..."
chmod +x "$BIN_DIR/mc-task"
chmod +x "$BIN_DIR/mc-activity"
chmod +x "$BIN_DIR/mc-agent"
echo "✓ CLI tools executable"
echo ""

# 3. Install jq if not present
echo "📦 Checking for jq (JSON processor)..."
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    if command -v apt-get &> /dev/null; then
        apt-get update -qq && apt-get install -y -qq jq
    elif command -v yum &> /dev/null; then
        yum install -y -q jq
    else
        echo "⚠️  WARNING: Could not install jq automatically"
        echo "   Please install manually: apt-get install jq"
    fi
else
    echo "✓ jq already installed"
fi
echo ""

# 4. Test CLI tools
echo "🧪 Testing CLI tools..."
echo ""

echo "Testing: mc-task list"
"$WORKSPACE/mc" mc-task list
echo ""

echo "Testing: mc-agent list"
"$WORKSPACE/mc" mc-agent list
echo ""

echo "Testing: mc-activity list --limit 5"
"$WORKSPACE/mc" mc-activity list --limit 5
echo ""

# 5. Set up enhanced notification daemon
echo "🔔 Setting up enhanced notification daemon..."

# Remove old Phase 1 cron
crontab -l 2>/dev/null | grep -v "mention-daemon.sh" | crontab -

# Add Phase 2 daemon
(crontab -l 2>/dev/null; echo "*/5 * * * * $WORKSPACE/scripts/notification-daemon-v2.sh >> $LOG_DIR/notification-v2.log 2>&1") | crontab -

echo "✓ Enhanced notification daemon installed (every 5 min)"
echo ""

# 6. Create convenience symlink
echo "🔗 Creating convenience commands..."
ln -sf "$WORKSPACE/mc" "/usr/local/bin/mc"
echo "✓ You can now use 'mc' command from anywhere"
echo ""

# 7. Quick test
echo "🧪 Quick test - Create a test task..."

TEST_TASK_ID=$("$WORKSPACE/mc" mc-task create "Test Task from Phase 2 Setup" \
    --assignee peter \
    --priority medium \
    --description "Testing Phase 2 CLI tools" 2>&1 | grep -oP 'Task created: \K[^ ]+')

if [ -n "$TEST_TASK_ID" ]; then
    echo "✓ Test task created: $TEST_TASK_ID"

    # Update the task
    "$WORKSPACE/mc" mc-task update "$TEST_TASK_ID" --status done > /dev/null
    echo "✓ Test task updated"
else
    echo "⚠️  Test task creation had issues (may still be working)"
fi
echo ""

# 8. Summary
echo "=========================================="
echo "Installation Complete"
echo "=========================================="
echo ""

echo "✅ Phase 2 Components Installed:"
echo ""
echo "  📊 Task Database: $DB"
echo "  🔧 CLI Tools: $BIN_DIR/"
echo "    • mc-task    - Task management"
echo "    • mc-activity - Activity feed"
echo "    • mc-agent   - Agent management"
echo "  🔔 Notification Daemon: Running every 5 min"
echo "  📝 Logs: $LOG_DIR/"
echo ""

echo "📖 Quick Start:"
echo ""
echo "  # View all tasks"
echo "  mc task list"
echo ""
echo "  # Create a task"
echo "  mc task create 'New task' --assignee vision --priority high"
echo ""
echo "  # Update task status"
echo "  mc task update task-123456 --status in_progress --progress 50"
echo ""
echo "  # Hand off task"
echo "  mc task update task-123456 --handoff fury"
echo ""
echo "  # View activity feed"
echo "  mc activity list --limit 10"
echo ""
echo "  # Log activity"
echo "  mc activity log 'Started working on SERP analysis' --agent fury"
echo ""
echo "  # Check agent status"
echo "  mc agent status vision"
echo ""

echo "📚 Documentation:"
echo "  • Full setup guide: $WORKSPACE/MISSION_CONTROL_PHASE2_SETUP.md"
echo "  • Task database: $DB"
echo "  • Logs: $LOG_DIR/*.log"
echo ""

echo "🎯 Next Steps:"
echo "  1. Test the CLI tools with the commands above"
echo "  2. Create real tasks for your agents"
echo "  3. Monitor activity feed with 'mc activity watch'"
echo "  4. Wait for notification daemon to send first alerts"
echo ""

echo "✨ Mission Control Phase 2 is ready!"
