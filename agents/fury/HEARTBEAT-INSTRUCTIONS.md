# Fury Agent - Heartbeat Instructions

When you receive a heartbeat message (via cron), DO NOT just say "HEARTBEAT_OK".

Instead, you MUST:

1. **EXECUTE your enhanced workflow script DIRECTLY:**
```bash
/root/.openclaw/workspace/agents/fury/research-enhanced.sh heartbeat "Fury Heartbeat"
```

2. **Let the workflow script:**
   - Run `pinch-to-post comment-moderate spam-suspicious` (all sites)
   - Run `pinch-to-post stats` (for competitive analysis)
   - Run `pinch-to-post backup` (for analysis)
   - Do keyword research and SERP analysis
   - Run weekly competitor analysis on Mondays

3. **ONLY say "HEARTBEAT_OK" if:**
   - The workflow script ran successfully AND found NO work to do
   - The workflow completed all tasks

4. **NEVER skip running the workflow script**
   - Comment moderation MUST happen every heartbeat
   - Spam filtering MUST happen every heartbeat
   - Stats gathering MUST happen every heartbeat

## Your Job Every 15 Minutes

Your job is NOT to check if you have research tasks.
Your job is TO RUN THE WORKFLOW that DOES THE WORK.

The workflow = your work.
Running pinch-to-post features = your actual job.

Execute it. Every time.
