#!/usr/bin/env python3
"""
Comprehensive keyword research for hobbysalon.be topical authority strategy.
Researching 4 pillars: Hobbybeurzen, Workshops, Creatieve markten, Hobbymaterialen
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path("/root/.openclaw/workspace/skills/seo-dataforseo/scripts")))

from main import keyword_research, full_keyword_analysis, competitor_analysis, get_competitors
from core.storage import list_results, load_result

# Define the 4 pillars with research keywords
PILLARS = {
    "hobbybeurzen": {
        "name": "Hobbybeurzen (Hobby Fairs/Expos)",
        "keywords": [
            "hobbybeurs",
            "hobbybeurzen nederland",
            "hobbybeurs belgië",
            "hobby fair",
            "creabea",
            "creatie beurs",
            "handwerk beurs",
            "knutsel beurs",
            "hobby evenementen",
            "hobby beurzen 2024",
            "hobby beurzen 2025"
        ],
        "location": "Netherlands",  # Will use location_name
        "language": "Dutch"
    },
    "workshops": {
        "name": "Workshops (Creative Workshops, Courses)",
        "keywords": [
            "creatieve workshop",
            "workshops nederland",
            "workshops belgië",
            "cursus hobby",
            "creatie cursus",
            "handwerk workshop",
            "knutsel workshop",
            "schilderen workshop",
            "keramiek cursus",
            "breien cursus",
            "haken workshop",
            "workshop boeken",
            "creatievakantie"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    },
    "creatieve_markten": {
        "name": "Creatieve Markten (Creative Markets, Craft Fairs)",
        "keywords": [
            "creatieve markt",
            "kunstmarkt",
            "handwerkmarkt",
            "ambachtmarkt",
            "creatie markten nederland",
            "creatie markten belgië",
            "kerstmarkt nederland",
            "rommelmarkt creatief",
            "design market nederland",
            "craft fair nederland",
            "makers market",
            "local makers market"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    },
    "hobbymaterialen": {
        "name": "Hobbymaterialen (Hobby Supplies, Materials)",
        "keywords": [
            "hobbybenodigdheden",
            "hobbymaterialen",
            "hobby winkel",
            "creatie materialen",
            "knutselspullen",
            "handwerk benodigdheden",
            "garen kopen",
            "breiwol kopen",
            "stof kopen",
            "kralen kopen",
            "verf kopen",
            "hobby online shop",
            "knutselmaterialen groothandel"
        ],
        "location": "Netherlands",
        "language": "Dutch"
    }
}

def research_pillar(pillar_key, pillar_data):
    """Research a single pillar comprehensively."""
    print(f"\n{'='*80}")
    print(f"RESEARCHING PILLAR: {pillar_data['name']}")
    print(f"{'='*80}\n")

    results = {
        "pillar": pillar_data["name"],
        "keywords_researched": pillar_data["keywords"],
        "data": {}
    }

    # Get keyword suggestions for each seed keyword
    for keyword in pillar_data["keywords"][:3]:  # Limit to first 3 for efficiency
        print(f"\n--- Researching: '{keyword}' ---")

        try:
            # Full keyword analysis including:
            # - Search volume
            # - Keyword difficulty
            # - Search intent
            # - Keyword ideas/suggestions
            # - Historical trends
            result = full_keyword_analysis(
                keywords=[keyword],
                location_name=pillar_data["location"],
                include_suggestions=True,
                include_difficulty=True,
                include_intent=True,
                include_ideas=True,
                include_historical=True,
                save=True
            )

            results["data"][keyword] = {
                "status": "success",
                "summary": f"Analyzed {keyword}"
            }
            print(f"✓ Completed analysis for '{keyword}'")

        except Exception as e:
            results["data"][keyword] = {
                "status": "error",
                "error": str(e)
            }
            print(f"✗ Error analyzing '{keyword}': {e}")

    # Get competitors for top keywords
    print(f"\n--- Analyzing competitors for {pillar_key} ---")
    try:
        top_keyword = pillar_data["keywords"][0]
        competitors = get_competitors(
            keywords=[top_keyword],
            location_name=pillar_data["location"],
            language_name=pillar_data["language"],
            limit=20,
            save=True
        )
        results["competitors"] = {
            "status": "success",
            "keyword_used": top_keyword
        }
        print(f"✓ Competitor analysis complete")

    except Exception as e:
        results["competitors"] = {
            "status": "error",
            "error": str(e)
        }
        print(f"✗ Competitor analysis error: {e}")

    return results

def main():
    """Run comprehensive research for all 4 pillars."""
    print("\n" + "="*80)
    print("HOBBYSALON.BE - TOPICAL AUTHORITY RESEARCH")
    print("="*80)
    print("\nResearching 4 pillars for Dutch/Belgium market:")
    print("1. Hobbybeurzen (Hobby Fairs)")
    print("2. Workshops (Creative Workshops)")
    print("3. Creatieve Markten (Creative Markets)")
    print("4. Hobbymaterialen (Hobby Supplies)")
    print("\nTarget location: Netherlands/Belgium")
    print("Target language: Dutch (NL)")
    print("\nStarting research...\n")

    all_results = {}

    for pillar_key, pillar_data in PILLARS.items():
        pillar_results = research_pillar(pillar_key, pillar_data)
        all_results[pillar_key] = pillar_results

    print("\n" + "="*80)
    print("RESEARCH COMPLETE!")
    print("="*80)
    print("\nAll results have been saved to:")
    print("/root/.openclaw/workspace/skills/seo-dataforseo/results/")
    print("\nNext step: Analyze results and create topical authority report")
    print("="*80 + "\n")

    return all_results

if __name__ == "__main__":
    main()
