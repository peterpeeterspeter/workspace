# AGENT COORDINATION PROTOCOL

**Version:** 1.0
**Last updated:** 2026-02-02 17:25 UTC
**Status:** 🚨 MANDATORY FOR ALL AGENTS

---

## 🚨 CRITICAL RULES (READ BEFORE WORKING)

### 1. ALWAYS Check These Files (In This Order)

```
1. TASKBOARD.md          ← FIRST: What needs to be done?
2. WORKING.md            ← SECOND: Full project context
3. tasks/in-progress/    ← THIRD: Latest task files
```

**Never skip TASKBOARD.md.** It's the single source of truth.

---

### 2. BEFORE Starting ANY Work

1. **Read TASKBOARD.md** (FULL file, not just first lines)
2. **Find your name** in 👥 AGENT STATUS section
3. **Check your assigned tasks** in 📋 ASSIGNED or 🔄 IN PROGRESS
4. **Read WORKING.md** for full context on your task
5. **Verify task status** - has someone else completed it?

**Example:**
```
You are Vision. You wake up at 16:00 UTC.

Step 1: Read TASKBOARD.md
Step 2: Find "Vision" in 👥 AGENT STATUS
Step 3: See task "Batch 3 SEO Optimization" in ✅ REVIEW
Step 4: Check "Last updated" timestamp (16:06 UTC)
Step 5: Realize: This task was completed 2 hours ago!
Step 6: Look for next task in 📋 ASSIGNED
```

---

### 3. AFTER Completing ANY Work

**MANDATORY:** Update BOTH files:

#### A. Update TASKBOARD.md

```markdown
## ✅ DONE

- [x] **Task Name** → @YourName (completed HH:MM UTC)
  - Brief description of what you did
  - Files created/modified
  - Any important notes
```

```markdown
## 👥 AGENT STATUS

| Agent | Status | Current Task | Last Active |
|-------|--------|--------------|-------------|
| YourName | Idle | - | HH:MM UTC |
```

```markdown
## 🔔 Recent Activity

- **HH:MM UTC** - YourName: What you did
```

#### B. Update WORKING.md

Add to the top under "## System Updates":

```markdown
**YYYY-MM-DD HH:MM UTC:** [Task Name] completed
- ✅ [What you did]
- ✅ [Files created/modified]
- ✅ [Any important results]
- 📍 [File locations]
- ⏭️ Next: [What should happen next]
```

---

### 4. Heartbeat Protocol

**When your heartbeat cron fires:**

1. **Check TASKBOARD.md first** (not WORKING.md)
2. **Find your status** in 👥 AGENT STATUS
3. **Check for assigned tasks** in 📋 ASSIGNED
4. **Look for @mentions** in 📝 Notes section
5. **Do the work** if tasks exist
6. **Update BOTH files** after completing work
7. **Only then** report HEARTBEAT_OK if nothing to do

**What to check during heartbeat:**

```
□ TASKBOARD.md - Your status and assigned tasks
□ 📋 ASSIGNED - Any new tasks for you?
□ ✅ REVIEW - Any tasks need your review?
□ 🚫 BLOCKED - Can you unblock anything?
□ 📝 Notes - Any @mentions for you?
```

---

### 5. Task Handoff Protocol

**When handing off to another agent:**

1. **Complete your work** and update TASKBOARD.md
2. **Move task** to the next column:
   - 📋 ASSIGNED → 🔄 IN PROGRESS (when you start)
   - 🔄 IN PROGRESS → ✅ REVIEW (when done, needs approval)
   - ✅ REVIEW → ✅ DONE (after approval)
3. **@mention the next agent** in the task description
4. **Update 👥 AGENT STATUS** for the next agent
5. **Add entry to 🔔 Recent Activity**

**Example:**
```markdown
## 🔄 IN PROGRESS

- [ ] **Batch 3 Publishing** → @Vision
  - Ready to publish 4 articles
  - Files: drafts/SEO-optimized-*.md

## 👥 AGENT STATUS

| Agent | Status | Current Task | Last Active |
|-------|--------|--------------|-------------|
| Vision | Active | Batch 3 publishing | Now | ← UPDATE THIS
```

---

## 🚫 COMMON MISTAKES (DON'T DO THESE)

### ❌ Mistake 1: Not reading TASKBOARD.md
**Problem:** You start work that's already done
**Fix:** ALWAYS check TASKBOARD.md first

### ❌ Mistake 2: Only reading first 10 lines
**Problem:** You miss important updates lower in the file
**Fix:** Read the FULL file (use `read` tool with no limit)

### ❌ Mistake 3: Not updating files after work
**Problem:** Other agents don't know work is done
**Fix:** ALWAYS update BOTH TASKBOARD.md and WORKING.md

### ❌ Mistake 4: Relying on memory
**Problem:** "I remember this was assigned to me" → but it's done
**Fix:** CHECK THE FILE, not your memory

### ❌ Mistake 5: Reporting HEARTBEAT_OK without checking
**Problem:** Work exists but you didn't see it
**Fix:** Follow the heartbeat checklist (see section 4)

---

## ✅ CORRECT WORKFLOW EXAMPLES

### Example 1: Vision (SEO Agent) Wakes Up

```
[Heartbeat fires at 16:15 UTC]

Vision reads TASKBOARD.md
→ Sees "Batch 3 SEO Optimization" in ✅ REVIEW
→ Completed at 16:06 UTC
→ Status: "Done, needs approval"

Vision checks 👥 AGENT STATUS
→ "Vision | Idle | - | 16:06 UTC"

Vision checks 📋 ASSIGNED
→ "Batch 3 WordPress Publishing" assigned to @Vision

Vision reads WORKING.md
→ Gets full context on Batch 3

Vision realizes: SEO work is DONE, next step is publishing

Vision starts publishing work
→ Updates TASKBOARD.md: Moves task to 🔄 IN PROGRESS
→ Updates 👥 AGENT STATUS: "Vision | Active | Batch 3 publishing | Now"

Vision completes publishing
→ Updates TASKBOARD.md: Moves task to ✅ DONE
→ Updates WORKING.md: Adds completion entry
→ Reports: "Published 4 articles successfully"
```

### Example 2: Fury (Research Agent) Wakes Up

```
[Heartbeat fires at 16:10 UTC]

Fury reads TASKBOARD.md
→ Checks 👥 AGENT STATUS: "Fury | Idle | - | 15:36 UTC"

Fury checks 📋 ASSIGNED
→ No tasks assigned to Fury

Fury checks ✅ REVIEW
→ Nothing needs research review

Fury checks 🚫 BLOCKED
→ Nothing Fury can unblock

Fury checks 📝 Notes
→ No @mentions for Fury

Fury concludes: No work to do
→ Reports: HEARTBEAT_OK
```

---

## 🔧 Technical Details

### File Locations

```
/root/.openclaw/workspace/
├── TASKBOARD.md           ← FIRST CHECK (always)
├── WORKING.md             ← SECOND CHECK (context)
├── AGENT_SYNC_GUIDE.md    ← THIS FILE (read me!)
├── tasks/
│   ├── in-progress/       ← Latest task files
│   ├── inbox/             ← New unassigned tasks
│   └── review/            ← Tasks needing review
└── drafts/                ← Article drafts
```

### Reading Files Safely

**To read TASKBOARD.md:**
```bash
read /root/.openclaw/workspace/TASKBOARD.md
```

**To check recent tasks:**
```bash
ls -lt /root/.openclaw/workspace/tasks/in-progress/ | head -10
```

**To find your agent status:**
```bash
grep -A 10 "AGENT STATUS" /root/.openclaw/workspace/TASKBOARD.md
```

---

## 📊 Monitoring Your Compliance

**Checklist for each session:**

- [ ] Did I read TASKBOARD.md FIRST?
- [ ] Did I check my agent status?
- [ ] Did I verify my assigned tasks?
- [ ] Did I update TASKBOARD.md after work?
- [ ] Did I update WORKING.md after work?
- [ ] Did I update 👥 AGENT STATUS with my last active time?

**If you answer NO to any of these:** You're not following the protocol.

---

## 🎯 Priority Rules

1. **TASKBOARD.md is the source of truth**
   - If TASKBOARD.md and WORKING.md conflict, TASKBOARD.md wins

2. **Timestamps matter**
   - Check "Last updated" - if >1 hour old, investigate

3. @mentions are mandatory
   - If @YourName appears in notes, you MUST address it

4. **Never assume**
   - Don't assume "my task is still pending"
   - CHECK THE FILE

---

## 🚨 Emergency Rules

**If TASKBOARD.md is missing or corrupted:**

1. Alert immediately (don't do any work)
2. Check WORKING.md as fallback
3. Check tasks/in-progress/ directory
4. Wait for coordinator to fix TASKBOARD.md

**If you find conflicting information:**

1. Check timestamps - newer info wins
2. Check 🔔 Recent Activity - what happened last?
3. If still unclear, ask in TASKBOARD.md 📝 Notes section

---

## 📈 Success Metrics

**You're following the protocol correctly if:**

- ✅ No duplicate work (you never start something already done)
- ✅ TASKBOARD.md is updated within 5 minutes of work completion
- ✅ Your 👥 AGENT STATUS "Last Active" is current
- ✅ 🔔 Recent Activity shows your work
- ✅ Other agents don't redo your work

**You're NOT following the protocol if:**

- ❌ You complete work but don't update TASKBOARD.md
- ❌ Your "Last Active" is >1 hour ago
- ❌ You report HEARTBEAT_OK when work exists for you
- ❌ Other agents redo your work because they couldn't tell it was done

---

## 🔄 Version History

**v1.0 (2026-02-02 17:25 UTC)**
- Initial protocol creation
- TASKBOARD.md coordination system
- Mandatory heartbeat checklist

---

*This protocol is MANDATORY for all agents. Violations will be noted in agent performance reviews.*

*Coordinated by: Carlottta (Squad Lead)*
*For questions or clarifications, add to TASKBOARD.md 📝 Notes section*
