# Task: Crash Gambling Sites Research & Content Strategy

**Created:** 2026-02-02
**Assigned to:** Fury (Research) → Vision (SEO/Content) → Quill (Marketing)
**Status:** In Progress (Fury)
**Priority:** High

## Objective

Research and prepare content strategy for 5 crash gambling sites in development. Goal: affiliate revenue through SEO-optimized content.

## Context

**5 Crash Gambling Sites:**

| # | Site | Target Theme | Status | Notes |
|---|------|--------------|--------|-------|
| 1 | **crashcasino.io** | General "crash casino" | ✅ Has content (7+ posts) | REST API access available |
| 2 | **freecrashgames.com** | Free/demo games | ✅ Has content (10+ posts) | REST API access available |
| 3 | **aviatorcrashgame.com** | Aviator game focus | ✅ Live (200) | No content audit yet |
| 4 | **cryptocrashgambling.com** | Crypto crash angle | ✅ Has content (but off-topic!) | REST API access available |
| 5 | **crashgamegambling.com** | "crash game gambling" | ✅ Has content (10+ posts) | REST API access available |

**Goal:** Affiliate revenue (casino reviews, bonus codes, strategy content)

**Challenge:** Each site needs unique identity/brand to avoid duplicate content issues

**Tool:** Perplexity Search skill installed and tested ✅

## Phase 1: Research (Fury)

### Competitor Analysis
- Who ranks for "crash gambling", "crash game", "crash strategy" keywords?
- What content formats work? (reviews, guides, news, comparisons?)
- What are competitors missing? (content gaps)
- Affiliate strategies — how do they monetize?

### Topic Research
- Core keyword clusters for crash gambling niche
- Search volume and difficulty analysis
- Content opportunities by funnel stage:
  - **Informational:** "how crash games work", "crash strategy tips"
  - **Commercial:** "best crash casinos", "crash bonus codes"
  - **Transactional:** "play crash game", "crash casino signup"

### Site Audit (When URLs available)
- Current content on each WordPress site
- Technical setup (themes, plugins, page builders)
- Existing brand elements (if any)

**Deliverables:**
- Competitor intelligence report (receipts, sources)
- Keyword opportunity matrix (keyword, volume, difficulty, intent)
- Recommended content topics per site

---

## Phase 2: Brand Identity & Positioning (Quill)

### Per-Site Branding
For each of the 5 sites, define:
- **Brand personality** — (e.g., pro gambler, beginner-friendly, data-driven)
- **Voice/tone** — (formal, casual, technical, entertaining?)
- **Unique angle** — what makes THIS site different?
- **Target audience** — (high rollers, casual players, strategy nerds?)

### Differentiation Strategy
- How do the 5 sites complement, not compete?
- Content distribution across sites (who covers what?)
- Affiliate positioning (different casinos or different angles?)

**Deliverables:**
- Brand identity document for each site
- Content distribution strategy (which site covers which topics)
- Positioning map (how sites differ)

---

## Phase 3: SEO Content Strategy (Vision)

### Content Planning
- Content calendar by site (what to publish, when)
- Keyword mapping (which site targets which keywords)
- Internal linking structure (cross-site if applicable, or separate?)

### Content Production
- Article briefs with SEO notes
- On-page optimization guidelines
- Affiliate link placement strategy

**Deliverables:**
- Content calendar (30-60 days)
- Article briefs (first 10 articles)
- SEO checklist for crash gambling niche

---

## Dependencies

- [x] Perplexity API key configured ✅ (tested and working)
- [x] All 5 site URLs identified ✅
- [x] WordPress REST API credentials for crashcasino.io ✅

**WordPress REST API Credentials (crashcasino.io):**
- Base URL: `https://crashcasino.io/wp-json/wp/v2/`
- Username: `peter`
- Password: `3vRhtTs2khfdLtTiDFqkdeXI`
- Auth: Basic Auth (username:password)

**curl example:**
```bash
curl -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" "https://crashcasino.io/wp-json/wp/v2/posts?per_page=100"
```

**Existing Content on crashcasino.io:**
- Rocket Crash Game Bonus: Maximize Your Winnings in 2024
- Crash Multiplier Strategy for Success in 2025
- Maximize Your Crash Game Profit in 2025 with Proven Tactics
- Crash Game House Edge Insights for 2025
- Is Crash Gambling Legal in the US? (State-by-State Guide)
- Crash Gambling 101: How to Play & Win (Beginner's Guide)
- Bitcoin Rocket Crash Game Guide 2025

**WordPress REST API Credentials (crashgamegambling.com):**
- Base URL: `https://crashgamegambling.com/wp-json/wp/v2/`
- Username: `peter`
- Password: `mSKJlnLmqDZZAkfs8ZbXOACT`
- Auth: Basic Auth (username:password)

**Existing Content on crashgamegambling.com:**
- Cybet Casino Review: Crash Game Analysis (2025)
- Testing Fairness Algorithms in Online Games
- Is Crash Gambling Rigged? Full Fairness Audit
- Crash Gambling Demo Mode: Try Before Playing
- Bustabit Crash Game Strategy Breakdown
- Note: Some duplicate posts detected (e.g., "title-2" versions)

**WordPress REST API Credentials (freecrashgames.com):**
- Base URL: `https://freecrashgames.com/wp-json/wp/v2/`
- Username: `peter`
- Password: `OdzePaOZCDFcHiKolrEk1eBI`
- Auth: Basic Auth (username:password)

**Existing Content on freecrashgames.com:**
- How Crash Algorithms Work in 2025 for Fair Gaming
- Crypto Casinos Compatible With VPNs: Play Anonymously
- Best Crash Casinos for China Players
- Best Crash Casinos for Singapore Players
- Crash Gambling for Beginners
- Crash Gambling for High Rollers
- Crash Gambling Safety Guide
- Crash Gambling Bankroll Guide
- Crash Gambling Odds Calculator
- Crash Gambling Patterns Explained
- Content angle: Educational, geo-specific (China, Singapore), safety/bankroll focus

**WordPress REST API Credentials (cryptocrashgambling.com):**
- Base URL: `https://cryptocrashgambling.com/wp-json/wp/v2/`
- Username: `peter`
- Password: `7cuXYZGjZW8k3kgKoPaCQGaM`
- Auth: Basic Auth (username:password)

**Existing Content on cryptocrashgambling.com:**
- ⚠️ **OFF-TOPIC CONTENT DETECTED** — Site has generic casino content (slots, roulette, poker), NOT crash-specific
- Hello world (2025)
- Classic books based online slot (2020)
- Slot machine that has no paylines (2020)
- Roulette house edge, origin, systems (2020)
- Online video poker rules (2020)
- How to win with online casinos (2020)
- Four ways to cheer yourself up (2018)
- **CRITICAL ISSUE:** Domain targets "crypto crash gambling" but content is generic casino/off-topic
- **Recommendation:** All content needs replacement with crash-specific crypto angle

[ ] REST API credentials for aviatorcrashgame.com

## Due Date

**Phase 1 (Research):** ASAP — blocks everything else
**Phase 2 (Branding):** After research — 1 day
**Phase 3 (SEO):** After branding — 1-2 days

## Notes

- **Perplexity skill is installed** at `/workspace/skills/perplexity/`
- Need PERPLEXITY_API_KEY env var to use it
- Affiliate revenue focus = prioritize commercial/transactional content
- Each site needs distinct identity to avoid duplicate content penalties
- Cross-linking strategy matters (if sites should link to each other or remain separate)

## Next Steps

1. **Peter provides:**
   - Perplexity API key
   - URLs of the 5 sites (if available)
   - Any initial thoughts on site differentiation

2. **Fury starts:** Competitor analysis using Perplexity search
3. **Quill follows:** Brand identities based on research gaps
4. **Vision finishes:** Content strategy and article production
