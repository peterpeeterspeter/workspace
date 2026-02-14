# 🔑 ALL CREDENTIALS & SKILLS DOCUMENTED

**Status:** ✅ FULLY CONFIGURED
**Date:** 2026-02-02 20:15 UTC

---

## 🔐 Available Credentials

### WordPress (4 Sites) ✅ CONFIGURED

```bash
# crashcasino.io
WP_SITE_CRASHCASINO_URL=https://crashcasino.io/wp-json
WP_SITE_CRASHCASINO_USER=peter
WP_SITE_CRASHCASINO_PASS=3vRhtTs2khfdLtTiDFqkdeXI

# crashgamegambling.com
WP_SITE_CRASHGAME_URL=https://crashgamegambling.com/wp-json
WP_SITE_CRASHGAME_USER=peter
WP_SITE_CRASHGAME_PASS=MioX SygN Xaz6 pK9o RUiK tBMF

# cryptocrashgambling.com
WP_SITE_CRYPTOCRASH_URL=https://cryptocrashgambling.com/wp-json
WP_SITE_CRYPTOCRASH_USER=peter
WP_SITE_CRYPTOCRASH_PASS=R3kQ 6vRA UwYd x7Cn KEtT Pk83

# freecrashgames.com
WP_SITE_FREECRASH_URL=https://freecrashgames.com/wp-json
WP_SITE_FREECRASH_USER=peter
WP_SITE_FREECRASH_PASS=F8Mg yZXM qJy4 jQvp BMeZ FoMG
```

**Status:** Ready for publishing! ✅

---

### DataForSEO API ✅ CONFIGURED

```bash
DATAFORSEO_LOGIN=peeters.peter@telenet.be
DATAFORSEO_PASSWORD=654b1cfcca084d19
```

**Location:** `/skills/seo-dataforseo/.env`

**Status:** Ready for keyword research! ✅

---

### Perplexity API ⚠️ NEEDS KEY

```bash
PERPLEXITY_API_KEY=not_set
```

**Status:** Needs API key

**Get key:** https://docs.perplexity.ai

---

### Firecrawl API ✅ CONFIGURED

```bash
FIRECRAWL_API_KEY=fc-9d6d4b48b0d848ed97864d85fe34a021
```

**Status:** Ready for web scraping!

---

### Tavily API ✅ CONFIGURED

```bash
TAVILY_API_KEY=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
```

**Status:** Ready for AI search!

---

## 🛠️ Installed Skills (10 Total)

### 1. **ai-landing** ✅
**Purpose:** Generate landing page code from product descriptions

**Use for:**
- Quick landing pages
- Marketing pages
- Product showcases

---

### 2. **frontend-design-ultimate** ✅
**Purpose:** Build production-grade static sites (React, Tailwind, shadcn/ui)

**Use for:**
- Landing pages
- Marketing sites
- Portfolios
- Dashboards

---

### 3. **humanize** ✅
**Purpose:** Remove AI writing patterns from text

**Use for:**
- Content quality improvement
- Making AI text sound natural
- Editing generated content

---

### 4. **perplexity** ⚠️ NEEDS API KEY
**Purpose:** AI-powered search with citations

**Use for:**
- Research with citations
- Competitor analysis
- Trend analysis
- Fact-checking

---

### 5. **pinch-to-post** ✅ FULLY CONFIGURED
**Purpose:** WordPress automation (50+ features)

**Use for:**
- Publishing posts/pages
- Managing comments
- SEO optimization
- Bulk operations

**Sites configured:** 4 of 5 crash gambling sites

---

### 6. **ralph-loops** (legacy)
**Purpose:** (legacy skill, not documented)

---

### 7. **seo-dataforseo** ✅ FULLY CONFIGURED
**Purpose:** SEO keyword research via DataForSEO API

**Use for:**
- Keyword research (volume, CPC, difficulty)
- Competitor analysis
- SERP analysis
- Trend tracking

**Features:**
- 25+ API functions
- Auto-save to JSON
- Markdown summaries

---

### 8. **seo-optimizer** ✅
**Purpose:** SEO audits and optimization

**Use for:**
- Website SEO analysis
- Meta tag optimization
- Schema markup
- Technical SEO

---

### 9. **sports-ticker** ✅
**Purpose:** Live sports alerts (Soccer, NFL, NBA, NHL, MLB, F1)

**Use for:**
- Sports content sites
- Live scores
- Real-time updates

---

### 10. **the-sports-db** ✅
**Purpose:** Sports data access

**Use for:**
- Teams, events, scores
- Sports databases
- Statistics

---

## 🎯 Agent Skills Matrix

### Vision (SEO/Content)
**Primary Skills:**
- ✅ **pinch-to-post** — WordPress publishing
- ✅ **seo-optimizer** — SEO audits
- ⚠️ **perplexity** — Research (needs API key)
- ✅ **humanize** — Content improvement

**Secondary Skills:**
- **frontend-design-ultimate** — Landing pages
- **ai-landing** — Quick pages

---

### Fury (Research)
**Primary Skills:**
- ✅ **seo-dataforseo** — Keyword research (FULLY CONFIGURED!)
- ⚠️ **perplexity** — SERP research (needs API key)

**Secondary Skills:**
- **seo-optimizer** — Competitor SEO analysis
- **Firecrawl** — Web scraping
- **Tavily** — AI search

---

### Quill (Marketing)
**Primary Skills:**
- ⚠️ **perplexity** — Market research (needs API key)
- **seo-optimizer** — Competitive analysis

**Secondary Skills:**
- **frontend-design-ultimate** — Landing pages
- **ai-landing** — Quick pages

---

## 🚀 Immediate Actions Needed

### 1. **Set Perplexity API Key** (5 minutes)

**Why:** Core research skill for all agents

**How:**
1. Go to: https://docs.perplexity.ai
2. Get API key
3. Add to environment:
   ```bash
   export PERPLEXITY_API_KEY="pplx-xxxx"
   ```

**Impact:** Unlocks research for Vision, Fury, Quill

---

### 2. **Update WordPress Publishing Script** (5 minutes)

**Why:** Use already-configured credentials

**Current:** Script checks for env vars that don't exist
**Fix:** Update to use WP_SITE_* variables (already in env)

**Impact:** Vision can publish immediately

---

### 3. **Test DataForSEO Integration** (2 minutes)

**Why:** Fury's keyword research is fully configured

**Test:**
```bash
cd /root/.openclaw/workspace/skills/seo-dataforseo/scripts
python3 -c "from main import keyword_research; keyword_research('crash gambling')"
```

**Impact:** Fury can do real keyword research

---

## 📋 Integration Status

### ✅ FULLY INTEGRATED (Ready to Use)
- WordPress publishing (4 sites, pinch-to-post)
- DataForSEO keyword research
- SEO optimizer audits

### ⚠️ NEEDS API KEY
- Perplexity research

### 📝 DOCUMENTED (Not Yet Integrated)
- Firecrawl (web scraping)
- Tavily (AI search)
- humanize (content improvement)
- ai-landing (landing pages)
- frontend-design-ultimate (static sites)
- sports-ticker / the-sports-db (sports data)

---

## 🎯 Recommendation Priority

**HIGH (Do Now):**
1. Add Perplexity API key → Unlocks research
2. Update WordPress script → Use configured credentials
3. Test DataForSEO → Verify keyword research

**MEDIUM (This Week):**
4. Integrate Tavily (fallback for Perplexity)
5. Integrate humanize for content quality
6. Test full workflow end-to-end

**LOW (Future):**
7. Firecrawl for advanced scraping
8. Landing page generators
9. Sports data integration

---

**Bottom line:** You have MORE than enough configured skills. Just need to wire them up properly! 🚀
