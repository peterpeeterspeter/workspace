#!/usr/bin/env python3
"""Debug JSON structure"""

import json
from pathlib import Path

results_dir = Path("/root/.openclaw/workspace/skills/seo-dataforseo/results/labs")
ov_file = "20260203_062244__keyword_overview__is_crash_gambling_rigged__5_keywords.json"
ov_path = results_dir / ov_file

with open(ov_path) as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()))
print()

# Navigate through the structure
if "data" in data:
    print("data keys:", list(data["data"].keys()))
    if "tasks" in data["data"]:
        tasks = data["data"]["tasks"]
        print(f"Number of tasks: {len(tasks)}")
        if len(tasks) > 0:
            first_task = tasks[0]
            print("First task keys:", list(first_task.keys()))
            if "result" in first_task:
                result = first_task["result"]
                print(f"Result type: {type(result)}")
                print(f"Result length: {len(result) if isinstance(result, list) else 'N/A'}")
                if isinstance(result, list) and len(result) > 0:
                    first_item = result[0]
                    print("First item keys:", list(first_item.keys()))
                    print("First item keyword:", first_item.get("keyword", "NOT FOUND"))
                    if "keyword_info" in first_item:
                        kw_info = first_item["keyword_info"]
                        print("keyword_info keys:", list(kw_info.keys()))
                        print("search_volume:", kw_info.get("search_volume", "NOT FOUND"))
