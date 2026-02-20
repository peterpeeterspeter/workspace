#!/usr/bin/env python3
"""
Comprehensive keyword research for hobbysalon.be topical authority strategy
Researching 4 pillars: Hobbybeurzen, Workshops, Creatieve markten, Hobbymaterialen
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from main import keyword_research

# Define the 4 pillars with seed keywords for research
PILLARS = {
    "hobbybeurzen": {
        "name": "Hobbybeurzen (Hobby Fairs)",
        "seed_keywords": [
            "hobbybeurs",
            "creabeurs",
            "handwerkbeurs",
            "craft fair",
            "naai en klosbeurs",
            "breibeurs",
            "hobbybeurs nederland",
            "creabeurs nederland",
            "handwerkbeurs nederland"
        ],
        "location": "Belgium"  # Targeting Belgium/Netherlands
    },
    "workshops": {
        "name": "Workshops (Creative Workshops, Courses)",
        "seed_keywords": [
            "creatieve workshop",
            "handwerk workshop",
            "hobby workshop",
            "breien workshop",
            "haken workshop",
            "naaien cursus",
            "kaarten maken workshop",
            "keramiek workshop",
            "schilderen workshop",
            "creatieve cursus"
        ],
        "location": "Belgium"
    },
    "creatieve_markten": {
        "name": "Creatieve Markten (Creative Markets, Craft Fairs)",
        "seed_keywords": [
            "creatieve markt",
            "makers markt",
            "handwerkmarkt",
            "craft market",
            "rommelmarkt creatief",
            "vintage markt",
            "brocante",
            "lokale markt",
            "kunstmarkt",
            "designmarkt"
        ],
        "location": "Belgium"
    },
    "hobbymaterialen": {
        "name": "Hobbymaterialen (Hobby Supplies, Materials)",
        "seed_keywords": [
            "hobbybenodigdheden",
            "handwerk materialen",
            "breiwol kopen",
            "haakwol kopen",
            "naaibenodigdheden",
            "kaarten maken spullen",
            "hobbywinkel",
            "creabeurs shop",
            "knutselspullen",
            "art supplies"
        ],
        "location": "Belgium"
    }
}

def research_pillar(pillar_id, pillar_config):
    """Research all keywords for a specific pillar"""
    print(f"\n{'='*80}")
    print(f"RESEARCHING PILLAR: {pillar_config['name']}")
    print(f"{'='*80}\n")

    results = {
        "pillar_id": pillar_id,
        "pillar_name": pillar_config['name'],
        "location": pillar_config.get('location', 'Belgium'),
        "research_date": datetime.now().isoformat(),
        "seed_keywords": pillar_config['seed_keywords'],
        "keyword_data": []
    }

    for keyword in pillar_config['seed_keywords']:
        print(f"\n--- Researching: {keyword} ---")
        try:
            # Research each keyword with full analysis
            result = keyword_research(
                keyword=keyword,
                location_name=pillar_config.get('location', 'Belgium'),
                include_suggestions=True,
                include_related=True,
                include_difficulty=True
            )

            if result:
                results['keyword_data'].append({
                    'keyword': keyword,
                    'data': result
                })
                print(f"✓ Completed research for '{keyword}'")
            else:
                print(f"✗ No data returned for '{keyword}'")

        except Exception as e:
            print(f"✗ Error researching '{keyword}': {str(e)}")
            continue

    return results

def categorize_keywords(research_data):
    """Categorize keywords into primary and secondary based on criteria"""
    primary_keywords = []  # Volume 500+, KD < 30
    secondary_keywords = []  # Volume 100+, KD < 40

    for keyword_result in research_data.get('keyword_data', []):
        # Process main keyword
        if 'overview' in keyword_result.get('data', {}):
            overview = keyword_result['data']['overview']
            volume = overview.get('search_volume', 0)
            difficulty_data = keyword_result['data'].get('difficulty', {})
            kd = difficulty_data.get('keyword_difficulty', 0) if difficulty_data else 0

            keyword_info = {
                'keyword': keyword_result['keyword'],
                'volume': volume,
                'kd': kd,
                'cpc': overview.get('cpc', 0),
                'competition': overview.get('competition', 0)
            }

            # Categorize
            if volume >= 500 and kd < 30:
                primary_keywords.append(keyword_info)
            elif volume >= 100 and kd < 40:
                secondary_keywords.append(keyword_info)

        # Process suggestions
        if 'suggestions' in keyword_result.get('data', {}):
            for suggestion in keyword_result['data']['suggestions']:
                vol = suggestion.get('search_volume', 0)
                kd_val = suggestion.get('keyword_difficulty', 0)

                suggestion_info = {
                    'keyword': suggestion.get('keyword', ''),
                    'volume': vol,
                    'kd': kd_val,
                    'cpc': suggestion.get('cpc', 0),
                    'competition': suggestion.get('competition', 0)
                }

                if vol >= 500 and kd_val < 30:
                    primary_keywords.append(suggestion_info)
                elif vol >= 100 and kd_val < 40:
                    secondary_keywords.append(suggestion_info)

    # Remove duplicates and sort by volume
    def dedup_and_sort(keywords):
        seen = set()
        unique = []
        for kw in keywords:
            if kw['keyword'] not in seen:
                seen.add(kw['keyword'])
                unique.append(kw)
        return sorted(unique, key=lambda x: x['volume'], reverse=True)

    return {
        'primary': dedup_and_sort(primary_keywords),
        'secondary': dedup_and_sort(secondary_keywords)
    }

def main():
    """Main execution"""
    print("Starting comprehensive keyword research for hobbysalon.be")
    print(f"Research date: {datetime.now().isoformat()}")
    print(f"Target location: Belgium/Netherlands")

    all_results = {}

    # Research each pillar
    for pillar_id, pillar_config in PILLARS.items():
        pillar_results = research_pillar(pillar_id, pillar_config)
        categorized = categorize_keywords(pillar_results)

        all_results[pillar_id] = {
            'config': pillar_config,
            'research': pillar_results,
            'categorized': categorized
        }

    # Save results
    output_file = Path(__file__).parent / "results" / f"hobbysalon_pillar_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"RESEARCH COMPLETE")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

    # Print summary
    for pillar_id, data in all_results.items():
        print(f"\n{data['config']['name']}:")
        print(f"  Primary keywords: {len(data['categorized']['primary'])}")
        print(f"  Secondary keywords: {len(data['categorized']['secondary'])}")

    return all_results

if __name__ == "__main__":
    main()
