#!/usr/bin/env python3
"""
Research VehicleMortgages.com domain using DataForSEO API
Direct API calls to avoid pydantic issues
"""

import requests
import json
import os
from datetime import datetime
import sys

# Get credentials
login = os.environ.get('DATAFORSEO_LOGIN')
password = os.environ.get('DATAFORSEO_PASSWORD')

print("🔍 VehicleMortgages.com Domain Research")
print("=" * 60)
print(f"Using DataForSEO API (Login: {login})\n")

# ============================================================================
# PHASE 1: Keyword Research - Search Volume
# ============================================================================
print("📊 Phase 1: Keyword Search Volume Analysis")
print("-" * 60)

keywords_to_research = [
    "vehicle mortgage",
    "auto loan", 
    "car loan",
    "car financing",
    "auto financing",
    "vehicle financing"
]

url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"

payload = [{
    "keywords": keywords_to_research,
    "location_name": "United States",
    "language_name": "English"
}]

response = requests.post(
    url,
    auth=(login, password),
    headers={'Content-Type': 'application/json'},
    json=payload
)

if response.status_code == 200:
    data = response.json()
    
    if 'tasks' in data and len(data['tasks']) > 0:
        task = data['tasks'][0]
        
        if 'result' in task and len(task['result']) > 0:
            results = task['result'][0]
            
            print(f"\n{'Keyword':<25} {'Search Volume':<15} {'CPC':<10} {'Competition':<12}")
            print("-" * 70)
            
            keyword_data = {}
            
            for item in results:
                keyword = item.get('keyword', 'N/A')
                search_volume = item.get('search_volume', 0)
                cpc = item.get('cpc', 0)
                competition = item.get('competition', 0)
                
                # Format competition
                if competition >= 0.8:
                    comp_str = "Very High"
                elif competition >= 0.6:
                    comp_str = "High"
                elif competition >= 0.4:
                    comp_str = "Medium"
                elif competition >= 0.2:
                    comp_str = "Low"
                else:
                    comp_str = "Very Low"
                
                print(f"{keyword:<25} {search_volume:>12,} ${cpc:>6.2f} {comp_str:<12}")
                
                keyword_data[keyword] = {
                    'search_volume': search_volume,
                    'cpc': cpc,
                    'competition': competition
                }
            
            print("\n" + "=" * 70)
else:
    print(f"❌ API Error: {response.status_code}")
    print(response.text)
    sys.exit(1)

# ============================================================================
# PHASE 2: Keyword Difficulty
# ============================================================================
print("\n📈 Phase 2: Keyword Difficulty Analysis")
print("-" * 60)

difficulty_url = "https://api.dataforseo.com/v3/keywords_data/google_ads/keyword_info/live"

payload2 = [{
    "keywords": keywords_to_research,
    "location_name": "United States",
    "language_name": "English"
}]

response2 = requests.post(
    difficulty_url,
    auth=(login, password),
    headers={'Content-Type': 'application/json'},
    json=payload2
)

if response2.status_code == 200:
    data2 = response2.json()
    
    if 'tasks' in data2 and len(data2['tasks']) > 0:
        task = data2['tasks'][0]
        
        if 'result' in task and len(task['result']) > 0:
            results2 = task['result'][0]
            
            print(f"\n{'Keyword':<25} {'Difficulty':<12} {'Keyword Ideas'}")
            print("-" * 70)
            
            for item in results2:
                keyword = item.get('keyword', 'N/A')
                difficulty = item.get('keyword_info', {}).get('keyword_difficulty', 0)
                
                diff_str = f"{difficulty}/100"
                
                print(f"{keyword:<25} {diff_str:<12}")
                
                if keyword in keyword_data:
                    keyword_data[keyword]['difficulty'] = difficulty

# ============================================================================
# PHASE 3: Keywords for Domain Analysis
# ============================================================================
print("\n🌐 Phase 3: Domain Keyword Analysis")
print("-" * 60)

domain_url = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live"

payload3 = [{
    "target": "vehiclemortgages.com",
    "location_name": "United States",
    "language_name": "English",
    "limit": 100
}]

response3 = requests.post(
    domain_url,
    auth=(login, password),
    headers={'Content-Type': 'application/json'},
    json=payload3
)

if response3.status_code == 200:
    data3 = response3.json()
    
    if 'tasks' in data3 and len(data3['tasks']) > 0:
        task = data3['tasks'][0]
        
        if 'result' in task and len(task['result']) > 0:
            results3 = task['result'][0]
            items = results3.get('items', [])
            
            print(f"\nFound {len(items)} keywords for VehicleMortgages.com domain:")
            print(f"\nTop 20 Keywords by Traffic:")
            print(f"{'Keyword':<30} {'Volume':<10} {'Traffic %'}")
            print("-" * 60)
            
            # Sort by traffic
            sorted_items = sorted(items, key=lambda x: x.get('keyword_info', {}).get('last_update_datetime', ''))[:20]
            
            for item in sorted_items[:20]:
                keyword = item.get('keyword', 'N/A')
                keyword_info = item.get('keyword_info', {})
                search_volume = keyword_info.get('search_volume', 0)
                traffic = item.get('keyword_info', {}).get('traffic', 0)
                
                print(f"{keyword:<30} {search_volume:>8,} {traffic:>6}%")
        else:
            print("\n⚠️  No keywords found for VehicleMortgages.com")
            print("   (Domain likely has no existing rankings/traffic)")
else:
    print(f"⚠️  Domain analysis returned: {response3.status_code}")

# ============================================================================
# PHASE 4: SERP Analysis
# ============================================================================
print("\n🔍 Phase 4: SERP Analysis for 'Vehicle Mortgage'")
print("-" * 60)

serp_url = "https://api.dataforseo.com/v3/serp/google/organic/live"

payload4 = [{
    "keyword": "vehicle mortgage",
    "location_name": "United States",
    "language_name": "English",
    "depth": 10
}]

response4 = requests.post(
    serp_url,
    auth=(login, password),
    headers={'Content-Type': 'application/json'},
    json=payload4
)

if response4.status_code == 200:
    data4 = response4.json()
    
    if 'tasks' in data4 and len(data4['tasks']) > 0:
        task = data4['tasks'][0]
        
        if 'result' in task and len(task['result']) > 0:
            results4 = task['result'][0]
            items = results4.get('items', [])
            
            print(f"\nTop 10 Organic Rankings for 'Vehicle Mortgage':")
            print(f"{'Rank':<6} {'Domain':<35} {'Title'}")
            print("-" * 80)
            
            for i, item in enumerate(items[:10], 1):
                domain = item.get('domain', 'N/A')
                title = item.get('title', 'N/A')[:40]
                
                print(f"{i:<6} {domain:<35} {title}")
        else:
            print("\n⚠️  No SERP results found")
else:
    print(f"⚠️  SERP analysis returned: {response4.status_code}")

# ============================================================================
# Save Results
# ============================================================================
print("\n💾 Saving Results...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

results_file = f"/root/.openclaw/workspace/research/vehiclemortgages_dataforseo_{timestamp}.json"

with open(results_file, 'w') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'search_volume': keyword_data,
        'api_response': data
    }, f, indent=2)

print(f"✅ Results saved to: {results_file}")

print("\n" + "=" * 70)
print("✅ DataForSEO Research Complete!")
print("=" * 70)
