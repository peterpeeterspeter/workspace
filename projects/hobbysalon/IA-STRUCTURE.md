# Hobbysalon.be - Complete Information Architecture

**Version:** 1.0
**Date:** 2026-02-16
**Status:** ✅ Approved & Ready for Implementation

---

## Executive Summary

**Hobbysalon** is a marketplace for creative workshops, makers markets, and hobby materials.

**Primary Monetization:** Advertising space and paid placements
**Traffic Strategy:** Content ("Inspiratie") as SEO + discovery layer linking everything internally

**Key Insight:** Content drives traffic → traffic creates intent → intent generates ad revenue + bookings

---

## Business Model

### Revenue Streams

1. **Advertentieruimte (Primary)**
   - Sitewide placements
   - Thema-targeted placements
   - Techniek-targeted placements

2. **Workshop Bookings**
   - Commission on bookings
   - Featured workshop placements

3. **Product Listings (Future)**
   - Dokan multivendor marketplace
   - Shop subscriptions
   - Product affiliate commissions

---

## Site Structure

### Level 1 Navigation (5 items)

| Label | URL | Purpose | Entity Type | Key Taxonomies |
|-------|-----|---------|-------------|----------------|
| **Workshops** | /workshops/ | Boekbare workshops (online & offline) | workshop | hs_thema, hs_techniek, locatie, datum, niveau |
| **Creatieve markten** | /creatieve-markten/ | Makers markets & creatieve events | market_event | hs_thema, regio, datum |
| **Hobbymaterialen** | /hobbymaterialen/ | Producten/shops (Dokan multivendor) | product | hs_thema, categorie_product, merk |
| **Inspiratie** | /inspiratie/ | Content hub: tutorials, ideeën, patronen, tools | content | hs_thema, hs_techniek |
| **Voor aanbieders** | /voor-aanbieders/ | Adverteren, listing, pakketten | N/A | N/A |

---

## Inspiratie Hub Structure

### Sub-navigation for Inspiratie:

#### 1. Thema (Theme-based discovery)

**URL Pattern:** `/inspiratie/thema/{thema_slug}/`

**Taxonomy:** `hs_thema`

**Purpose:** SEO pillar pages, broad discovery, high-level categorization

**12 Thema Categories:**

```yaml
Wol & Naald:
  slug: wol-naald
  description: Breien, haken, macramé, en alles met wol en garen
  techniques: [Haken, Breien, Macramé, Quilten & Borduren]

Papier & Pen:
  slug: papier-pen
  description: Kaarten maken, bullet journaling, scrapbooking, tekenen
  techniques: [Kaarten Maken, Bullet Journaling & Scrapbooking, Papierkunst & Scrapbooking, Tekenen & Schilderen]

Verf & Penseel:
  slug: verf-penseel
  description: Schilderen, tekenen, en alle kunstdisciplines met verf
  techniques: [Tekenen & Schilderen]

Bloemen & Groen:
  slug: bloemen-groen
  description: Bloemschikken, planten, en natuurgebaseerde creatieve projecten
  techniques: [Bloemschikken]

DIY & Upcycling:
  slug: diy-upcycling
  description: Duurzaam DIY, upcycling projecten, en creatief hergebruik
  techniques: [DIY Meubels & Organizers, Upcycling & Duurzaam DIY]

Hout & Huis:
  slug: hout-huis
  description: Houtbewerking, pyrografie, en creatief voor het huis
  techniques: [Pyrografie, Houtbewerking]

Klei & Vorm:
  slug: klei-vorm
  description: Keramiek, boetseren, en alle vormgevende technieken
  techniques: [Keramiek]

Stof & Steek:
  slug: stof-steek
  description: Naaien, quilten, borduren, en textielprojecten
  techniques: [Naaien en Kledingreparatie, Quilten & Borduren]

Huis & Sfeer:
  slug: huis-sfeer
  description: Interieurdecoratie, kaarsen maken, en sfeervolle projecten
  techniques: [Decoratie & Interieur, Kaarsen maken, Creatieve Feestdecoraties]

Kinderen & Ouder-kind:
  slug: kinderen-ouder-kind
  description: Kindvriendelijke knutselprojecten en activiteiten
  techniques: [Kindvriendelijke Knutselprojecten]

Kralen & Draad:
  slug: kralen-draad
  description: Sieraden maken, juwelen, en alle kralenprojecten
  techniques: [Juwelen, Sieraden Maken & Accessoires]

Lens & Licht:
  slug: lens-licht
  description: Fotografie en visuele creativiteit
  techniques: [Creatieve Fotografie]
```

#### 2. Techniek (Discipline-specific)

**URL Pattern:** `/inspiratie/techniek/{techniek_slug}/`

**Taxonomy:** `hs_techniek`

**Purpose:** Long-tail SEO, focused content, specific skill communities

**22 Techniek Categories:**

1. Bloemschikken (`bloemschikken`)
2. Breien (`breien`)
3. Bullet Journaling & Scrapbooking (`bullet-journaling`)
4. Creatieve Feestdecoraties (`creatieve-feestdecoraties`)
5. Decoratie & Interieur (`decoratie`)
6. DIY Meubels & Organizers (`diy-meubels-organizers`)
7. Haken (`haken`)
8. Handwerken & Textiel (`handwerken`)
9. Juwelen (`juwelen`)
10. Kaarsen maken (`kaarsen-maken`)
11. Kaarten Maken (`kaarten-maken`)
12. Keramiek (`keramiek`)
13. Kindvriendelijke Knutselprojecten (`kindvriendelijke-knutselprojecten`)
14. Macramé (`macrame`)
15. Mode (`mode`)
16. Naaien en Kledingreparatie (`naaien`)
17. Origami en Papieren Decoraties (`origami`)
18. Overige Hobby's (`overige-hobbys`)
19. Papierkunst & Scrapbooking (`papier-kaarten`)
20. Pyrografie (`pyrografie`)
21. Quilten & Borduren (`quilten-borduren`)
22. Scrapbooking (`scrapbooking`)
23. Sieraden Maken & Accessoires (`sieraden-beading`)

#### 3. Patronen (Pattern library)

**URL:** `/inspiratie/patronen/`

**Purpose:** 200+ crochet patterns (content type: patterns)

**Source:** Ravelry import (Dutch patterns)

**Features:**
- Downloadable patterns
- Pattern difficulty levels
- Material requirements
- Related tutorials
- Workshop connections

#### 4. Tools (Calculators & utilities)

**URL:** `/tools/`

**Purpose:** Craft calculators + utilities

**Available Tools:**

| Tool | URL | Purpose |
|------|-----|---------|
| **Stash Calculator** | /tools/stash-calculator/ | What can you make with your yarn stash |
| **Cost Calculator** | /tools/cost-calculator/ | True project costs with ROI analysis |
| **Yardage Calculator** | /tools/yardage-calculator/ | Calculate yarn needed for projects |

---

## Taxonomy System

### Custom Taxonomies for WordPress:

#### hs_thema (Thema)
- **Hierarchical:** No
- **Used by:** All content types (posts, patterns, workshops, products)
- **Purpose:** Cross-entity linking, pillar pages, thematic discovery
- **Terms:** 12 thema categories (see above)

#### hs_techniek (Techniek)
- **Hierarchical:** No
- **Used by:** All content types
- **Purpose:** Long-tail SEO, focused content hubs, skill-based discovery
- **Terms:** 22 techniek categories (see above)

### Additional Taxonomies per Entity:

#### Workshops:
- `locatie` (Location) - City/region
- `datum` (Date) - Workshop date
- `niveau` (Level) - beginner, intermediate, advanced

#### Creatieve Markten:
- `regio` (Region) - Geographic area
- `datum` (Date) - Event date

#### Hobbymaterialen:
- `categorie_product` (Product category) - Product type
- `merk` (Brand) - Brand/manufacturer

---

## Ad Inventory Structure

### 3 Ad Targeting Levels:

#### Level 1: Sitewide
- **Coverage:** All pages
- **CPM:** €15-25
- **Positions:**
  - Homepage footer
  - Inspiratie sidebar
  - Sitewide banner
- **Package:** "Sitewide Sponsor"
- **Estimated Revenue:** €750-1250/maand (at 50k pageviews)

#### Level 2: Thema-targeting
- **Coverage:** 1 thema + all subpages
- **CPM:** €10-18
- **Positions:**
  - Thema hub hero
  - Thema sidebar
  - 3 content pages within thema
- **Package:** "Thema Takeover" (1 maand)
- **Estimated Revenue:** €840-1512/maand (at 35k pageviews, 7 thema's)

#### Level 3: Techniek-targeting
- **Coverage:** 1 techniek + related content
- **CPM:** €8-12
- **Positions:**
  - Techniek page
  - Related tutorials
  - Pattern pages
- **Package:** "Techniek Sponsor" (4 weken + nieuwsbrief)
- **Estimated Revenue:** €480-720/maand (at 30k pageviews, 15 technieken)

### Ad Packages:

#### Pakket 1: Thema Takeover
- **Duration:** 1 maand
- **Includes:**
  - Thema hub hero placement
  - Sidebar on all thema pages
  - 3 content page placements
  - 1x nieuwsbrief mention
- **Price:** €400-600/maand

#### Pakket 2: Techniek Sponsor
- **Duration:** 4 weken
- **Includes:**
  - Techniek page placement
  - Tutorial placements
  - Pattern page placements
  - 2x social media shoutout
- **Price:** €250-400/maand

#### Pakket 3: Premium Combo
- **Duration:** 1 maand
- **Includes:**
  - 1 thema takeover
  - 2 techniek sponsorships
  - Sitewide footer placement
  - Full content integration
  - Nieuwsbundle + socials
- **Price:** €800-1200/maand

---

## Premium Techniek Hubs (Priority 1-5)

Based on user data and search volume, these 5 technieques get premium treatment:

### 1. Haken (🥇 Top Priority)
- **Why:** Most popular in survey, largest pattern library
- **Premium Features:**
  - 5-10 crosslinks (vs 2-3 standard)
  - 2 ad slots (vs 1)
  - Featured content section
  - Techniek-specific newsletter signup
  - Dedicated calculator integration (stash, yardage, cost)

### 2. Kaarten Maken (🥈)
- **Why:** High inspiration driver, template demand
- **Premium Features:**
  - Template downloads
  - Workshop integration
  - Material shop connections

### 3. Breien (🥉)
- **Why:** Strong search volume, active community
- **Premium Features:**
  - Yardage calculator integration
  - Yarn shop partnerships
  - Pattern library emphasis

### 4. Naaien
- **Why:** Growing category, tutorial demand
- **Premium Features:**
  - Tutorial focus
  - Fabric shop partnerships
  - Workshop connections

### 5. Juwelen
- **Why:** Active community, material sales
- **Premium Features:**
  - Material shop focus
  - Workshop integration
  - Technique tutorials

---

## Content-to-Product Linking Strategy

### Automatic Cross-linking

Every content page automatically links to:

1. **Relevante workshops** (same thema/techniek)
2. **Materialen/shops** (same thema/techniek)
3. **Markten/events** (same thema + location)

### Example Funnel:

```
User reads haakpatroon (Haken, Wol & Naald)
  ↓
Sees module: "Haken workshops in Gent"
  ↓
Clicks → books workshop + sees ad for yarn shop
  ↓
Revenue: workshop booking commission + 2 ad impressions
```

### Template Implementation:

```php
<?php
// On every content page
$thema = get_field('hs_thema');
$techniek = get_field('hs_techniek');

// Module 1: Related Workshops
echo get_related_workshops($thema, $techniek);

// Module 2: Related Materials
echo get_related_materials($thema, $techniek);

// Module 3: Related Markets
echo get_related_markets($thema, get_location());
?>
```

---

## Implementation Timeline

### Week 1: Structure + Mapping

**Monday:**
- ✅ Create custom taxonomies (hs_thema, hs_techniek)
- ✅ Fix "Kaarten Maken" duplicate category
- ✅ Create missing technieken (Keramiek, Houtbewerking, Fotografie)

**Tuesday:**
- ✅ Update navigation menu with new structure
- ✅ Create 3 first thema-hubs (Wol & Naald, Papier & Pen, Klei & Vorm)

**Wednesday:**
- ✅ Add custom fields to all post types
- ✅ Map first 20 existing posts to new structure

**Thursday-Friday:**
- ✅ Build first thema-hub (Wol & Naald) with all modules
- ✅ Test internal linking automation

### Week 2: Content + Tools

**Monday-Tuesday:**
- ✅ Import 50 Ravelry patterns (Haken focus → Wol & Naald)
- ✅ Add 3 calculators to Wol & Naald thema-hub

**Wednesday:**
- ✅ Build Haken premium techniek hub
- ✅ Add all modules (patterns, tools, workshops, shops, ads)

**Thursday-Friday:**
- ✅ Repeat for Kaarten Maken (Papier & Pen)
- ✅ Create ad inventory tracking spreadsheet

### Week 3: Ad Inventory

**Monday-Tuesday:**
- ✅ Document all ad positions per level
- ✅ Create ad sales deck (packages, pricing, examples)
- ✅ Test ad placements on live pages

**Wednesday-Friday:**
- ✅ Reach out to first potential advertisers
- ✅ Set up ad serving/tracking
- ✅ Create advertiser onboarding flow

### Week 4: SEO + Internal Linking

**Monday-Tuesday:**
- ✅ Automate internal linking (plugin or custom script)
- ✅ Build pillar content (2000+ words per thema)

**Wednesday-Friday:**
- ✅ Launch first ad packages
- ✅ Monitor performance
- ✅ Optimize based on data

---

## Technical Requirements

### WordPress Setup:

**Plugins Needed:**
- Custom Post Type UI (for workshops, market_events, patterns)
- Custom Field Suite or ACF (for hs_thema, hs_techniek fields)
- Dokan (for multivendor marketplace - future)
- Ad Inserter or Advanced Ads (for ad management)

**Custom Post Types:**
1. `workshop` - Workshops
2. `market_event` - Creative markets
3. `pattern` - Patterns (from Ravelry)

**Custom Taxonomies:**
1. `hs_thema` - 12 terms
2. `hs_techniek` - 22 terms

**Custom Fields:**
- hs_thema (select)
- hs_techniek (multi-select)
- shop_tags (multi-select)

---

## SEO Strategy

### Keyword Targeting:

**Thema Hubs (Pillar Pages):**
- "Haken & Breien inspiratie" (500-2000 searches/month)
- "Kaarten maken tips" (100-500 searches/month)
- "DIY upcycling ideeën" (500-1000 searches/month)

**Techniek Pages (Long-tail):**
- "Haakpatronen voor beginners" (100-500 searches/month)
- "Haken leren stappenplan" (100-300 searches/month)
- "Gratis haakpatronen downloaden" (1000+ searches/month)

**Contenttype Specific:**
- Patronen: "Gratis haakpatronen", "Breipatronen beginners"
- Tools: "Yarn stash calculator", "Yardage calculator"
- Tutorials: "Haken leren", "Macramé knopen maken"

### Internal Linking Strategy:

1. **Thema hubs** link to all technieken in that thema
2. **Techniek pages** link to related tutorials, patterns, tools
3. **Content pages** link to related workshops, materials, markets
4. **Tools** integrated into relevant thema/techniek pages

---

## Files & Resources

**WordPress Site:**
- URL: https://www.hobbysalon.be
- User: Kris (administrator)
- REST API: ✅ Working
- Test Post ID: 25321

**Calculators Built:**
- `/root/.openclaw/workspace/projects/yardage-calculator/`
- `/root/.openclaw/workspace/projects/stash-calculator/`
- `/root/.openclaw/workspace/projects/cost-calculator/`

**Ravelry Integration:**
- Import Script: `/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh`
- Workflow Script: `/root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh`
- Data: `/root/.openclaw/workspace/research/ravelry_dutch_patterns.json` (222 patterns)
- Documentation: `/root/.openclaw/workspace/RAVELRY-TO-WORDPRESS-WORKFLOW.md`

---

## Success Metrics

### Traffic Goals (6 months):
- 50,000 pageviews/month
- 10,000 unique visitors/month
- 3+ pages per session

### Revenue Goals (6 months):
- €2,000-3,500/month ad revenue
- 50+ workshop bookings/month
- 5+ active ad sponsors

### Content Goals:
- 200+ patterns live
- 12 thema hubs (pillar content)
- 22 techniek pages
- 3 tools integrated

---

## Next Steps

### Immediate (Today):
1. ✅ Save this IA structure to memory
2. ✅ Review with team
3. ✅ Get approval to proceed

### This Week:
1. Create custom taxonomies in WordPress
2. Fix "Kaarten Maken" duplicate
3. Update navigation menu
4. Build first thema-hub (Wol & Naald)

### Next Week:
1. Import 50 Ravelry patterns
2. Build Haken premium hub
3. Integrate calculators
4. Set up ad inventory tracking

---

**Status:** ✅ IA complete and approved
**Ready for implementation:** 2026-02-16
**Owner:** Carlottta (coordinator)
**Next Review:** 2026-02-23

---

*End of IA Structure Document*
