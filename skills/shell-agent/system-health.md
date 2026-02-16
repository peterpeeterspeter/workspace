# Skill: System Health Check

## When to Use
- Before starting any major task (publishing batch, data processing, long-running jobs)
- When system seems slow or unresponsive
- As part of daily/weekly maintenance routine
- After any crash or restart

## When NOT to Use
- For quick lookups (wastes time)
- When you just need a simple fact check
- For tasks that take <30 seconds (overhead not worth it)

## Dependencies
- System: `df`, `free`, `systemctl`, `ps`
- Scripts: None
- External: None

## Execution Steps

1. **Check disk space**
   ```bash
   df -h /root/.openclaw
   ```
   - If >80%: Run disk cleanup skill
   - If >90%: Alert immediately, halt non-essential ops

2. **Check memory usage**
   ```bash
   free -h
   ```
   - If swap usage >50%: Look for memory leaks
   - If available <500MB: Be cautious with heavy tasks

3. **Check critical services**
   ```bash
   systemctl is-active aimusicstore-api.service
   systemctl is-active caddy.service
   ```
   - If inactive: Restart and log

4. **Check for hung processes**
   ```bash
   ps aux | grep -E "(defunct|Z)" | head -5
   ```
   - If defunct processes >5: Investigate parent process

5. **Check recent errors**
   ```bash
   journalctl -n 20 --no-pager | grep -i error
   ```
   - Look for patterns, critical failures

## Output
- **Location:** `/mnt/data/reports/system-health-YYYYMMDD.md`
- **Format:** Markdown report with sections:
  - Disk usage (with %)
  - Memory usage (with %)
  - Service status (active/inactive)
  - Hung processes (count, PIDs)
  - Recent errors (last 5, if any)
  - Overall status (🟢/🟡/🔴)
  - Recommendations (if any)

## Negative Examples (What Not to Do)

- **Mistake:** Not checking disk space before large data export
  - **Result:** Disk filled mid-export, process crashed, data lost
  - **Fix:** Always check before any operation that creates large files
  - **Date learned:** 2026-02-15

- **Mistake:** Ignoring defunct processes
  - **Result:** Zombie processes accumulated, system slowed
  - **Fix:** Always investigate parent process if >5 defunct
  - **Date learned:** 2026-02-15

- **Mistake:** Running health check on every small task
  - **Result:** Wasted 30 minutes on unnecessary checks
  - **Fix:** Only run before major tasks or when system seems slow
  - **Date learned:** 2026-02-15

## Example Output

```markdown
# System Health Report - 2026-02-15

## Disk Usage
- /root/.openclaw: 45% used (18G of 40G)
- Status: 🟢 OK

## Memory Usage
- Total: 16G
- Used: 8.2G (51%)
- Swap: 0% (0/2G)
- Status: 🟢 OK

## Critical Services
- aimusicstore-api.service: 🟢 Active
- caddy.service: 🟢 Active
- Status: 🟢 All running

## Hung Processes
- Defunct processes: 0
- Status: 🟢 OK

## Recent Errors
- [None in last 20 entries]
- Status: 🟢 OK

## Overall Status
🟢 System healthy

## Recommendations
- None
```

## Last Updated
- **Date:** 2026-02-15
- **Status:** working
- **Tested:** Yes
