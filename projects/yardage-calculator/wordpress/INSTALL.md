# Yardage Calculator - WordPress Installatiegids

Twee manieren om de calculator aan je WordPress site toe te voegen:

---

## OPTIE 1: Page Template (Aanbevolen)

**Fullscreen pagina, schoonste resultaat**

### Installatie:

1. **Upload template:**
   ```bash
   # Upload naar je theme:
   wp-content/themes/your-theme/yardage-calculator-template.php
   ```

2. **Maak nieuwe page in WordPress:**
   - Ga naar: Pages → Add New
   - Titel: "Yardage Calculator"
   - Right sidebar → Page Attributes → Template: "Yardage Calculator"
   - Publish

3. **Done!** Calculator nu live op: `yoursite.com/yardage-calculator`

### Voordelen:
- ✅ Fullscreen, geen sidebar/header conflicts
- ✅ Eigen URL (goed voor SEO)
- ✅ Schoonste design
- ✅ Werkt met elk theme

---

## OPTIE 2: Shortcode (Flexibelst)

**Embed in elke page/post**

### Installatie:

1. **Upload plugin folder:**
   ```bash
   # Maak plugin folder:
   wp-content/plugins/yardage-calculator/
   
   # Upload files:
   - yardage-calculator-shortcode.php
   - style.css
   - script.js
   ```

2. **Activeer plugin:**
   - WordPress Admin → Plugins
   - Vind: "Yardage Calculator Shortcode"
   - Activate

3. **Gebruik shortcode:**
   ```
   [yardage_calculator]
   ```

### Voorbeelden:

**In een page:**
```
---
Title: Garen Calculator

Welkom bij onze gratis yardage calculator! 

[yardage_calculator]

Heb je vragen? Contact ons!
---
```

**In een blog post:**
```
---
Title: Hoeveel garn heb je nodig voor een sjaal?

... je artikel content ...

[yardage_calculator]

... meer content ...
---
```

**In sidebar widget:**
- Appearance → Widgets
- Text widget → `[yardage_calculator]`

### Voordelen:
- ✅ Overal embedden
- ✅ Makkelijk te verplaatsen
- ✅ Meerdere keren gebruiken
- ✅ Widget support

---

## Aanpassingen

### Kleuren aanpassen (Page Template):

Edit `yardage-calculator-template.php`:

```php
/* Verander gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* naar */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Teksten aanpassen (Shortcode):

Edit `yardage-calculator-shortcode.php`:

```php
<option value="scarf">Sjaal</option>
/* naar */
<option value="scarf">Scarf</option>  // Engels
```

### Extra project types toevoegen:

Voeg toe aan beide files:

```php
<option value="vest">Vest</option>
```

```javascript
presets: {
    vest: { width: 55, length: 60, stitches: 18, rows: 24 },
    // ...
}
```

---

## Performance

 beide opties zijn:
- ✅ 100% client-side (geen server load)
- ✅ Geen database queries
- ✅ Geen external dependencies
- ✅ < 50KB total (CSS + JS)
- ✅ Mobile responsive

---

## SEO Tips (Page Template)

```
Title: Yardage Calculator - Bereken je Garen
Meta Description: Gratis calculator om te berekenen hoeveel garn je nodig hebt voor je brei- en haakprojecten. Perfect voor sjaal, trui, deken en meer.

Focus Keyword: yardage calculator
URL: /yardage-calculator
```

---

## Troubleshooting

**Calculator verschijnt niet:**
- Check of template in juiste folder staat
- Clear cache (WP Rocket, W3 Total Cache, etc.)
- Check browser console voor errors

**Styling lijkt kapot:**
- Theme conflict → probeer shortcode optie
- Check CSS priority in browser DevTools

**JavaScript werkt niet:**
- Check console voor errors
- Verifieër dat script.js geladen wordt
- Clear browser + server cache

---

## Updates

Komende features (gratis):
- [ ] Print-friendly versie
- [ ] Project opslaan (localStorage)
- [ ] Imperial units (inches) optie
- [ ] Meertalig (NL/EN/DE/FR)

---

**Vragen?** Mail peter@yourdomain.com

**Gemaakt met ❤️ voor hobby crafters**
