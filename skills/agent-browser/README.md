# Agent Browser Skill - Installed & Configured

**Version:** 0.2.0
**Author:** TheSethRose (via ClawHub)
**Status:** ✅ Installed, configured, and tested
**Binary:** `/usr/bin/agent-browser`

---

## What It Does

**Agent Browser** is a fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to:
- Navigate websites
- Extract structured data from pages
- Fill forms programmatically
- Test web UIs
- Snapshot pages with interactive element refs
- Click, type, and interact with pages

---

## Installation

### ✅ Completed

1. **Installed via npm:**
   ```bash
   npm install -g agent-browser
   ```

2. **Installed dependencies:**
   ```bash
   npm install @playwright/test
   npx playwright install chromium
   ```

3. **Binary location:** `/usr/bin/agent-browser`

4. **Verified working:** Tested with `agent-browser open https://example.com`

---

## Quick Start

### Basic Workflow

```bash
# 1. Navigate to page
agent-browser open https://example.com

# 2. Get interactive elements with refs
agent-browser snapshot -i

# Output example:
# [✓] Example Domain
#   @e1 (a) "More information..."
#   @e2 (h1) "Example Domain"

# 3. Interact using refs
agent-browser click @e1

# 4. Re-snapshot after changes
agent-browser snapshot -i

# 5. Close browser
agent-browser close
```

---

## Common Commands

### Navigation

```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (page analysis)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
```

### Interactions (use @refs from snapshot)

```bash
agent-browser click @e1           # Click element
agent-browser dblclick @e1        # Double-click
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown
```

### Get Information

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
```

### Wait

```bash
agent-browser wait @e1                 # Wait for element
agent-browser wait 2000                # Wait milliseconds
agent-browser wait --text "Success"    # Wait for text
agent-browser wait --url "/dashboard"  # Wait for URL pattern
```

### Screenshots & PDF

```bash
agent-browser screenshot              # Screenshot to stdout
agent-browser screenshot path.png     # Save to file
agent-browser screenshot --full       # Full page
agent-browser pdf output.pdf          # Save as PDF
```

---

## Example Workflows

### Fill and Submit a Form

```bash
# 1. Open form page
agent-browser open https://example.com/form

# 2. Get elements
agent-browser snapshot -i

# 3. Fill inputs
agent-browser fill @e2 "test@example.com"
agent-browser fill @e3 "password123"

# 4. Submit
agent-browser click @e4

# 5. Wait for success
agent-browser wait --text "Success"

# 6. Verify
agent-browser get url
```

### Extract Data from Page

```bash
# 1. Open page
agent-browser open https://example.com/products

# 2. Snapshot
agent-browser snapshot -i

# 3. Extract text from multiple elements
agent-browser get text @e1
agent-browser get text @e2
agent-browser get text @e3

# 4. Screenshot for reference
agent-browser screenshot products.png
```

### Navigate Multi-Page Flow

```bash
# 1. Start at home
agent-browser open https://example.com

# 2. Click through to products
agent-browser snapshot -i
agent-browser click @e5  # Products link

# 3. Wait for navigation
agent-browser wait --url "/products"

# 4. Click product
agent-browser snapshot -i
agent-browser click @e10  # First product

# 5. Extract product info
agent-browser get title
agent-browser get text @e15  # Product name
agent-browser get text @e16  # Price

# 6. Screenshot
agent-browser screenshot product.png
```

---

## Helper Script

Created: `/root/.openclaw/workspace/skills/agent-browser/agent-browser-helper.sh`

```bash
# Usage
./skills/agent-browser/agent-browser-helper.sh open https://example.com
./skills/agent-browser/agent-browser-helper.sh snapshot
./skills/agent-browser/agent-browser-helper.sh click @e1
./skills/agent-browser/agent-browser-helper.sh close
```

---

## Integration with OpenClaw

The `browser` tool in OpenClaw is a separate implementation (Google Chrome integration). Agent browser is complementary:

| Feature | OpenClaw browser | agent-browser |
|---------|-----------------|---------------|
| Implementation | Chrome CDP | Rust CLI + Playwright |
| Use case | Attaching tabs, relay | Headless automation |
| Control | Via `browser` tool | Via CLI commands |
| Refs system | role/name based | @e1, @e2 refs |

**Use agent-browser when:**
- Headless browser automation needed
- Want ref-based element interaction
- Need video recording of actions
- Programmatic form filling
- Structured data extraction

**Use OpenClaw browser when:**
- Attaching to existing browser tabs
- Browser Relay extension
- Visual debugging
- Interactive testing

---

## Use Cases for Peter's Projects

### Photostudio.io
- Test upload functionality
- Automate form fills for product details
- Extract competitor pricing from websites
- Screenshot product pages for analysis

### DeBadkamer.com
- Test lead generation forms
- Navigate bathroom planning tools
- Extract product data from supplier sites
- Automate competitor research

### Domain Portfolio
- Check domain availability on registrars
- Extract auction data from marketplaces
- Automate login to domain management tools
- Monitor expiring domains

### General
- Form automation
- Data extraction
- UI testing
- Competitor monitoring

---

## Testing

✅ **Verified working:**

```bash
agent-browser open https://example.com
# Output: ✓ Example Domain
#         https://example.com
```

**Status:** Working correctly

---

## Files

```
skills/agent-browser/
├── SKILL.md (installed via ClawHub) - Full documentation
├── README.md (this file) - Installation & usage guide
└── agent-browser-helper.sh - Helper wrapper script
```

---

**Last Updated:** 2026-02-20
**Binary:** `/usr/bin/agent-browser`
**Dependencies:** Playwright Chromium installed
**Status:** ✅ Active and ready to use
