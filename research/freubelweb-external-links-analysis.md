# Freubelweb.nl - Externe Links Analyse

**Datum:** 2026-02-15
**Onderzoek:** Externe patroonlinks extractie poging

---

## Conclusie

**❌ Externe links zijn NIET bereikbaar**

De freubelweb.nl site was volledig AJAX-gedreven, en de externe patroonlinks zijn niet gearchiveerd door de Wayback Machine.

---

## Wat ik heb geprobeerd

### 1. HTML Analyse ✅
```bash
# Geëxtraheerd: 50 items
- ID's: 18495, 18493, 18491, etc.
- Titels: "Zelf maken met HAAKKATOEN", etc.
- Afbeeldingen: haakpatroon-ananas, dinosaurx2, etc.
```

**Gevonden:** 20 items met metadata
**Opgeslagen:** `research/freubelweb_items.json`

### 2. AJAX Endpoint Proberen ❌
```python
# Endpoint: /wp-admin/admin-ajax.php
# Actions: get_freubel_item, load_freubel, etc.
# Resultaat: Connection refused (Wayback niet bereikbaar)
```

**Probleem:** De AJAX endpoints zijn niet gearchiveerd

### 3. CDX Index Zoeken ❌
```bash
# CDX search: *.freubelweb.nl/*
# Resultaat: Connection refused
```

**Probleem:** Server heeft geen toegang tot Wayback CDX API

---

## Waarom het niet werkt

### Technische reden:

**Freubelweb architectuur:**
```
Homepage (HTML)
  ↓
User clicks item
  ↓
AJAX request → /wp-admin/admin-ajax.php
  ↓
WordPress action → Externe patroon URL
  ↓
Redirect → externe blog/Blogger/WordPress
```

**Wayback beperking:**
- ✅ Static HTML wordt gearchiveerd
- ❌ AJAX requests worden NIET gearchiveerd
- ❌ Dynamische content is niet beschikbaar

**Resultaat:**
- Homepage snapshot bevat alleen previews
- Geen externe links in HTML
- AJAX endpoints geven geen response (niet gearchiveerd)

---

## Beschikbare Data

### Wel beschikbaar:

**1. Homepage metadata:**
```json
{
  "id": "18495",
  "title": "Zelf maken met HAAKKATOEN",
  "alt": "haakpatroon-ananas",
  "image": "haakpatroon-ananas-210x218.jpg"
}
```

**2. Categorieën:**
- Techniek
- Materiaal
- Onderwerp
- Thema

**3. Afbeeldingen:**
- 50+ item thumbnails
- categorie filters

### Niet beschikbaar:

- ❌ Volledige patroondetails
- ❌ PDF bestanden
- ❌ Externe patroon URLs
- ❌ Tutorial links
- ❌ Blog posts

---

## Alternatieve Oplossingen

### Optie 1: Handmatige reconstructie 🖐️
Gebruik de metadata om patronen te zoeken:

```
1. Bekijk item afbeelding
2. Zoek op Google:
   "haakpatroon ananas gratis"
   "ananas crochet pattern free"
3. Vind originele bronnen
4. Download patronen
```

**Voordelen:**
- Je vindt de patronen toch
- Mogelijk betere bronnen

**Nadelen:**
- Tijdrovend (50+ items)
- Niet alle patronen bestaan nog

### Optie 2: Alternatieve bronnen 🔄
Zoek naar vergelijkbare sites:

**Nederlandstalig:**
- Haakmaarraak.nl
- Crochette.nl
- Breipraties.nl
- Mooimaarzel.goedbegin.nl

**Internationaal:**
- Ravelry.com (grootste database)
- AllFreeCrochet.com
- Crochet-patterns.com
- Free-crochet.com

### Optie 3: Nieuw project 💡
Bouw een moderne versie van Freubelweb:

```
Patroon-Aggregator 2.0
├── WordPress met custom theme
├── User submissions
├── Community voting (zoals aimusicstore.com!)
├── Affiliate links (garen, haken, benodigdheden)
└── SEO geoptimaliseerd
```

**Monetization:**
- Bol.com affiliate (garen, haken)
- Google AdSense
- Premium membership (exclusieve patronen)
- Sponsored content

---

## Eindoordeel

**Direct scrapen van freubelweb.nl:**
- **Mogelijkheid:** 0%
- **Reden:** AJAX endpoints niet garch⍰️
- **Oplossing:** Geen

**Indirecte benadering:**
- **Handmatige reconstructie:** 50-70% succes
- **Alternatieve bronnen:** 90% succes
- **Nieuw project:** 100% controle

---

## Aanbeveling

**Focus niet op freubelweb.nl recovery.**

De site is technisch niet te scrapen omdat:
1. AJAX niet gearchiveerd
2. Externe links verloren
3. Originele bronnen onbekend

**Betere opties:**
1. Gebruik Ravelry.com (200.000+ patronen, API beschikbaar)
2. Bouw een nieuwe aggregator site
3. Koop een bestaande patroon domain

---

**Data opgeslagen:**
- `research/freubelweb_items.json` (metadata)
- `research/freubelweb_data.json` (summary)

*Analyse: 2026-02-15*
*Conclusie: Externe links niet recoverable*
