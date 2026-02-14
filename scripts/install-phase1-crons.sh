#!/bin/bash
#
# Install Mission Control Phase 1 cron jobs
# Sets up @mention daemon and daily standup
#

echo "=========================================="
echo "Mission Control Phase 1 - Cron Setup"
echo "=========================================="
echo ""

WORKSPACE="/root/.openclaw/workspace"

# 1. @Mention Daemon - Run every 5 minutes
echo "📝 Installing @Mention Daemon (every 5 min)..."

crontab -l 2>/dev/null | grep -v "mention-daemon" | crontab -

(crontab -l 2>/dev/null; echo "*/5 * * * * $WORKSPACE/scripts/mention-daemon.sh >> $WORKSPACE/logs/mention-cron.log 2>&1") | crontab -

echo "✓ @Mention daemon installed"
echo "  Schedule: Every 5 minutes"
echo "  Log: $WORKSPACE/logs/mention-cron.log"
echo ""

# 2. Daily Standup - Run at 11 PM CET (10 PM UTC)
echo "📊 Installing Daily Standup (11 PM CET / 10 PM UTC)..."

crontab -l 2>/dev/null | grep -v "daily-standup" | crontab -

(crontab -l 2>/dev/null; echo "0 22 * * * /usr/bin/python3 $WORKSPACE/scripts/daily-standup.py >> $WORKSPACE/logs/standup-cron.log 2>&1") | crontab -

echo "✓ Daily Standup installed"
echo "  Schedule: 10 PM UTC (11 PM CET)"
echo "  Log: $WORKSPACE/logs/standup-cron.log"
echo ""

# 3. Verify installation
echo "=========================================="
echo "Verifying Installation"
echo "=========================================="
echo ""

crontab -l | grep -E "(mention-daemon|daily-standup)"

echo ""
echo "✅ Mission Control Phase 1 cron jobs installed!"
echo ""
echo "Next steps:"
echo "1. Monitor logs: tail -f $WORKSPACE/logs/*.log"
echo "2. Test @mention: Add @Vision to TASKBOARD_ENHANCED.md"
echo "3. Wait for 11 PM CET for first daily standup"
