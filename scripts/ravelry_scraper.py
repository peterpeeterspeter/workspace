#!/usr/bin/env python3
"""
Ravelry Pattern Scraper - Nederlandstalige Haak/Breipatronen

Gebruik:
1. Maak Ravelry account aan: https://www.ravelry.com/account/signup
2. Genereer Personal Access Token: Settings → API Access
3. Maak .env bestand met credentials
4. Run script: python3 ravelry_scraper.py

Output: research/ravelry_dutch_patterns.json
"""

import requests
import json
import time
import os
from typing import List, Dict
import sys

# ============================================================
# CONFIGURATIE
# ============================================================

# Ravelry credentials (zet in .env bestand!)
RAVELRY_USERNAME = os.getenv('RAVELRY_USERNAME', '')
RAVELRY_PASSWORD = os.getenv('RAVELRY_PASSWORD', '')  # Personal access token

# Zoek parameters
CRAFT = 'crochet'  # 'crochet' of 'knitting'
AVAILABILITY = 'free'  # 'free' voor gratis patronen
LANGUAGE = 'dutch'  # 'dutch' voor Nederlandstalig
PAGE_SIZE = 200  # Max 200 per pagina

# Rate limiting
REQUEST_DELAY = 1.0  # Seconde tussen requests
MAX_PAGES = 100  # Max pages om op te halen

# ============================================================
# FUNCTIONS
# ============================================================

class RavelryScraper:
    """Ravelry API Scraper"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://api.ravelry.com"
        self.auth = (username, password)
        self.all_patterns = []

    def search_patterns(self, query: str = None, page: int = 1) -> Dict:
        """Zoek patronen via Ravelry API"""

        params = {
            'craft': CRAFT,
            'availability': AVAILABILITY,
            'page_size': PAGE_SIZE,
            'page': page
        }

        # Note: language parameter causes 500 error - use query search instead
        if query:
            params['query'] = query

        try:
            # Use /patterns/search.json endpoint for search
            response = requests.get(
                f"{self.base_url}/patterns/search.json",
                auth=self.auth,
                params=params,
                headers={
                    'User-Agent': 'NLPatternScraper/1.0 (educational/research)'
                },
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ Authentication failed - check credentials")
                return None
            elif response.status_code == 429:
                print("⏸️  Rate limited - waiting 5 seconds...")
                time.sleep(5)
                return self.search_patterns(query, page)
            else:
                print(f"❌ Error {response.status_code}: {response.text[:100]}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None

    def fetch_all_dutch_patterns(self) -> List[Dict]:
        """Haal alle Nederlandstalige patronen op"""

        print(f"\n🧶 Ravelry Pattern Scraper")
        print(f"   Craft: {CRAFT}")
        print(f"   Availability: {AVAILABILITY}")
        print(f"   Language: {LANGUAGE}")
        print(f"   Page size: {PAGE_SIZE}\n")

        page = 1
        total_fetched = 0

        while page <= MAX_PAGES:
            print(f"📄 Page {page}...", end=" ")

            data = self.search_patterns(page=page)

            if not data:
                break

            patterns = data.get('patterns', [])
            if not patterns:
                print("No patterns found")
                break

            self.all_patterns.extend(patterns)
            total_fetched += len(patterns)

            print(f"✅ {len(patterns)} patterns (total: {total_fetched})")

            # Check pagination
            paginator = data.get('paginator', {})
            if paginator.get('last_page', False):
                print(f"\n✅ Last page reached")
                break

            if paginator.get('page', 1) >= paginator.get('page_count', 1):
                print(f"\n✅ All pages fetched")
                break

            page += 1
            time.sleep(REQUEST_DELAY)

        return self.all_patterns

    def save_patterns(self, output_file: str = None):
        """Bewaar patronen naar JSON"""

        if not output_file:
            output_file = '/root/.openclaw/workspace/research/ravelry_dutch_patterns.json'

        # Create output directory
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save to file
        with open(output_file, 'w') as f:
            json.dump(self.all_patterns, f, indent=2)

        return output_file

    def print_summary(self):
        """Print summary van opgehaalde data"""

        if not self.all_patterns:
            print("\n❌ No patterns fetched")
            return

        print(f"\n{'='*60}")
        print(f"📊 SUMMARY")
        print(f"{'='*60}")
        print(f"Total patterns: {len(self.all_patterns)}")

        # Unique designers
        designers = set()
        for p in self.all_patterns:
            designer = p.get('designer', {}).get('name', 'Unknown')
            designers.add(designer)

        print(f"Unique designers: {len(designers)}")

        # Pattern sources
        sources = set()
        for p in self.all_patterns:
            for source in p.get('pattern_sources', []):
                url = source.get('pattern_url', '')
                if url:
                    sources.add(url)

        print(f"Unique sources: {len(sources)}")

        # Languages
        languages = set()
        for p in self.all_patterns:
            for lang in p.get('languages', []):
                languages.add(lang)

        print(f"Languages: {', '.join(sorted(languages))}")

        # Sample patterns
        print(f"\n🧶 Sample patterns:")
        for p in self.all_patterns[:5]:
            print(f"  • {p.get('name', 'N/A')}")
            designer = p.get('designer', {}).get('name', 'Unknown')
            print(f"    Designer: {designer}")

            # First source URL
            if p.get('pattern_sources'):
                source = p['pattern_sources'][0]
                url = source.get('pattern_url', 'N/A')
                print(f"    URL: {url[:80]}...")

        print(f"{'='*60}\n")

# ============================================================
# MAIN
# ============================================================

def check_credentials():
    """Check of credentials aanwezig zijn"""

    if not RAVELRY_USERNAME or not RAVELRY_PASSWORD:
        print("❌ Ravelry credentials niet gevonden!")
        print("\n📝 STAPPEN:")
        print("   1. Maak account: https://www.ravelry.com/account/signup")
        print("   2. Genereer Personal Access Token:")
        print("      - Login op Ravelry")
        print("      - Settings → Account → API Access")
        print("      - Click 'Create a personal access token'")
        print("   3. Maak .env bestand:")
        print("      RAVELRY_USERNAME=jouw_username")
        print("      RAVELRY_PASSWORD=jouw_personal_access_token")
        print("   4. Run script opnieuw\n")
        return False

    return True

def main():
    """Main function"""

    print("\n" + "="*60)
    print("  RAVELRY PATTERN SCRAPER")
    print("  Nederlandstalige Haak/Breipatronen")
    print("="*60)

    # Check credentials
    if not check_credentials():
        sys.exit(1)

    # Initialize scraper
    scraper = RavelryScraper(RAVELRY_USERNAME, RAVELRY_PASSWORD)

    # Fetch patterns
    patterns = scraper.fetch_all_dutch_patterns()

    if not patterns:
        print("\n❌ Geen patronen gevonden")
        sys.exit(1)

    # Save patterns
    output_file = scraper.save_patterns()
    print(f"\n💾 Saved to: {output_file}")

    # Print summary
    scraper.print_summary()

    # Next steps
    print("🎯 Next steps:")
    print("   1. Review data in JSON file")
    print("   2. Filter by category/difficulty")
    print("   3. Extract pattern URLs")
    print("   4. Download patterns (respect copyright!)\n")

if __name__ == "__main__":
    main()
