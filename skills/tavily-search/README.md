# Tavily Search Skill

**Version:** 1.0.0
**Author:** arun-8687 (via ClawHub)
**Status:** ✅ Installed and Configured
**API Key:** Configured

---

## What It Does

Tavily Search provides AI-optimized web search with:
- Clean, extracted content (not raw HTML)
- AI-generated answers to queries
- Automatic citations
- Optimized for LLM consumption
- Complex query understanding

---

## Quick Start

### Command Line

```bash
# Basic search
./skills/tavily-search/tavily-search.sh "your query here"

# Advanced search
./skills/tavily-search/tavily-search.sh "your query" advanced 15

# Example
./skills/tavily-search/tavily-search.sh "AI fashion photography trends 2026"
```

### Response Format

```json
{
  "answer": "AI-generated summary answer",
  "query": "your search query",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "content": "Extracted content...",
      "score": 0.98
    }
  ]
}
```

---

## Configuration

**API Key:** Stored in `/root/.openclaw/workspace/.env`
```
TAVILY_API_KEY=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
```

**API Endpoint:** https://api.tavily.com/search

**Documentation:** https://tavily.com/docs

---

## Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| query | (required) | Search query string |
| depth | basic | basic, advanced |
| max_results | 10 | 1-100 |

---

## Use Cases

### Photostudio.io
- Competitor research
- Technology research (background removal APIs)
- Trend analysis (AI fashion photography)

### DeBadkamer.com
- Market research (bathroom renovation Belgium)
- Product research (smart bathroom tech)
- Competitor analysis

### Domain Portfolio
- Valuation research
- Market trends
- Tool research

### General
- Industry trends
- Competitor monitoring
- Technology research

---

## Comparison

| Feature | Tavily | web_search (Brave) |
|---------|--------|-------------------|
| AI Answers | ✅ Yes | ❌ No |
| Content Cleaning | ✅ Optimized | ⚠️ Raw |
| Citations | ✅ Auto | ❌ Manual |
| API Key | Required | Built-in |

**Use Tavily when:**
- Need AI-generated answers
- Complex research queries
- Want cleaner results

**Use web_search when:**
- Quick searches
- No API setup needed

---

## Testing

✅ **Tested and working:**

```bash
./skills/tavily-search/tavily-search.sh "test query"
```

**Response:** Successfully returned JSON with answer and 10 results in 0.92s

---

## Files

```
skills/tavily-search/
├── SKILL.md (7.4 KB) - Full documentation
├── tavily-search.sh (1.4 KB) - Helper script (executable)
└── README.md - This file
```

---

**Last Updated:** 2026-02-20
**Status:** ✅ Active and ready to use
