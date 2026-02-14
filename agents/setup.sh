#!/bin/bash
# Quick setup script for autonomous agent heartbeat system

echo "🤖 Mission Control - Autonomous Agent Setup"
echo "=========================================="
echo ""

# Create log directories
echo "📁 Creating log directories..."
mkdir -p /root/.openclaw/workspace/agents/logs
mkdir -p /root/.openclaw/workspace/tasks/logs
echo "✅ Log directories created"
echo ""

# Test heartbeat scripts
echo "🧪 Testing heartbeat scripts..."
echo "Testing Vision..."
/root/.openclaw/workspace/agents/vision/heartbeat.sh
echo ""
echo "Testing Fury..."
/root/.openclaw/workspace/agents/fury/heartbeat.sh
echo ""
echo "Testing Quill..."
/root/.openclaw/workspace/agents/quill/heartbeat.sh
echo ""
echo "✅ Heartbeat scripts tested"
echo ""

# Show crontab commands
echo "⏰ Add these to crontab (crontab -e):"
echo ""
echo "# Vision - Every 15 minutes"
echo "*/15 * * * * /root/.openclaw/workspace/agents/vision/heartbeat.sh >> /root/.openclaw/workspace/agents/logs/vision-cron.log 2>&1"
echo ""
echo "# Fury - Every 15 minutes (staggered by 5 min)"
echo "*/15 * * * * sleep 300 && /root/.openclaw/workspace/agents/fury/heartbeat.sh >> /root/.openclaw/workspace/agents/logs/fury-cron.log 2>&1"
echo ""
echo "# Quill - Every 15 minutes (staggered by 10 min)"
echo "*/15 * * * * sleep 600 && /root/.openclaw/workspace/agents/quill/heartbeat.sh >> /root/.openclaw/workspace/agents/logs/quill-cron.log 2>&1"
echo ""

# Show how to create test task
echo "🎯 To test autonomous coordination:"
echo ""
echo "1. Go to: https://dashboard.convex.dev/t/peter-peeters/mission-control-86f58/fast-duck-920"
echo "2. Navigate to: Functions → tasks:createTask"
echo "3. Run with:"
echo ''
echo '   {'
echo '     "title": "Test Task for Vision",'
echo '     "description": "Draft a test article",'
echo '     "priority": "medium",'
echo '     "assigneeId": "j97fma866sp303v03nt61sphmn80dvac",'
echo '     "tags": ["test"]'
echo '   }'
echo ''
echo "4. Run Vision's heartbeat manually:"
echo "   /root/.openclaw/workspace/agents/vision/heartbeat.sh"
echo ""
echo "5. Watch dashboard: http://23.95.148.204:5174/"
echo ""
echo "✅ Setup complete! See README.md for full documentation."
