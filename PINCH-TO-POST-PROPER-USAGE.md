# Pinch-to-Post Proper Usage Guide

## ✅ What Works Now

### 1. wp-rest.sh is FIXED
- ✅ Site health checks work
- ✅ Stats display correctly
- ✅ List-posts returns proper JSON
- ✅ Multi-site support works

### 2. Markdown to Gutenberg Conversion
The built-in `markdown_to_gutenberg()` function properly converts:

```markdown
# Heading 1
## Heading 2
**Bold text**
*Italic text*
- List item 1
- List item 2
> Quote text

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

Into proper Gutenberg blocks:
```html
<!-- wp:heading {"level":1} -->
<h1>Heading 1</h1>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li>List item 1</li><li>List item 2</li></ul>
<!-- /wp:list -->

<!-- wp:table -->
<figure class="wp-block-table">
<table>...</table>
</figure>
<!-- /wp:table -->
```

## ❌ What Broke Earlier

### Bad Internal Linking (First Attempt)
The first script replaced keywords **everywhere**, including:
- Inside HTML attributes: `id="crash-<a href...">game</a>"`
- Inside headings: `<h1>Crash <a href...">Gambling</a></h1>`
- Breaking existing HTML structure

### Result: 15 posts have broken HTML mixed with markdown

## 🔧 Proper Workflow Going Forward

### Creating New Posts (Markdown → WordPress)

1. Write content in markdown:
```bash
cat > /tmp/new-post.md << 'EOF'
# Title: Best Crash Casinos 2026

Crash gambling is exciting. Here's what to look for:

## Safety Checklist

- Licensed casino
- Provably fair games
- Fast withdrawals

| Casino | Rating | Link |
|--------|--------|------|
| Stake  | 9.5/10 | [Play](https://cybetplay.com/xxx) |
EOF
```

2. Use pinch-to-post to create post:
```bash
cd /root/.openclaw/workspace/skills/pinch-to-post
export WP_SITE_URL="https://crashcasino.io/wp-json"
export WP_USERNAME="peter"
export WP_APP_PASSWORD="3vRhtTs2khfdLtTiDFqkdeXI"

./wp-rest.sh create-post-markdown "Best Crash Casinos 2026" /tmp/new-post.md draft
```

### Adding Internal Links (Proper Way)

**WRONG:** Replace keywords in HTML string (breaks tags)
**RIGHT:** Add links to plain text BEFORE markdown conversion

Example:
```markdown
# How to Choose a Safe Casino

When selecting a **crash casino**, you should verify...

See also: [Crash Game Scams](https://crashcasino.io/crash-scams)
```

The markdown converter handles the link syntax `[text](url)` properly!

## 🚨 Current Post Status

### Posts Needing Manual Cleanup (15 posts)

**Issues:**
1. Broken internal links inside HTML attributes
2. Markdown tables not converted to HTML
3. Loose `<li>` tags without `<ul>` wrappers

**Options:**

**A) Manual cleanup via WordPress admin**
- Go to WordPress → Posts → Edit
- Use visual editor to fix broken HTML
- Time: ~5-10 minutes per post

**B) Restore from backup (if available)**
- Revert to pre-internal-link version
- Redo internal linking properly
- Need backup files

**C) Use pinch-to-post to recreate posts**
- Export post content as markdown
- Clean it up
- Re-import with `create-post-markdown`

## 📋 Recommended Action Plan

1. **For new posts:** Always use markdown → Gutenberg workflow
2. **For existing posts:**
   - Quick fix: Manual cleanup of critical pages (top 5 posts)
   - Slow fix: Gradually recreate all posts from markdown
3. **Internal linking:** Add as `[text](url)` in markdown BEFORE conversion

## 🎯 Next Steps

Would you like me to:
1. Create a markdown export script for the 15 broken posts?
2. Write proper internal linking in markdown format?
3. Set up a workflow for future posts to avoid this?

The pinch-to-post skill is **great** when used with markdown input. The issues came from trying to modify existing HTML directly.

🦞 **Key lesson:** Markdown first, convert second. Don't edit HTML directly!
