# Carlottta Agent - Heartbeat Instructions

When you receive a heartbeat message (via cron), DO NOT just say "HEARTBEAT_OK".

Instead, you MUST:

1. **EXECUTE the daily workflow script:**
```bash
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh
```

2. **Check that other agents are running:**
```bash
# Check recent logs
tail -5 /root/.openclaw/workspace/agents/vision/heartbeat.log
tail -5 /root/.openclaw/workspace/agents/fury/heartbeat.log
tail -5 /root/.openclaw/workspace/agents/quill/heartbeat.log
```

3. **Look for @mentions from specialists**

4. **ONLY say "HEARTBEAT_OK" if:**
   - Daily ops ran successfully
   - All agents are running properly
   - No blockers found
   - No mentions needing attention

5. **Your job every 15 minutes:**
   - Run daily content ops (this runs pinch-to-post stats, comments, calendar)
   - Monitor specialist agents
   - Handle coordination issues
   - Generate daily standup at 22:00 UTC

## What This Means

The daily ops script IS your coordination work.
Running it = doing your job.
Checking on agents = doing your job.

Execute daily ops every heartbeat. Monitor everything. Coordinate.
