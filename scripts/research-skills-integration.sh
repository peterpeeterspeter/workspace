#!/bin/bash
# Research Integration Helper
# Shows how to use skills for content research

echo "=== Research Skills Integration Guide ==="
echo ""

# 1. PERPLEXITY SKILL (AI-powered search with citations)
echo "📚 1. PERPLEXITY SKILL (AI Research + Citations)"
echo "   Location: /root/.openclaw/workspace/skills/perplexity"
echo ""
echo "   Usage:"
echo "   cd /root/.openclaw/workspace/skills/perplexity"
echo "   node scripts/search.mjs \"your research query here\""
echo ""
echo "   Example:"
echo "   node scripts/search.mjs \"crash game strategies 2026 RTP house edge\""
echo "   node scripts/search.mjs \"provably fair crash gambling algorithms\""
echo ""
echo "   Batch research (multiple queries at once):"
echo "   node scripts/search.mjs \"query 1\" \"query 2\" \"query 3\""
echo ""

# 2. WEB SEARCH (Brave Search API)
echo "🔍 2. WEB SEARCH (Brave Search API)"
echo "   Built-in tool: web_search"
echo ""
echo "   Usage in agent scripts:"
echo "   web_search \"crash game tips\" --count 5"
echo ""
echo "   Example:"
echo '   web_search "crash gambling strategies 2026" --count 10 --freshness pw'
echo ""

# 3. WEB FETCH (Extract content from URLs)
echo "📖 3. WEB FETCH (Content extraction)"
echo "   Built-in tool: web_fetch"
echo ""
echo "   Usage in agent scripts:"
echo "   web_fetch \"https://example.com/article\" --extract-mode markdown"
echo ""

# 4. SEO DATAFORSEO (Keyword research)
echo "🎯 4. SEO DATAFORSEO (Keyword research)"
echo "   Location: /root/.openclaw/workspace/skills/seo-dataforseo"
echo ""
echo "   Usage:"
echo "   cd /root/.openclaw/workspace/skills/seo-dataforseo"
echo "   # Check SKILL.md for specific commands"
echo ""

# 5. HOW TO INTEGRATE INTO CONTENT PRODUCTION
echo ""
echo "=== Integrating into Content Production ==="
echo ""
echo "In Vision's content-production-enhanced.sh, add research step:"
echo ""
cat << 'EXAMPLE'

# Step 1: Research using Perplexity
echo "Researching topic using Perplexity..." >> "$LOG_FILE"

PERPLEXITY_SKILL="/root/.openclaw/workspace/skills/perplexity"
cd "$PERPLEXITY_SKILL"

# Create research query based on brief
RESEARCH_QUERY="${ARTICLE_TOPIC} statistics trends examples best practices site:${SITE} keywords:${KEYWORDS}"

# Run Perplexity search
node scripts/search.mjs "$RESEARCH_QUERY" > "/root/.openclaw/workspace/tasks/research/${TASK_ID}-research.txt" 2>> "$LOG_FILE"

# Step 2: Additional web search for latest info
web_search "${ARTICLE_TOPIC} ${KEYWORDS}" --count 5 --freshness pw > "/root/.openclaw/workspace/tasks/research/${TASK_ID}-web-search.txt" 2>> "$LOG_FILE"

# Step 3: Extract content from competitor URLs (if needed)
# web_fetch "https://competitor.com/article" --extract-mode markdown > /tmp/competitor-analysis.txt

# Step 4: Use research in content generation
# Read research files and incorporate into article

EXAMPLE

echo ""
echo "=== Skill Invocation Methods ==="
echo ""
echo "Method 1: Direct script execution (as shown above)"
echo "Method 2: Tell agent to use skill"
echo '  Message: "Use the perplexity skill to research crash game strategies"'
echo "Method 3: Automatic (if skill description matches task)"
echo "  System auto-loads skill when relevant"
echo ""

# 6. CHECK WHAT'S CONFIGURED
echo "=== Checking Configuration ==="
echo ""

if [ -f "/root/.openclaw/workspace/.env" ]; then
  echo "Environment variables set:"
  grep -E "PERPLEXITY|DATAFORSEO" /root/.openclaw/workspace/.env | sed 's/.*/  *&/' || echo "  None found"
else
  echo "  No .env file found"
fi

echo ""
echo "=== Testing Skills ==="
echo ""

# Test Perplexity
if [ -f "/root/.openclaw/workspace/skills/perplexity/scripts/search.mjs" ]; then
  echo "✅ Perplexity skill installed"
  echo "   Test: cd /root/.openclaw/workspace/skills/perplexity && node scripts/search.mjs \"test query\""
else
  echo "❌ Perplexity skill not found"
fi

echo ""
echo "=== Summary ==="
echo ""
echo "To research content like before:"
echo "1. Add Perplexity research step to content production"
echo "2. Use web_search for supplementary research"
echo "3. Use web_fetch to analyze competitor content"
echo "4. Use seo-dataforseo for keyword research"
echo ""
echo "Documentation:"
echo "  - Perplexity: /root/.openclaw/workspace/skills/perplexity/SKILL.md"
echo "  - DataForSEO: /root/.openclaw/workspace/skills/seo-dataforseo/SKILL.md"
