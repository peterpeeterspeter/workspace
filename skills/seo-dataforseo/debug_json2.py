#!/usr/bin/env python3
"""Debug JSON structure - check items"""

import json
from pathlib import Path

results_dir = Path("/root/.openclaw/workspace/skills/seo-dataforseo/results/labs")
ov_file = "20260203_062244__keyword_overview__is_crash_gambling_rigged__5_keywords.json"
ov_path = results_dir / ov_file

with open(ov_path) as f:
    data = json.load(f)

# Navigate to items
tasks = data["data"]["tasks"]
result = tasks[0]["result"]
first_result_item = result[0]

print("First result item keys:", list(first_result_item.keys()))
print()

if "items" in first_result_item:
    items = first_result_item["items"]
    print(f"Number of items: {len(items)}")
    print()

    for i, item in enumerate(items):
        print(f"Item {i+1}:")
        print(f"  keyword: {item.get('keyword', 'NOT FOUND')}")
        kw_info = item.get("keyword_info", {})
        print(f"  search_volume: {kw_info.get('search_volume', 'NOT FOUND')}")
        print(f"  cpc: {kw_info.get('cpc', 'NOT FOUND')}")
        print(f"  competition: {kw_info.get('competition', 'NOT FOUND')}")
        print()
