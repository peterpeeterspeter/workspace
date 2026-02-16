# 🎯 HOBBYSALON.BE - STRUCTURE & CONTENT STRATEGY

**Date:** 2026-02-16
**Analysis:** 100 published posts
**Tool:** Pinch-to-post features + REST API analysis

---

## 📊 CURRENT SITUATION

### Content Overview
- **Total Posts:** 100
- **Main Categories:** 5 pillars
- **Craft Types:** 13 different crafts
- **Uncategorized:** 25 posts (need better categorization)

### Category Breakdown

| Category | Posts | Description |
|----------|-------|-------------|
| **Inspiration** | 61 (61%) | Creative DIY ideas, projects, tutorials |
| **Workshops** | 6 (6%) | Learning content, step-by-step guides |
| **Materials** | 8 (8%) | Supplies, tools, materials info |
| **Creative Markets** | 1 (1%) | Fairs, markets, events |
| **Uncategorized** | 25 (25%) | Needs categorization |

---

## 🏗️ PROPOSED STRUCTURE

### Main Navigation

```
hobbysalon.be
├── workshops/          # Learning platform
├── inspiratie/         # DIY inspiration & content
├── materialen/         # Supplies marketplace
├── creative-markets/   # Events & fairs calendar
└── patronen/           # Ravelry patterns (import ready)
```

### Craft-Specific Sections

Top crafts by volume (create dedicated pages for these):

| Craft | Posts | Opportunity |
|-------|-------|------------|
| **Knutselen** | 26 | General DIY, kids crafts |
| **Bloemen** | 9 | Paper flowers, felt flowers, arranging |
| **Haken** | 8 | Crochet patterns, tutorials |
| **Kaarsen** | 6 | Candle making |
| **Breien** | 4 | Knitting patterns |
| **Hout** | 4 | Woodworking |
| **Schilderen** | 3 | Painting techniques |

---

## 🎯 PRODUCT MAPPING

### 1. **WORKSHOPS** → Course Platform (Future)
**Current:** 6 posts
**Goal:** Online workshops, courses, learning paths

**Content:**
- Origami workshops
- Painting tutorials
- Jewelry making guides
- Shrinky Dink crafts

**Pinch-to-Post Features:**
- ✅ Use `health-check` to ensure quality (80+ score)
- ✅ Add meta descriptions for SEO
- ✅ Set focus keywords
- ✅ Add course structure tags

**Monetization:**
- Paid workshops (future)
- Affiliate links to materials
- Course platform integration

---

### 2. **INSPIRATION** → Content Engine (Current Priority)
**Current:** 61 posts (61% of content!)
**Goal:** Drive traffic, affiliate revenue, brand awareness

**Content Types:**
- DIY projects (knutselen)
- Craft tutorials (haken, breien)
- Holiday crafts (kerst, halloween)
- Room decoration ideas
- Gift ideas (cadeaus)

**Pinch-to-Post Features:**
- ✅ `stats` - Track which posts perform best
- ✅ `health-check` - Fix SEO issues (meta descriptions, focus keywords)
- ✅ `comment-moderate` - Engage with community
- ✅ Add internal linking (tool tags)

**Monetization:**
- Affiliate links (LoveCrafts, yarn shops, tool stores)
- Ad revenue (if traffic grows)
- Product roundups (best tools, best materials)

---

### 3. **MATERIALS** → E-commerce Integration (Future)
**Current:** 8 posts
**Goal:** Marketplace for hobby supplies

**Content:**
- Yarn/guides (haakgaren)
- Clay/paper (knutsel materialen)
- Paints (verf)
- Tools overview

**Pinch-to-Post Features:**
- ✅ Add affiliate links to all material posts
- ✅ `health-check` - Ensure product posts are quality
- ✅ Add comparison tables (tool A vs tool B)
- ✅ Link to workshops (materials needed)

**Monetization:**
- Affiliate programs (LoveCrafts 5-10%, material suppliers)
- Future: Direct e-commerce (drop-shipping)

---

### 4. **CREATIVE MARKETS** → Event Calendar (Future)
**Current:** 1 post
**Goal:** List fairs, markets, events

**Content:**
- Market strategies for exhibitors
- Upcoming event calendar
- Tips for selling at markets

**Pinch-to-Post Features:**
- ✅ Create event calendar posts
- ✅ Link to workshops (what to sell)

**Monetization:**
- Event listings (paid)
- Vendor spotlights
- Workshop bookings at markets

---

### 5. **PATTERNEN** → Pattern Library (Ready to Import)
**Current:** 0 posts
**Ready:** 222 Ravelry patterns (Dutch)
**Goal:** Pattern marketplace/library

**Action Plan:**
1. Import 222 Ravelry patterns
2. Categorize: breien, haken, gratis, betaald
3. Add affiliate links (pattern platforms, yarn shops)
4. Link patterns to materials (what yarn needed)

**Monetization:**
- Pattern affiliate links
- Yarn affiliate links (LoveCrafts)
- Paid pattern placements

---

## 📋 NEXT ACTIONS (Using Pinch-to-Post)

### Priority 1: Fix Content Quality (This Week)

**Run Health Checks:**
```bash
# Check all posts
for id in {17711,13922,17675,17564,17653,17595,17256,16951,16886,16827}; do
  pinch-to-post health-check hobbysalon $id
done
```

**Fix Common Issues:**
- Add meta descriptions (SEO critical)
- Set focus keywords (SEO critical)
- Add H2 headings (2+ recommended)
- Add images where missing

### Priority 2: Categorize Posts (This Week)

**Add Categories & Tags:**
- Create categories: workshops, inspiratie, materialen, evenementen
- Add craft tags: breien, haken, knutselen, schilderen, etc.
- Add theme tags: kerst, cadeau, decoratie, etc.

**Use WordPress:**
```bash
# Batch update categories via REST API
# (script ready to build)
```

### Priority 3: Add Affiliate Links (This Week)

**Target Posts:**
- Materials posts (8) → LoveCrafts, yarn shops
- Tool posts → Tool affiliate programs
- Pattern posts → Ravelry, LoveCrafts

**Action:**
```bash
# Audit posts for affiliate opportunities
# Add links to:
# - LoveCrafts (yarn, patterns)
# - Ravelry (patterns)
# - Tool shops
```

### Priority 4: Import Ravelry Patterns (Next Week)

**Script Ready:**
```bash
/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh
```

**Categories:**
- /patronen/breien/
- /patronen/haken/
- /patronen/gratis/
- /patronen/betaald/

---

## 🎯 CONTENT STRATEGY

### Content Pillars

1. **INSPIRATION (61 posts)** - "What can I make?"
   - DIY projects for beginners
   - Seasonal crafts (kerst, zomer)
   - Holiday gifts (valentijn, moederdag)
   - Room decoration ideas

2. **PATTERNS** (222 ready to import) - "How do I make it?"
   - Breipatronen (knitting)
   - Haakpatronen (crochet)
   - Gratis patterns (traffic drivers)
   - Betaald patterns (affiliate revenue)

3. **WORKSHOPS** (6 posts) - "Teach me"
   - Step-by-step tutorials
   - Technique guides
   - Beginner to advanced paths
   - Video tutorials (future)

4. **MATERIALS** (8 posts) - "What do I need?"
   - Yarn guides (haakgaren, breigaren)
   - Tool comparisons
   - Material overviews
   - Affiliate product links

5. **MARKETS** (1 post) - "Where can I sell?"
   - Event calendar
   - Vendor tips
   - Market strategies
   - Community features

---

## 💡 RECOMMENDATIONS

### Quick Wins (Do This Week)

1. ✅ **Fix Health Scores** - Run `health-check` on all posts, fix meta descriptions
2. ✅ **Add Categories** - Categorize all 100 posts
3. ✅ **Add Affiliate Links** - Top 20 posts get LoveCrafts links
4. ✅ **Internal Linking** - Link related posts (patterns → materials → workshops)

### Medium-Term (This Month)

1. 📝 **Import Ravelry Patterns** - 222 patterns ready
2. 📝 **Create Category Pages** - Landing pages for main sections
3. 📝 **Add Calculators** - Yardage, stash, cost calculators (already built!)
4. 📝 **Newsletter Signup** - Capture email addresses

### Long-Term (Next Quarter)

1. 🚀 **Workshop Platform** - Online courses
2. 🚀 **Marketplace** - Sell materials, patterns
3. 🚀 **Community Features** - User galleries, project sharing
4. 🚀 **Mobile App** - On-the-go patterns, tutorials

---

## 🔧 PINCH-TO-POST WORKFLOWS

### Daily Operations
```bash
# Run every morning
/root/.openclaw/workspace/scripts/workflows/daily-content-ops.sh
```

**Shows:**
- Content statistics
- Pending comments
- Today's calendar
- Recommendations

### Quality Assurance
```bash
# Before publishing anything
pinch-to-post health-check hobbysalon <post_id>
```

**Score must be 80+ to publish**

### Content Calendar
```bash
# View publishing schedule
pinch-to-post calendar 2026-02 hobbysalon
```

### Backup
```bash
# Weekly backup
pinch-to-post backup /root/backups/hobbysalon-$(date +%Y%m%d) hobbysalon
```

---

## 📈 SUCCESS METRICS

### Traffic
- Google Analytics integration
- Track top performing crafts
- Monitor affiliate link clicks

### Engagement
- Comments (via `comment-moderate`)
- Social shares
- Newsletter signups

### Revenue
- Affiliate link clicks & EPC
- Pattern purchases (future)
- Workshop sales (future)

---

**Next Step:** Run health checks on all posts and create prioritized fix list.

Want me to start with Priority 1 (health checks)?
