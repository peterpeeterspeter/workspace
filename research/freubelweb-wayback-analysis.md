# Freubelweb.nl - Wayback Machine Analyse

**Datum:** 2026-02-15
**Onderwerp:** Historische analyse van freubelweb.nl (haak- en breipatronen)

---

## Samenvatting

**Status:** ⚠️ Beperkte data beschikbaar

De site freubelweb.nl was een **patroon-aggregator** voor gratis haak- en breipatronen, maar de meeste content is niet gearchiveerd door de Wayback Machine.

---

## Wat is gevonden

### Site Profiel (2015)

| Eigenschap | Waarde |
|------------|--------|
| **Platform** | WordPress |
| **Type** | Patroon aggregator / community |
| **Content** | 2000+ patronen (volgens homepage) |
| **Categorieën** | Techniek, Materiaal, Onderwerp, Thema |
| **Social Media** | Twitter, Facebook, Instagram, Pinterest |
| **Laatste snapshot** | 7 september 2015 |

### Voorbeeld Items (van homepage)

**Titels van items op de homepage:**
- Zelf maken met HAAKKATOEN
- Zelf maken met BORDUURGAREN
- Zelf maken met VILT en LINTJES
- Zelf maken met HAAKGAREN
- Zelf maken met BREIGAREN
- Zelf maken met KRALEN
- Zelf maken met TEXTIELGAREN

**Afbeeldingen:**
- haakpatroon-ananas-210x218.jpg
- dinosaurx2-210x135.jpeg
- Coussin fleuri (borduren)
- Amigurumi patronen

---

## Problemen met scraping

### 1. **AJAX-gedreven content**
De site laadde patronen via AJAX calls zonder unieke URL's per patroon. Hierdoor zijn:
- ❌ Geen individuele patroonpagina's
- ❌ Geen directe downloadlinks
- ❌ Geen PDF-bestanden gearchiveerd

### 2. **Externe links**
Patronen waren waarschijnlijk doorverwijzingen naar externe blogs (bijv. Blogger, WordPress.com), maar:
- ❌ Externe links zijn niet gearchiveerd
- ❌ Detailpagina's laden niet via Wayback

### 3. **Beperkte snapshots**
- Alleen homepage snapshot beschikbaar (sep 2015)
- Blogsectie is niet gearchiveerd
- Categoriepagina's zijn niet gearchiveerd

---

## Wat is WEL beschikbaar

### Via Wayback Machine:
```
http://web.archive.org/web/20150907051323/http://www.freubelweb.nl/
```

**Beschikbaar:**
- ✅ Homepage met 50 items (preview)
- ✅ Afbeeldingen van patronen
- ✅ Categorieën en filters
- ✅ Site structuur

**Niet beschikbaar:**
- ❌ Volledige patroondetails
- ❌ PDF downloads
- ❌ Externe patroonlinks
- ❌ Blogposts met instructies

### Data die ik heb geëxporteerd:

**Bestand:** `research/freubelweb_data.json`

```json
{
  "total_items": 50,
  "titles": [
    "Zelf maken met VILT en LINTJES",
    "Zelf maken met HAAKGAREN",
    "Zelf maken met BREIGAREN",
    ...
  ],
  "categories": {
    "techniek": "Techniek",
    "materiaal": "Materiaal",
    "onderwerp": "Onderwerp",
    "thema": "Thema"
  }
}
```

---

## Mogelijke vervolgstappen

### Optie 1: Handmatige extractie
- Bekijk de Wayback snapshot handmatig
- Noteer interessante patronen
- Zoek naar externe bronnen via Google

### Optie 2: Alternatieve bronnen
Zoek naar vergelijkbare sites DIE wel volledig gearchiveerd zijn:

**Gratis haak/breipatroon sites:**
- Ravelry.com (grote database)
- Crochet-patterns.com
- Free-crochet.com
- AllFreeCrochet.com
- Dutch sites: haakmaarraak.nl, crochette.nl

### Optie 3: Contact opnemen
- Zoek naar de originele eigenaar
- Vraag of de content nog ergens anders beschikbaar is
- Check social media accounts (Twitter: @freubelweb)

### Optie 4: Nieuw project starten
Gebruik de kennis van Freubelweb om een **nieuwe patroon-site** te bouwen:
- WordPress met custom theme
- User-submitted patronen
- Community features
- Affiliate monetization (garen, benodigdheden)

---

## Conclusie

**Direct scrapen van freubelweb.nl is NIET mogelijk** omdat:
1. Content werd via AJAX geladen (niet gearchiveerd)
2. Patronen waren externe links (niet gearchiveerd)
3. Site is offline sinds 2015

**Wat WEL kan:**
- Handmatig browsen van Wayback snapshot voor inspiratie
- Data analyseren voor marktonderzoek
- Alternatieve patroonbronnen vinden
- Nieuwe soortgelijke site bouwen

---

**Aanbeveling:** Focus op alternatieve bronnen of start een nieuw project gebaseerd op het Freubelweb concept.

*Analyse: 2026-02-15*
*Tools: Wayback Machine, Browser Automation, Python scraping*
