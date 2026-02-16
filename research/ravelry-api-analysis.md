# Ravelry API - Complete Analyse

**Datum:** 2026-02-15
**Doel:** Onderzoek naar scrapen van Nederlandstalige haak/breipatronen via Ravelry API

---

## Samenvatting

**✅ Ravelry API is beschikbaar maar vereist authentication**

- **Grootste database:** 200.000+ patronen
- **API toegang:** Ja, maar authentication vereist
- **Nederlandstalige patronen:** Beschikbaar via filters
- **Rate limits:** Zacht, maar respecteer limits
- **Kosten:** Gratis voor basis gebruik

---

## API Details

### 1. Authentication

**Type:** Basic Authentication (username/password)

```python
import requests
from requests.auth import HTTPBasicAuth

username = "your_ravelry_username"
password = "your_ravelry_password"  # Of personal access token

response = requests.get(
    "https://api.ravelry.com/patterns.json",
    auth=HTTPBasicAuth(username, password),
    params={'craft': 'crochet', 'availability': 'free'}
)
```

**Of via Personal Access Token:**
1. Ga naar Ravelry.com
2. Account settings → API access
3. Genereer een personal access token
4. Gebruik token als password

### 2. Belangrijke Endpoints

#### Pattern Search
```
GET https://api.ravelry.com/patterns.json
```

**Parameters:**
- `query` - Zoekterm (bijv. "dutch", "nederlands")
- `craft` - "knitting" of "crochet"
- `availability` - "free" (gratis patronen)
- `page` - Paginanummer
- `page_size` - Resultaten per pagina (max 200)
- `fit` - "adult", "child", "baby"
- `weight` - Garen dikte
- `language` - Taal filter

**Response:**
```json
{
  "patterns": [
    {
      "id": 12345,
      "name": "Pattern Name",
      "permalink": "https://www.ravelry.com/patterns/library/pattern-name",
      "designer": {
        "id": 678,
        "name": "Designer Name"
      },
      "pattern_sources": [
        {
          "pattern_url": "https://example.com/pattern",
          "name": "Source Name"
        }
      ],
      "free": true,
      "currency": "USD",
      "price": 0.00,
      "languages": ["dutch", "english"],
      "photos": [
        {
          "url": "https://images4.ravelry.com/..."
        }
      ]
    }
  ],
  "paginator": {
    "page": 1,
    "page_count": 50,
    "last_page": false
  }
}
```

#### Pattern Details
```
GET https://api.ravelry.com/patterns/{id}.json
```

**Voorbeeld:**
```
GET https://api.ravelry.com/patterns/12345.json
```

#### Designer Search
```
GET https://api.ravelry.com/designers/search.json
```

#### Yarn Search
```
GET https://api.ravelry.com/yarns/search.json
```

---

## Nederlandstalige Patronen Vinden

### Strategie 1: Taal Filter

```python
params = {
    'craft': 'crochet',
    'availability': 'free',
    'language': 'dutch',  # 🇳🇱 Nederlandstalig
    'page_size': 200
}
```

### Strategie 2: Zoektermen

```python
# Nederlandse zoekwoorden
queries = [
    "dutch",
    "nederlands",
    "haken",
    "breien",
    "gratishaken",
    "gratisbreien"
]

for query in queries:
    params = {
        'query': query,
        'craft': 'crochet',
        'availability': 'free',
        'page_size': 200
    }
```

### Strategie 3: Designer Location

```python
# Zoek Nederlandse designers
params = {
    'query': 'designer_location:netherlands',
    'craft': 'crochet',
    'availability': 'free'
}
```

---

## Rate Limits & Gebruiksvoorwaarden

### Rate Limits

- **Max requests:** ~100 requests/minuut (zacht)
- **Respecteer 429 responses:** Wacht en retry
- **User-Agent:** Identificeer jezelf

```python
headers = {
    'User-Agent': 'MyPatternBot/1.0 (contact@example.com)'
}
```

### Gebruiksvoorwaarden

**✅ Toegestaan:**
- Persoonlijk gebruik van data
- Research en analyse
- Apps voor Ravelry gebruikers

**⚠️ Beperkt:**
- Commercial gebruik (contacteer Ravelry)
- Bulk data export (geen complete database dump)
- Re-publishing van complete patronen

**❌ Niet toegestaan:**
- Data doorverkopen
- Concurrerende database bouwen
- Patronen kopiëren zonder toestemming

---

## Complete Scraping Script

### Setup

1. **Maak Ravelry account aan** (gratis)
   - URL: `https://www.ravelry.com/account/signup`

2. **Genereer Personal Access Token**
   - Settings → API Access → Create Token
   - Save token veilig!

3. **Python dependencies:**
```bash
pip install requests python-dotenv
```

### Script

```python
#!/usr/bin/env python3
"""
Ravelry Pattern Scraper - Nederlandstalige Patronen
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Ravelry credentials
RAVELRY_USERNAME = os.getenv('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.getenv('RAVELRY_PASSWORD')  # Personal access token

def fetch_dutch_patterns():
    """Haal Nederlandstalige haakpatronen op"""

    base_url = "https://api.ravelry.com"
    auth = (RAVELRY_USERNAME, RAVELRY_PASSWORD)

    # Zoekparameters
    params = {
        'craft': 'crochet',
        'availability': 'free',
        'language': 'dutch',
        'page_size': 200,
        'page': 1
    }

    all_patterns = []

    print("🧶 Ophalen van Nederlandstalige haakpatronen...\n")

    while True:
        try:
            print(f"Page {params['page']}...")

            response = requests.get(
                f"{base_url}/patterns.json",
                auth=auth,
                params=params,
                headers={'User-Agent': 'NLPatternBot/1.0'}
            )

            if response.status_code == 200:
                data = response.json()
                patterns = data.get('patterns', [])
                all_patterns.extend(patterns)

                print(f"  ✅ {len(patterns)} patterns found")

                # Check if last page
                paginator = data.get('paginator', {})
                if paginator.get('last_page', True):
                    break

                params['page'] += 1
                time.sleep(1)  # Rate limiting

            elif response.status_code == 429:
                print("  ⏸️  Rate limited, waiting...")
                time.sleep(5)
            else:
                print(f"  ❌ Error: {response.status_code}")
                break

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            break

    return all_patterns

def save_patterns(patterns):
    """Bewaar patronen naar JSON"""

    output_file = '/root/.openclaw/workspace/research/ravelry_dutch_patterns.json'

    with open(output_file, 'w') as f:
        json.dump(patterns, f, indent=2)

    print(f"\n💾 {len(patterns)} patterns saved to:")
    print(f"   {output_file}")

    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   Total patterns: {len(patterns)}")
    print(f"   Designers: {len(set(p.get('designer', {}).get('name') for p in patterns))}")

    # Pattern types
    categories = {}
    for p in patterns:
        cat = p.get('craft', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"   Categories: {categories}")

if __name__ == "__main__":
    if not RAVELRY_USERNAME or not RAVELRY_PASSWORD:
        print("❌ RAVELRY_USERNAME en RAVELRY_PASSWORD nodig!")
        print("   1. Maak account op ravelry.com")
        print("   2. Genereer personal access token")
        print("   3. Voeg toe aan .env bestand")
    else:
        patterns = fetch_dutch_patterns()
        save_patterns(patterns)
```

---

## Aan de Slag

### Stap 1: Account Aanmaken
1. Ga naar `https://www.ravelry.com/account/signup`
2. Maak gratis account aan
3. Verifieer email

### Stap 2: API Access
1. Login op Ravelry
2. Settings → Account → API Access
3. Genereer Personal Access Token
4. Kopieer token

### Stap 3: Script Configureren
```bash
# .env bestand aanmaken
RAVELRY_USERNAME=jouw_username
RAVELRY_PASSWORD=jouw_personal_access_token
```

### Stap 4: Script Draaien
```bash
python3 ravelry_scraper.py
```

---

## Verwachte Resultaten

**Aantal patronen:**
- Nederlandstalige haakpatronen: ~500-1,000+
- Nederlandstalige breipatronen: ~300-800+
- Totale gratis patronen: ~8,000-12,000+

**Data beschikbaar:**
- Pattern naam, ID, permalink
- Designer info
- Download URL (indien gratis)
- Afbeeldingen (meerdere per patroon)
- Garen dikte, naald/hook maat
- Rating, aantal favorieten
- Taal, description

**Kwaliteit:**
- ★★★★★ (uitstekend)
- Professionele database
- Actieve community
- Regelmatige updates

---

## Alternatieven

### 1. HTML Scraping
- Target: `https://www.ravelry.com/patterns/search`
- Moeilijker dan API
- Rate limiting strikter

### 2. R Package (ravelRy)
- Goed voor R gebruikers
- Vergelijkbare functionaliteit

### 3. Community Forums
- Ravelry forums hebben NL patterns
- Handmatig verzamelen

---

## Conclusie

**✅ Ravelry API is de beste optie voor:**
- Grootste patroon database
- NL taal filters
- Professionele API
- Gratis toegang

**⚠️ Vereist:**
- Ravelry account (gratis)
- Personal access token (gratis)
- Respect voor rate limits
- Persoonlijk gebruik (niet commercieel zonder toestemming)

**🎯 Strategie:**
1. Maak account aan
2. Test API met kleine queries
3. Bouw scraper met rate limiting
4. Begin met NL taal filter
5. Exporteer naar eigen database

---

**Volgende stap:**
Wil je dat ik:
1. Het scraping script schrijf?
2. Test met jouw Ravelry credentials?
3. Data analyse plan maak?

*Analyse: 2026-02-15*
*Bron: Ravelry API + Community research*
