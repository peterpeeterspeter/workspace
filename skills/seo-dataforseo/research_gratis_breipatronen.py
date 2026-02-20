#!/usr/bin/env python3
"""
Research script for "gratis breipatronen" keyword - HobbySalon.be project
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from main import keyword_research, get_google_serp, get_search_intent
import json

def main():
    # Research the keyword for Netherlands
    print('🔍 Starting keyword research for "gratis breipatronen" in Netherlands...')
    print('=' * 70)

    result = keyword_research(
        keyword='gratis breipatronen',
        location_name='Netherlands',
        include_suggestions=True,
        include_related=True,
        include_difficulty=True
    )

    print('\n' + '=' * 70)
    print('✅ Research complete!')
    print('=' * 70)

    # Print summary of results
    print('\n📊 KEYWORD OVERVIEW:')
    print('-' * 70)
    if 'overview' in result and result['overview']:
        overview = result['overview']
        if 'tasks' in overview and overview['tasks']:
            task = overview['tasks'][0]
            if 'result' in task and task['result']:
                kw_data = task['result'][0]
                print(f"Keyword: {kw_data.get('keyword', 'N/A')}")
                print(f"Search Volume: {kw_data.get('search_volume', 'N/A')}")
                print(f"CPC: {kw_data.get('cpc', 'N/A')}")
                print(f"Competition: {kw_data.get('competition', 'N/A')}")
                print(f"Keyword Difficulty: {kw_data.get('keyword_difficulty', 'N/A')}")
                print(f"Search Intent: {kw_data.get('search_intent', 'N/A')}")

    print('\n💡 TOP KEYWORD SUGGESTIONS:')
    print('-' * 70)
    if 'suggestions' in result and result['suggestions']:
        suggestions = result['suggestions']
        if 'tasks' in suggestions and suggestions['tasks']:
            task = suggestions['tasks'][0]
            if 'result' in task and task['result']:
                items = task['result'][:10]
                for i, item in enumerate(items, 1):
                    vol = item.get('search_volume', 0)
                    diff = item.get('keyword_difficulty', 0)
                    cpc = item.get('cpc', 0)
                    print(f"{i}. {item.get('keyword', 'N/A')} - Vol: {vol}, Diff: {diff}, CPC: €{cpc:.2f}")

    print('\n🔗 TOP RELATED KEYWORDS:')
    print('-' * 70)
    if 'related' in result and result['related']:
        related = result['related']
        if 'tasks' in related and related['tasks']:
            task = related['tasks'][0]
            if 'result' in task and task['result']:
                items = task['result'][:10]
                for i, item in enumerate(items, 1):
                    vol = item.get('search_volume', 0)
                    diff = item.get('keyword_difficulty', 0)
                    print(f"{i}. {item.get('keyword', 'N/A')} - Vol: {vol}, Diff: {diff}")

    print('\n📈 DIFFICULTY SCORE:')
    print('-' * 70)
    if 'difficulty' in result and result['difficulty']:
        difficulty = result['difficulty']
        if 'tasks' in difficulty and difficulty['tasks']:
            task = difficulty['tasks'][0]
            if 'result' in task and task['result']:
                item = task['result'][0]
                print(f"Keyword Difficulty: {item.get('keyword_difficulty', 'N/A')}")
                print(f"Difficulty Percentage: {item.get('difficulty_percentage', 'N/A')}")

    print('\n🔍 Getting SERP data for competition overview...')
    print('-' * 70)
    serp_result = get_google_serp(
        keyword='gratis breipatronen',
        location_name='Netherlands',
        depth=20
    )

    if 'tasks' in serp_result and serp_result['tasks']:
        task = serp_result['tasks'][0]
        if 'result' in task and task['result']:
            items = task['result'][:15]
            print(f"\nTop {len(items)} results in Google.nl:")
            for i, item in enumerate(items, 1):
                title = item.get('title', 'N/A')[:60]
                url = item.get('url', 'N/A')[:50]
                domain = url.split('/')[2] if '/' in url else url
                print(f"{i}. {title}")
                print(f"   → {domain}")

    print('\n✨ All results have been saved to the results/ directory')
    print('=' * 70)

if __name__ == '__main__':
    main()
