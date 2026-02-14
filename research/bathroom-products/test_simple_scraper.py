#!/usr/bin/env python3
"""Test simple scraper on one category."""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/research/bathroom-products')

from simple_scraper import SimpleSawidayScraper

scraper = SimpleSawidayScraper()

# Test on Baden / alle-baden
category = "Baden"
subcategory_url = "/nl-be/baden/alle-baden/"

print(f"\nTesting: {category} - {subcategory_url}")
print("="*70)

brands = scraper.scrape_subcategory(category, subcategory_url)

if brands:
    print(f"\n✅ Success! Found {len(brands)} brands")

    for brand, products in list(brands.items())[:3]:  # Show 3 brands
        print(f"\n{brand}: {len(products)} products")
        for p in products[:2]:  # Show 2 products
            print(f"  - {p.get('name', 'Unknown')[:60]}")
            print(f"    Price: €{p.get('price', 0)}")
            print(f"    Images: {len(p.get('images', []))}")

    print(f"\n✅ Test passed! Ready for full run.")
else:
    print("\n❌ Test failed")
