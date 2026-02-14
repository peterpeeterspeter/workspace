# Fury's Current Task: Crash Gambling Sites Research

**Started:** 2026-02-02
**Task File:** /workspace/tasks/in-progress/001-crash-gambling-research.md

## Your Mission

Audit and research 5 crash gambling sites to prepare for content strategy and brand development.

## Phase 1: Site Audit (DO THIS FIRST)

### crashcasino.io (Has REST API access)

**Get full content inventory:**
```bash
curl -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" "https://crashcasino.io/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,title,link,date,content"
```

**Document:**
- All existing articles (titles, slugs, publish dates)
- Content quality assessment (thin, good, needs work?)
- Internal linking structure
- Any affiliate links present
- WordPress plugins/themes used (if visible)
- Technical issues (broken links, indexing problems)

### crashgamegambling.com (Has REST API access)

**Get full content inventory:**
```bash
curl -u "peter:mSKJlnLmqDZZAkfs8ZbXOACT" "https://crashgamegambling.com/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,title,link,date,content"
```

**Document:**
- All existing articles (titles, slugs, publish dates)
- Note: Duplicate posts detected (e.g., "title-2" versions) — investigate
- Content quality assessment
- Internal linking structure
- Affiliate links present?
- Technical issues

### freecrashgames.com (Has REST API access)

**Get full content inventory:**
```bash
curl -u "peter:OdzePaOZCDFcHiKolrEk1eBI" "https://freecrashgames.com/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,title,link,date,content"
```

**Document:**
- All existing articles (titles, slugs, publish dates)
- Content quality assessment
- Geo-specific content focus (China, Singapore players)
- Educational angle (algorithms, safety, bankroll)
- Internal linking structure
- Affiliate links present?
- Technical issues

### cryptocrashgambling.com (Has REST API access)

**Get full content inventory:**
```bash
curl -u "peter:7cuXYZGjZW8k3kgKoPaCQGaM" "https://cryptocrashgambling.com/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,title,link,date,content"
```

**Document:**
- All existing articles (titles, slugs, publish dates)
- ⚠️ **CRITICAL:** Content is off-topic (slots, roulette, poker) NOT crash-specific
- Content age: Mix of 2018-2025, very old
- Assess: What can be repurposed vs. needs complete replacement?
- Site structure and technical setup
- Redirects or migration issues?

### aviatorcrashgame.com (No API credentials yet)

**Fetch and analyze:**
- Fetch via web (no API access)
- Document any existing content
- Site structure and setup

For each site, document:
- Current content (if any)
- Site structure/theme
- Technical setup (WordPress version if visible)
- Any obvious issues

## Phase 2: Competitor Research (Use Perplexity)

**Research queries to run:**
```
export PERPLEXITY_API_KEY="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"
cd /workspace/skills/perplexity

# Competitors for each keyword cluster
node scripts/search.mjs "best crash gambling sites 2025"
node scripts/search.mjs "free crash games no deposit"
node scripts/search.mjs "aviator crash game strategy"
node scripts/search.mjs "crypto crash gambling sites"
node scripts/search.mjs "crash game gambling bonus codes"
```

**For each competitor, document:**
- Who ranks top 3 for each term?
- What content formats? (reviews, guides, comparisons?)
- How do they monetize? (affiliate links, ads?)
- What are they missing? (content gaps)
- Domain authority rough estimate

## Phase 3: Keyword & Opportunity Analysis

**Build keyword matrix:**

| Keyword Cluster | Target Site | Volume | Difficulty | Competitor Gap | Priority |
|-----------------|-------------|--------|------------|----------------|----------|
| crash casino | crashcasino.io | ? | ? | ? | ? |
| free crash games | freecrashgames.com | ? | ? | ? | ? |
| aviator crash game | aviatorcrashgame.com | ? | ? | ? | ? |
| crypto crash game | cryptocrashgame.com | ? | ? | ? | ? |
| crash game gambling | crashgamegambling.com | ? | ? | ? | ? |

**Research each:**
- Search volume and difficulty (use Perplexity + web search)
- Search intent (informational vs. transactional)
- Competitor content quality (can we beat it?)
- Affiliate opportunity (are people making money here?)

## Deliverables

Create research report at: `/workspace/memory/agents/fury-research-report.md`

**Include:**
1. **Site Audit Summary** — what's on each domain now
2. **Competitor Intelligence** — who we're up against
3. **Keyword Matrix** — opportunities by site
4. **Content Gaps** — what competitors miss
5. **Recommendations** — what to build first

**Quality Standard:**
- Receipts for every claim (URLs, sources)
- Confidence levels (High/Medium/Low)
- Actionable insights (so what? what do we do?)
- No "I think" without "here's the evidence"

## Tools Available

- **Perplexity Search:** `/workspace/skills/perplexity/scripts/search.mjs`
- **Web search:** Built-in (use web_search tool)
- **Web fetch:** Built-in (use web_fetch tool for competitor content)
- **WordPress API:** curl for crashcasino.io
- **File system:** Save all research to workspace

## Next Steps

1. Start with crashcasino.io API audit (we have access)
2. Fetch/analyze other 4 sites
3. Run Perplexity searches for competitor intelligence
4. Compile keyword matrix
5. Write research report
6. Move task file to /review/ when done

---

*You're the research lead. Find what others miss. Get receipts.*
