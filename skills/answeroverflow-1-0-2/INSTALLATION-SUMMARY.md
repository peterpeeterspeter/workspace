# Answer Overflow Skill - Installation Complete

## Status: ✅ INSTALLED

**Date:** 2026-02-16 15:43 UTC
**Skill:** answeroverflow-1-0-2
**Location:** `/root/.openclaw/workspace/skills/answeroverflow-1-0-2/`
**Method:** ClawdHub CLI

---

## What It Does

**Core Function:**
Search indexed Discord community discussions via Answer Overflow API. Makes Discord content discoverable on Google.

**Key Features:**
- Search Discord conversations indexed in Google
- Fetch thread content in Markdown format
- MCP server with 4 tools available
- Real community discussions and solutions

---

## How to Use

### 1. Search Discord Content

Use `web_search` with `site:answeroverflow.com` filter:

```bash
# General search
web_search "site:answeroverflow.com <topic>"

# Examples:
web_search "site:answeroverflow.com knitting pattern help"
web_search "site:answeroverflow.com nextjs app router error"
web_search "site:answeroverflow.com prisma connection pooling"
```

### 2. Fetch Thread Content

```bash
# Markdown format
web_fetch url="https://www.answeroverflow.com/m/<message-id>"
```

### 3. MCP Server Tools

Available at: `https://www.answeroverflow.com/mcp`

| Tool | Description |
|------|-------------|
| `search_answeroverflow` | Search indexed Discord communities |
| `search_servers` | Discover indexed servers |
| `get_thread_messages` | Get all thread messages |
| `find_similar_threads` | Find similar threads |

---

## Use Cases for Your Projects

### Hobbysalon.be
**Search Queries:**
- `site:answeroverflow.com knitting pattern help`
- `site:answeroverflow.com crochet stitches tutorial`
- `site:answeroverflow.com yarn substitution guide`

**Benefits:**
- Find real community discussions
- Discover common questions
- Get content ideas
- Understand pain points

### Aimusicstore.com
**Search Queries:**
- `site:answeroverflow.com suno ai music generation`
- `site:answeroverflow.com udio music tips`
- `site:answeroverflow.com music prompt engineering`

**Benefits:**
- User experiences with AI tools
- Common issues/solutions
- Feature requests
- Community feedback

### Photostudio.io
**Search Queries:**
- `site:answeroverflow.com fashion ai tools`
- `site:answeroverflow.com image generation api`
- `site:answeroverflow.com background removal`

**Benefits:**
- Technical discussions
- Integration examples
- User testimonials
- Feature requests

---

## URL Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Thread | `/m/<message-id>` | `https://www.answeroverflow.com/m/1234567890123456789` |
| Server | `/c/<server-slug>` | `https://www.answeroverflow.com/c/prisma` |
| Channel | `/c/<server>/<channel>` | `https://www.answeroverflow.com/c/prisma/help` |

---

## Tips

**Content Quality:**
- Results are real Discord conversations (informal)
- Context may be scattered across messages
- Check server/channel for authority
- Official support vs community discussions

**Research Strategy:**
1. Search with `site:answeroverflow.com` + topic
2. Fetch relevant threads in Markdown
3. Extract key insights/solutions
4. Identify common patterns
5. Create content based on findings

**Content Ideas:**
- FAQ pages from common Discord questions
- Tutorial content from thread solutions
- Blog posts addressing recurring issues
- Community spotlights featuring helpful users

---

## Integration Ideas

### For Hobbysalon.be

**1. Content Research:**
```bash
# Find common knitting questions
web_search "site:answeroverflow.com how to knit"
```

**2. Pain Point Discovery:**
```bash
# Find problems crafters face
web_search "site:answeroverflow.com crochet help problem"
```

**3. Trending Topics:**
```bash
# What's popular in crafting Discord
web_search "site:answeroverflow.com trending knitting pattern"
```

**4. Community Building:**
```bash
# Find active crafting communities
search_servers (MCP tool)
```

---

## Technical Details

**Skill Metadata:**
```json
{
  "name": "answeroverflow",
  "description": "Search indexed Discord community discussions via Answer Overflow",
  "version": "1.0.2"
}
```

**Skill Files:**
- `SKILL.md` - Documentation
- `_meta.json` - Metadata
- `.clawdhub/` - ClawdHub data

**Installation Method:**
```bash
clawdhub install answeroverflow-1-0-2
```

---

## Next Steps

**Immediate:**
1. ✅ Test skill with sample searches
2. ⏳ Document useful findings
3. ⏳ Create content based on insights

**This Week:**
1. Research hobbysalon topics (knitting, crochet)
2. Identify common questions
3. Create FAQ pages
4. Add to content calendar

**Ongoing:**
1. Regular Discord research
2. Content ideation
3. Community insights
4. SEO opportunities

---

## Links

- **Website:** https://www.answeroverflow.com
- **Docs:** https://docs.answeroverflow.com
- **MCP:** https://www.answeroverflow.com/mcp
- **GitHub:** https://github.com/AnswerOverflow/AnswerOverflow

---

**Installed by:** Carlottta (Coordinator)
**Date:** 2026-02-16 15:43 UTC
**Status:** ✅ Active and ready to use

Want me to search specific topics or create content based on Discord insights?
