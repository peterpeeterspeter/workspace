# Hobbysalon.be Post Analysis
**Date:** 2026-02-16
**Analyzed by:** Carlottta (WordPress Pro + Pinch-to-Post)
**Total Posts:** 100 (sample of published posts)

---

## Executive Summary

**Overall Site Health:** ⚠️ NEEDS ATTENTION

The site has good content volume but suffers from critical SEO and content quality issues that are likely impacting search rankings and user engagement.

---

## Content Statistics

### Post Distribution
- **Total Posts Analyzed:** 100 (published)
- **All posts created:** February 2025 (mass content batch)
- **Content freshness:** All dated 2025-02-18

### Top Categories by Post Count
1. **decoratie** (Decoratie & Interieur) - 36 posts
2. **papier-kaarten** (Papierkunst & Scrapbooking) - 33 posts
3. **handwerken** (Handwerken & Textiel) - 30 posts
4. **tekenen-schilderen** (Tekenen & Schilderen) - 24 posts
5. **overige-hobbys** (Overige Hobby's) - 24 posts

### Top Tags by Usage
1. **knutselen** - 161 posts (over-tagged)
2. **creatief** - 158 posts (over-tagged)
3. **DIY** - 55 posts
4. **Beginners** - 18 posts
5. **gratis patronen** - 12 posts

---

## Critical Issues Found

### 🔴 CRITICAL - Featured Images
**Issue:** 98 out of 100 posts lack featured images
- **Impact:** devastating for SEO and social sharing
- **Fix priority:** HIGHEST
- **Action:** Need to assign relevant images to all posts

### 🟡 HIGH - Missing Meta Descriptions
**Issue:** 1 post (minimal) has proper excerpt/meta description
- **Impact:** Poor CTR in search results
- **Fix priority:** HIGH
- **Action:** Write compelling meta descriptions for all posts

---

## Content Quality Assessment

### Word Count Analysis
- Not fully analyzed due to batch processing
- Need manual sample check of 10-20 posts
- **Target:** 300+ words for SEO

### Title Quality
**Issues observed:**
- Titles are overly long (truncated in search results)
- Example: "29 inspirerende DIY ideeën voor het maken van een macramé..."
- HTML entities in titles (&#038; instead of &)
- Duplicates or near-duplicates likely exist

### Content Structure
**Unknown** - need deeper analysis of:
- H2/H3 heading usage
- Internal linking
- Keyword optimization
- Readability scores

---

## SEO Issues

### On-Page SEO
1. **No featured images** → No rich snippets, no social cards
2. **Missing meta descriptions** → Poor search CTR
3. **Tag stuffing** → "knutselen" and "creatief" on 90%+ of posts
4. **Batch publishing** → All posts same date (unnatural)

### Keyword Targeting
**Observations:**
- Generic tags overused (knutselen, creatief)
- No clear keyword strategy visible
- Categories are well-organized
- Specific long-tail keywords needed

### Internal Linking
**Not analyzed** - needs manual review

---

## Technical SEO

### Site Structure
- **Categories:** Well-organized (15+ categories)
- **Tags:** Too generic, overused
- **URLs:** Standard WordPress structure
- **Permalinks:** Not checked (need sample)

### Performance
**Plugin Installed:** ✅ hobbysalon-performance-optimizer (12 optimizations)
- Site loads fast (0.67s baseline)
- Lazy loading enabled
- WebP support active

---

## Recommendations

### Immediate Actions (This Week)

1. **Add Featured Images** (Priority: CRITICAL)
   - Batch upload relevant images
   - Use pinch-to-post media-upload
   - Assign to all 100 posts
   - **Estimated time:** 2-3 hours

2. **Write Meta Descriptions** (Priority: HIGH)
   - Target 150-160 characters
   - Include keywords naturally
   - Add CTA where appropriate
   - **Estimated time:** 2 hours

3. **Fix Title Issues** (Priority: MEDIUM)
   - Shorten titles to 60 characters max
   - Fix HTML entities
   - Remove duplicates
   - **Estimated time:** 1 hour

### Next Week

4. **Audit Content Quality**
   - Random sample of 20 posts
   - Check word counts
   - Verify H2/H3 structure
   - Add internal links

5. **Tag Cleanup**
   - Remove generic over-tags (knutselen, creatief)
   - Use specific, descriptive tags
   - Limit to 5-7 relevant tags per post

6. **Spread Publish Dates**
   - Randomize post dates over 6-12 months
   - More natural publication pattern
   - Stagger updates

### Month 2

7. **Content Enhancement**
   - Add FAQ sections
   - Include step-by-step instructions
   - Add image galleries
   - Create related posts sections

8. **Schema Markup**
   - Article schema
   - HowTo schema for tutorials
   - Breadcrumb schema
   - Review/Rating schema

---

## Action Plan with Pinch-to-Post

### Using pinch-to-post to Fix Issues:

```bash
# Health check all posts
for id in {17000..18000}; do
  /root/.openclaw/workspace/scripts/pinch-to-post.sh health-check hobbysalon $id
done

# Bulk upload images (prepare images first)
/root/.openclaw/workspace/scripts/pinch-to-post.sh media-upload hobbysalon image.jpg "Alt text"

# Calendar view for planning
/root/.openclaw/workspace/scripts/pinch-to-post.sh calendar 2026-02 hobbysalon
```

---

## Performance Tracking

### Metrics to Monitor:
- Featured image coverage: Target 100%
- Meta description coverage: Target 100%
- Average word count: Target 300+
- Organic traffic growth: Monitor via Google Search Console
- Search rankings: Track top 20 keywords

---

## Next Steps

**Carlottta will:**
1. Create batch scripts for featured image assignment
2. Generate meta description templates
3. Run quality health checks on 20 post sample
4. Update after fixes applied

**Peter should:**
1. Approve action plan
2. Provide or approve image sources
3. Set timeline for implementation
4. Review and prioritize recommendations

---

**Analysis Complete.** 📊

For detailed post-by-post analysis, run deeper diagnostics or request specific audits.
