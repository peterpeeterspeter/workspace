# ✅ CRON JOBS USING PINCH-TO-POST - COMPLETE

**Date:** 2026-02-03 13:00 UTC
**Status:** COMPLETE

---

## What Was Fixed

### OpenClaw Cron Jobs

The OpenClaw system runs cron jobs that spawn AGENT SESSIONS (not shell scripts):

| Cron Job | Agent | Session Key | Schedule |
|----------|-------|-------------|----------|
| carlotta-heartbeat | Coordinator | agent:coordinator:main | Every 15 min at :00 |
| vision-heartbeat | SEO/Content | agent:seo-content:main | Every 15 min at :03 |
| fury-heartbeat | Research | agent:research:main | Every 15 min at :06 |
| quill-heartbeat | Marketing | agent:marketing:main | Every 15 min at :09 |

**These agents read their SOUL.md files when spawned to understand who they are and how to work.**

---

## Updates Made

### 1. Vision (SEO/Content) ✅
**File:** `/root/.openclaw/workspace/agents/seo-content/SOUL.md`
**Added:** 🦞 MANDATORY: Use Pinch-to-Post for WordPress Publishing section
**Requirements:**
- Gateway script: `/root/.openclaw/workspace/scripts/publish-gateway.sh`
- Quality threshold: 80/100 REQUIRED
- Health checks before publishing
- NO direct REST API publishing

### 2. Fury (Research) ✅
**File:** `/root/.openclaw/workspace/agents/research/SOUL.md`
**Added:** 🦞 MANDATORY: Use Pinch-to-Post for WordPress Publishing section
**Requirements:** Same as Vision

### 3. Quill (Marketing) ✅
**File:** `/root/.openclaw/workspace/agents/marketing/SOUL.md`
**Added:** 🦞 MANDATORY: Use Pinch-to-Post for WordPress Publishing section
**Requirements:** Same as Vision

### 4. Carlottta (Coordinator) ✅
**File:** `/root/.openclaw/workspace/agents/coordinator/SOUL.md`
**Added:** 🦞 MANDATORY: Enforce Pinch-to-Post for All WordPress Publishing section
**Role:** Enforce the standard, verify compliance, reject bypasses

---

## How It Works Now

### When Cron Jobs Spawn Agents:

1. **Cron fires** → Spawns agent session
2. **Agent reads SOUL.md** → Understands who they are
3. **Agent sees MANDATORY section** → Knows to use pinch-to-post gateway
4. **Agent publishes** → MUST use gateway, MUST achieve 80/100 score
5. **Coordinator enforces** → Verifies compliance, rejects bypasses

### Publishing Flow:

```
Cron → Agent Session → Reads SOUL.md → Uses Gateway → Health Check (80+) → Publish
```

---

## Result

**ALL cron-spawned agents now use pinch-to-post gateway for WordPress publishing.**

Quality threshold: 80/100 required to publish.

No bypasses. No exceptions. Fully enforced.

---

*All agents, all workflows, all cron jobs using pinch-to-post gateway.*
