# Cardfair Credit Card Comparison Tool - WordPress Setup Guide

## 📦 What You Get

### 1. **Interactive Comparison Tables**
- Side-by-side card comparisons
- Filter by card type (secured, student, travel, cashback)
- Filter by issuer, annual fee, credit score
- Mobile-responsive design

### 2. **Pre-Built Pages**
- "Best Secured Credit Cards 2025"
- "Best Student Credit Cards"
- "Best Travel Credit Cards"
- "Best Cash Back Credit Cards"

### 3. **Shortcodes**
```
[cardfair_compare cards="Discover it,Capital One,Citi Double" features="annual_fee,rewards,apr"]
[cardfair_top_picks type="secured" limit="5"]
```

---

## 🚀 Installation Methods

### **Option A: Custom Plugin (Recommended)**

#### Step 1: Create Plugin Folder
```bash
cd /path-to-wordground/wp-content/plugins/
mkdir cardfair-comparison
cd cardfair-comparison
```

#### Step 2: Upload Files
Upload these files to the plugin folder:
- `cardfair-comparison-tables.php` (main plugin)
- `comparison-tables.css` (styles)
- `template-comparison-table.php` (comparison template)
- `template-top-picks.php` (top picks template)
- `credit-cards.json` (your data)

#### Step 3: Activate Plugin
1. Go to WordPress Admin → Plugins
2. Find "Cardfair Comparison Tables"
3. Click "Activate"

#### Step 4: Create Pages
Create new pages in WordPress with these shortcodes:

**Best Secured Cards:**
```
[cardfair_top_picks type="secured" limit="10"]
```

**Best Student Cards:**
```
[cardfair_top_picks type="student" limit="8"]
```

**Side-by-Side Comparison:**
```
[cardfair_compare cards="Discover it,Capital One,Citi Double,Citi Simplicity" features="annual_fee,rewards,apr,credit_score"]
```

---

### **Option B: Copy-Paste HTML Pages (Fastest)**

#### Step 1: Download the HTML File
File: `secured-cards-page.html`

#### Step 2: Create New Page in WordPress
1. Pages → Add New
2. Title: "Best Secured Credit Cards 2025"
3. Switch to "Code Editor" (not Visual editor)
4. Paste the HTML content
5. Publish

#### Step 3: Customize
- Add your affiliate links
- Update cards data
- Add your branding

---

### **Option C: Custom Page Template**

#### Step 1: Upload Template
```bash
cd /path-to-wordground/wp-content/themes/your-theme/
# Upload: page-secured-cards.php
```

#### Step 2: Create Page with Template
1. Pages → Add New
2. Title: "Secured Credit Cards"
3. Page Attributes → Template → "Secured Cards"
4. Publish

---

## 📝 Adding Your Data

### Using JSON File
Your `credit-cards.json` should contain:
```json
{
  "credit_cards": [
    {
      "name": "Card Name",
      "issuer": "Bank Name",
      "rewards": "Rewards info",
      "annual_fee": "$0",
      "interest_rate": "18.24% - 28.99%",
      "additional_features": "Card features...",
      "credit_score_required": "Good to Excellent"
    }
  ]
}
```

### Updating Data
1. Edit `credit-cards.json`
2. Or update in WordPress Admin (if plugin supports it)
3. Changes reflect immediately

---

## 🔗 Adding Affiliate Links

### Method 1: Edit Shortcode Output
Add affiliate links in `template-comparison-table.php`:
```php
<a href="https://your-affiliate-link.com/offer-id" 
   class="cardfair-apply-btn"
   rel="nofollow sponsored">
    Apply Now
</a>
```

### Method 2: Use URL Parameters
```php
$card_slug = sanitize_title($card['name']);
$affiliate_link = "https://your-network.com/click/{$card_slug}";
```

---

## 🎨 Styling Options

### Custom CSS
Add to Appearance → Customize → Additional CSS:

```css
/* Change primary color */
:root {
    --primary: #2563eb;
}

/* Modify card hover */
.cardfair-card:hover {
    transform: translateY(-10px);
}

/* Custom CTA button */
.cardfair-apply-btn {
    background: linear-gradient(135deg, #f59e0b, #d97706);
}
```

---

## 📊 Available Shortcodes

### `[cardfair_compare]`
Compare specific cards side-by-side

**Parameters:**
- `cards=""` - Comma-separated card names (partial match)
- `limit="3"` - Number of cards to show
- `type=""` - Filter: secured, student, travel, cashback
- `features=""` - Features to show

**Examples:**
```
[cardfair_compare cards="Discover it,Capital One"]
[cardfair_compare type="secured" limit="5"]
[cardfair_compare cards="Amex Gold" features="annual_fee,rewards,apr"]
```

### `[cardfair_top_picks]`
Show top cards in a grid

**Parameters:**
- `type=""` - Card type filter
- `limit="5"` - Number of cards
- `sort="featured"` - Sort order

**Examples:**
```
[cardfair_top_picks type="secured" limit="10"]
[cardfair_top_picks type="student" limit="8"]
[cardfair_top_picks type="no-fee" limit="5"]
```

---

## 🔍 SEO Best Practices

### 1. Schema Markup Included
- Product schema for each card
- ItemList for rankings
- Review schema

### 2. Optimized Pages
- Use keyword-rich titles
- Include "2025" for freshness
- Add long-tail keywords in descriptions

### 3. Internal Linking
```
Link to comparison pages:
→ "Compare best secured cards"
→ "View student card rankings"
→ "See all no-annual-fee cards"
```

### 4. URL Structure
```
/secured-credit-cards/
/student-credit-cards/
/travel-credit-cards/
/best-cash-back-cards/
```

---

## 📈 Content Ideas

### Blog Posts to Support Comparison Pages
1. "How to Choose Between Secured Cards"
2. "Secured vs Student Cards: Which is Right?"
3. "Credit Building Timeline: What to Expect"
4. "5 Mistakes to Avoid with Secured Cards"

### Supporting Pages
- Credit Score Guide
- Application Tips
- Glossary of Terms
- FAQ pages

---

## ⚡ Performance Tips

1. **Cache Output**: Use WP Rocket or W3 Total Cache
2. **Lazy Load**: Defer card images
3. **Minify CSS/JS**: Use Autoptimize
4. **CDN**: Serve static files via CDN
5. **Database Queries**: Cache card data

---

## 🛠️ Troubleshooting

### Cards Not Showing
- Check JSON file path
- Verify JSON syntax
- Enable PHP error logging

### Styling Issues
- Clear browser cache
- Check for theme conflicts
- Test with default theme

### Shortcodes Not Working
- Verify plugin is activated
- Check for plugin conflicts
- Test with shortcode in code editor

---

## 📞 Support

For issues or customizations:
1. Check plugin documentation
2. Test on staging site first
3. Keep backups before updates

---

## ✅ Next Steps

1. **Install the plugin** → 5 min
2. **Add affiliate links** → 10 min
3. **Create comparison pages** → 20 min
4. **Add internal links** → 15 min
5. **Publish and monitor** → Ongoing

**Total Setup Time: ~50 minutes**

---

**Ready to launch?** Start with Option B (copy-paste HTML) for fastest deployment, then upgrade to plugin for long-term scalability.
