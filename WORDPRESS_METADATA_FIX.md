# WordPress Metadata Fix - Complete SEO Data

**Problem:** Published articles missing critical SEO metadata

---

## 📊 Current State (Broken)

**What's Missing:**
- ❌ No Yoast SEO title (using WordPress default)
- ❌ No meta description (or auto-generated)
- ❌ No focus keyword
- ❌ No schema markup (Article, FAQPage)
- ❌ No OpenGraph tags
- ❌ No Twitter Card data

**Current WordPress Data:**
```json
{
  "meta": {
    "_acf_changed": false,
    "footnotes": ""
  }
}
```

**Yoast SEO Data:** Missing entirely

---

## ✅ Solution

**Updated WordPress Publishing Script**

**File:** `/agents/vision/wordpress-publish-with-metadata.sh`

**Now Includes:**
1. **Meta Description** - From markdown `**Meta Description:**`
2. **SEO Title** - From markdown `**Title Tag:**`
3. **Focus Keyword** - From markdown `**Primary Keyword:**` or `**Target Keyword:**`
4. **Keywords** - From markdown `**Target Keywords:**`
5. **Schema Markup** - Auto-generated Article schema
6. **Excerpt** - Proper meta description

**Payload Structure:**
```json
{
  "title": "Article Title",
  "content": "HTML content",
  "excerpt": "Meta description",
  "meta": {
    "yoastseo": {
      "title": "SEO Title (60 chars)",
      "metadesc": "Meta description (160 chars)",
      "focuskw": "Focus keyword",
      "keywords": ["keyword1", "keyword2"]
    }
  }
}
```

---

## 📋 Metadata Extracted from Markdown

The script now looks for these fields in your markdown:

```markdown
---
title: Article Title
description: Meta description for SEO
keywords: primary keyword, secondary keyword
---

# H1 Article Title

**Title Tag:** SEO Title (appears in search results)
**Meta Description:** Description for search results (160 chars)
**Primary Keyword:** Main keyword for Yoast SEO
**Target Keywords:** Comma-separated keyword list

Article content...
```

---

## 🔧 How to Use

**For Existing Articles:**

1. Add metadata to draft files:
```markdown
**Title Tag:** Optimized Title for Search Engines
**Meta Description:** Compelling 160-character description
**Primary Keyword:** main keyword here
**Target Keywords:** kw1, kw2, kw3
```

2. Run publishing script:
```bash
/root/.openclaw/workspace/agents/vision/wordpress-publish-with-metadata.sh "task-id" "Publish with SEO metadata"
```

**For New Articles:**

- Vision agent now uses this script automatically
- All future articles will include full SEO metadata
- Yoast SEO data properly populated

---

## 📈 SEO Benefits

**With Proper Metadata:**
- ✅ Search engines show custom titles (not auto-generated)
- ✅ Custom descriptions in search results
- ✅ Focus keyword tracking in Yoast SEO
- ✅ Schema markup for rich snippets
- ✅ Better CTR from search results
- ✅ Improved rankings

**Example:**

**BEFORE (Auto-generated):**
- Title: "Crash Casino Scams: 7 Red Flags That Scream 'Rogue Site' - Crash, Cash, Collect"
- Description: "Crash casino scams: 7 red flags..."

**AFTER (Optimized):**
- Title: "Crash Casino Scams: 7 Red Flags That Scream Rogue Site (2026)"
- Description: "Don't get scammed. Learn 7 warning signs of fake crash casinos, how withdrawal stalling works, and blacklisted sites to avoid."

---

## 🎯 Next Steps

**Option 1: Update Published Articles**
1. Add metadata to existing markdown files
2. Republish with metadata script
3. All 9 articles get proper SEO data

**Option 2: Future Articles Only**
- New articles automatically include metadata
- Old articles stay without optimized metadata
- Not recommended - better to fix all

**Option 3: Bulk Metadata Update**
- Create script to update all published posts
- Add Yoast SEO metadata via REST API
- Takes 5-10 minutes

---

## 📝 Documentation

**Files:**
- `/agents/vision/wordpress-publish-with-metadata.sh` - Full metadata support
- `/agents/shared/md2html-fixed.py` - Converts markdown with metadata extraction

**Learning:**
- Logged to `.learnings/LEARNINGS.md` as LRN-20260202-003

---

*All future WordPress publishing will now include complete SEO metadata!*
