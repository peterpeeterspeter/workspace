# Quill Agent - Heartbeat Instructions

When you receive a heartbeat message (via cron), DO NOT just say "HEARTBEAT_OK".

Instead, you MUST:

1. **EXECUTE your enhanced workflow script DIRECTLY:**
```bash
/root/.openclaw/workspace/agents/quill/content-strategy-enhanced.sh heartbeat "Quill Heartbeat"
```

2. **Let the workflow script:**
   - Run `pinch-to-post calendar 2026-02`
   - Run `pinch-to-post stats` (all sites)
   - Bulk publish ready articles to all sites
   - Coordinate social media distribution
   - Run weekly distribution review on Fridays

3. **ONLY say "HEARTBEAT_OK" if:**
   - The workflow script ran successfully AND found NO work to do
   - The workflow completed all tasks

4. **NEVER skip running the workflow script**
   - Calendar reviews MUST happen every heartbeat
   - Stats tracking MUST happen every heartbeat
   - Publishing readiness MUST be checked every heartbeat

## Your Job Every 15 Minutes

Your job is NOT to check if you have publishing tasks.
Your job is TO RUN THE WORKFLOW that DOES THE WORK.

The workflow = your work.
Running pinch-to-post features = your actual job.

Execute it. Every time.
