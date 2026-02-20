#!/usr/bin/env python3
"""
Research keywords for livetussenstanden.com domain
Dutch sports live scores market
"""

import sys
from pathlib import Path

# Add the skill scripts path
skill_path = Path("/root/.openclaw/workspace/skills/seo-dataforseo")
sys.path.insert(0, str(skill_path / "scripts"))

try:
    from main import keyword_research, full_keyword_analysis
    import json

    print("🔍 Researching keywords for livetussenstanden.com...")
    print("=" * 60)

    # Primary keywords to research
    keywords = [
        "live tussenstanden",
        "live voetbal tussenstanden",
        "live scores nederland",
        "voetbal uitslagen live",
        "eredivisie live",
        "live voetbalwedstrijden",
        "voetbal live kijken",
        "tussenstanden eredivisie",
        "live voetbal uitslagen",
        "voetbalstand live"
    ]

    print(f"\n📊 Analyzing {len(keywords)} keywords...\n")

    # Research each keyword
    results = []
    for keyword in keywords[:5]:  # Start with first 5 to save API credits
        print(f"🔍 {keyword}...")
        try:
            data = keyword_research(keyword, country_code="NL", language_code="nl")
            results.append({
                "keyword": keyword,
                "data": data
            })
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                "keyword": keyword,
                "error": str(e)
            })

    # Print results
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)

    for result in results:
        print(f"\n🔑 {result['keyword']}")
        if "error" in result:
            print(f"   ❌ {result['error']}")
        elif "data" in result and result["data"]:
            # Extract key metrics from DataForSEO response
            data = result["data"]
            print(f"   📈 Search Volume: {data.get('search_volume', 'N/A')}")
            print(f"   💰 CPC: €{data.get('cpc', 0):.2f}" if data.get('cpc') else "   💰 CPC: N/A")
            print(f"   📊 Competition: {data.get('competition', 'N/A')}")

    # Save to file
    output_file = "/root/.openclaw/workspace/research/livetussenstanden-keywords.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Saved to: {output_file}")

except ImportError as e:
    print(f"❌ Error importing DataForSEO modules: {e}")
    print("Note: DataForSEO skill may need dependencies installed")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
