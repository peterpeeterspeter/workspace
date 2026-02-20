# Tavily Search Skill

**Version:** 1.0.0
**Author:** arun-8687
**API:** Tavily Search API (https://tavily.com)

AI-optimized web search with results tailored for LLM consumption.

---

## Purpose

Tavily Search provides web search results specifically optimized for AI/LLM consumption:
- Clean, extracted content (not just raw HTML)
- Citations included automatically
- Optimized for question-answering
- Handles complex queries better than generic search
- Includes answer extraction and summarization

---

## Configuration

### API Key

**Required:** Tavily API key

**Get key here:** https://tavily.com

**Store in:** `/root/.openclaw/workspace/.env`

```bash
TAVILY_API_KEY=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
```

---

## API Endpoint

**Base URL:** `https://api.tavily.com/search`

**Method:** POST

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

---

## Request Format

### Basic Search

```json
{
  "api_key": "YOUR_TAVILY_API_KEY",
  "query": "your search query here",
  "search_depth": "basic",
  "max_results": 10
}
```

### Advanced Search

```json
{
  "api_key": "YOUR_TAVILY_API_KEY",
  "query": "your search query here",
  "search_depth": "advanced",
  "max_results": 10,
  "include_answer": true,
  "include_raw_content": false,
  "include_images": false,
  "include_image_descriptions": false,
  "days_range": 3
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | string | Yes | - | Your Tavily API key |
| `query` | string | Yes | - | Search query string |
| `search_depth` | string | No | "basic" | "basic" or "advanced" |
| `max_results` | integer | No | 10 | Number of results to return |
| `include_answer` | boolean | No | false | Include AI-generated answer |
| `include_raw_content` | boolean | No | false | Include raw HTML content |
| `include_images` | boolean | No | false | Include images in results |
| `include_image_descriptions` | boolean | No | false | Include AI image descriptions |
| `days_range` | integer | No | 3 | Search only last X days |

---

## Response Format

```json
{
  "answer": "AI-generated answer to the query",
  "query": "original search query",
  "results": [
    {
      "title": "Page title",
      "url": "https://example.com/page",
      "content": "Extracted and cleaned page content",
      "score": 0.98,
      "raw_content": "Optional raw HTML if requested"
    }
  ],
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "description": "AI-generated image description"
    }
  ]
}
```

---

## Usage Examples

### Basic Search (curl)

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "latest AI trends 2026",
    "search_depth": "basic",
    "max_results": 5
  }'
```

### Advanced Search with Answer

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "What is the best e-commerce platform for small business?",
    "search_depth": "advanced",
    "max_results": 10,
    "include_answer": true
  }'
```

### Search with Time Range

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "Photostudio AI competitor analysis",
    "search_depth": "advanced",
    "max_results": 10,
    "days_range": 7
  }'
```

---

## Helper Script

Create `/root/.openclaw/workspace/skills/tavily-search/tavily-search.sh`:

```bash
#!/bin/bash

API_KEY="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"
QUERY="$1"
DEPTH="${2:-basic}"
MAX_RESULTS="${3:-10}"

if [ -z "$QUERY" ]; then
  echo "Usage: $0 <query> [basic|advanced] [max_results]"
  exit 1
fi

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"$DEPTH\",
    \"max_results\": $MAX_RESULTS,
    \"include_answer\": true
  }" | jq '.'
```

**Usage:**

```bash
# Basic search
./skills/tavily-search/tavily-search.sh "AI image generation trends 2026"

# Advanced search
./skills/tavily-search/tavily-search.sh "best e-commerce platform 2026" advanced 15
```

---

## Comparison with web_search Tool

| Feature | Tavily Search | web_search (Brave) |
|---------|--------------|-------------------|
| API Key | Required (dev/free tier) | Built-in to OpenClaw |
| Answer Extraction | ✅ Yes (AI-generated) | ❌ No |
| Content Cleaning | ✅ Optimized for LLMs | ⚠️ Raw search results |
| Citations | ✅ Automatic | ❌ Manual |
| Search Depth | basic/advanced | Fixed |
| Rate Limits | Depends on plan | Built-in limits |
| Cost | Free tier available | Included with OpenClaw |

**When to use Tavily:**
- Need AI-generated answers
- Want cleaner content extraction
- Complex research queries
- Need automatic citations

**When to use web_search:**
- Quick searches
- No API key needed
- Simple result listings
- Already integrated

---

## Rate Limits

**Free/Dev Tier:**
- Requests per month: Limited
- Concurrent requests: Limited
- Check https://tavily.com for current limits

**Production:**
- Upgrade to paid tier for higher limits
- Monitor usage to avoid rate limiting

---

## Error Handling

### Common Errors

**401 Unauthorized**
- Invalid API key
- Check key in `.env` file

**429 Too Many Requests**
- Rate limit exceeded
- Wait before retrying
- Consider upgrading plan

**400 Bad Request**
- Invalid query format
- Missing required parameters
- Check JSON syntax

---

## Integration with OpenClaw

The Tavily Search skill integrates with OpenClaw's workspace system:

1. **API Key Storage:** `.env` file in workspace
2. **Helper Scripts:** `skills/tavily-search/` directory
3. **Logging:** Use self-improvement skill to log issues

---

## Best Practices

1. **Use for research:** Tavily excels at research queries
2. **Include answers:** Set `include_answer: true` for AI-compiled responses
3. **Advanced depth:** Use "advanced" for comprehensive research
4. **Time filtering:** Set `days_range` for recent info
5. **Monitor usage:** Track API usage to stay within limits

---

## Use Cases for Peter's Projects

### Photostudio.io
- Competitor research: "AI fashion photography competitors 2026"
- Trend analysis: "product photography automation trends"
- Technology research: "background removal API comparison"

### DeBadkamer.com
- Market research: "bathroom renovation trends Belgium 2026"
- Product research: "smart bathroom technology"
- Competitor analysis: "bathroom planning tools comparison"

### Domain Portfolio
- Valuation research: "domain valuation metrics 2026"
- Market trends: "expired domain investing strategies"
- Tool research: "domain auction platforms comparison"

### General Business
- Industry trends
- Competitor monitoring
- Technology research
- Market analysis

---

## Testing

Test the installation:

```bash
# Test basic search
./skills/tavily-search/tavily-search.sh "test query"

# Check response includes answer
# Should return JSON with 'answer' and 'results' fields
```

---

**Last Updated:** 2026-02-20
**API Key:** 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
**Status:** Configured and ready to use
