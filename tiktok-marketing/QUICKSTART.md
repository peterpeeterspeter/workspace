# Larry Setup Complete - Quick Reference

**Project:** Photostudio.io TikTok Marketing  
**Date:** February 19, 2026  
**Status:** ✅ READY TO LAUNCH

---

## 🎯 What Was Just Created

### Core Files
- ✅ `config.json` - App configuration & settings
- ✅ `strategy.md` - Full content strategy & posting plan
- ✅ `competitor-research.md` - 25 tested hooks + market analysis
- ✅ `README.md` - Complete usage guide
- ✅ `analytics/tracking.csv` - Performance tracking spreadsheet
- ✅ `analytics/weekly-reports/TEMPLATE.md` - Weekly report format

### Automation
- ✅ **Weekly Analytics Cron** - Runs every Monday at 9 AM UTC
  - Auto-generates performance reports
  - Identifies top hooks & formats
  - Sends summary via Telegram

---

## 🚀 Your Next Steps (In Order)

### Step 1: Upload First Images (5 minutes)

```bash
# Create your first project folder
mkdir -p /root/.openclaw/workspace/tiktok-marketing/slideshows/input/first-project

# Add your images (you'll do this via SFTP/SCP)
# Required files:
# - before.jpg (raw product shot)
# - after-1.jpg (ghost mannequin)
# - after-2.jpg (flatlay)
# - after-3.jpg (on-model front)
# - after-4.jpg (on-model side)
# - after-5.jpg (video clip - optional)
```

### Step 2: Generate First Slideshow (2 minutes)

```bash
cd /root/.openclaw/workspace/skills/larry

node scripts/generate-slides.js \
  --project first-project \
  --hook "We replaced our $5,000/month photographer with AI. Here's what happened." \
  --music "trending-upbeat" \
  --duration 30
```

**Output:** `/root/.openclaw/workspace/tiktok-marketing/slideshows/output/first-project.mp4`

### Step 3: Post to TikTok (3 minutes)

1. Open TikTok app on your phone
2. Upload the video from `output/`
3. Add caption: Copy hook text + "Link in bio ↗️"
4. Add trending music (check For You page for what's hot)
5. Post!

### Step 4: Track Performance (2 minutes)

After 24 hours, update `analytics/tracking.csv`:

```csv
Date,Hook_Category,Hook_Text,Views,Likes,Comments,Shares,Saves,Duration,Music,CTA,Notes
2026-02-20,Money_Savings,We replaced our $5,000/month photographer with AI...,15000,1200,34,89,267,30,Trending upbeat,Link in bio,Great performance!
```

---

## 📋 Posting Schedule (Phase 1)

**Frequency:** 2-3 posts/day  
**Days:** Monday-Friday  
**Times:** 7:30 AM, 4:30 PM UTC

**Weekly Mix:**
- Monday: Before/After → Money Savings → Speed Demo
- Tuesday: SMB Education → Before/After → Money Savings
- Wednesday: Speed Demo → SMB Education → Before/After
- Thursday: Money Savings → Speed Demo → SMB Education
- Friday: Before/After → Money Savings → Speed Demo

---

## 🎣 Top 5 Hooks to Start With

1. **"We replaced our $5,000/month photographer with AI. Here's what happened."**
2. **"Small fashion brands: Stop paying for photoshoots. Here's what alternative."**
3. **"This is what our product photos looked like... then we tried AI."**
4. **"Watch AI create our entire visual catalog in 30 seconds."**
5. **"Ghost mannequin. Flatlay. On-model. Video. All from one image."**

---

## 📁 File Locations

**Project Root:** `/root/.openclaw/workspace/tiktok-marketing/`

**Input:** `slideshows/input/{project-name}/`  
**Output:** `slideshows/output/`  
**Tracking:** `analytics/tracking.csv`  
**Reports:** `analytics/weekly-reports/`

---

## ⚙️ Config Summary

```json
{
  "app": "Photostudio.io",
  "audience": "E-commerce SMBs, fashion brands, DTC apparel",
  "format": "1 before + 4-5 after images",
  "posting": "2-3/day, Mon-Fri, 7:30 AM & 4:30 PM UTC",
  "phase": "testing (Weeks 1-2)"
}
```

---

## 🎵 Music Tips

**Always use trending music** from TikTok's library:

1. Scroll For You page
2. Note tracks with "↑ rising" badges
3. Match energy to content:
   - Money savings → Dramatic, cinematic
   - Before/after → Upbeat, energetic
   - Speed demos → Electronic, tech vibes
4. Use within 48 hours (trends move fast)

---

## 📊 Success Metrics (Phase 1)

**Week 1-2 Goals:**
- [ ] 1 hook hits 10K+ views
- [ ] 40%+ average completion rate
- [ ] 5%+ engagement on at least 1 video
- [ ] Identify top 2 performing hook categories

**Week 3-4 Goals:**
- [ ] 1K+ followers
- [ ] Consistent 10K+ views per post
- [ ] 1 viral video (100K+ views)
- [ ] 100+ clicks to photostudio.io

---

## 🔧 Quick Commands

```bash
# Generate slideshow
cd /root/.openclaw/workspace/skills/larry
node scripts/generate-slides.js --project <name> --hook "<text>"

# View tracking data
cat /root/.openclaw/workspace/tiktok-marketing/analytics/tracking.csv

# View latest config
cat /root/.openclaw/workspace/tiktok-marketing/config.json

# Read full strategy
cat /root/.openclaw/workspace/tiktok-marketing/strategy.md

# Check competitor research
cat /root/.openclaw/workspace/tiktok-marketing/competitor-research.md
```

---

## 📱 What to Post Today

If you start **right now**, here's your first post:

**Hook:** "We replaced our $5,000/month photographer with AI. Here's what happened."

**Caption:** 
```
Small fashion brands: Stop paying for photoshoots. 

One photo → Ghost mannequin + flatlay + on-model + video in seconds.

Link in bio ↗️

#fashion #ecommerce #ai #productphotography #smallbusiness
```

**Music:** Trending upbeat track (check For You page)

**CTA:** "Link in bio" (pointing to photostudio.io)

---

## 🔄 Weekly Workflow

**Monday Morning:**
- Review last week's top performers (check analytics)
- Plan this week's content calendar
- Gather new before/after image sets

**Daily:**
- Create slideshows in morning batch
- Post at 7:30 AM & 4:30 PM UTC
- Monitor performance in TikTok analytics

**Friday Evening:**
- Review week's performance
- Update tracking CSV
- Note which hooks/formats won
- Adjust next week's plan

**Weekly (Automated):**
- Cron job runs Monday 9 AM UTC
- Generates performance report
- Sends summary via Telegram

---

## 🎯 You're All Set!

**Larry is configured and ready to help you dominate TikTok.**

**Next action:** Upload your first set of images to:
```
/root/.openclaw/workspace/tiktok-marketing/slideshows/input/first-project/
```

**Files needed:**
- `before.jpg`
- `after-1.jpg`
- `after-2.jpg`
- `after-3.jpg`
- `after-4.jpg`
- `after-5.jpg` (optional)

Then run the generator and get your first post live! 🚀

---

**Questions? Check the full README:** `/root/.openclaw/workspace/tiktok-marketing/README.md`
