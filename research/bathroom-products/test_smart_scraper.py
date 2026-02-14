#!/usr/bin/env python3
"""
Test the smart scraper on a single subcategory.
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/research/bathroom-products')

from smart_scraper import SmartSawidayScraper

def test_single_subcategory():
    scraper = SmartSawidayScraper()

    # Test with Baden / vrijstaande-baden
    main_category = "Baden"
    subcategory = "vrijstaande-baden"

    print(f"\nTesting: {main_category} / {subcategory}")
    print("="*60)

    brands = scraper.scrape_subcategory(main_category, subcategory)

    if brands:
        print(f"\n✅ Success! Found {len(brands)} brands")

        for brand, products in brands.items():
            print(f"\n{brand}: {len(products)} products")
            for product in products[:2]:  # Show 2 samples
                print(f"  - {product.get('name', 'Unknown')[:60]}")
                print(f"    Price: €{product.get('price', 0)}")
                print(f"    Images: {len(product.get('images', []))}")

        # Save test results
        import json
        from datetime import datetime

        test_results = {
            "test": "single_subcategory",
            "main_category": main_category,
            "subcategory": subcategory,
            "brands": brands,
            "scraped_at": datetime.now().isoformat()
        }

        filename = f"test_smart_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/root/.openclaw/workspace/research/bathroom-products/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Test results saved to: {filename}")
        print(f"✅ Scraper ready for full run!")
    else:
        print("\n❌ No brands found. Check URL structure and selectors.")

if __name__ == '__main__':
    test_single_subcategory()
