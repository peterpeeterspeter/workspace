# SEO Research Cache System

**Cache-first workflow to minimize API calls and maximize research reuse.**

---

## 🎯 Problem Solved

**Before:** Every post optimization → fresh API calls → expensive & slow

**After:** One-time research → cached forever → 50% API cost reduction

---

## 📁 Directory Structure

```
/root/.openclaw/workspace/
├── research/
│   └── hobbysalon/
│       ├── keyword-clusters.md          # Master keyword research
│       ├── competitor-intel.md          # Competitor analysis
│       ├── serp-features.md             # SERP feature mapping
│       └── content-gap-analysis.md      # Missing topics
├── cache/
│   └── post-metadata/
│       ├── 17711.json                   # Per-post metadata cache
│       └── ...
└── scripts/
    ├── build-research-cache.sh          # Initial site analysis
    ├── seo-optimize-cached.sh           # Main workflow (cache-first)
    ├── vision-analyze-post.sh           # Vision post analysis
    ├── apply-seo-enrichment.sh          # Apply to WordPress
    ├── refresh-research-cache.sh        # Weekly delta updates
    └── get-site-creds.sh                # Credentials helper
```

---

## 🚀 Workflow

### Step 1: Build Master Research (One-Time)

**First time only:** Vision analyzes entire site

```bash
/root/.openclaw/workspace/scripts/build-research-cache.sh hobbysalon
```

**What happens:**
1. Vision analyzes top 20 posts
2. Extracts keyword clusters
3. Maps SERP features
4. Identifies content gaps
5. Creates 4 master research docs

**Time:** 5-10 minutes
**API calls:** ~100 (one-time)
**Result:** Reusable research forever

### Step 2: Optimize Posts (Cache-First)

**Every post optimization:**

```bash
/root/.openclaw/workspace/scripts/seo-optimize-cached.sh 17711 hobbysalon
```

**What happens:**
1. Check cache → Hit? Use it (0 API calls)
2. Cache miss? Vision analyzes → saves to cache
3. Apply metadata to WordPress
4. Validate with health check

**Time:** 30 seconds (cache) or 2 minutes (miss)
**API calls:** 0 (cache) or ~5 (miss)

### Step 3: Weekly Refresh (Automated)

**Every Monday at 3 AM:** Cron updates research

```bash
0 3 * * 1 /root/.openclaw/workspace/scripts/refresh-research-cache.sh hobbysalon
```

**What happens:**
1. Vision checks for changes (delta mode)
2. Updates keyword clusters if needed
3. Adds new competitors if found
4. Updates SERP feature mapping
5. Refreshes content gaps

**Time:** 5-15 minutes
**API calls:** ~20 (deltas only)

---

## 💰 API Savings

### Without Cache
- 10 posts/week × 5 API calls = 50 calls/week
- 200 calls/month

### With Cache
- **Month 1:** ~200 calls (build + usage)
- **Month 2+:** ~100 calls/month (refresh only)

**Savings: 50% reduction after month 1**

---

## 🎯 Configuration

### SEO Plugin: RankMath

**Fields updated:**
- `rank_math_description` - Meta description
- `rank_math_focus_keyword` - Primary keyword

### Mode: DEEP

**Analysis depth:**
- SERP analysis
- Competitor gap checks
- Full keyword research
- Content type mapping

---

## 📋 Examples

### Optimize single post (uses cache if available)
```bash
seo-optimize-cached.sh 17711 hobbysalon
```

### Build research for new site
```bash
build-research-cache.sh crashcasino
```

### Manual refresh
```bash
refresh-research-cache.sh hobbysalon
```

### Clear cache (force re-analysis)
```bash
rm /root/.openclaw/workspace/cache/post-metadata/17711.json
seo-optimize-cached.sh 17711 hobbysalon
```

---

## 🔍 Cache Files

### Post Metadata Cache (`cache/post-metadata/*.json`)

```json
{
  "post_id": 17711,
  "site": "hobbysalon",
  "last_analyzed": "2026-02-04T22:00:00Z",
  "keywords": {
    "primary": "mokken versieren",
    "secondary": ["mokken ideeën", "mokken inspiratie"],
    "lsi": ["diy mokken", "mokken zelf maken"]
  },
  "meta": {
    "title": "DIY Mokken Versieren: 15 Creatieve Ideeën (2026 Gids)",
    "description": "Ontdek hoe je je mokken zelf kunt versieren met deze 15 creatieve DIY ideeën..."
  },
  "suggestions": {
    "content_gaps": ["mokken materiaal tips", "mokken voor beginners"],
    "internal_links": ["kerst mokken versieren", "mokken personaliseren"],
    "serp_features": ["images", "faq"]
  },
  "confidence": "high",
  "sources": ["keyword-clusters.md", "web_search"]
}
```

---

## 🧪 Testing

### Test workflow on single post
```bash
# 1. Check health before
publish-gateway.sh check 17711 hobbysalon

# 2. Optimize
seo-optimize-cached.sh 17711 hobbysalon

# 3. Check health after (should be higher)
publish-gateway.sh check 17711 hobbysalon

# 4. Publish if 80+
publish-gateway.sh publish 17711 hobbysalon
```

### Test cache hit
```bash
# Run twice - second run should use cache
seo-optimize-cached.sh 17711 hobbysalon
seo-optimize-cached.sh 17711 hobbysalon  # Should show "CACHE HIT"
```

---

## 📊 Monitoring

### Check cache size
```bash
ls -lh /root/.openclaw/workspace/cache/post-metadata/ | wc -l
```

### Check research freshness
```bash
ls -lh /root/.openclaw/workspace/research/hobbysalon/
```

### View cron schedule
```bash
crontab -l | grep refresh-research
```

### View refresh logs
```bash
tail -f /root/.openclaw/workspace/logs/refresh-research.log
```

---

## 🛠️ Troubleshooting

### Vision analysis fails
- Check agent:seo:main is running: `sessions_list`
- Check Vision has access to web tools
- Try running Vision task manually

### Cache not working
- Check cache directory exists: `ls /root/.openclaw/workspace/cache/post-metadata/`
- Check file permissions: `ls -l /root/.openclaw/workspace/cache/post-metadata/`
- Clear cache: `rm /root/.openclaw/workspace/cache/post-metadata/*.json`

### WordPress update fails
- Check credentials in `get-site-creds.sh`
- Test API: `curl -u "user:pass" https://site.com/wp-json/wp/v2/posts/1`
- Check RankMath plugin is active

### Cron not running
- Check crontab: `crontab -l`
- Check cron logs: `grep CRON /var/log/syslog`
- Test script manually first

---

## 🎯 Success Metrics

### Week 1
- [ ] Master research built
- [ ] First 10 posts optimized
- [ ] Cache hit rate > 80%

### Week 2
- [ ] 20 posts optimized
- [ ] Cache hit rate > 90%
- [ ] API usage down 40%

### Week 3
- [ ] 50 posts optimized
- [ ] Cache hit rate > 95%
- [ ] API usage down 50%

---

## 🔄 Maintenance

### Weekly (automated)
- Research refresh runs via cron
- Check logs for errors

### Monthly
- Review cache effectiveness
- Remove stale cache entries
- Update research docs if major SERP changes

### Quarterly
- Full rebuild of research cache
- Archive old cache files
- Performance review

---

## 📝 Notes

- **Vision agent** does all analysis (no manual work)
- **Cache is permanent** until manually cleared
- **Research is reusable** across all posts
- **Refresh is incremental** (not full rebuild)
- **API costs drop** 50% after month 1

---

**Last Updated:** 2026-02-04
**Status:** Production Ready ✅
