#!/bin/bash
# Quick test to verify pinch-to-post is actually working
# This simulates what the heartbeat does

echo "=== Testing Pinch-to-Post Integration ==="
echo ""

# Test 1: Stats
echo "Test 1: Can we get stats?"
/root/.openclaw/workspace/scripts/pinch-to-post.sh stats crashcasino 2>&1 | head -5
echo ""

# Test 2: Calendar
echo "Test 2: Can we view calendar?"
/root/.openclaw/workspace/scripts/pinch-to-post.sh calendar 2026-02 crashcasino 2>&1 | head -5
echo ""

# Test 3: Comments
echo "Test 3: Can we check comments?"
/root/.openclaw/workspace/scripts/pinch-to-post.sh comment-moderate crashcasino show-pending 2>&1 | head -10
echo ""

echo "=== Test Complete ==="
