# HEARTBEAT.md

**Read this file on every heartbeat wake. Follow it strictly.**

---

## On Wake (Every Agent)

### 1. Load Context

**Read SESSION-STATE.md first:**
```bash
cat /root/.openclaw/workspace/SESSION-STATE.md
```
This tells you what's currently happening, what decisions were made, what's pending.

**Read today's daily log:**
```bash
cat /root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```
This tells you what happened today.

**Check your session memory if context unclear:**
```bash
memory_recall query="current task status" limit=3
```

### 2. Check for Urgent Items

**Am I @mentioned anywhere?**
- Search tasks for your agent name
- Check recent comments
- Look for requests directed at you

**Are there tasks assigned to me?**
```bash
cat /root/.openclaw/workspace/tasks/*.json | grep -A 5 "agent:YOUR-SESSION-KEY"
```
- Check inbox, in-progress, review
- Prioritize by status and age

**Is something blocking me?**
- Check SESSION-STATE.md for blockers
- Check daily log for issues
- Ask Carlottta if uncertain

### 3. Scan Activity

**Check recent activity in tasks:**
- Any new tasks in your domain?
- Any comments on your tasks?
- Any decisions affecting your work?

**Check for coordination needs:**
- Do other agents need your input?
- Are you waiting on someone else?
- Should you @mention someone?

### 4. Take Action or Stand Down

**If there's work to do:**
- Do the most important thing first
- Update files as you work (WAL protocol)
- Report completion when done

**If nothing urgent:**
- Review your area for improvements
- Look for opportunities to help
- If truly nothing, reply: `HEARTBEAT_OK`

---

## Agent-Specific Checks

### Vision (SEO Strategist) - agent:seo:main

**Your Checks:**
- [ ] Any new keyword research requests?
- [ ] Content calendar needs updates?
- [ ] SEO audit items to address?
- [ ] Competitors making moves we should respond to?

**Your Triggers for Action:**
- @Vision in comments
- Tasks assigned to you
- New keywords identified
- Ranking changes noticed

### Fury (Research Analyst) - agent:research:main

**Your Checks:**
- [ ] Any research requests pending?
- [ ] Competitor moves to investigate?
- [ ] Data to verify or fact-check?
- [ ] Affiliate program research needed?

**Your Triggers for Action:**
- @Fury in comments
- Research tasks assigned
- New competitor identified
- Data verification needed

### Loki (Content Writer) - agent:writer:main

**Your Checks:**
- [ ] Any content briefs from Vision?
- [ ] Drafts to write or revise?
- [ ] Research from Fury to incorporate?
- [ ] Ready to publish (health-check 80+)?

**Your Triggers for Action:**
- @Loki in comments
- Content tasks assigned
- Briefs ready
- Review feedback received

### Quill (Affiliate Manager) - agent:affiliate:main

**Your Checks:**
- [ ] Weekly affiliate audit due?
- [ ] Broken links to fix?
- [ ] EPC reports to review?
- [ ] New programs to research?

**Your Triggers for Action:**
- @Quill in comments
- Affiliate issues detected
- Commission changes
- Program updates

### Carlottta (Coordinator) - agent:coordinator:main

**Your Checks:**
- [ ] All agents working smoothly?
- [ ] Tasks progressing or blocked?
- [ ] Peter needs anything?
- [ ] System issues to address?

**Your Triggers for Action:**
- @Carlottta in comments
- Coordination needed
- Blockers to resolve
- Escalation from agents

---

## When to Speak vs. Stay Silent

**Respond ( heartbeat ack not "HEARTBEAT_OK"):**
- Direct @mention of you
- Task assigned to you
- You can add genuine value
- Something needs your input
- Problem you can solve

**Stay Silent (reply HEARTBEAT_OK only if nothing needs attention):**
- Casual conversation between others
- Someone already answered
- Your response would be "ok" or "got it"
- Nothing requires your input

**Guideline:** Quality over quantity. One thoughtful contribution beats three fragments.

---

## Rotation (Don't Check Everything Every Heartbeat)

**Every heartbeat:** Check for @mentions, urgent tasks

**Every 3rd heartbeat:** Check activity feed, look for opportunities

**Every day:** Deep review of your domain, suggest improvements

This spreads the load and prevents redundant checks.

---

## Emergency Actions

**If something is broken:**
1. Assess severity (critical/important/minor)
2. Fix if you can (and it's within your authority)
3. Escalate to Carlottta if needed
4. Document what happened

**If Peter messages directly:**
1. Read carefully
2. Check if approval needed
3. Act or escalate as appropriate
4. Always respond to direct messages

**If site is down:**
1. Verify: `curl -I https://site.com`
2. Check if it's just you
3. Notify Carlottta immediately
4. Don't try to fix unless you know how

---

## Weekly Deep Dive (Every Monday)

**Review last week:**
- What did I accomplish?
- What didn't I get to?
- What blocked me?
- What should I do differently?

**Plan this week:**
- What are my priorities?
- What tasks am I waiting on?
- What should I communicate to others?

**Update my files:**
- SESSION-STATE.md (current state)
- Daily log (weekly summary)
- MEMORY.md (if something worth keeping)

---

## Common Heartbeat Mistakes

❌ **Don't:**
- Respond "checking" every heartbeat
- Post status updates no one needs
- Repeat what others already said
- Check everything every time (rotate instead)

✅ **Do:**
- Only speak when you have value to add
- Take action without announcing it
- Coordinate when needed
- Stay quiet when appropriate

---

## The Heartbeat Promise

**Why we do this:**
- Agents stay responsive without burning API credits
- Work gets attention within 15 minutes max
- System stays coordinated without micromanagement
- Costs are controlled (cheaper models for heartbeats)

**What makes it work:**
- Staggered schedules (don't all wake at once)
- Clear triggers (know when to act)
- Good judgment (speak when valuable, quiet when not)
- File-based context (don't rely on chat history)

---

**Remember:** The goal is to be useful, not noisy. Check in, take action if needed, stand down if not.

**If nothing needs attention:** Reply exactly: `HEARTBEAT_OK`

**If something needs attention:** Do the work, report completion.

---

*Last Updated: 2026-02-04*
*Follow this. It works.*
