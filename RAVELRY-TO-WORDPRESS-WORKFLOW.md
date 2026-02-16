# Ravelry → WordPress Publishing Workflow

**Volledige automatisering:** Ravelry API importeren → WordPress aanmaken → Kwaliteitscheck → Publiceren

---

## **Overzicht**

Deze workflow combineert:
1. **Ravelry JSON data** (200+ Nederlandse patronen)
2. **WordPress REST API** (automatisch posts aanmaken)
3. **Pinch-to-Post** (kwaliteitscheck en publiceren)

**Resultaat:** Geïmporteerde patronen op je WordPress site met foto's, meta data, en kwaliteit gegarandeerd.

---

## **Snelste Start**

### **Optie A: Importeer + Bekijk (Geen auto-publish)**

```bash
/root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh crashcasino 20 false
```

**Wat het doet:**
- Importeert 20 Ravelry patronen
- Maakt WordPress posts aan (status: draft)
- Download foto's als featured images
- Kwaliteitscheck op alle posts
- Toont publish ready lijst

**Tijd:** ~2-3 minuten

---

### **Optie B: Importeer + Publish Alles**

```bash
/root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh crashcasino 20 true
```

**Wat het doet:**
- Importeert 20 Ravelry patronen
- Publiceert automatisch alle posts met score 80+
- Toont publicatie kalender

**Tijd:** ~3-4 minuten

---

## **Stap voor Stap**

### **Stap 1: Importeer Ravelry Patronen**

```bash
/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh <site> <post_type> <limit>
```

**Parameters:**
- `site` - crashcasino, crashgame, freecrash, cryptocrash
- `post_type` - post (default) of custom post type
- `limit` - Aantal patronen (1-200)

**Voorbeeld:**
```bash
# Importeer 50 patronen naar crashcasino
/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh crashcasino post 50
```

**Resultaat:**
- 50 WordPress posts (status: draft)
- Foto's gedownload en als featured image
- Meta data: designer, gratis/betaald, ravelry_id

---

### **Stap 2: Bekijk Geïmporteerde Posts**

```bash
# Via WordPress Admin
https://jousite.com/wp-admin/edit.php?post_status=draft&meta_key=ravelry_id

# Via WP-CLI
wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --fields=ID,post_title
```

---

### **Stap 3: Kwaliteitscheck**

```bash
# Check alle geïmporteerde posts
for id in $(wp post list --post_type=post --post_status=draft --meta_key=ravelry_id --field=ID); do
  /root/.openclaw/workspace/scripts/pinch-to-post.sh health-check crashcasino $id
done
```

**Quality Criteria (80+ score):**
- ✅ Minimaal 300 woorden
- ✅ Meta description
- ✅ Focus keyword
- ✅ Featured image
- ✅ H2 headings

---

### **Stap 4: Publiceer**

**Manier A: Individueel**
```bash
pinch-to-post publish crashcasino 123
```

**Manier B: Bulk (Pinch-to-Post)**
```bash
# Publish range
pinch-to-post bulk-publish crashcasino 100-150

# Publish specific IDs
pinch-to-post bulk-publish crashcasino 123 456 789
```

**Manier C: Workflow Auto-Publish**
```bash
# Importeer + publish alles met 80+ score
/root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh crashcasino 50 true
```

---

## **Features Per Post**

Elke geïmporteerd post heeft:

### **Content**
- ✅ Titel (met "Gratis: " prefix indien gratis)
- ✅ Designer naam
- ✅ Gratis/Betaald badge
- ✅ Link naar Ravelry
- ✅ Stash Calculator embed (indien geïnstalleerd)

### **Meta Data**
- ✅ `ravelry_id` - Uniek Ravelry ID
- ✅ `ravelry_designer` - Designer naam
- ✅ `ravelry_free` - true/false
- ✅ `ravelry_permalink` - Ravelry URL slug

### **Images**
- ✅ Featured image (van Ravelry)
- ✅ Alt text (patroon naam)
- ✅ Caption (indien beschikbaar)

---

## **Voorbeeld Post**

```html
<!-- Title -->
Gratis: Dutch Cap

<!-- Content -->
<p><strong>✅ Gratis patroon!</strong></p>

<h3>Details</h3>
<ul>
<li><strong>Designer:</strong> Thread Mills</li>
<li><strong>Type:</strong> Breien/Haken</li>
</ul>

<h3>Bekijk Patroon</h3>
<p><a href="https://www.ravelry.com/patterns/library/dutch-cap" target="_blank" rel="nofollow">
Bekijk dit patroon op Ravelry →</a></p>

<h3>Bereken Garen</h3>
<p>Gebruik onze <a href="/stash-calculator/">Stash Calculator</a> om te zien wat je met je garen kunt maken!</p>

<!-- Featured Image -->
<img src="/uploads/dutch-cap.jpg" alt="Gratis: Dutch Cap">
```

---

## **Advanced Features**

### **Custom Post Type**

Maak een custom post type voor patronen:

```php
// In functions.php
register_post_type('ravelry_pattern', [
  'label' => 'Ravelry Patronen',
  'public' => true,
  'has_archive' => true,
  'supports' => ['title', 'editor', 'thumbnail'],
  'rewrite' => ['slug' => 'patronen'],
]);
```

Importeer naar CPT:
```bash
/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh crashcasino ravelry_pattern 50
```

### **Categorieën Auto-Toewijzen**

Pas import script aan om categories toe te wijzen:

```bash
# In ravelry-to-wordpress-import.sh
POST_CATEGORY="breien"  # of haken, gratis, etc.
```

### **Scheduled Publishing**

Publiceer op specifieke tijden:

```bash
# Importeer als draft met scheduled date
# In ravelry-to-wordpress-import.sh:
DATE_SCHEDULED=$(date -d "+2 days" +%Y-%m-%dT%H:%M:%S)
# Add to JSON: "date": "${DATE_SCHEDULED}"
```

---

## **SEO Optimalisatie**

### **Zoektermen**
- "Gratis haakpatronen"
- "Nederlandse breipatronen"
- "Gratis breipatronen"
- "Ravelry patronen NL"

### **Meta Description Template**

Pas aan in `ravelry-to-wordpress-import.sh`:

```bash
if [[ "${IS_FREE}" == "true" ]]; then
  META_DESC="Gratis ${PATTERN_NAME} patroon door ${DESIGNER}. Download nu op Ravelry. Inclusief materialenlijst en instructies."
else
  META_DESC="${PATTERN_NAME} patroon door ${DESIGNER}. Beschikbaar op Ravelry."
fi
```

### **Focus Keywords**

Voeg automatisch toe:
- Gratis haakpatroon
- Nederlandse breipatronen
- Designer naam

---

## **Update Existing Posts**

```bash
# Re-import to update existing patterns
/root/.openclaw/workspace/scripts/ravelry-to-wordpress-import.sh crashcasino post 200
```

Script detecteert bestaande posts via `ravelry_id` en update ze.

---

## **Volledige Automatisering (Cron)**

### **Elke dag 10 nieuwe patronen:**

```bash
# Add to crontab
0 9 * * * /root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh crashcasino 10 true >> /root/.openclaw/workspace/logs/ravelry-daily.log 2>&1
```

### **Elke week alle nieuwe patronen:**

```bash
# Add to crontab
0 10 * * 1 /root/.openclaw/workspace/scripts/workflows/ravelry-publish-workflow.sh crashcasino 50 true >> /root/.openclaw/workspace/logs/ravelry-weekly.log 2>&1
```

---

## **Troubleshooting**

### **Import mislukt**

**Check:** JSON bestand bestaat
```bash
ls -lh /root/.openclaw/workspace/research/ravelry_dutch_patterns.json
```

**Check:** WordPress credentials
```bash
cat ~/.openclaw/workspace/.env | grep WP_SITE
```

**Check:** Site is bereikbaar
```bash
curl -I https://crashcasino.io
```

### **Foto's uploaden niet**

**Check:** PHP upload limits
```bash
# In wp-admin
Media → Add New → Upload limit
```

**Check:** Schijfruimte
```bash
df -h /root/.openclaw
```

### **Quality check faalt**

**Oplossing:** Voeg meer content toe

```bash
# Edit post via WordPress admin
# Of via WP-CLI
wp post update 123 --post_content="Meer content hier..."
```

---

## **Statistics & Reporting**

### **Bekijk statistieken**

```bash
# Total geïmporteerde patronen
wp post list --post_type=post --meta_key=ravelry_id --format=count

# Gratis patronen
wp post list --post_type=post --meta_key=ravelry_free --meta_value=true --format=count

# Per designer
wp post list --post_type=post --meta_key=ravelry_designer --meta_value="Thread Mills" --format=count
```

---

## **Volgende Stappen**

### **Vandaag:**
1. ✅ Test import met 10 patronen
2. ✅ Bekijk posts in WordPress admin
3. ✅ Publiceer er 2-3 om te testen

### **Deze week:**
1. ✅ Importeer alle 200+ patronen
2. ✅ Publiceer 5-10 per dag
3. ✅ Voeg affiliate links toe (Ravelry, LoveCrafts)

### **Volgende maand:**
1. ⏳ Update patronen (nieuwe uit Ravelry API)
2. ⏳ Voeg reviews toe
3. ⏳ Gebruiker uploads (mijn garen projecten)

---

## **Integratie met Calculators**

Patronen linken automatisch naar calculators:

```html
<!-- In ravelry-to-wordpress-import.sh -->
POST_CONTENT="${POST_CONTENT}
<h3>Tools</h3>
<ul>
<li><a href=\"/yardage-calculator/\">Yardage Calculator</a> - Hoeveel garn nodig?</li>
<li><a href=\"/stash-calculator/\">Stash Calculator</a> - Wat kan ik maken?</li>
<li><a href=\"/cost-calculator/\">Cost Calculator</a> - Hoeveel kost het?</li>
</ul>
"
```

---

## **Support**

**Vragen?**
- Check: `/root/.openclaw/workspace/logs/ravelry-*.log`
- Test: `/root/.openclaw/workspace/scripts/test-pinch-to-post.sh`
- Email: peter@joudomein.com

**Klaar voor gebruik!** 🚀

---
*Laatst bijgewwerkt: 2026-02-16*
*Versie: 1.0.0*
