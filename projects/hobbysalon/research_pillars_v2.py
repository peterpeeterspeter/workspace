#!/usr/bin/env python3
"""
Comprehensive keyword research for hobbysalon.be topical authority strategy.
Researching 4 pillars: Hobbybeurzen, Workshops, Creatieve markten, Hobbymaterialen
Working version using direct API imports
"""

import sys
from pathlib import Path
from urllib.parse import urlparse
import json
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path("/root/.openclaw/workspace/skills/seo-dataforseo")))

from scripts.api.labs import get_keyword_overview, get_keyword_suggestions, get_bulk_keyword_difficulty
from scripts.api.serp import get_google_serp

# Define the 4 pillars with seed keywords
PILLARS = {
    "hobbybeurzen": {
        "name": "Hobbybeurzen (Hobby Fairs/Expos)",
        "seed_keywords": [
            "hobbybeurs",
            "hobbybeurzen nederland",
            "hobbybeurs belgië",
            "creabea",
            "creatie beurs"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    },
    "workshops": {
        "name": "Workshops (Creative Workshops, Courses)",
        "seed_keywords": [
            "creatieve workshop",
            "workshops nederland",
            "workshops belgië",
            "cursus hobby",
            "handwerk workshop"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    },
    "creatieve_markten": {
        "name": "Creatieve Markten (Creative Markets, Craft Fairs)",
        "seed_keywords": [
            "creatieve markt",
            "kunstmarkt",
            "handwerkmarkt",
            "ambachtmarkt",
            "design market nederland"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    },
    "hobbymaterialen": {
        "name": "Hobbymaterialen (Hobby Supplies, Materials)",
        "seed_keywords": [
            "hobbybenodigdheden",
            "hobbymaterialen",
            "hobby winkel",
            "creatie materialen",
            "knutselspullen"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    }
}

def research_keyword(keyword, location, language):
    """Research a single keyword comprehensively."""
    print(f"\n{'─'*70}")
    print(f"Researching: '{keyword}'")
    print(f"{'─'*70}")

    result = {
        "keyword": keyword,
        "location": location,
        "language": language,
        "data": {}
    }

    # Get keyword overview
    try:
        print("  → Getting overview...")
        overview = get_keyword_overview(
            keywords=[keyword],
            location_name=location,
            language_name=language,
            save=False
        )
        result["data"]["overview"] = overview

        # Extract key metrics
        if 'tasks' in overview and overview['tasks']:
            task = overview['tasks'][0]
            if task.get('status_code') == 20000 and 'result' in task:
                kw_data = task['result'][0]
                sv = kw_data.get('search_volume', 0)
                cpc = kw_data.get('cpc', 0)
                comp = kw_data.get('competition', 0)
                intent = kw_data.get('search_intent', 'N/A')
                print(f"  ✓ Volume: {sv:,} | CPC: €{cpc:.2f} | Intent: {intent}")
    except Exception as e:
        print(f"  ✗ Overview error: {e}")
        result["data"]["overview"] = {"error": str(e)}

    # Get keyword suggestions
    try:
        print("  → Getting suggestions...")
        suggestions = get_keyword_suggestions(
            keyword=keyword,
            location_name=location,
            language_name=language,
            limit=100,
            save=False
        )
        result["data"]["suggestions"] = suggestions
        print(f"  ✓ Retrieved suggestions")
    except Exception as e:
        print(f"  ✗ Suggestions error: {e}")
        result["data"]["suggestions"] = {"error": str(e)}

    # Get keyword difficulty
    try:
        print("  → Getting difficulty...")
        difficulty = get_bulk_keyword_difficulty(
            keywords=[keyword],
            location_name=location,
            language_name=language,
            save=False
        )
        result["data"]["difficulty"] = difficulty

        if 'tasks' in difficulty and difficulty['tasks']:
            task = difficulty['tasks'][0]
            if task.get('status_code') == 20000 and 'result' in task:
                diff = task['result'][0].get('keyword_difficulty', 0)
                print(f"  ✓ Difficulty: {diff}/100")
    except Exception as e:
        print(f"  ✗ Difficulty error: {e}")
        result["data"]["difficulty"] = {"error": str(e)}

    # Get SERP competition
    try:
        print("  → Getting SERP data...")
        serp = get_google_serp(
            keyword=keyword,
            location_name=location,
            language_name=language,
            depth=15,
            save=False
        )
        result["data"]["serp"] = serp
        print(f"  ✓ SERP data retrieved")
    except Exception as e:
        print(f"  ✗ SERP error: {e}")
        result["data"]["serp"] = {"error": str(e)}

    return result

def research_pillar(pillar_key, pillar_data):
    """Research a single pillar."""
    print(f"\n{'='*80}")
    print(f"PILLAR: {pillar_data['name']}")
    print(f"{'='*80}")

    pillar_results = {
        "pillar_name": pillar_data["name"],
        "location": pillar_data["location"],
        "language": pillar_data["language"],
        "keywords": {}
    }

    for keyword in pillar_data["seed_keywords"]:
        keyword_result = research_keyword(
            keyword,
            pillar_data["location"],
            pillar_data["language"]
        )
        pillar_results["keywords"][keyword] = keyword_result

    return pillar_results

def save_results(all_results):
    """Save results to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path("/root/.openclaw/workspace/projects/hobbysalon") / f"research_results_{timestamp}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Results saved to: {output_file}")
    return output_file

def main():
    """Run comprehensive research for all 4 pillars."""
    print("\n" + "="*80)
    print("HOBBYSALON.BE - TOPICAL AUTHORITY RESEARCH")
    print("="*80)
    print("\n📍 Target: Netherlands/Belgium (Dutch language)")
    print("🎯 Goal: Build topical authority for hobby events & supplies")
    print("\nResearching 4 pillars:")
    print("  1. Hobbybeurzen (Hobby Fairs/Expos)")
    print("  2. Workshops (Creative Workshops, Courses)")
    print("  3. Creatieve Markten (Creative Markets, Craft Fairs)")
    print("  4. Hobbymaterialen (Hobby Supplies, Materials)")
    print("\n" + "="*80)

    all_results = {}

    for pillar_key, pillar_data in PILLARS.items():
        pillar_results = research_pillar(pillar_key, pillar_data)
        all_results[pillar_key] = pillar_results

    # Save results
    output_file = save_results(all_results)

    print("\n" + "="*80)
    print("✅ RESEARCH COMPLETE!")
    print("="*80)
    print(f"\n📊 All data saved to: {output_file}")
    print("\nNext: Generate comprehensive topical authority report")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
