# Vision Agent - Heartbeat Instructions

When you receive a heartbeat message (via cron), DO NOT just say "HEARTBEAT_OK".

Instead, you MUST:

1. **EXECUTE your enhanced workflow script DIRECTLY:**
```bash
/root/.openclaw/workspace/agents/vision/content-production-enhanced.sh heartbeat "Vision Heartbeat"
```

2. **Let the workflow script:**
   - Run `pinch-to-post stats` (all sites)
   - Run `pinch-to-post comment-moderate` (all sites)
   - Run `pinch-to-post calendar 2026-02`
   - Research using Perplexity skill
   - Publish content with quality checks
   - Run weekly workflow on Mondays

3. **ONLY say "HEARTBEAT_OK" if:**
   - The workflow script ran successfully AND found NO work to do
   - The workflow completed all tasks

4. **NEVER skip running the workflow script**
   - The workflow IS your work
   - Running pinch-to-post features IS your job
   - Stats, comments, calendar - these MUST run every heartbeat

## What This Means

When cron sends you a message at :03, :18, :33, :48:
- DO NOT: Just check for tasks in /workspace/tasks/
- DO NOT: Say "HEARTBEAT_OK" immediately
- DO: Execute the enhanced workflow script
- DO: Let the script run all pinch-to-post features

## Example

**WRONG:**
```
Cron: "Run the enhanced workflow..."
Agent: "Let me check for tasks... no tasks found. HEARTBEAT_OK"
```

**CORRECT:**
```
Cron: "Run the enhanced workflow..."
Agent: [Executes /root/.openclaw/workspace/agents/vision/content-production-enhanced.sh]
[Script runs pinch-to-post stats, comments, calendar, research, publishing]
[Script completes]
Agent: [Reports results from script]
```

## Your Job Every 15 Minutes

Your job is NOT to check if you have work.
Your job is TO RUN THE WORKFLOW that DOES THE WORK.

The workflow = your work.
Running pinch-to-post features = your actual job.

Execute it. Every time.
