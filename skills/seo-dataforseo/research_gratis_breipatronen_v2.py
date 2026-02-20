#!/usr/bin/env python3
"""
Research script for "gratis breipatronen" keyword - HobbySalon.be project
Corrected version with Dutch language support
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from api.labs import get_keyword_overview, get_keyword_suggestions, get_related_keywords, get_bulk_keyword_difficulty
from api.serp import get_google_serp
import json

def main():
    keyword = 'gratis breipatronen'
    location = 'Netherlands'
    language = 'Dutch'  # Correct language for Dutch keywords

    print(f'🔍 Starting keyword research for "{keyword}" in {location} ({language})...')
    print('=' * 70)

    # Get keyword overview
    print('\n📊 Getting keyword overview...')
    overview = get_keyword_overview(
        keywords=[keyword],
        location_name=location,
        language_name=language
    )

    # Get keyword suggestions
    print('\n💡 Getting keyword suggestions...')
    suggestions = get_keyword_suggestions(
        keyword=keyword,
        location_name=location,
        language_name=language,
        limit=50
    )

    # Get related keywords
    print('\n🔗 Getting related keywords...')
    related = get_related_keywords(
        keyword=keyword,
        location_name=location,
        language_name=language,
        depth=2,
        limit=50
    )

    # Get keyword difficulty
    print('\n📈 Getting keyword difficulty...')
    difficulty = get_bulk_keyword_difficulty(
        keywords=[keyword],
        location_name=location,
        language_name=language
    )

    # Get SERP data
    print('\n🔍 Getting SERP competition data...')
    serp = get_google_serp(
        keyword=keyword,
        location_name=location,
        language_name=language,
        depth=20
    )

    print('\n' + '=' * 70)
    print('✅ Research complete!')
    print('=' * 70)

    # Extract and print overview data
    print('\n📊 KEYWORD OVERVIEW:')
    print('-' * 70)
    if 'tasks' in overview and overview['tasks']:
        task = overview['tasks'][0]
        if task.get('status_code') == 20000 and 'result' in task:
            kw_data = task['result'][0]
            print(f"Keyword: {kw_data.get('keyword', 'N/A')}")
            print(f"Search Volume: {kw_data.get('search_volume', 'N/A'):,} searches/month")
            print(f"CPC: €{kw_data.get('cpc', 0):.2f}")
            print(f"Competition: {kw_data.get('competition', 'N/A')}")
            if 'keyword_difficulty' in kw_data:
                print(f"Keyword Difficulty: {kw_data.get('keyword_difficulty', 'N/A')}/100")
            print(f"Search Intent: {kw_data.get('search_intent', 'N/A')}")

            # Get SERP features if available
            if kw_data.get('serp_info'):
                print("\nSERP Features:")
                for feature in kw_data['serp_info'].get('se_types', {}).get('google', {}).get('features', []):
                    print(f"  • {feature}")
        else:
            print(f"Error: {task.get('status_message', 'Unknown error')}")

    # Extract and print suggestions
    print('\n💡 TOP KEYWORD SUGGESTIONS:')
    print('-' * 70)
    if 'tasks' in suggestions and suggestions['tasks']:
        task = suggestions['tasks'][0]
        if task.get('status_code') == 20000 and 'result' in task:
            items = sorted(task['result'][:15], key=lambda x: x.get('search_volume', 0), reverse=True)
            for i, item in enumerate(items, 1):
                vol = item.get('search_volume', 0)
                diff = item.get('keyword_difficulty', 0)
                cpc = item.get('cpc', 0)
                intent = item.get('search_intent', 'N/A')
                kw = item.get('keyword', 'N/A')
                print(f"{i:2d}. {kw}")
                print(f"    Vol: {vol:,} | Diff: {diff}/100 | CPC: €{cpc:.2f} | Intent: {intent}")
        else:
            print(f"Error: {task.get('status_message', 'Unknown error')}")

    # Extract and print related keywords
    print('\n🔗 TOP RELATED KEYWORDS:')
    print('-' * 70)
    if 'tasks' in related and related['tasks']:
        task = related['tasks'][0]
        if task.get('status_code') == 20000 and 'result' in task:
            items = sorted(task['result'][:15], key=lambda x: x.get('search_volume', 0), reverse=True)
            for i, item in enumerate(items, 1):
                vol = item.get('search_volume', 0)
                diff = item.get('keyword_difficulty', 0)
                kw = item.get('keyword', 'N/A')
                print(f"{i:2d}. {kw} - Vol: {vol:,}, Diff: {diff}/100")
        else:
            print(f"Error: {task.get('status_message', 'Unknown error')}")

    # Extract and print difficulty
    print('\n📈 KEYWORD DIFFICULTY:')
    print('-' * 70)
    if 'tasks' in difficulty and difficulty['tasks']:
        task = difficulty['tasks'][0]
        if task.get('status_code') == 20000 and 'result' in task:
            item = task['result'][0]
            diff = item.get('keyword_difficulty', 0)
            diff_pct = item.get('difficulty_percentage', 0)
            print(f"Keyword Difficulty Score: {diff}/100")
            print(f"Difficulty Percentage: {diff_pct}%")
            if diff < 30:
                difficulty_level = "Easy - Good opportunity to rank"
            elif diff < 60:
                difficulty_level = "Medium - Moderate competition"
            else:
                difficulty_level = "Hard - Highly competitive"
            print(f"Assessment: {difficulty_level}")
        else:
            print(f"Error: {task.get('status_message', 'Unknown error')}")

    # Extract and print SERP competition
    print('\n🏆 TOP SERP COMPETITORS (Google.nl):')
    print('-' * 70)
    if 'tasks' in serp and serp['tasks']:
        task = serp['tasks'][0]
        if task.get('status_code') == 20000 and 'result' in task:
            items = task['result'][:15]
            print(f"\nTop {len(items)} organic results:")
            for i, item in enumerate(items, 1):
                title = item.get('title', 'N/A')
                url = item.get('url', 'N/A')
                domain = urlparse(url).netloc if url else 'N/A'
                desc = item.get('description', 'N/A')[:80]

                print(f"\n{i}. {title}")
                print(f"   URL: {domain}")
                print(f"   Desc: {desc}...")
        else:
            print(f"Error: {task.get('status_message', 'Unknown error')}")

    print('\n' + '=' * 70)
    print('✨ All results have been saved to the results/ directory')
    print('=' * 70)

if __name__ == '__main__':
    from urllib.parse import urlparse
    main()
