# 🔧 How to Add IndexNow Keys on MeDo.dev Sites

## MeDo.dev Platform

Your sites are built on **MeDo** — a no-code AI platform for building full-stack apps and websites.

---

## 🎯 Methods to Add IndexNow Keys (Try in Order)

### Method 1: MeDo SEO Settings (Easiest) ⭐

1. **Log into MeDo.dev**
2. **Open each site project**
3. **Look for:**
   - "Settings" → "SEO" → "Custom Meta Tags"
   - OR "Pages" → "Page Settings" → "Advanced" → "Head Code"
   - OR "Site Settings" → "Custom Code"

4. **Add this line to Custom Head/HTML:**

```html
<meta name="indexnow-key" content="YOUR_KEY_HERE">
```

**For each site:**

**DEVISMAISON.COM:**
```html
<meta name="indexnow-key" content="33b73a50-d6cc-4d30-9ad2-3cdb953f59b6">
```

**SOSTOITURES.COM:**
```html
<meta name="indexnow-key" content="57a63d3d-2b62-4555-b84c-cbe8da033545">
```

**COMPARATEURDEPRET.COM:**
```html
<meta name="indexnow-key" content="6d479592-ac7f-414e-b815-0af99b09cdc6">
```

**PINTORESDECASAS.COM:**
```html
<meta name="indexnow-key" content="0fae67c8-b907-48a9-8843-1d2184f926bb">
```

**ABOGADOSPENAL.COM:**
```html
<meta name="indexnow-key" content="5dbad253-267a-4de1-8ded-69bd1ed7b879">
```

5. **Save/Publish the site**

---

### Method 2: Upload Verification Files (Alternative)

If MeDo has file management:

1. **Create text files:**

   - `33b73a50-d6cc-4d30-9ad2-3cdb953f59b6.txt` (content: `33b73a50-d6cc-4d30-9ad2-3cdb953f59b6`)
   - `57a63d3d-2b62-4555-b84c-cbe8da033545.txt` (content: `57a63d3d-2b62-4555-b84c-cbe8da033545`)
   - `6d479592-ac7f-414e-b815-0af99b09cdc6.txt` (content: `6d479592-ac7f-414e-b815-0af99b09cdc6`)
   - `0fae67c8-b907-48a9-8843-1d2184f926bb.txt` (content: `0fae67c8-b907-48a9-8843-1d2184f926bb`)
   - `5dbad253-267a-4de1-8ded-69bd1ed7b879.txt` (content: `5dbad253-267a-4de1-8ded-69bd1ed7b879`)

2. **Upload to each site's root folder** (usually `/public` or `/`)

---

### Method 3: Ask MeDo Support (Fastest If Stuck)

**Message to MeDo Support:**

```
Hi, I need to add a custom meta tag to my site for IndexNow verification.

Tag to add:
<meta name="indexnow-key" content="KEY">

Where do I add this in MeDo? I've tried looking in Settings/SEO but can't find it.

Thanks!
```

**MeDo likely has:**
- Support chat
- Help docs
- Community forum

---

## 🚀 OR: Skip IndexNow, Use Search Console (MeDo-Compatible)

If IndexNow doesn't work with MeDo, **Google Search Console definitely will.**

### Step-by-Step:

#### 1. Go to Google Search Console
https://search.google.com/search-console

#### 2. Add Each Site
- Click "Add property"
- Choose "URL prefix"
- Paste: `https://devismaison.com/`
- Click "Continue"

#### 3. Verify Ownership
- Download the HTML verification file
- **In MeDo:**
  - Look for "File Manager" or "Public Files"
  - Upload the verification file
  - Publish/deploy

#### 4. Submit Sitemap
- In Search Console, go to "Sitemaps"
- Enter: `sitemap.xml`
- Click "Submit"

**Repeat for all 5 sites.**

---

## 💡 MY RECOMMENDATION FOR MeDo SITES

**Use Search Console** — it's platform-agnostic and guaranteed to work.

**Why:**
- ✅ MeDo supports file upload (for verification)
- ✅ Sitemaps already exist on your sites
- ✅ More reliable than IndexNow
- ✅ Official Google method

**Skip IndexNow** unless MeDo specifically supports custom meta tags.

---

## 📋 Quick Action Plan

### Right Now (5 minutes):
1. Log into MeDo.dev
2. Open one site (e.g., devismaison.com)
3. Look for "Custom Head HTML" or "SEO Settings"
4. If found → Add IndexNow meta tag
5. If not found → Move to Search Console

### Next 15 Minutes:
- Add all 5 sites to Google Search Console
- Upload verification files via MeDo
- Submit sitemaps

### Result:
- Indexing in 24-72 hours
- Zero platform compatibility issues

---

## ❓ What to Tell Me

**Reply with:**
- "Found custom HTML in MeDo" → I'll help add the tags
- "Can't find it, using Search Console" → I'll guide you step-by-step
- "MeDo doesn't support either" → I'll find alternative methods

**Or just send me a screenshot of MeDo's interface** and I'll tell you exactly where to click! 📸

---

Which approach sounds better to you?
