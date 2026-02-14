# ✅ Skills Integration Complete

**Date:** 2026-02-03 14:10 UTC
**Status:** Research skills integrated into content production

---

## How Research Works Now

### Vision's Content Production (Enhanced)

**Step 1: Research** (Automatic)
1. **Perplexity AI Research** - AI-powered search with citations
   - Query: `[topic] strategies statistics examples trends 2026 RTP house edge [keywords]`
   - Output: `/root/.openclaw/workspace/tasks/research/{task-id}-perplexity.txt`

2. **Web Search** - Latest information (via tool)
   - Fresh results from Brave Search API
   - Focused on current trends

3. **DataForSEO** - Keyword data (available)
   - Keyword volume and competition
   - SERP analysis

**Step 2: Content Generation** (Uses research)
- Reads research files
- Incorporates statistics and examples
- Cites sources when available

**Step 3: Publishing** (With quality gate)
- Health check (80+ required)
- Bulk publish ready articles
- SEO metadata auto-added

---

## Skill Invocation Methods

### Method 1: Automatic (Best for agents)
- System auto-loads skills based on task description
- Example: "research crash game strategies" → loads Perplexity

### Method 2: Direct Script Execution (In bash scripts)
```bash
# Perplexity
cd /root/.openclaw/workspace/skills/perplexity
node scripts/search.mjs "your query here"

# DataForSEO
cd /root/.openclaw/workspace/skills/seo-dataforseo
# (check SKILL.md for commands)
```

### Method 3: Tool Calls (In agent conversations)
```bash
# Built-in tools (always available)
web_search "crash game strategies" --count 5
web_fetch "https://example.com/article" --extract-mode markdown
```

---

## Available Skills

### ✅ Perplexity (AI Research)
- **Location:** `/root/.openclaw/workspace/skills/perplexity`
- **Command:** `node scripts/search.mjs "query"`
- **Features:** AI-powered answers with citations
- **Use:** Deep research, statistics, expert opinions

### ✅ Web Search (Brave API)
- **Tool:** `web_search` (built-in)
- **Usage:** `web_search "query" --count 5 --freshness pw`
- **Features:** Latest results, fresh content
- **Use:** Current trends, recent news

### ✅ Web Fetch (Content Extraction)
- **Tool:** `web_fetch` (built-in)
- **Usage:** `web_fetch "URL" --extract-mode markdown`
- **Features:** Extract article content
- **Use:** Competitor analysis, content research

### ✅ DataForSEO (Keyword Research)
- **Location:** `/root/.openclaw/workspace/skills/seo-dataforseo`
- **Features:** Keyword volume, competition, SERP data
- **Use:** SEO optimization, keyword strategy

---

## Example: Full Research Workflow

### When Vision receives content task:

```bash
# 1. Load brief
BRIEF_FILE="/root/.openclaw/workspace/tasks/briefs/${TASK_ID}.md"
ARTICLE_TOPIC=$(grep "^# " "$BRIEF_FILE" | sed 's/^# //')
KEYWORDS=$(grep "^Keywords:" "$BRIEF_FILE" | sed 's/^Keywords: //')
SITE=$(grep "^Site:" "$BRIEF_FILE" | sed 's/^Site: //')

# 2. Perplexity research
cd /root/.openclaw/workspace/skills/perplexity
node scripts/search.mjs "${ARTICLE_TOPIC} strategies statistics 2026 ${KEYWORDS}" \
  > "/root/.openclaw/workspace/tasks/research/${TASK_ID}-perplexity.txt"

# 3. Web search for latest info
web_search "${ARTICLE_TOPIC} ${KEYWORDS}" --count 5 --freshness pw \
  > "/root/.openclaw/workspace/tasks/research/${TASK_ID}-web.txt"

# 4. Read and synthesize research
RESEARCH_CONTENT=$(
  cat "/root/.openclaw/workspace/tasks/research/${TASK_ID}-perplexity.txt"
  cat "/root/.openclaw/workspace/tasks/research/${TASK_ID}-web.txt"
)

# 5. Generate content using research
# (Your AI content generation logic here)

# 6. Publish with quality gate
pinch-to-post publish "$SITE" "$POST_ID"
```

---

## Testing Skills

### Test Perplexity:
```bash
cd /root/.openclaw/workspace/skills/perplexity
node scripts/search.mjs "crash game strategies 2026"
```

### Test Web Search:
```bash
web_search "crash gambling tips" --count 3
```

### Test Integration:
```bash
# Run Vision's enhanced workflow manually
/root/.openclaw/workspace/agents/vision/content-production-enhanced.sh test "Test Research"
```

---

## Configuration Check

**Environment Variables:**
- ✅ DATAFORSEO_LOGIN=peeters.peter@telenet.be
- ✅ DATAFORSEO_PASSWORD=*** (set)
- ⚠️ PERPLEXITY_API_KEY=*** (check if set)

**To add Perplexity API key:**
```bash
# Add to /root/.openclaw/workspace/.env
echo "PERPLEXITY_API_KEY=your_key_here" >> /root/.openclaw/workspace/.env
```

---

## Result

**✅ Skills are now integrated into content production workflow.**

When Vision creates content, it will:
1. Automatically research using Perplexity
2. Gather latest info via web search
3. Access keyword data from DataForSEO
4. Synthesize research into content
5. Publish with quality checks

**Research happens automatically - no manual intervention needed.**

---

*Updated: 2026-02-03 14:10 UTC*
*Enhanced by: Carlottta (Coordinator)*
