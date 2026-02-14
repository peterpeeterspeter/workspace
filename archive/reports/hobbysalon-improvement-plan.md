# Hobbysalon.be Technical Analysis & Improvement Plan

**Date:** 2026-02-04
**Site:** https://www.hobbysalon.be
**WordPress REST API:** Accessible ✅
**Redirect:** hobbysalon.be → www.hobbysalon.be (HTTP 301)

---

## Executive Summary

**Site Status:** WordPress site with RankMath SEO plugin
**Focus:** Hobby content (beauty, nails, salon)
**Immediate Needs:** Performance optimization, content strategy, SEO improvements

---

## Phase 1: Technical Analysis (DO FIRST)

### 1.1 Performance Analysis

**Current Issues:**
- HTTP 301 redirect (hobbysalon.be → www.hobbysalon.be)
  - Impact: Minor latency (+50-100ms per request)
  - Recommendation: Ensure canonical URLs set correctly

**Page Speed Needs Assessment:**
```bash
# Check current page load times
curl -w "@-" -o /dev/null -s "https://www.hobbysalon.be/" <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
   time_pretransfer:  %{time_pretransfer}\n
      time_redirect:  %{time_redirect}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
```

### 1.2 WordPress Health Check

**Run via pinch-to-post:**
```bash
/root/.openclaw/workspace/scripts/pinch-to-post.sh stats \
  https://www.hobbysalon.be/wp-json \
  kris BAvt knyO ystE qYXk YQUo v9mu
```

**What to Check:**
- Total post count
- Total page count
- Media library size
- Plugin count (too many = slow)
- Theme performance
- PHP version
- WordPress version

### 1.3 RankMath Configuration Analysis

**Current SEO Settings to Audit:**
- Titles & Meta (are they optimized?)
- XML Sitemap (is it generated?)
- Schema Markup (what types enabled?)
- Open Graph tags (social sharing)
- Robot.txt configuration
- Canonical URLs
- Redirect rules (404s)

---

## Phase 2: Content Audit (DO SECOND)

### 2.1 Content Inventory

**Extract via WordPress API:**
```bash
# Get all posts
curl -s -u "kris:BAvt knyO ystE qYXk YQUo v9mu" \
  "https://www.hobbysalon.be/wp-json/wp/v2/posts?per_page=100&_fields=id,title,link,date,categories"

# Get all pages
curl -s -u "kris:BAvt knyO ystE qYXk YQUo v9mu" \
  "https://www.hobbysalon.be/wp-json/wp/v2/pages?per_page=100&_fields=id,title,link,date"
```

**Analyze:**
- Total content count
- Content frequency (how often published)
- Content categories
- Content length distribution
- Last publish date

### 2.2 SEO Content Analysis

**For Each Post/Page:**
- Title tag length (50-60 chars ideal)
- Meta description (150-160 chars)
- H1 structure (one per page)
- Image alt tags
- Internal links
- External links
- Keyword focus
- Readability score

---

## Phase 3: Speed Optimization Plan

### 3.1 Image Optimization (HIGH IMPACT)

**Current State:** Unknown
**Recommendation:**
- Compress all images (WebP format preferred)
- Lazy loading for images below fold
- Image dimensions matching display size
- CDN for static assets (if not using)

**Implementation:**
```bash
# Use wp-cli or WordPress plugin
# Recommended plugins:
- Smush (free image optimization)
- WP Rocket (caching + performance)
- ShortPixel (image optimization)
```

### 3.2 Caching Strategy (HIGH IMPACT)

**Recommendation:**
- Page caching (static HTML cache)
- Browser caching (expires headers)
- GZIP compression
- Database query caching
- Object caching (Redis if available)

**Plugin Options:**
- WP Rocket (paid, excellent)
- W3 Total Cache (free, complex)
- WP Super Cache (free, simple)
- LiteSpeed Cache (if on LiteSpeed server)

### 3.3 Database Optimization (MEDIUM IMPACT)

**Tasks:**
- Clean post revisions (limit to 3-5 per post)
- Optimize database tables
- Remove spam comments
- Clean transients
- Remove unused plugins/themes

---

## Phase 4: SEO Improvement Plan

### 4.1 Keyword Research (HIGH PRIORITY)

**Hobby Salon Keywords to Target:**
- "hobby salon [city/region]"
- "nail salon [city/region]"
- "beauty salon [city/region]"
- "hobby products reviews"
- "DIY beauty tutorials"
- "nail art tutorials"
- "hobby events [city/region]"

**Long-tail Opportunities:**
- "beginner hobby classes [city]"
- "kids hobby parties [city]"
- "hobby supplies online belgium"
- "nail salon near me"
- "best hobbies for beginners"

### 4.2 On-Page SEO Fixes

**For Each Page/Post:**
1. **Title Tags:** 50-60 characters, include keyword
2. **Meta Descriptions:** 150-160 characters, compelling
3. **H1 Tags:** One per page, keyword included
4. **URL Structure:** Short, keyword-rich, hyphens
5. **Internal Linking:** Related content links
6. **Image Alt Text:** Descriptive, keyword-rich
7. **Content Length:** 300+ words (minimum)
8. **Schema Markup:** LocalBusiness, Article, FAQPage

### 4.3 Local SEO (CRITICAL for Salon)

**Google Business Profile:**
- Claim/verify listing
- Add photos (interior, exterior, work)
- Get reviews (ask happy customers)
- Update hours, contact info
- Add services (nails, beauty, hobbies)
- Posts weekly (offers, events)

**Local Directories:**
- Yelp (if applicable in Belgium)
- Golden Pages (Belgium)
- Local business directories
- Industry-specific directories

### 4.4 Content Strategy

**Content Pillars (Hub Pages):**
1. "Hobby Services" (overview of all services)
2. "Hobby Classes" (classes, workshops, events)
3. "Hobby Products" (products, supplies, reviews)
4. "Hobby Blog" (tutorials, tips, trends)
5. "About Us" (story, team, gallery)

**Supporting Content (Spoke Pages):**
- Service detail pages (nails, beauty, workshops)
- Location-specific pages (if multiple locations)
- Product reviews
- How-to guides
- Trending topics

---

## Phase 5: Technical SEO Fixes

### 5.1 XML Sitemap

**Ensure:**
- Sitemap generated (RankMath does this)
- All pages/posts included
- Images included (if applicable)
- Submitted to Google Search Console
- Updated automatically

**Location:** https://www.hobbysalon.be/sitemap_index.xml

### 5.2 Robots.txt

**Required:**
```
User-agent: *
Allow: /
Sitemap: https://www.hobbysalon.be/sitemap_index.xml

# Block admin areas
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/plugins/
Disallow: /wp-content/themes/
Disallow: /wp-includes/json/
Disallow: /wp-json/
```

### 5.3 Schema Markup (RankMath Supports)

**Implement:**
- **LocalBusiness** schema (critical for salon)
- **Article** schema (blog posts)
- **Review** schema (customer reviews)
- **FAQPage** schema (common questions)
- **Event** schema (classes, workshops)
- **Product** schema (if selling products)

### 5.4 Canonical URLs

**Ensure:**
- Self-referencing canonical tags
- No duplicate content issues
- HTTPS canonical (not HTTP)
- WWW canonical (not non-WWW)
- No parameters in canonical URLs

---

## Phase 6: User Experience (UX) Improvements

### 6.1 Mobile Responsiveness

**Test:**
- Mobile-friendly test (Google)
- Responsive design check
- Touch-friendly navigation
- Readable text on mobile
- Fast load on mobile (3G connection)

### 6.2 Navigation Structure

**Optimize:**
- Clear menu hierarchy
- Services prominently displayed
- Contact info visible
- Call-to-action buttons (book now, call now)
- Search functionality

### 6.3 Conversion Optimization

**Add:**
- Phone number in header
- Click-to-call buttons (mobile)
- Contact form on every page
- Online booking (if applicable)
- Social proof (testimonials, reviews)
- Trust signals (certifications, awards)

---

## Phase 7: Security & Maintenance

### 7.1 Security Checklist

- SSL certificate valid (HTTPS enforced)
- WordPress updated to latest version
- Plugins updated to latest versions
- Theme updated to latest version
- Strong passwords (admin, FTP, database)
- Two-factor authentication (if available)
- Regular backups (offsite)
- Security plugin (Wordfence, iThemes Security)

### 7.2 Backup Strategy

**Recommend:**
- Daily automated backups
- Offsite storage (Dropbox, Google Drive, cloud)
- Retention: 30 days
- Test restore quarterly

---

## Implementation Priority (What to Do First)

### Week 1 (CRITICAL - Do This First)
1. **Performance Analysis** - Pinch-to-post stats command
2. **Image Optimization** - Install Smush or similar
3. **Caching Plugin** - Install WP Rocket or W3 Total Cache
4. **RankMath Audit** - Review all SEO settings
5. **Sitemap** - Verify generated and submitted

### Week 2 (HIGH PRIORITY)
6. **Keyword Research** - Identify target keywords
7. **On-Page SEO** - Fix title tags, meta descriptions
8. **Local SEO** - Claim/optimize Google Business Profile
9. **Content Audit** - Inventory all content
10. **Schema Markup** - Add LocalBusiness schema

### Week 3 (MEDIUM PRIORITY)
11. **Content Strategy** - Create content calendar
12. **Internal Linking** - Improve link structure
13. **Mobile Optimization** - Test and fix mobile issues
14. **Security Review** - Update plugins/themes
15. **Backup Setup** - Configure automated backups

### Week 4 (ONGOING)
16. **Monitor Performance** - Weekly page speed checks
17. **Content Creation** - Publish 2-3 blog posts/week
18. **Review Analytics** - Google Search Console, Analytics
19. **Build Backlinks** - Local directories, industry sites
20. **Social Media** - Cross-post content to social channels

---

## Success Metrics (Track These)

### Performance
- Page load time: < 3 seconds (current target: < 2 seconds)
- Mobile score: > 90 (Google PageSpeed Insights)
- Desktop score: > 90 (Google PageSpeed Insights)

### SEO
- Organic traffic: +50% in 3 months
- Keyword rankings: Top 10 for 10+ keywords
- Indexed pages: 100% of content indexed
- Backlinks: +20 quality backlinks in 3 months

### Engagement
- Bounce rate: < 60%
- Time on site: +30 seconds
- Pages per session: +1 page
- Conversion (contact/bookings): +50%

---

## Tools Needed

### WordPress Plugins (Recommended)
- **RankMath SEO** (already installed ✅)
- **Smush** or **ShortPixel** (image optimization)
- **WP Rocket** or **W3 Total Cache** (caching)
- **Wordfence** or **iThemes Security** (security)
- **UpdraftPlus** or **BackupBuddy** (backups)

### Analysis Tools
- **Google Search Console** (free, essential)
- **Google Analytics** (free, essential)
- **Google PageSpeed Insights** (free, performance)
- **Screaming Frog** (free version, SEO audit)
- **Ahrefs Free Backlink Checker** (free, backlinks)

---

## Risk Assessment (What NOT to Do)

### ⚠️ HIGH RISK - DON'T DO THESE

1. **Don't delete content** without backing up first
2. **Don't change URL structures** (301 redirects needed)
3. **Don't install too many plugins** (slows site)
4. **Don't edit theme files directly** (use child theme)
5. **Don't forget backups** before major changes
6. **Don't ignore mobile users** (50%+ traffic)
7. **Don't keyword stuff** (penalty risk)
8. **Don't buy backlinks** (penalty risk)
9. **Don't copy content** (duplicate content penalty)
10. **Don't forget social proof** (reviews, testimonials)

---

## Next Steps (Do This Now)

1. **Run technical analysis:**
   ```bash
   /root/.openclaw/workspace/scripts/pinch-to-post.sh stats \
     https://www.hobbysalon.be/wp-json \
     kris BAvt knyO ystE qYXk YQUo v9mu
   ```

2. **Check current performance:**
   - Google PageSpeed Insights: https://pagespeed.web.dev/
   - GTmetrix: https://gtmetrix.com/
   - Pingdom: https://www.pingdom.com/

3. **Install RankMath** (if not active) and configure:
   - Connect Google Search Console
   - Generate XML sitemap
   - Setup schema markup
   - Configure title/meta templates

4. **Content inventory:**
   - Export all posts/pages
   - Identify thin content (< 300 words)
   - Identify duplicate content
   - Identify missing SEO elements

---

**Plan created by:** Carlottta (Coordinator)
**Date:** 2026-02-04
**Priority:** Start with Week 1 (Performance + SEO basics)
**Goal:** Improve speed, rankings, and user experience without breaking anything

**Want me to run the technical analysis now?**
