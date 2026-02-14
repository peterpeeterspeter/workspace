# Article Publishing Fix Required

**Issue:** Published articles have formatting problems — WordPress UI text mixed into content, broken HTML structure.

**Root Cause:** The `publish_articles.py` script uses basic string replacement for markdown-to-HTML conversion, which is inadequate.

**Current Markdown Conversion (BROKEN):**
```python
# Simple regex-based replacement — doesn't work properly
html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
# This breaks tables, code blocks, lists, etc.
```

**Required Fix:** Use proper markdown library

---

## Solution

### Option 1: Use Python `markdown2` Library

```python
import markdown2

def markdown_to_html(markdown_text):
    """Convert markdown to HTML properly."""
    html = markdown2.markdown(
        markdown_text,
        extras=['tables', 'fenced-code-blocks', 'header-ids', 'strike-through']
    )
    return html
```

**Install:**
```bash
pip install markdown2
```

### Option 2: Use Python `markdown` Library

```python
import markdown

def markdown_to_html(markdown_text):
    """Convert markdown to HTML properly."""
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'toc',
        'sane_lists',
        'nl2br',
        'extra'
    ])
    html = md.convert(markdown_text)
    return html
```

**Install:**
```bash
pip install markdown
```

---

## Updated Publishing Workflow

For each article:

1. **Read source markdown** from `/drafts/`
2. **Extract frontmatter** (site, title, slug, etc.)
3. **Convert markdown to HTML** using proper library
4. **Create WordPress post** with HTML content
5. **Verify** no WordPress UI artifacts in content

---

## Articles to Republish (All 12)

After fixing the conversion script, republish all 12 articles with proper HTML formatting.

---

## Priority

**HIGH — This is blocking content quality improvements.**

Vision must:
1. Fix the publishing script first
2. Then republish all 12 articles
3. Then proceed with quality improvements (compliance, SEO, content depth)

**Otherwise, quality improvements won't matter if the HTML is broken.**