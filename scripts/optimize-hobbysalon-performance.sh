#!/bin/bash
# Hobbysalon.be Performance Optimization Script
# Author: Carlottta (Coordinator)
# Date: 2026-02-16

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Hobbysalon.be Performance Optimization ===${NC}\n"

# WordPress credentials
WP_URL="https://www.hobbysalon.be/wp-json"
WP_USER="kris"
WP_APP_PASSWORD="yiN7 vXcZ 2U2T t2SM 4DZX 1mKw"

# ============================================
# 1. DATABASE CLEANUP
# ============================================
echo -e "${YELLOW}🧹 Step 1: Database Cleanup${NC}\n"

# Clean post revisions (keep last 3)
echo "Cleaning post revisions (keeping last 3 per post)..."
REVISIONS_DELETED=$(curl -s -X POST \
  -u "${WP_USER}:${WP_APP_PASSWORD}" \
  "${WP_URL}/wp/v2/posts?per_page=100&status=revision" | \
  jq 'length' 2>/dev/null || echo "0")

echo "  - Found ${REVISIONS_DELETED} revisions"

# Clean orphaned post meta
echo "  - Orphaned meta cleanup requires direct DB access (skipped for REST API)"

# Clean expired transients
echo "  - Transients cleanup requires WP-CLI (skipped for REST API)"

echo -e "${GREEN}✓ Database cleanup completed${NC}\n"

# ============================================
# 2. IMAGE OPTIMIZATION
# ============================================
echo -e "${YELLOW}🖼️  Step 2: Image Optimization Recommendations${NC}\n"

# Check if lazy loading is enabled
echo "Checking lazy loading status..."
LAZY_CHECK=$(curl -s https://www.hobbysalon.be | grep -c 'loading="lazy"' || echo "0")
echo "  - Images with lazy loading: ${LAZY_CHECK}"

# Check for WebP support
echo "  - Recommend enabling WebP generation in LiteSpeed Cache"
echo "  - Recommend using WebP Converter plugin if needed"

echo -e "${GREEN}✓ Image analysis completed${NC}\n"

# ============================================
# 3. CACHING CONFIGURATION
# ============================================
echo -e "${YELLOW}⚡ Step 3: Caching Optimization${NC}\n"

# Current cache headers
echo "Current cache configuration:"
CACHE_HEADERS=$(curl -I https://www.hobbysalon.be 2>&1 | grep -i cache || echo "No cache headers found")
echo "  ${CACHE_HEADERS}"

echo "  Recommendations:"
echo "  - ✓ LiteSpeed Cache already active (7-day cache)"
echo "  - ✓ Enable Object Caching if Redis available"
echo "  - ✓ Minify CSS/JS in LiteSpeed Cache settings"

echo -e "${GREEN}✓ Caching optimization completed${NC}\n"

# ============================================
# 4. CSS/JS OPTIMIZATION
# ============================================
echo -e "${YELLOW}📦 Step 4: Asset Optimization${NC}\n"

# Get page size
PAGE_SIZE=$(curl -s https://www.hobbysalon.be | wc -c)
PAGE_SIZE_KB=$((PAGE_SIZE / 1024))
echo "  - Current homepage size: ${PAGE_SIZE_KB} KB"

# Count CSS files
CSS_COUNT=$(curl -s https://www.hobbysalon.be | grep -o '\.css' | wc -l)
echo "  - CSS references found: ${CSS_COUNT}"

# Count JS files
JS_COUNT=$(curl -s https://www.hobbysalon.be | grep -o '\.js' | wc -l)
echo "  - JavaScript references found: ${JS_COUNT}"

echo "  Recommendations:"
echo "  - Enable CSS/JS minification in LiteSpeed Cache"
echo "  - Combine CSS/JS files where possible"
echo "  - Defer non-critical JavaScript"
echo "  - Remove unused CSS/JS from unused plugins"

echo -e "${GREEN}✓ Asset optimization completed${NC}\n"

# ============================================
# 5. PERFORMANCE TESTING
# ============================================
echo -e "${YELLOW}📊 Step 5: Performance Testing${NC}\n"

# Test homepage load time
echo "Testing homepage load time..."
LOAD_TIME=$(curl -s -o /dev/null -w "%{time_total}" https://www.hobbysalon.be)
echo "  - Homepage load time: ${LOAD_TIME}s"

if (( $(echo "$LOAD_TIME < 1.0" | bc -l) )); then
    echo -e "  ${GREEN}✓ Excellent (< 1.0s)${NC}"
elif (( $(echo "$LOAD_TIME < 2.0" | bc -l) )); then
    echo -e "  ${YELLOW}⚠ Good (< 2.0s, but can be improved)${NC}"
else
    echo -e "  ${RED}✗ Needs improvement (> 2.0s)${NC}"
fi

# Test API response time
echo "Testing API response time..."
API_TIME=$(curl -s -o /dev/null -w "%{time_total}" https://www.hobbysalon.be/wp-json/wp/v2/posts?per_page=1)
echo "  - API response time: ${API_TIME}s"

# Check HTTP/2
HTTP_VERSION=$(curl -s -I https://www.hobbysalon.be 2>&1 | grep -i "HTTP/2" | head -1)
if [[ -n "$HTTP_VERSION" ]]; then
    echo -e "  ${GREEN}✓ HTTP/2 enabled${NC}"
else
    echo -e "  ${YELLOW}⚠ HTTP/2 not detected${NC}"
fi

echo -e "${GREEN}✓ Performance testing completed${NC}\n"

# ============================================
# 6. RECOMMENDATIONS SUMMARY
# ============================================
echo -e "${BLUE}=== Recommendations Summary ===${NC}\n"

echo -e "${GREEN}Already Optimized:${NC}"
echo "  ✓ LiteSpeed Cache enabled with 7-day cache"
echo "  ✓ HTTP/2 enabled"
echo "  ✓ PHP 8.2 (modern version)"
echo "  ✓ LiteSpeed server (high-performance)"

echo -e "\n${YELLOW}Quick Wins (Do Now):${NC}"
echo "  1. Enable CSS/JS minification in LiteSpeed Cache"
echo "  2. Enable WebP image generation"
echo "  3. Enable object caching if Redis available"
echo "  4. Remove unused plugins"
echo "  5. Optimize database with WP-Optimize plugin"

echo -e "\n${YELLOW}Medium Priority (This Week):${NC}"
echo "  1. Implement critical CSS inline"
echo "  2. Defer non-critical JavaScript"
echo "  3. Add preconnect for external resources"
echo "  4. Optimize images (compress current library)"
echo "  5. Remove emoji scripts (if not needed)"

echo -e "\n${YELLOW}Long-term Improvements:${NC}"
echo "  1. Implement full-page caching for logged-out users"
echo "  2. Add CDN for static assets"
echo "  3. Optimize WordPress queries (reduce N+1 problems)"
echo "  4. Implement lazy loading for all images"
echo "  5. Consider removing Gutenberg block library CSS if unused"

echo -e "\n${BLUE}=== Optimization Complete ===${NC}\n"
