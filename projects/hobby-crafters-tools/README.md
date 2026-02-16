# Hobby Crafters Tools - Volledige Set

3 gratis calculators voor breien, haken, naaien en andere handwerkprojecten.

---

## 🎯 De Tools

### 1. Yardage Calculator
**Wat:** Bereken hoeveel garen je nodig hebt voor je project
**Input:** Project type, afmetingen, garen dikte, gauge
**Output:** Benodigde meters, yards, aantal ballen

### 2. Stash Calculator ⭐
**Wat:** Ontdek wat je met je huidige stash kunt maken
**Input:** Aantal ballen, gewicht per bal, garen dikte
**Output:** Lijst met mogelijke projecten (muts, sjaal, deken, etc.)

### 3. Cost Calculator
**Wat:** Bereken de echte kosten van je project
**Input:** Materialen (garn, naalden, accessoires) + tijd + uurloon
**Output:** Totale kosten, uurloon, ROI vs. winkel

---

## 📦 Bestanden Per Tool

Elke tool is een **standalone HTML file** (geen dependencies):

```
yardage-calculator/
├── index.html (15KB)

stash-calculator/
├── index.html (16KB)

cost-calculator/
├── index.html (18KB)
```

**Features:**
- ✅ 100% client-side (geen server nodig)
- ✅ Mobile responsive
- ✅ Tailwind CSS + Font Awesome (via CDN)
- ✅ Direct te gebruiken in browser
- ✅ Embed in WordPress, Shopify, elke website

---

## 🚀 Installatie Opties

### Optie A: Direct Openen
```bash
# Open file in browser
open stash-calculator/index.html
# of
python3 -m http.server 8080
# Ga naar http://localhost:8080
```

### Optie B: WordPress Shortcode

**Stap 1: Upload files**
- Ga naar: wp-content/uploads/
- Maak folder: `calculators/`
- Upload alle 3 files

**Stap 2: Maak custom shortcode plugin**
```php
// In functions.php of custom plugin:
function hobby_calculators_shortcode($atts) {
    $tool = $atts['tool'] ?? 'yardage';
    $url = get_site_url() . "/wp-content/uploads/calculators/{$tool}-calculator/index.html";
    
    return '<iframe src="' . $url . '" 
            style="width:100%;height:800px;border:none;"
            scrolling="yes"></iframe>';
}
add_shortcode('hobby_calculator', 'hobby_calculators_shortcode');
```

**Stap 3: Gebruik in elke page/post**
```
[hobby_calculator tool="stash"]
[hobby_calculator tool="cost"]
[hobby_calculator tool="yardage"]
```

### Optie C: Losse Pagina's (WordPress)

1. Nieuwe page aanmaken
2. Add custom HTML block
3. Embed met iframe:

```html
<iframe 
    src="/wp-content/uploads/calculators/stash-calculator/index.html"
    style="width:100%;height:900px;border:none;"
    scrolling="yes">
</iframe>
```

### Optie D: Externe Hosting

**Vercel/Netlify (gratis):**
1. Sleep folder naar Vercel
2. Deploy in 30 seconden
3. Custom domein: `stash.jouwdomein.com`

**GitHub Pages:**
1. Push to GitHub repo
2. Settings → Pages
3. Deploy from main branch

---

## 🎨 Customization

### Kleuren Aanpassen

Alle tools gebruiken Tailwind CSS. Verander de gradient:

```javascript
// Stash Calculator (roze/paars)
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

// Cost Calculator (paars/indigo)
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

// Yardage Calculator (roze/paars)
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Projecten Toevoegen (Stash Calculator)

Voeg toe aan `projects` array:

```javascript
{
    name: "Naam",
    category: "Categorie",
    minMeters: 100,
    maxMeters: 200,
    icon: "fa-icon-naam",
    level: "Beginner"
}
```

---

## 💰 Monetization Tips

### Affiliate Links

**Stash Calculator:**
- "Nog wat garn nodig?" → LoveCrafts affiliate
- "Bekek patronen" → Ravelry affiliate

**Cost Calculator:**
- "Shop goedkoper garn" → LoveCrafts, Yarnsub
- "Naalden/accessoires" → Amazon affiliate

**Yardage Calculator:**
- "Garn nodig" → Brand affiliates (Stylecraft, Drops, etc.)

### Premium Features (Toekomst)

**Pro Version (€5/mo):**
- Projecten opslaan (localStorage → cloud)
- Stash inventory management
- Cost tracking over tijd
- PDF export

**Database:**
- Meer dan 10 projecten tegelijk
- Custom projecten toevoegen
- Garen database (brand reviews, substitutie)

---

## 📊 SEO Potential

**Keywords:**
- "yarn stash calculator" (1k searches/maand)
- "knitting project calculator" (500 searches)
- "how much yarn do i need" (2k searches)
- "knitting cost calculator" (200 searches)

**Meta Tags:**
```html
<title>Stash Calculator - Wat kun je maken? | JouwDomein</title>
<meta name="description" content="Bereken direct wat je met je garen stash kunt maken. Gratis tool voor breien, haken en handwerkprojecten.">
```

---

## 🔄 Updates Coming

**V1.1 (This Week):**
- [ ] Print-friendly versie
- [ ] Project opslaan (localStorage)
- [ ] Shareable results (permalink)

**V1.2 (Next Month):**
- [ ] Imperial units (inches/yards)
- [ ] Meertalig (EN/NL/DE/FR)
- [ ] Dark mode

**V2.0 (Future):**
- [ ] User accounts
- [ ] Stash inventory management
- [ ] Pattern library integration
- [ ] Mobile app

---

## 🐛 Known Issues

- Mobile menu: Niet geïmplementeerd (nog niet nodig)
- Loading states: Zou skeleton screens kunnen gebruiken
- A/B testing: Kan worden toegevoegd met Google Optimize

---

## 📞 Support

**Vragen?** Mail peter@joudomein.com

**Bug gevonden?** Open issue op GitHub

**Feature request?** Laat het weten!

---

## 📄 License

Free to use for personal and commercial projects.

**Attribution appreciated but not required:**
"Gemaakt met JouwDomein Tools"

---

**Gemaakt met ❤️ voor hobby crafters**

*Meer gratis tools: jouwdomein.com/tools*
