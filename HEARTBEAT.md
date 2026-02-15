# HEARTBEAT.md

**Read on every heartbeat. Keep under 20 lines.**

---

## On Heartbeat (Every ~30 minutes)

1. **Read active-tasks.md FIRST** (crash recovery)
2. **Check task freshness:** Any task >2h without update? Stale = ping agent
3. **Archive sessions:** Any session >2MB? Archive it
4. **Self-review:** Been ~4 hours since last self-review.md update? Do it
5. **Report:** Nothing urgent? → HEARTBEAT_OK

## Quick Checks (Under 1 min)

- Blocked tasks: Can you unblock?
- Stale tasks: Can you nudge agent?
- System issues: Can you fix?

## Don't Do in Heartbeat

- No batch work (use cron jobs)
- No long reports (save to files)
- No deep research (spawn sub-agent)

**Heartbeat = Health check only. Real work = Cron jobs.**

---

*Last Updated: 2026-02-15 00:55 UTC*
*Lines: 20 (max)*
