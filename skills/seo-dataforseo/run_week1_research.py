#!/usr/bin/env python3
"""Week 1 (Month 2) Keyword Research for Feb 3, 2026"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from main import keyword_research, full_keyword_analysis

# Week 1 Day 1 Keywords (Monday Feb 3 - 5 HIGH priority articles)
keywords_day1 = [
    "is crash gambling rigged",  # crashcasino.io
    "bitcoin crash gambling",     # cryptocrashgambling.com
    "crash gambling for beginners",  # crashgamegambling.com
    "crash casinos india",        # freecrashgames.com
    "aviator strategy",           # aviatorcrashgame.com
]

print("=" * 60)
print("Week 1 Day 1 Keyword Research (Month 2)")
print("=" * 60)
print(f"Keywords to research: {len(keywords_day1)}")
print()

results = {}
for kw in keywords_day1:
    print(f"\n🔍 Researching: {kw}")
    print("-" * 60)
    try:
        result = keyword_research(kw, location_name="United States")
        results[kw] = result
        print(f"✅ Complete: {kw}")
    except Exception as e:
        print(f"❌ Error: {e}")
        results[kw] = None

print("\n" + "=" * 60)
print(f"✅ Research complete: {len([r for r in results.values() if r])}/{len(keywords_day1)} keywords")
print("=" * 60)

# Now create a full analysis for all keywords together
print("\n📊 Running full keyword analysis for all 5 keywords...")
try:
    full_analysis = full_keyword_analysis(keywords_day1, location_name="United States")
    print("✅ Full analysis complete")
except Exception as e:
    print(f"❌ Full analysis error: {e}")
