#!/usr/bin/env python3
"""Analyze Week 1 Day 1 keyword research results"""

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

keywords = []

for i, ov_file in enumerate(overview_files):
    ov_path = results_dir / ov_file
    diff_path = results_dir / difficulty_files[i]

    if ov_path.exists():
        with open(ov_path) as f:
            ov_data = json.load(f)

    if diff_path.exists():
        with open(diff_path) as f:
            diff_data = json.load(f)

    # Extract primary keyword metrics
    if ov_data and "tasks" in ov_data and len(ov_data["tasks"]) > 0:
        task = ov_data["tasks"][0]
        if "result" in task and len(task["result"]) > 0:
            result = task["result"][0]
            keyword = result.get("keyword", "N/A")
            volume = result.get("search_volume", 0)
            cpc = result.get("cpc", 0)
            competition = result.get("competition", 0)

            # Get difficulty
            difficulty = None
            if diff_data and "tasks" in diff_data and len(diff_data["tasks"]) > 0:
                diff_task = diff_data["tasks"][0]
                if "result" in diff_task and len(diff_task["result"]) > 0:
                    diff_result = diff_task["result"][0]
                    difficulty = diff_result.get("keyword_difficulty", None)

            keywords.append({
                "keyword": keyword,
                "volume": volume,
                "cpc": round(cpc, 2),
                "competition": round(competition, 2),
                "difficulty": difficulty
            })

# Print summary table
print("=" * 100)
print("Week 1 Day 1 Keyword Research Results (Month 2)")
print("=" * 100)
print()

# Sort by opportunity score (volume × cpc / difficulty if available, else volume)
def opportunity_score(kw):
    if kw["difficulty"] and kw["difficulty"] > 0:
        return (kw["volume"] * kw["cpc"]) / kw["difficulty"]
    return kw["volume"] * kw["cpc"]

sorted_keywords = sorted(keywords, key=opportunity_score, reverse=True)

print(f"{'Keyword':<40} {'Volume':<10} {'CPC':<8} {'Comp':<8} {'Difficulty':<12} {'Priority'}")
print("-" * 100)

for kw in sorted_keywords:
    keyword = kw["keyword"]
    volume = kw["volume"]
    cpc = kw["cpc"]
    comp = kw["competition"]
    diff = kw["difficulty"] if kw["difficulty"] else "N/A"

    # Calculate priority
    if volume > 1000 and cpc > 5 and (diff == "N/A" or diff < 50):
        priority = "🔴 HIGH"
    elif volume > 100 and cpc > 2:
        priority = "🟠 MEDIUM"
    else:
        priority = "🟡 LOW"

    print(f"{keyword:<40} {volume:<10} ${cpc:<7} {comp:<8} {str(diff):<12} {priority}")

print()
print("=" * 100)
print(f"Total keywords researched: {len(keywords)}")
print("=" * 100)

# Save to JSON for reference
output_path = Path("/root/.openclaw/workspace/skills/seo-dataforseo/results/summary/week1-day1-keyword-research-raw.json")
with open(output_path, "w") as f:
    json.dump(keywords, f, indent=2)

print(f"\n✅ Raw data saved to: {output_path}")
