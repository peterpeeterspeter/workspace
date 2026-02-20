# Photostudio.io TikTok Marketing - Larry Setup

**Project:** AI visual suite for fashion/ecommerce  
**Date:** February 19, 2026  
**Status:** ✅ Configured & Ready

---

## 📁 Project Structure

```
/root/.openclaw/workspace/tiktok-marketing/
├── config.json                    # App config & settings
├── strategy.md                    # Content strategy & posting plan
├── competitor-research.md         # Full competitive analysis
├── README.md                      # This file
├── slideshows/
│   ├── input/                     # Drop your images here
│   │   └── {project-name}/
│   │       ├── before.jpg         # 1 before image
│   │       ├── after-1.jpg        # 4-5 after images
│   │       ├── after-2.jpg
│   │       ├── after-3.jpg
│   │       ├── after-4.jpg
│   │       └── after-5.jpg (optional)
│   ├── output/                    # Generated slideshows
│   └── posted/                    # Archive of posted content
└── analytics/
    ├── weekly-reports/            # Automated weekly reports
    └── tracking.csv               # Manual performance tracking
```

---

## 🚀 Quick Start

### Step 1: Upload Your Images

Create a project folder in `slideshows/input/` and add your images:

```bash
mkdir -p /root/.openclaw/workspace/tiktok-marketing/slideshows/input/my-first-project
```

**Required format:**
- 1 **before** image (raw product shot)
- 4-5 **after** images (AI outputs: ghost mannequin, flatlay, on-model, etc.)
- Naming: `before.jpg`, `after-1.jpg`, `after-2.jpg`, etc.

### Step 2: Generate Slideshow

Run Larry's slideshow generator:

```bash
cd /root/.openclaw/workspace/skills/larry
node scripts/generate-slides.js \
  --project my-first-project \
  --hook "We replaced our $5,000/month photographer with AI. Here's what happened." \
  --music "trending-upbeat"
```

**Output:** Video file in `slideshows/output/`

### Step 3: Post to TikTok

**Option A: Manual Upload**
1. Open TikTok app
2. Upload video from `slideshows/output/`
3. Add caption from hooks library
4. Add trending music
5. Post & track performance

**Option B: Postiz (Automated)**
- Coming soon - Postiz setup required
- Will enable scheduled posting + analytics

### Step 4: Track Performance

Update `analytics/tracking.csv` after each post:

```csv
Date,Hook,Views,Likes,Shares,Comments,Saves,CTA,Notes
2026-02-20,Money savings #1,15000,1200,89,34,267,Link in bio,Great performace!
```

---

## 📊 Your Content Strategy

### Posting Schedule (Phase 1: Testing)

**Frequency:** 2-3 posts/day  
**Days:** Monday-Friday  
**Times:** 7:30 AM, 4:30 PM UTC (optimal engagement)

**Weekly Mix:**
- 40% Before/After transformations
- 30% Money savings hooks
- 20% Speed demonstrations
- 10% SMB education

### Top 5 Hooks to Start With

1. **"We replaced our $5,000/month photographer with AI. Here's what happened."**
2. **"Small fashion brands: Stop paying for photoshoots. Here's the alternative."**
3. **"This is what our product photos looked like... then we tried AI."**
4. **"Watch AI create our entire visual catalog in 30 seconds."**
5. **"Ghost mannequin. Flatlay. On-model. Video. All from one image."**

---

## 🎯 What Makes This Work

### Perfect Product-Market Fit for TikTok

✅ **Visual-first** (TikTok is 100% visual)  
✅ **Fashion/ecommerce** (massive niche, highly engaged)  
✅ **Before/After** (incredible transformation content)  
✅ **Time-lapse potential** (watch AI create visuals in real-time)  
✅ **Money-saving angle** ("Skip $5K fashion shoots")  
✅ **SMB pain point** (every small brand struggles with content)

### Your Competitive Advantage

**What everyone else does:**
- Shows single AI feature (one transformation)
- Targets enterprise/pro photographers
- Generic "better photos" messaging

**What Photostudio.io does:**
- Shows FULL visual suite (5+ outputs from one image)
- Targets SMB fashion brands (underserved)
- Specific formats (ghost mannequin, flatlay, on-model)
- Money + time savings (proven ROI)

---

## 📈 Success Metrics

### Phase 1 (Weeks 1-2): Hook Testing
- 1 hook hits 10K+ views
- 40%+ average completion rate
- 5%+ engagement on at least 1 video
- Identify top 2 performing categories

### Phase 2 (Weeks 3-4): Optimization
- 1K+ followers
- Consistent 10K+ views per post
- 1 viral video (100K+ views)
- 100+ clicks to photostudio.io

### Phase 3 (Month 2+): Scale
- 10K+ followers
- 50K+ average views
- 1K+ website clicks/month
- 5+ viral videos (100K+ views)

---

## 🎵 Music Strategy

**Music is CRITICAL on TikTok:**

1. **Always use trending music** from TikTok's library
2. **Match energy to content:**
   - Exciting transformations → Upbeat, energetic
   - Money savings → Dramatic, cinematic
   - Speed demos → Electronic, tech vibes
3. **Trends move fast** – use sounds within 48 hours
4. **Create a playlist** of 10-15 go-to tracks

**How to find trending sounds:**
- Scroll TikTok's For You page
- Look for "↑ rising" or viral badges
- Save sounds that match your brand energy
- Test across different content types

---

## 🔄 Weekly Workflow

**Monday Morning:**
- Review last week's top performers
- Plan this week's content calendar
- Gather new before/after image sets

**Daily:**
- Create slideshows (morning batch)
- Post at scheduled times (7:30 AM, 4:30 PM)
- Monitor performance in TikTok analytics

**Friday Evening:**
- Review week's performance
- Update `analytics/tracking.csv`
- Note which hooks/formats won
- Adjust next week's plan

**Weekly (Automated):**
- Larry runs analytics cron (Mondays 9 AM)
- Generates performance report
- Sends summary via Telegram

---

## 🛠️ Tools & Scripts

### generate-slides.js
**Location:** `/root/.openclaw/workspace/skills/larry/scripts/generate-slides.js`

**Usage:**
```bash
node scripts/generate-slides.js \
  --project <project-name> \
  --hook "<hook-text>" \
  --music <music-style> \
  --duration <seconds>
```

**Features:**
- Reads images from `input/{project}/`
- Generates slideshow with overlays
- Adds text captions
- Exports MP4 to `output/`

### analytics-cron.js
**Location:** `/root/.openclaw/workspace/skills/larry/scripts/analytics-cron.js`

**Schedule:** Every Monday at 9 AM UTC

**Features:**
- Pulls TikTok analytics via API
- Generates weekly performance report
- Identifies top hooks & formats
- Sends summary to Telegram

---

## 📝 Content Ideas Bank

### Before/After Transformations
- Raw product shot → Ghost mannequin
- Basic flatlay → Lifestyle scene
- Single angle → 360° view
- Static image → Video clip
- Amateur photo → Pro catalog

### Money Savings Content
- "$5K photoshoot vs $50 AI"
- "What we did with the money we saved"
- "ROI of AI visuals after 30 days"
- "Why we fired our photographer"

### Speed Demonstrations
- "Watch AI create 20 product images in 30 seconds"
- "From upload to catalog in under 1 minute"
- "Real-time: Ghost mannequin generation"

### SMB Education
- "Small brand hack: AI product photography"
- "DTC brands: Your competitive advantage"
- "Bootstrapping fashion? Skip photoshoots"

---

## 🎨 Best Practices

### Visual Guidelines
- **High contrast:** Clear before vs after difference
- **Consistent style:** Match brand aesthetic
- **Text overlays:** Minimal, let visuals speak
- **Duration:** 15-30 seconds (sweet spot)
- **Aspect ratio:** 9:16 (TikTok standard)

### Hook Guidelines
- **Front-load value:** Hook in first 1 second
- **Be specific:** "$5,000" not "expensive"
- **Use numbers:** "5 outputs" not "multiple outputs"
- **Create curiosity:** "You won't believe this..."
- **Promise results:** "In 30 seconds..."

### CTA Guidelines
- **Hard CTAs:** "Link in bio", "DM for demo"
- **Soft CTAs:** "Follow for more", "Save this"
- **No CTA:** Let content go viral naturally
- **Test all three:** See what works for your audience

---

## 🔧 Troubleshooting

### Slideshow Generation Issues

**Problem:** `generate-slides.js` can't find images
**Solution:** Check file naming – must be `before.jpg`, `after-1.jpg`, etc.

**Problem:** Output video is blurry
**Solution:** Check source image resolution – use minimum 1080x1920

**Problem:** Text overlays are cut off
**Solution:** Reduce text length or use smaller font size

### Performance Issues

**Problem:** Low views (<1K)
**Solutions:**
- Test different hooks
- Post at different times
- Try trending music
- Check video quality

**Problem:** High views, low engagement
**Solutions:**
- Add CTAs
- Ask questions in captions
- Create more shareable content
- Test different formats

**Problem:** Good engagement, no clicks
**Solutions:**
- Make CTA more prominent
- Test "link in bio" vs direct URL
- Create urgency ("free trial ends soon")

---

## 📞 Support

**Larry Skill Documentation:**
`/root/.openclaw/workspace/skills/larry/SKILL.md`

**Project Status Tracking:**
`/root/.openclaw/workspace/tiktok-marketing/strategy.md`

**Competitive Intelligence:**
`/root/.openclaw/workspace/tiktok-marketing/competitor-research.md`

---

## ✅ Setup Checklist

- [x] Config created (`config.json`)
- [x] Content strategy documented (`strategy.md`)
- [x] Competitor research completed
- [x] Hook library created (25 tested hooks)
- [x] Project structure initialized
- [x] Posting schedule defined
- [x] Success metrics established
- [ ] **First image set uploaded** ← YOU ARE HERE
- [ ] First slideshow generated
- [ ] First post to TikTok
- [ ] Postiz connected (for automation)
- [ ] Analytics cron running

---

## 🎬 Ready to Launch!

**Next Action: Upload your first set of images**

Create your first project folder:
```bash
mkdir -p /root/.openclaw/workspace/tiktok-marketing/slideshows/input/first-project
```

Add images:
- `before.jpg` – Raw product shot
- `after-1.jpg` – Ghost mannequin
- `after-2.jpg` – Flatlay
- `after-3.jpg` – On-model (front)
- `after-4.jpg` – On-model (side)
- `after-5.jpg` – Video clip (optional)

Then run the generator and post to TikTok!

---

**Your TikTok marketing system is ready. Let's get Photostudio.io viral! 🚀**
