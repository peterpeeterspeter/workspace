# Content Deletion Plan - Conservative Approach

**Date:** 2026-02-02
**Strategy:** Delete duplicates + off-topic, preserve any pages with potential backlinks via 301 redirects

---

## Risk Assessment

**Low Risk (Delete Directly):**
- Duplicate posts ("-2" versions) — created by error, zero backlinks
- Off-topic posts from 2018-2020 — old, low quality, unlikely to have backlinks
- Posts with <10 pageviews (check Analytics)

**Medium Risk (301 Redirect):**
- Posts with any pageviews in last 6 months
- Posts with internal links pointing to them
- Posts ranking for keywords (check Search Console)

---

## Deletion Plan by Site

### 1. crashgamegambling.com (30+ deletions)

**Duplicate Pairs (10+ pairs = 20 posts)**
```
ACTION: Keep original, delete "-2" version
EXAMPLE: Keep "crash-bonus-codes", delete "crash-bonus-codes-2"
RISK: Zero — duplicates have no backlinks
```

**Off-Topic Posts (2018-2020)**
```
Delete these generic casino posts:
- "how to play slots" (not crash-specific)
- "roulette strategy" (not crash-specific)
- "poker tips" (not crash-specific)
- Any other pre-2021 non-crash content
RISK: Low — old content, low quality
```

**Action Items:**
1. Get list of all posts via WordPress REST API
2. Identify duplicates (title + "-2")
3. Identify off-topic (date < 2021, not crash-related)
4. Delete via WordPress API
5. Verify deletions

---

### 2. cryptocrashgambling.com (13 deletions)

**Complete Site Wipe**
```
ACTION: Delete all 13 posts
REASON: 100% off-topic (slots, roulette, poker)
RISK: Low — niche mismatch, no relevant backlinks
```

**Post-Deletion:**
- Replace with 10 crypto-crash articles
- Focus: Bitcoin, Ethereum, USDT, Monero crash games
- No-KYC, privacy, VPN content

---

### 3. freecrashgames.com (6 deletions)

**Off-Topic AI/Crypto Posts**
```
Delete:
- "AI interpretability techniques" (not gambling)
- "Cybersecurity best practices" (not gambling)
- Any other non-crash content
RISK: Low — wrong topic entirely
```

**Action Items:**
1. Get all posts via API
2. Filter by topic (not crash-gambling related)
3. Delete 6 off-topic posts
4. Verify

---

### 4. crashcasino.io (0 deletions)

**Status:** Clean site, no deletion needed
**Next:** Scale content (7 → 20-30 posts)

---

## Execution Steps

**Step 1: WordPress API Setup**
```
GET /wp/v2/posts
GET /wp/v2/posts/{id}
DELETE /wp/v2/posts/{id}?force=true
```

**Step 2: Audit Each Site**
- List all posts
- Flag duplicates
- Flag off-topic
- Check pageviews (if Analytics available)

**Step 3: Execute Deletions**
- Batch delete duplicates
- Delete off-topic
- Verify each deletion

**Step 4: 301 Redirects (if needed)**
- If any deleted page had traffic → 301 to relevant replacement
- Document redirect map

---

## Before Deleting: Checklist

- [ ] Get full post list for each site
- [ ] Identify duplicates and off-topic posts
- [ ] Check for internal links (don't break own site)
- [ ] Check Analytics (optional — if available)
- [ ] Prepare redirect map (for any pages with traffic)

---

## After Deleting: Verification

- [ ] Confirm deletions via API (posts not returned)
- [ ] Check for broken internal links
- [ ] Test site navigation
- [ ] Update sitemaps

---

*Created: 2026-02-02 | Next: Execute deletions via WordPress API*
