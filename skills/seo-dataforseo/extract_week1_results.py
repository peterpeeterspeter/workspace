#!/usr/bin/env python3
"""Extract Week 1 Day 1 keyword research results correctly"""

import json
from pathlib import Path

results_dir = Path("/root/.openclaw/workspace/skills/seo-dataforseo/results/labs")

# Keyword overview files (newest first)
overview_files = [
    "20260203_062244__keyword_overview__is_crash_gambling_rigged__5_keywords.json",
    "20260203_062243__keyword_overview__aviator_strategy__1_keywords.json",
    "20260203_062242__keyword_overview__crash_casinos_india__1_keywords.json",
    "20260203_062241__keyword_overview__crash_gambling_for_beginners__1_keywords.json",
    "20260203_062241__keyword_overview__bitcoin_crash_gambling__1_keywords.json",
]

difficulty_files = [
    "20260203_062244__keyword_difficulty__is_crash_gambling_rigged__5_keywords.json",
    "20260203_062244__keyword_difficulty__aviator_strategy__1_keywords.json",
    "20260203_062243__keyword_difficulty__crash_casinos_india__1_keywords.json",
    "20260203_062242__keyword_difficulty__crash_gambling_for_beginners__1_keywords.json",
    "20260203_062241__keyword_difficulty__bitcoin_crash_gambling__1_keywords.json",
]

# Create a dict to store difficulty scores
difficulty_scores = {}

# First, extract all difficulty scores
for diff_file in difficulty_files:
    diff_path = results_dir / diff_file
    if diff_path.exists():
        with open(diff_path) as f:
            diff_data = json.load(f)

        # Navigate to results
        if "data" in diff_data and "tasks" in diff_data["data"]:
            for task in diff_data["data"]["tasks"]:
                if "result" in task and task["result"]:
                    for result in task["result"]:
                        kw = result.get("keyword", "")
                        diff = result.get("keyword_difficulty", None)
                        if kw:
                            difficulty_scores[kw] = diff

# Now extract overview data
keywords = []

for ov_file in overview_files:
    ov_path = results_dir / ov_file
    if not ov_path.exists():
        continue

    with open(ov_path) as f:
        ov_data = json.load(f)

    # Navigate to results
    if "data" in ov_data and "tasks" in ov_data["data"]:
        for task in ov_data["data"]["tasks"]:
            if "result" in task and task["result"]:
                for result in task["result"]:
                    keyword = result.get("keyword", "N/A")
                    volume = result.get("search_volume", 0)
                    cpc = result.get("cpc", 0)
                    competition = result.get("competition", 0)

                    # Get difficulty from our dict
                    difficulty = difficulty_scores.get(keyword, None)

                    keywords.append({
                        "keyword": keyword,
                        "volume": volume,
                        "cpc": round(cpc, 2) if cpc else 0,
                        "competition": round(competition, 2) if competition else 0,
                        "difficulty": difficulty
                    })

# Print summary table
print("=" * 110)
print("Week 1 Day 1 Keyword Research Results (Month 2)")
print("=" * 110)
print()

# Sort by volume
sorted_keywords = sorted(keywords, key=lambda x: x["volume"], reverse=True)

print(f"{'Keyword':<45} {'Volume':<10} {'CPC':<8} {'Comp':<8} {'Difficulty':<12} {'Priority'}")
print("-" * 110)

for kw in sorted_keywords:
    keyword = kw["keyword"]
    volume = kw["volume"]
    cpc = kw["cpc"]
    comp = kw["competition"]
    diff = kw["difficulty"] if kw["difficulty"] is not None else "N/A"

    # Calculate priority
    if volume > 1000 and cpc > 5 and (diff == "N/A" or diff < 50):
        priority = "🔴 HIGH"
    elif volume > 100 and cpc > 2:
        priority = "🟠 MEDIUM"
    else:
        priority = "🟡 LOW"

    print(f"{keyword:<45} {volume:<10} ${cpc:<7} {comp:<8} {str(diff):<12} {priority}")

print()
print("=" * 110)
print(f"Total keywords researched: {len(keywords)}")
print("=" * 110)

# Save to JSON for reference
output_path = Path("/root/.openclaw/workspace/skills/seo-dataforseo/results/summary/week1-day1-keyword-research-raw.json")
with open(output_path, "w") as f:
    json.dump(keywords, f, indent=2)

print(f"\n✅ Raw data saved to: {output_path}")
