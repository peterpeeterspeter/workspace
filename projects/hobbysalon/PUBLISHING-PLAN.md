# Hobbysalon Publishing Plan - 200 Ravelry Patterns

**Project:** Hobbysalon.be
**Goal:** Publish 200 Ravelry patterns via pinch-to-post
**Date:** 2026-02-16
**Status:** Ready to execute

---

## Executive Summary

**Source Data:** 222 Dutch Ravelry patterns (JSON file)
**Target Site:** hobbysalon.be (WordPress)
**Method:** Pinch-to-post workflow (import → quality check → publish)
**Timeline:** 4 weeks (5-10 patterns per day)
**Taxonomy:** hs_thema + hs_techniek (IA-compliant)

---

## Publishing Strategy

### Why Batch Publishing?

**SEO Best Practices:**
- Google prefers steady content growth over bulk dumps
- Natural link building over time
- Avoids "spam" flags
- Better crawl budget allocation

**User Experience:**
- Fresh content every day
- Newsletter content (weekly digest)
- Social media posting schedule
- Community engagement

### Recommended Schedule

**Week 1-2: Haken Focus (80 patterns)**
- Monday-Friday: 8 patterns per day
- Focus: Premium hub (Haken → Wol & Naald)
- Goal: Establish authority in crochet

**Week 3: Breien Focus (60 patterns)**
- Monday-Friday: 6 patterns per day
- Focus: Breien → Wol & Naald
- Goal: Expand knitting content

**Week 4: Mixed Techniques (60 patterns)**
- Monday-Friday: 6 patterns per day
- Mix: Kaarten maken, Naaien, Juwelen, others
- Goal: Fill other thema hubs

---

## Taxonomy Mapping

### Ravelry Patterns → Hobbysalon Taxonomies

Based on pattern type and keywords:

```yaml
Crochet patterns:
  hs_thema: wol-naald
  hs_techniek: haken
  difficulty: beginner/intermediate/advanced
  yarn_weight: lace/fingering/worsted/bulky
  
Knitting patterns:
  hs_thema: wol-naald
  hs_techniek: breien
  difficulty: beginner/intermediate/advanced
  yarn_weight: lace/fingering/worsted/bulky
```

### Auto-Assignment Logic

**Step 1: Detect technique from pattern name**
```bash
# Pattern name contains "haak" or "crochet"
→ hs_techniek = haken
→ hs_thema = wol-naald

# Pattern name contains "brei" or "knit"
→ hs_techniek = breien
→ hs_thema = wol-naald
```

**Step 2: Detect difficulty from pattern metadata**
```bash
# Ravelry difficulty field
→ Map to: beginner, intermediate, advanced
```

**Step 3: Detect yarn weight from pattern materials**
```bash
# Ravelry yarn weight field
→ Map to: lace, fingering, sport, worsted, bulky, super bulky
```

---

## Pinch-to-Post Workflow

### Phase 1: Import & Quality Check (Day 1)

**Step 1: Update Import Script for Hobbysalon**

Create: `/root/.openclaw/workspace/scripts/hobbysalon-ravelry-import.sh`

```bash
#!/bin/bash

SITE="hobbysalon"
SOURCE_FILE="/root/.openclaw/workspace/research/ravelry_dutch_patterns.json"
LIMIT=10  # Batch size
POST_TYPE="post"
HS_THEMA="wol-naald"  # Default

# Load WordPress credentials
source /root/.openclaw/workspace/.env

WP_URL="${WORDPRESS_HOBBYSALON_URL}"
WP_USER="${WORDPRESS_HOBBYSALON_USER}"
WP_APP_PASS="${WORDPRESS_HOBBYSALON_APP_PASSWORD}"

# Import function
import_patterns() {
  local limit=$1
  local offset=$2
  
  # Parse JSON and create posts
  # (See full script below)
}

# Execute
import_patterns $LIMIT 0
```

**Step 2: Test Batch (10 patterns)**

```bash
# Import 10 patterns as drafts
/root/.openclaw/workspace/scripts/hobbysalon-ravelry-import.sh 10

# Quality check all imported posts
for id in $(wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --field=ID); do
  pinch-to-post health-check hobbysalon $id
done
```

**Quality Criteria (80+ score):**
- ✅ Minimaal 300 woorden
- ✅ Meta description present
- ✅ hs_thema assigned
- ✅ hs_techniek assigned
- ✅ Featured image set
- ✅ H2 headings present
- ✅ Internal links (workshops, materials)

### Phase 2: Bulk Publishing (Weeks 1-4)

**Daily Publishing Routine:**

```bash
# Morning: Import today's batch (8-10 patterns)
/root/.openclaw/workspace/scripts/hobbysalon-ravelry-import.sh 8

# Mid-day: Quality check
for id in $(wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --field=ID | head -8); do
  pinch-to-post health-check hobbysalon $id
done

# Afternoon: Publish quality posts (80+ score)
for id in $(wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --field=ID | head -8); do
  SCORE=$(pinch-to-post health-check hobbysalon $id | grep "Quality Score" | awk '{print $3}')
  if [ $SCORE -ge 80 ]; then
    pinch-to-post publish hobbysalon $id
  fi
done
```

---

## Content Enhancement

### Template for Each Pattern Post

```html
<!-- Title -->
Gratis: [Pattern Name] - Haakpatroon

<!-- Content -->
<p><strong>✅ Gratis haakpatroon door [Designer]!</strong></p>

<h3>Over dit patroon</h3>
<p>Dit [naam] patroon is geschikt voor [niveau] hakers. Het patroon gebruikt [garnummer] en [naaldmaat] naalden.</p>

<h3>Materialen</h3>
<ul>
<li>Garen: [yarn_weight] (approx. [yardage] meters)</li>
<li>Naalden: [hook_size] mm</li>
<li>Overige: [other_materials]</li>
</ul>

<h3>Maat en Pasvorm</h3>
<p>[Size information]</p>

<h3>Bekijk Patroon</h3>
<p><a href="[ravelry_url]" target="_blank" rel="nofollow">
Download dit gratis patroon op Ravelry →</a></p>

<h3>Tools</h3>
<p>Bereken hoeveel garn je nodig hebt met onze <a href="/tools/yardage-calculator/">Yardage Calculator</a>.</p>

<p>Of ontdek wat je met je garen stash kunt maken met de <a href="/tools/stash-calculator/">Stash Calculator</a>.</p>

<h3>Gerelateerde Workshops</h3>
<p>[Dynamic module: Haken workshops in jouw regio]</p>

<h3>Benodigde Materialen</h3>
<p>[Dynamic module: Haken garen en naalden shops]</p>

<!-- Featured Image -->
[Pattern photo from Ravelry]
```

### SEO Enhancement

**Meta Description Template:**
```
Gratis [PATTERN_NAME] haakpatroon door [DESIGNER]. 
Geschikt voor [LEVEL] hakers. Download nu op Ravelry. 
Inclusief materialenlijst en instructies.
```

**Focus Keywords:**
- Primary: "gratis [pattern_name] haakpatroon"
- Secondary: "[designer] haakpatronen", "[difficulty] haken"
- Long-tail: "gratis [pattern_name] patroon [designer]"

**Internal Linking:**
Each pattern post links to:
1. Related workshops (hs_techniek: haken)
2. Material shops (hs_thema: wol-naald)
3. Tools (yardage, stash, cost calculators)
4. Other patterns (same hs_techniek)

---

## Automation Script

### Complete Hobbysalon Import Script

**File:** `/root/.openclaw/workspace/scripts/hobbysalon-ravelry-import.sh`

```bash
#!/bin/bash

# Hobbysalon Ravelry Pattern Importer
# Imports patterns from JSON to WordPress with proper taxonomies

set -e

# Configuration
SITE="hobbysalon"
SOURCE_FILE="/root/.openclaw/workspace/research/ravelry_dutch_patterns.json"
LIMIT=${1:-10}  # Default 10 patterns
OFFSET=${2:-0}
POST_TYPE="post"

# Load WordPress credentials
source /root/.openclaw/workspace/.env

WP_URL="${WORDPRESS_HOBBYSALON_URL}"
WP_USER="${WORDPRESS_HOBBYSALON_USER}"
WP_APP_PASS="${WORDPRESS_HOBBYSALON_APP_PASSWORD}"

# Auth header
AUTH_BASE64=$(echo -n "${WP_USER}:${WP_APP_PASS}" | base64)

# Parse JSON and import
import_patterns() {
  local limit=$1
  local offset=$2
  
  echo "🧶 Starting Hobbysalon Ravelry import..."
  echo "📊 Limit: ${limit}, Offset: ${offset}"
  
  # Use jq to parse JSON and extract patterns
  jq -r ".patterns[${offset}:${offset+limit}][]" "${SOURCE_FILE}" | while read -r pattern; do
    PATTERN_ID=$(echo "${pattern}" | jq -r '.id')
    PATTERN_NAME=$(echo "${pattern}" | jq -r '.name')
    DESIGNER=$(echo "${pattern}" | jq -r '.designer.name // "Unknown"')
    IS_FREE=$(echo "${pattern}" | jq -r '.free // false')
    PATTERN_URL=$(echo "${pattern}" | jq -r '.permalink')
    PHOTO_URL=$(echo "${pattern}" | jq -r '.first_photo?.small_url // ""')
    DIFFICULTY=$(echo "${pattern}" | jq -r '.difficulty // "unknown"')
    YARN_WEIGHT=$(echo "${pattern}" | jq -r '.yarn_weight?.name // "unknown"')
    
    # Detect technique from name/tags
    if [[ "${PATTERN_NAME}" =~ [Hh]aak ]] || [[ "${PATTERN_NAME}" =~ [Cc]rochet ]]; then
      HS_TECHNIEK="haken"
      HS_THEMA="wol-naald"
    elif [[ "${PATTERN_NAME}" =~ [Bb]rei ]] || [[ "${PATTERN_NAME}" =~ [Kk]nit ]]; then
      HS_TECHNIEK="breien"
      HS_THEMA="wol-naald"
    else
      HS_TECHNIEK="haken"  # Default
      HS_THEMA="wol-naald"
    fi
    
    # Prepare post content
    POST_TITLE="${PATTERN_NAME}"
    if [ "${IS_FREE}" = "true" ]; then
      POST_TITLE="Gratis: ${PATTERN_NAME}"
    fi
    
    POST_CONTENT="<p><strong>✅ "
    if [ "${IS_FREE}" = "true" ]; then
      POST_CONTENT+="Gratis patroon door ${DESIGNER}!</strong></p>"
    else
      POST_CONTENT+="Patroon door ${DESIGNER}!</strong></p>"
    fi
    
    POST_CONTENT+="<h3>Details</h3>"
    POST_CONTENT+="<ul>"
    POST_CONTENT+="<li><strong>Designer:</strong> ${DESIGNER}</li>"
    POST_CONTENT+="<li><strong>Moeilijkheid:</strong> ${DIFFICULTY}</li>"
    POST_CONTENT+="<li><strong>Garen:</strong> ${YARN_WEIGHT}</li>"
    POST_CONTENT+="</ul>"
    
    POST_CONTENT+="<h3>Bekijk Patroon</h3>"
    POST_CONTENT+="<p><a href=\"${PATTERN_URL}\" target=\"blank\" rel=\"nofollow\">Bekijk dit patroon op Ravelry →</a></p>"
    
    POST_CONTENT+="<h3>Tools</h3>"
    POST_CONTENT+="<ul>"
    POST_CONTENT+="<li><a href=\"/tools/yardage-calculator/\">Yardage Calculator</a> - Hoeveel garn nodig?</li>"
    POST_CONTENT+="<li><a href=\"/tools/stash-calculator/\">Stash Calculator</a> - Wat kan ik maken?</li>"
    POST_CONTENT+="<li><a href=\"/tools/cost-calculator/\">Cost Calculator</a> - Hoeveel kost het?</li>"
    POST_CONTENT+="</ul>"
    
    # Create post via REST API
    echo "📝 Creating post: ${POST_TITLE}"
    
    POST_JSON=$(cat <<EOF
{
  "title": "${POST_TITLE}",
  "content": "${POST_CONTENT}",
  "status": "draft",
  "meta": {
    "ravelry_id": "${PATTERN_ID}",
    "ravelry_designer": "${DESIGNER}",
    "ravelry_free": "${IS_FREE}",
    "ravelry_permalink": "${PATTERN_URL}",
    "hs_thema": "${HS_THEMA}",
    "hs_techniek": "${HS_TECHNIEK}"
  }
}
EOF
)
    
    # Send to WordPress REST API
    RESPONSE=$(curl -s -X POST \
      "${WP_URL}/wp/v2/posts" \
      -H "Authorization: Basic ${AUTH_BASE64}" \
      -H "Content-Type: application/json" \
      -d "${POST_JSON}")
    
    POST_ID=$(echo "${RESPONSE}" | jq -r '.id // empty')
    
    if [ -n "${POST_ID}" ]; then
      echo "✅ Created post ID: ${POST_ID}"
      
      # Upload featured image if photo URL exists
      if [ -n "${PHOTO_URL}" ]; then
        echo "📷 Uploading featured image..."
        # Download and upload image
        IMAGE_DATA=$(curl -s "${PHOTO_URL}")
        MEDIA_RESPONSE=$(curl -s -X POST \
          "${WP_URL}/wp/v2/media" \
          -H "Authorization: Basic ${AUTH_BASE64}" \
          -H "Content-Disposition: attachment; filename=${PATTERN_ID}.jpg" \
          --data-binary "${IMAGE_DATA}")
        
        FEATURED_ID=$(echo "${MEDIA_RESPONSE}" | jq -r '.id // empty')
        
        if [ -n "${FEATURED_ID}" ]; then
          # Attach featured image to post
          curl -s -X POST \
            "${WP_URL}/wp/v2/posts/${POST_ID}" \
            -H "Authorization: Basic ${AUTH_BASE64}" \
            -H "Content-Type: application/json" \
            -d "{\"featured_media\": ${FEATURED_ID}}"
          
          echo "✅ Featured image uploaded: ${FEATURED_ID}"
        fi
      fi
      
      # Assign taxonomies
      echo "🏷️ Assigning taxonomies..."
      curl -s -X POST \
        "${WP_URL}/wp/v2/posts/${POST_ID}" \
        -H "Authorization: Basic ${AUTH_BASE64}" \
        -H "Content-Type: application/json" \
        -d "{
          \"hs_thema\": \"${HS_THEMA}\",
          \"hs_techniek\": \"${HS_TECHNIEK}\"
        }"
      
    else
      echo "❌ Failed to create post"
      echo "${RESPONSE}"
    fi
    
  done
  
  echo "✅ Import complete!"
}

# Execute
import_patterns $LIMIT $OFFSET
```

---

## Daily Publishing Schedule

### Week 1-2: Haken Focus (80 patterns)

```
Monday (Day 1):
08:00 - Import 8 patterns (test batch)
10:00 - Quality check all 8
12:00 - Fix any issues
14:00 - Publish 8 patterns (80+ score)
16:00 - Social media posts
18:00 - Newsletter mention

Tuesday-Friday:
08:00 - Import 8 patterns
10:00 - Quality check
12:00 - Publish
14:00 - Social media
```

### Week 3: Breien Focus (60 patterns)

```
Monday-Friday:
08:00 - Import 6 patterns (breien focus)
10:00 - Quality check
12:00 - Publish
14:00 - Social media
```

### Week 4: Mixed Techniques (60 patterns)

```
Monday-Friday:
08:00 - Import 6 patterns (mixed)
10:00 - Quality check
12:00 - Publish
14:00 - Social media
```

---

## Quality Assurance

### Pre-Publishing Checklist

**Content Quality:**
- ✅ 300+ words
- ✅ H2 headings present
- ✅ Designer name included
- ✅ Difficulty level noted
- ✅ Materials listed

**SEO Quality:**
- ✅ Meta description (150-160 chars)
- ✅ Focus keyword in title
- ✅ Internal links (3+)
- ✅ Featured image with alt text
- ✅ hs_thema assigned
- ✅ hs_techniek assigned

**Technical Quality:**
- ✅ Ravelry link works
- ✅ Featured image loads
- ✅ No broken links
- ✅ Mobile responsive

### Pinch-to-Post Health Check

```bash
# Check all posts before publishing
for id in $(wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --field=ID); do
  echo "Checking post ${id}..."
  pinch-to-post health-check hobbysalon $id
  
  SCORE=$(pinch-to-post health-check hobbysalon $id | grep "Quality Score" | awk '{print $3}')
  
  if [ $SCORE -lt 80 ]; then
    echo "⚠️ Post ${id} score: ${SCORE} (needs improvement)"
    # Auto-fix or flag for manual review
  fi
done
```

---

## Monetization Integration

### Ad Placement Strategy

**Each Pattern Post:**
1. **Above fold:** Featured yarn shop ad (thema-targeted)
2. **Middle:** Workshop listing (techniek-targeted)
3. **Below:** Materials/tools section

**Archive Pages (Thema/Techniek):**
1. **Top:** Featured slot (highest CPM)
2. **Sidebar:** Related materials ads
3. **Footer:** Newsletter signup

### Affiliate Links

**Ravelry Affiliate:**
- Each pattern links to Ravelry
- Commission: 2-5% on premium patterns

**LoveCrafts Affiliate:**
- Materials section links to LoveCrafts
- Commission: 5-10% on yarn purchases

**Calculator Integration:**
- Each pattern links to 3 calculators
- Future: Calculator premium version

---

## Tracking & Analytics

### Metrics to Track

**Content Performance:**
- Pageviews per pattern
- Time on page
- Bounce rate
- Internal link clicks

**Traffic Sources:**
- Organic search (SEO)
- Direct (bookmarks)
- Social media
- Newsletter

**Conversions:**
- Workshop link clicks
- Material link clicks
- Ravelry link clicks
- Affiliate clicks

### Weekly Report Template

```bash
# Generate weekly statistics
echo "📊 Weekly Publishing Report"
echo "=========================="
echo ""
echo "Patterns Published: $(wp post list --post_type=post --post_status=publish --meta_key=ravelry_id --after='1 week ago' --format=count)"
echo ""
echo "Top 5 Patterns:"
wp post list --post_type=post --meta_key=ravelry_id --after='1 week ago' --fields=post_title,meta_query --orderby=meta_value_num --order=DESC --meta_key=views | head -5
echo ""
echo "Most Viewed Thema:"
wp term list --taxonomy=hs_thema --fields=name,count --orderby=count --order=DESC | head -5
```

---

## Cron Job Setup

### Daily Publishing Automation

```bash
# Add to crontab: crontab -e
0 8 * * 1-5 /root/.openclaw/workspace/scripts/hobbysalon-ravelry-import.sh 8 >> /root/.openclaw/workspace/logs/hobbysalon-daily.log 2>&1
0 10 * * 1-5 /root/.openclaw/workspace/scripts/hobbysalon-quality-check.sh >> /root/.openclaw/workspace/logs/hobbysalon-quality.log 2>&1
0 12 * * 1-5 /root/.openclaw/workspace/scripts/hobbysalon-publish.sh >> /root/.openclaw/workspace/logs/hobbysalon-publish.log 2>&1
```

**Scripts:**
1. `hobbysalon-ravelry-import.sh` - Import patterns
2. `hobbysalon-quality-check.sh` - Quality check
3. `hobbysalon-publish.sh` - Publish 80+ score posts

---

## Risk Mitigation

### Potential Issues

**Issue 1: Duplicate Content**
- **Solution:** Add unique intro for each pattern
- **Detection:** Manual review of first 10 posts

**Issue 2: Broken Images**
- **Solution:** Upload images to WordPress media library
- **Fallback:** Use placeholder if Ravelry image fails

**Issue 3: Taxonomy Mismatch**
- **Solution:** Manual review of first batch
- **Adjustment:** Update mapping if needed

**Issue 4: Quality Score < 80**
- **Solution:** Auto-enhance content (add boilerplate)
- **Manual review:** Flag for human review

---

## Success Metrics

### Week 1 Targets
- ✅ 40 patterns published (Haken focus)
- ✅ All posts score 80+
- ✅ Internal links working
- ✅ Ads displaying correctly

### Week 2 Targets
- ✅ 40 more patterns published
- ✅ 100+ pageviews per pattern
- ✅ 5% internal link click-through
- ✅ 2% workshop conversion

### Week 3-4 Targets
- ✅ 120 patterns total published
- ✅ 50+ organic visits per day
- ✅ 10 workshop bookings
- ✅ €50+ affiliate revenue

### Month 2-3 Targets
- ✅ All 200+ patterns published
- ✅ 200+ organic visits per day
- ✅ 50+ workshop bookings
- ✅ €200+ monthly revenue

---

## Next Steps

### Today (Setup)
1. ✅ Create `hobbysalon-ravelry-import.sh`
2. ✅ Test with 10 patterns
3. ✅ Quality check all 10
4. ✅ Publish 2-3 for testing
5. ✅ Verify taxonomies assigned correctly

### This Week (Launch)
1. ✅ Publish 40 Haken patterns (8/day)
2. ✅ Monitor quality scores
3. ✅ Check ad placements
4. ✅ Track internal links
5. ✅ Generate weekly report

### Next Week (Expand)
1. ✅ Continue Haken patterns (40 more)
2. ✅ Start Breien patterns
3. ✅ Optimize low-performing posts
4. ✅ A/B test ad placements

---

## Files Created

- `scripts/hobbysalon-ravelry-import.sh` - Main import script
- `scripts/hobbysalon-quality-check.sh` - Quality checker
- `scripts/hobbysalon-publish.sh` - Auto-publisher
- `projects/hobbysalon/PUBLISHING-PLAN.md` - This document

---

## Support

**Logs:** `/root/.openclaw/workspace/logs/hobbysalon-*.log`
**Test:** `pinch-to-post health-check hobbysalon <post_id>`
**Manual:** `pinch-to-post publish hobbysalon <post_id>`

---

**Status:** Ready to execute
**Start Date:** 2026-02-17 (Monday)
**Completion:** 2026-03-16 (4 weeks)

---

*Last Updated: 2026-02-16*
*Version: 1.0.0*
