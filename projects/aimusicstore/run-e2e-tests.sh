#!/bin/bash
# E2E Tests for aimusicstore.com
# Tests all critical API endpoints and frontend pages

set -e

API_BASE="http://localhost:8000"
FRONTEND_BASE="http://localhost:3001"

echo "🧪 aimusicstore.com - E2E Test Suite"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Test counter
TEST_NUM=0

run_test() {
    TEST_NUM=$((TEST_NUM + 1))
    TEST_NAME=$1
    COMMAND=$2
    
    echo "Test $TEST_NUM: $TEST_NAME"
    
    if eval "$COMMAND" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# ============================================
# API Tests
# ============================================
echo "🔧 API Tests"
echo "------------------------------------------"

# Health check
run_test "Health endpoint" "curl -f -s ${API_BASE}/health"

# Trending endpoint
run_test "Trending endpoint (songs + tools)" "curl -f -s ${API_BASE}/api/v1/trending | grep -q 'songs'"

# Top 50 endpoint - alltime
run_test "Top 50 alltime endpoint" "curl -f -s ${API_BASE}/api/v1/top/alltime | grep -q 'items'"

# Top 50 endpoint - daily
run_test "Top 50 daily endpoint" "curl -f -s ${API_BASE}/api/v1/top/daily | grep -q 'items'"

# Top 50 endpoint - weekly
run_test "Top 50 weekly endpoint" "curl -f -s ${API_BASE}/api/v1/top/weekly | grep -q 'items'"

# Top 50 endpoint - monthly
run_test "Top 50 monthly endpoint" "curl -f -s ${API_BASE}/api/v1/top/monthly | grep -q 'items'"

# Vote endpoint (with test data)
# Note: Vote requires agent_id, so we expect 422 response (validation working)
run_test "Vote endpoint (validation works)" "! curl -f -s -X POST ${API_BASE}/api/v1/vote \
  -H 'Content-Type: application/json' \
  -d '{\"item_type\":\"song\",\"item_id\":\"test-song\",\"vote\":\"1\"}' \
  > /dev/null 2>&1"

# Song detail endpoint (if song-1 exists from previous tests)
run_test "Song detail endpoint" "curl -f -s ${API_BASE}/api/v1/songs/song-1 | grep -q 'title'"

# Tool detail endpoint (if tool-1 exists from previous tests)
run_test "Tool detail endpoint" "curl -f -s ${API_BASE}/api/v1/tools/tool-1 | grep -q 'name'"

# ============================================
# Frontend Tests
# ============================================
echo "🌐 Frontend Tests"
echo "------------------------------------------"

# Home page
run_test "Home page loads" "curl -f -s ${FRONTEND_BASE}/ | grep -q 'aimusicstore.com'"

# Trending page (check for React app load)
run_test "Trending page loads" "curl -f -s ${FRONTEND_BASE}/trending | grep -q 'aimusicstore.com'"

# Top 50 page (check for React app load)
run_test "Top 50 page loads" "curl -f -s ${FRONTEND_BASE}/top | grep -q 'aimusicstore.com'"

# ============================================
# Database Tests
# ============================================
echo "💾 Database Tests"
echo "------------------------------------------"

# Health check includes database stats
run_test "Database connection (via health)" "curl -f -s ${API_BASE}/health | grep -q 'database'"

# Check for tables exist
run_test "Agents table exists" "curl -f -s ${API_BASE}/health | grep -q 'agents_count'"

run_test "Songs table exists" "curl -f -s ${API_BASE}/health | grep -q 'songs_count'"

run_test "Tools table exists" "curl -f -s ${API_BASE}/health | grep -q 'tools_count'"

run_test "Votes table exists" "curl -f -s ${API_BASE}/health | grep -q 'votes_count'"

# ============================================
# Response Time Tests
# ============================================
echo "⚡ Performance Tests"
echo "------------------------------------------"

# API response time (should be < 500ms)
API_TIME=$(curl -o /dev/null -s -w '%{time_total}' ${API_BASE}/api/v1/trending)
API_TIME_MS=$(echo "$API_TIME * 1000" | bc)
echo "API Response Time: ${API_TIME_MS}ms"
if (( $(echo "$API_TIME < 0.5" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED${NC} - Response time under 500ms"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAILED${NC} - Response time over 500ms"
    FAILED=$((FAILED + 1))
fi
echo ""

# Frontend load time (should be < 2000ms)
FRONTEND_TIME=$(curl -o /dev/null -s -w '%{time_total}' ${FRONTEND_BASE}/)
FRONTEND_TIME_MS=$(echo "$FRONTEND_TIME * 1000" | bc)
echo "Frontend Load Time: ${FRONTEND_TIME_MS}ms"
if (( $(echo "$FRONTEND_TIME < 2.0" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED${NC} - Load time under 2s"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAILED${NC} - Load time over 2s"
    FAILED=$((FAILED + 1))
fi
echo ""

# ============================================
# Data Integrity Tests
# ============================================
echo "🔍 Data Integrity Tests"
echo "------------------------------------------"

# Trending returns both songs and tools
run_test "Trending has songs array" "curl -f -s ${API_BASE}/api/v1/trending | grep -q 'songs'"

run_test "Trending has tools array" "curl -f -s ${API_BASE}/api/v1/trending | grep -q 'tools'"

run_test "Trending has updated_at field" "curl -f -s ${API_BASE}/api/v1/trending | grep -q 'updated_at'"

# Top 50 returns combined items
run_test "Top 50 has items array" "curl -f -s ${API_BASE}/api/v1/top/alltime | grep -q '\"items\":'"

run_test "Top 50 has rank field" "curl -f -s ${API_BASE}/api/v1/top/alltime | grep -q '\"rank\":'"

# ============================================
# Summary
# ============================================
echo "=========================================="
echo "📊 Test Summary"
echo "=========================================="
echo ""
TOTAL_TESTS=$((PASSED + FAILED))
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    exit 1
fi
