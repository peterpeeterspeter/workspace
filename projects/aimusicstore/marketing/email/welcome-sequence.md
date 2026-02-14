# aimusicstore Welcome Email Sequence

**Version:** 1.0
**Created:** 2026-02-14
**Status:** Ready to load into email tool
**Trigger:** Waitlist signup (Task 1.6 coming soon page)

---

## Overview

**3-email welcome sequence:**
- Email 1: Welcome (immediate)
- Email 2: Behind the scenes (Day 2)
- Email 3: Referral incentive (Day 5)

**Goals:**
- Welcome new waitlist signups
- Explain unique value (weighted voting, anti-gaming)
- Build trust through transparency
- Encourage referrals for viral growth

**Expected outcomes:**
- Open rate: 40%+
- Reply rate: 5%+ (engagement with Peter)
- Referral rate: 15%+ (forwarding to friends)

---

## Email 1: Welcome (Immediate)

**Subject:** Welcome to aimusicstore 🎵

**Preheader:** Thanks for joining our waitlist

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

**Metrics to track:**
- Open rate (benchmark: 40%+)
- Click rate (benchmark: 5%+)
- Reply rate (benchmark: 5%+)
- Time to open (within 1 hour ideal)

---

## Email 2: Behind the Scenes (Day 2)

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

**Metrics to track:**
- Open rate (benchmark: 35%+)
- Reply rate (benchmark: 10%+ - higher due to beta offer)
- Beta signups (track email replies asking for beta access)

---

## Email 3: Referral Incentive (Day 5)

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

Just forward this email and tell them to mention your name (or email) in the waitlist signup.

Sound fair?

[Link: http://23.95.148.204:3001/waitlist]

Thanks for being part of this from the start,
Peter
Founder, aimusicstore

---
P.S. Early adopters get special recognition. Want to be featured on our site? Reply and I'll share details.
```

**Timing:** 5 days after Email 1
**Goal:** Viral growth + reward early adopters + create FOMO

**Metrics to track:**
- Open rate (benchmark: 35%+)
- Forward rate (benchmark: 15%+)
- Referral signups (track "referred_by" in waitlist database)
- Conversion to beta (how many referrals convert to active users)

---

## Technical Setup

### Email Tool Options

**Option A: Mailgun (Free Tier - Recommended)**

**Pros:**
- Free: 5,000 emails/month
- Full API control
- Can automate sequences via backend

**Cons:**
- Requires technical setup
- No drag-and-drop builder

**Setup Steps:**
1. Sign up: https://www.mailgun.com/
2. Verify sending domain (or use sandbox domain for testing)
3. Get API key from dashboard
4. Configure in backend (see integration below)
5. Test with sandbox domain first

**Option B: ConvertKit ($9/month)**

**Pros:**
- Easy drag-and-drop sequences
- Visual automation builder
- Good for non-technical users

**Cons:**
- Costs $9/month (up to 300 subscribers)
- Less API control

**Setup Steps:**
1. Sign up: https://convertkit.com/
2. Create form (waitlist signup)
3. Create sequence (automated email flow)
4. Embed form in landing page
5. Test signup flow

---

## Integration with Backend

### Mailgun API Integration (Recommended)

**Backend code (FastAPI):**

```python
# Add to main.py
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

# Mailgun configuration
mailgun_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAILGUN_API_KEY"),
    MAIL_PASSWORD=os.getenv("MAILGUN_DOMAIN"),
    MAIL_FROM="peter@aimusicstore.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mailgun.org",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

fastmail = FastMail(mailgun_config)

async def send_welcome_email(email: str, first_name: str = "there"):
    """Send Email 1 (Welcome - Immediate)"""
    message = MessageSchema(
        subject="Welcome to aimusicstore 🎵",
        recipients=[email],
        body=f"""
        Hi {first_name},

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
        """,
        subtype="plain"
    )

    await fastmail.send_message(message)

# Update waitlist endpoint
@app.post("/api/v1/waitlist")
async def join_waitlist(email: EmailStr):
    """Join waitlist and trigger welcome sequence"""
    try:
        # 1. Store email in database
        waitlist = Waitlist(email=email)
        db.add(waitlist)
        db.commit()

        # 2. Send Email 1 (immediate)
        first_name = email.split("@")[0].capitalize()
        await send_welcome_email(email, first_name)

        # 3. Schedule Emails 2 and 3 (cron job or task queue)
        # Email 2: 2 days later
        # Email 3: 5 days later

        return {"success": True, "message": "Joined waitlist"}

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already on waitlist")
```

**Scheduled Emails (Emails 2 and 3):**

```python
# Add cron job or use task queue (Celery, Redis Queue)
# Example with APScheduler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def send_day2_email(email: str, first_name: str):
    """Send Email 2 (Behind the scenes)"""
    message = MessageSchema(
        subject="How we're fixing fake rankings 🛡️",
        recipients=[email],
        body=f"""
        [Full email 2 body from above]
        """,
        subtype="plain"
    )
    await fastmail.send_message(message)

async def send_day5_email(email: str, first_name: str):
    """Send Email 3 (Referral incentive)"""
    message = MessageSchema(
        subject="Early access + invite friends 🚀",
        recipients=[email],
        body=f"""
        [Full email 3 body from above]
        """,
        subtype="plain"
    )
    await fastmail.send_message(message)

# Schedule when user signs up
@app.post("/api/v1/waitlist")
async def join_waitlist(email: EmailStr):
    # ... store email ...

    # Schedule Email 2 (2 days later)
    scheduler.add_job(
        send_day2_email,
        'date',
        run_date=datetime.now() + timedelta(days=2),
        args=[email, first_name]
    )

    # Schedule Email 3 (5 days later)
    scheduler.add_job(
        send_day5_email,
        'date',
        run_date=datetime.now() + timedelta(days=5),
        args=[email, first_name]
    )

    return {"success": True}
```

### ConvertKit Integration (Alternative)

**Frontend form (replace Task 1.6 email form):**

```html
<!-- ConvertKit Form Embed -->
<script async data-uid="YOUR_FORM_ID" src="https://your-convertkit-form.js"></script>
```

**Backend:**
- No backend changes needed (ConvertKit handles everything)
- Waitlist still stored in local database for tracking

---

## Environment Variables

Add to `.env` or environment:

```bash
# Mailgun (if using)
MAILGUN_API_KEY=your_api_key_here
MAILGUN_DOMAIN=your_domain_here (e.g., mg.aimusicstore.com)

# OR ConvertKit (if using)
CONVERTKIT_API_KEY=your_api_key_here
CONVERTKIT_FORM_ID=your_form_id_here
```

---

## Testing Checklist

**Before going live:**

- [ ] Sign up for Mailgun (or ConvertKit)
- [ ] Get API keys
- [ ] Add API keys to `.env`
- [ ] Implement backend integration (if using Mailgun)
- [ ] OR embed ConvertKit form (if using ConvertKit)
- [ ] Test signup yourself:
  - [ ] Receive Email 1 immediately
  - [ ] Wait 2 days → Receive Email 2
  - [ ] Wait 5 days → Receive Email 3
- [ ] Check email formatting (plain text vs HTML)
- [ ] Test unsubscribe link (required by law)
- [ ] Test with spam filters (send to Gmail, Outlook, etc.)

**After going live:**

- [ ] Monitor first 10 signups: Did they receive all 3 emails?
- [ ] Check open rates (goal: 40%+)
- [ ] Check reply rates (goal: 5%+)
- [ ] Respond to every reply personally (Peter)
- [ ] Track referrals (check "referred_by" field in database)
- [ ] Iterate subject lines if open rates < 30%

---

## Success Metrics

**Week 1:**
- Emails sent: 50-100
- Email 1 open rate: 40%+
- Email 2 open rate: 35%+
- Email 3 open rate: 35%+
- Reply rate: 5%+
- Referral rate: 15%+

**Week 2-4:**
- Total signups: 500+
- Email sequence completion: 60%+ (receive all 3 emails)
- Referral conversions: 20%+ (referred users who sign up)
- Beta signups from email replies: 50+

---

## A/B Testing Ideas (Future Optimization)

**Test variations after 100+ signups:**

1. **Subject lines:**
   - Current: "Welcome to aimusicstore 🎵"
   - Test: "You're in! Welcome to aimusicstore"
   - Test: "Thanks for joining (early access inside)"

2. **Email 1 body:**
   - Current: Long form (see above)
   - Test: Short version (2-3 paragraphs)
   - Test: Video intro (30-second Loom)

3. **Email 3 referral incentive:**
   - Current: Forward this email
   - Test: Unique referral link (track who referred whom)
   - Test: Social sharing buttons (Twitter, Facebook)

4. **Timing:**
   - Current: Email 2 (Day 2), Email 3 (Day 5)
   - Test: Email 2 (Day 1), Email 3 (Day 3)

---

## Legal Compliance

**GDPR/CAN-SPAM requirements:**

- [ ] Unsubscribe link in every email (automated by Mailgun/ConvertKit)
- [ ] Physical mailing address in footer (required by CAN-SPAM)
- [ ] Clear identification of sender (Peter Peeters, Founder, aimusicstore)
- [ ] No misleading subject lines
- [ ] Clear opt-in (user signed up for waitlist)

**Footer to add to all emails:**
```
---
aimusicstore
[Your mailing address or "Online at aimusicstore.com"]

You received this email because you signed up for the aimusicstore waitlist.
Unsubscribe: [Link]
```

---

## Next Steps

1. **Peter:** Choose email tool (Mailgun free tier or ConvertKit $9/month)
2. **Carlottta:** Implement integration (backend code or form embed)
3. **Carlottta:** Test full sequence (sign up → receive all 3 emails)
4. **Peter:** Respond to every reply personally
5. **Carlottta:** Monitor metrics and iterate

---

**Status:** ✅ Sequence complete, ready to load into email tool
**Last Updated:** 2026-02-14
