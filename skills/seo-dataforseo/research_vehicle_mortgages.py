#!/usr/bin/env python3
"""
Research VehicleMortgages.com domain value
Analyzes keywords, search volume, CPC, competition, and domain potential
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts")))

from main import keyword_research, full_keyword_analysis
import json
from datetime import datetime

print("🔍 Researching VehicleMortgages.com domain potential...\n")

# Primary keywords to research
primary_keywords = [
    "vehicle mortgage",
    "car mortgage",
    "auto mortgage",
    "vehicle financing",
    "car loan"
]

print("📊 Phase 1: Keyword Research")
print("=" * 50)

# Research primary keyword "vehicle mortgage"
print("\n1️⃣ Researching: 'vehicle mortgage'")
result = keyword_research("vehicle mortgage", location_name="United States")

print("\n2️⃣ Researching: 'car mortgage'")
result2 = keyword_research("car mortgage", location_name="United States")

print("\n3️⃣ Researching: 'auto mortgage'")
result3 = keyword_research("auto mortgage", location_name="United States")

print("\n\n📈 Phase 2: Full Analysis of All Keywords")
print("=" * 50)

# Full analysis of all keywords
full_analysis = full_keyword_analysis(
    primary_keywords,
    location_name="United States"
)

print("\n\n💰 Saving results...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Save summary
summary_file = f"results/summary/{timestamp}__vehicle_mortgages_domain_research.md"
Path(summary_file).parent.mkdir(parents=True, exist_ok=True)

with open(summary_file, 'w') as f:
    f.write(f"# VehicleMortgages.com Domain Research\n\n")
    f.write(f"**Research Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"**Domain:** VehicleMortgages.com\n\n")
    f.write(f"---\n\n")
    f.write(f"## Executive Summary\n\n")
    f.write(f"This report analyzes the SEO potential and domain value of VehicleMortgages.com\n\n")
    f.write(f"---\n\n")
    f.write(f"## Phase 1: Primary Keyword Research\n\n")
    f.write(f"### Keyword: 'vehicle mortgage'\n\n")

print(f"\n✅ Summary saved to: {summary_file}")

print("\n\n🎯 Analysis Complete!")
print("=" * 50)
print("Check results/summary/ for detailed analysis")
