# Task 1.8: Email Welcome Sequence Draft

**Assigned to:** Carlottta (agent:coordinator:main)
**Priority:** HIGH
**Estimated time:** 2 hours
**Dependencies:** Task 1.6 (coming soon page) for email capture integration
**Status:** inbox
**Created:** 2026-02-14
**Due:** 2026-02-16

## Description

Create a 3-email welcome sequence for aimusicstore waitlist signups. Sequence should introduce the product, explain the anti-gaming system, and encourage referrals. Load into email tool (Mailgun/ConvertKit) and test.

## Deliverables

1. **3-email welcome sequence** written and ready to send:
   - Email 1: Immediate welcome (what aimusicstore is, key differentiators)
   - Email 2: Day 2 - Behind the scenes (anti-gaming system explained)
   - Email 3: Day 5 - Invite + referral incentive

2. **Loaded into email tool**:
   - Mailgun (free tier) or ConvertKit ($9/month)
   - Automated sequence (triggered on signup)
   - Tested (send test email to verify)

3. **Integration with landing page**:
   - Task 1.6 email capture feeds into this sequence
   - Waitlist signups receive emails automatically

## Email Tool Setup

**Option A: Mailgun (Free Tier)**
- Sign up: https://www.mailgun.com/
- Free tier: 5,000 emails/month
- Requires: Technical setup (API integration)
- Good if: You want free + technical control

**Option B: ConvertKit ($9/month)**
- Sign up: https://convertkit.com/
- Pricing: Starts at $9/month for up to 300 subscribers
- Requires: Minimal setup (drag-and-drop sequences)
- Good if: You want ease of use + automation

**Recommendation:** Start with Mailgun free tier. If you hit limits, can upgrade or switch.

## Email Sequence Details

### Email 1: Welcome (Immediate)

**Subject:** Welcome to aimusicstore 🎵

**Preheader:** Thanks for joining the waitlist

**Body:**
```
Hi [First Name],

Thanks for joining the aimusicstore waitlist!

You're now part of the first community-powered voting platform for AI music and tools.

What makes us different:

✓ Weighted voting (reputation matters, not just 1 person = 1 vote)
✓ Anti-gaming protection (manipulation attempts are blocked)
✓ Real-time rankings (scores update live)

We're launching soon. You'll be the first to know when we go live.

In the meantime, reply to this email and tell me: What's your favorite AI music tool?

Talk soon,
Peter
Founder, aimusicstore

---
P.S. I read every reply. If you have questions or ideas, just hit reply.
```

**Timing:** Send immediately after signup (automated trigger)
**Goal:** Welcome + set expectations + encourage engagement (reply)

---

### Email 2: Behind the Scenes (Day 2)

**Subject:** How we're fixing fake rankings 🛡️

**Preheader:** The problem with current voting systems

**Body:**
```
Hi [First Name],

Yesterday I told you about aimusicstore. Today I want to show you HOW we're solving the fake ranking problem.

The issue with most voting systems:

- 1 person = 1 vote (easy to game with bots)
- No reputation system (new accounts = same influence as experts)
- Daily snapshots (easy to coordinate voting attacks)

Our solution:

✓ Weighted voting (high-reputation accounts have more influence)
✓ Anti-gaming detection (pattern recognition + rate limiting)
✓ Real-time rankings (harder to manipulate when scores update constantly)

We're building trust back into AI music rankings.

Want early access? Reply to this email and I'll personally add you to the beta list.

Best,
Peter
Founder, aimusicstore

---
P.S. Curious about the anti-gaming system? Reply and I'll share more details.
```

**Timing:** 2 days after Email 1
**Goal:** Build trust + explain unique value + encourage beta signup

---

### Email 3: Referral Incentive (Day 5)

**Subject:** Early access + invite friends 🚀

**Preheader:** Get early access by inviting friends

**Body:**
```
Hi [First Name],

Good news: aimusicstore is almost ready for beta testers!

I'd love to give you early access. But first, a favor:

Know anyone else who cares about AI music? Forward this email to them.

If they join the waitlist, you'll both get:

✓ Early access (before public launch)
✓ Reputation boost (start with higher score than latecomers)
✓ Your profile featured on our "Early Supporters" page

Just forward this email and tell them to mention your name in the waitlist signup.

Sound fair?

[Link to shareable waitlist page from Task 1.6]

Thanks for being part of this from the start,
Peter
Founder, aimusicstore

---
P.S. Early adopters get special recognition. Want to be featured on our site? Reply and I'll share details.
```

**Timing:** 5 days after Email 1
**Goal:** Viral growth + reward early adopters + create FOMO

---

## Technical Implementation

### If Using Mailgun:

**Setup Steps:**
1. Sign up at mailgun.com
2. Verify sending domain (or use sandbox domain for testing)
3. API key from Mailgun dashboard
4. Integrate with Task 1.6 landing page (email capture)
5. Create automated sequence in Mailgun or via API

**Integration with Landing Page:**
```python
# Pseudo-code for backend
def add_to_waitlist(email):
    # 1. Store email in database
    waitlist.save(email)

    # 2. Trigger Mailgun automated sequence
    mailgun.send_template(
        to=email,
        template="welcome_sequence",
        variables={"first_name": extract_first_name(email)}
    )

    return {"success": True}
```

### If Using ConvertKit:

**Setup Steps:**
1. Sign up at convertkit.com
2. Create form (waitlist signup)
3. Create sequence (automated email flow)
4. Embed form in landing page
5. Test signup sequence

**Integration with Landing Page:**
- Replace Task 1.6 email form with ConvertKit form embed
- Copy-paste form code from ConvertKit to landing page

## Output Files

**Email Templates:**
`/root/.openclaw/workspace/email-sequences/aimusicstore-welcome-sequence.md`

**Integration Docs:**
`/root/.openclaw/workspace/email-sequences/integration-guide.md`

## Success Criteria

- [ ] Email tool account created (Mailgun or ConvertKit)
- [ ] 3 emails written and loaded into tool
- [ ] Automated sequence configured (triggers on signup)
- [ ] Test email sent and received successfully
- [ ] Integration with landing page working
- [ ] Test signup receives full 3-email sequence

## Handoff Notes

@Carlottta - Test sequence yourself before promoting
@Carlottta - Monitor open rates after launch (goal: 40%+)
@Carlottta - Use this sequence for all waitlist signups from Task 1.6

## Dependencies

**BLOCKED until:** Task 1.6 (Coming Soon Landing Page) has email capture working

Wait for Task 1.6 to move to `done/` before integrating this sequence.

## Comments

**🔔 NOTIFICATION (Carlottta):**
You have 3 new tasks assigned for aimusicstore.com GTM execution:

1. **Task 1.6:** Coming Soon Landing Page - URGENT, due 2026-02-15 (TOMORROW)
2. **Task 1.7:** Twitter Account Creation - Due 2026-02-15
3. **THIS TASK** (Task 1.8): Email Welcome Sequence - Due 2026-02-16 (BLOCKED until Task 1.6 complete)

All tasks are in your inbox/. This task is blocked until the coming soon page (Task 1.6) has email capture working.

**Next Action:** Wait for Task 1.6 to complete, then start this task.

---
[Agent updates, progress, issues will be added here]
