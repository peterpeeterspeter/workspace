#!/usr/bin/env python3
"""Extract infrarood douchepanelen URLs from snapshot."""

import json

# Page 1 product URLs from snapshot (first 10)
page1_urls = [
    "/nl-be/p/77493692/sunshower-pure-black-infrarood-inbouwapparaat-19.9x61.9x10cm-half-body-1250watt-zwart-aluminium",
    "/nl-be/p/77666935/sunshower-round-installatiebox-m",
    "/nl-be/p/77493696/sunshower-solo-infrarood-opbouwapparaat-20x125x18cm-full-body-1500watt-aluminium",
    "/nl-be/p/77493702/sunshower-deluxe-white-32x187x16cm-uv-en-infrarood-inbouw-full-body-2000watt-aluminium-wit",
    "/nl-be/p/77263614/sunshower-ventilatieposter-13x13cm-voor-pure-en-pure-xl-en-deluxe-glas-organic-grey",
    "/nl-be/p/77263395/sunshower-ventilatieposter-15x9cm-voor-pure-en-pure-xl-en-deluxe-glas-organic-grey",
    "/nl-be/p/77263391/sunshower-ventilatieposter-15x9cm-voor-pure-en-pure-xl-en-deluxe-glas-zwart",
    "/nl-be/p/77545174/sunshower-round-medium-plus-infrarood-uv-licht-inbouw-140x33x10cm-sand-white",
    "/nl-be/p/77545169/sunshower-round-medium-one-infrarood-inbouw-140x33x10cm-sand-white",
    "/nl-be/p/77545177/sunshower-round-one-l-infrarood-inbouw-185x33x10cm-full-body-sand-white",
]

# Save to JSON
all_urls = sorted(page1_urls[:10])  # Take first 10

data = {
    "category": "infrarood_douchepanelen",
    "target_count": 10,
    "total_collected": len(all_urls),
    "urls": ["https://www.sawiday.be" + url for url in all_urls]
}

filename = "/root/.openclaw/workspace/output/sawiday_infrarood_douchepanelen_urls.json"
with open(filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Complete! Saved {len(all_urls)} infrarood douchepanelen URLs to {filename}")
print(f"\nAll 10 URLs:")
for url in all_urls:
    print(f"  - https://www.sawiday.be{url}")
print(f"\n{'='*60}")
print(f"Target: 10 products")
print(f"Collected: {len(all_urls)} products")
print(f"Status: ✓ COMPLETE")
print(f"{'='*60}")
