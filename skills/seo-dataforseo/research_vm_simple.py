#!/usr/bin/env python3
"""
Research VehicleMortgages.com using DataForSEO API (Simplified)
"""

import requests
import json
import os
from datetime import datetime

login = os.environ.get('DATAFORSEO_LOGIN')
password = os.environ.get('DATAFORSEO_PASSWORD')

print("🔍 VehicleMortgages.com - DataForSEO Research")
print("=" * 60)

# ============================================================================
# PHASE 1: Search Volume for Keywords
# ============================================================================
print("\n📊 Phase 1: Keyword Search Volume")
print("-" * 60)

keywords = ["vehicle mortgage", "auto loan", "car loan", "car financing", "auto financing"]

url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"

payload = [{
    "keywords": keywords,
    "location_name": "United States",
    "language_name": "English"
}]

response = requests.post(url, auth=(login, password), json=payload)

print(f"API Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    
    # Debug: save full response
    with open('/tmp/dfo_response.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nFull response saved to /tmp/dfo_response.json")
    
    # Print structure
    print(f"\nResponse structure:")
    print(f"  - status_code: {data.get('status_code')}")
    print(f"  - tasks_count: {data.get('tasks_count')}")
    
    if 'tasks' in data and len(data['tasks']) > 0:
        task = data['tasks'][0]
        print(f"  - task status_code: {task.get('status_code')}")
        print(f"  - task result_count: {task.get('result_count')}")
        
        if 'data' in task:
            task_data = task['data']
            print(f"  - data type: {type(task_data)}")
            
            # Handle different response formats
            if isinstance(task_data, dict):
                if 'result' in task_data and len(task_data['result']) > 0:
                    result = task_data['result'][0]
                    
                    if isinstance(result, list):
                        print(f"\n{'Keyword':<25} {'Volume':<12} {'CPC':<10}")
                        print("-" * 50)
                        
                        for item in result:
                            if isinstance(item, dict):
                                kw = item.get('keyword', 'N/A')
                                vol = item.get('search_volume', 0)
                                cpc = item.get('cpc', 0)
                                print(f"{kw:<25} {vol:>10,} ${cpc:>6.2f}")
                    
                    elif isinstance(result, dict):
                        print(f"\nResult is dict with keys: {list(result.keys())[:10]}")

else:
    print(f"Error: {response.text}")

print("\n✅ Script complete")
