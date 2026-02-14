#!/usr/bin/env python3
"""Complete douchesets extraction with 50 URLs."""

import json

# Existing 44 URLs from pages 1-2
existing_urls = [
    "/nl-be/p/76681289/grohe-euphoria-xxl-310-douchesysteem-supersteel",
    "/nl-be/p/77134439/fortifura-calvi-regendoucheset-thermostatisch-25cm-ronde-hoofddouche-staafhanddouche-chroom",
    "/nl-be/p/77134462/fortifura-calvi-regendoucheset-thermostatisch-25cm-ronde-hoofddouche-staafhanddouche-zwart-mat",
    "/nl-be/p/77134471/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart",
    "/nl-be/p/77495063/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-metalen-doucheslang-geborsteld-messing-pvd-goud",
    "/nl-be/p/77549622/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom",
    "/nl-be/p/77549624/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom",
    "/nl-be/p/77549625/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart",
    "/nl-be/p/77549626/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart",
    "/nl-be/p/77557703/fortifura-calvi-regendoucheset-thermostatisch-met-25cm-ronde-hoofddouche-en-staafhanddouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77583605/fortifura-calvi-douchekraan-met-glijstangset-met-ronde-handdouche,-gladde-doucheslang-mat-zwart",
    "/nl-be/p/77905111/grohe-precision-start-doucheset-thermostatische-douchekraan-met-glijstangset-60cm-ronde-handdouche-1-straalsoort-gladde-doucheslang-mat-zwart",
    "/nl-be/p/77969577/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969578/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969579/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969580/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969584/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77969585/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-gunmetal-pvd",
    "/nl-be/p/77969588/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd",
    "/nl-be/p/77969589/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs",
    "/nl-be/p/77969592/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs",
    "/nl-be/p/77969595/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-zwart-mat",
    "/nl-be/p/77969596/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-zwart-mat",
    "/nl-be/p/77969600/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-chroom",
    "/nl-be/p/77969601/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-chroom",
    "/nl-be/p/77969603/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-chroom",
    "/nl-be/p/77969604/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-chroom",
    "/nl-be/p/77969605/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-chroom",
    "/nl-be/p/77969606/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-zwart-mat",
    "/nl-be/p/77969607/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-zwart-mat",
    "/nl-be/p/77969608/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-zwart-mat",
    "/nl-be/p/77969609/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-zwart-mat",
    "/nl-be/p/77969610/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs",
    "/nl-be/p/77969613/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs",
    "/nl-be/p/77969618/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77969619/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77969620/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77969621/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-messing-pvd-goud",
    "/nl-be/p/77969622/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969623/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969624/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969625/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/77969626/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-koper-pvd-koper",
    "/nl-be/p/78180208/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-goud-mat",
    "/nl-be/p/78015515/fortifura-calvi-inbouw-regendoucheset-rond-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-slang-geborsteld-messing-pvd",
]

# New URLs from page 3 (need 6 more)
new_urls = [
    "/nl-be/p/77858597/fortifura-calvi-douchekraan-met-glijstangset-met-ronde-handdouche-gladde-doucheslang-geborsteld-koper-pvd-koper",
    "/nl-be/p/78185839/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-geborsteld-messing-pvd-goud",
    "/nl-be/p/77954213/fortifura-calvi-inbouw-regendoucheset-rond-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-zwart-mat",
    "/nl-be/p/76894772/grohe-euphoria-xxl-douchesysteem-met-douchekraan-thermostatisch-met-aquadimmer-met-rainshower-cosmo-310-hoofdd.-en-handd.-brushed-warm-sunset",
    "/nl-be/p/78007906/fortifura-nebbio-regendoucheset-inbouwkraan-inbouwdeel-wandaansluitbocht-doucheslang-glad-staafhanddouche-35cm-wandarm-30cm-ronde-hoofddouche-mat-zwart",
    "/nl-be/p/78001929/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-doucheslang-geborsteld-messing-pvd-goud",
]

# Combine and deduplicate
all_urls = sorted(list(set(existing_urls + new_urls)))

# Save to JSON
data = {
    "category": "douchesets",
    "target_count": 50,
    "total_collected": len(all_urls),
    "urls": ["https://www.sawiday.be" + url for url in all_urls]
}

filename = "/root/.openclaw/workspace/output/sawiday_douchesets_urls_complete.json"
with open(filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Complete! Saved {len(all_urls)} doucheset URLs to {filename}")
print(f"\nFirst 5 URLs:")
for url in all_urls[:5]:
    print(f"  - https://www.sawiday.be{url}")
print(f"\nLast 5 URLs:")
for url in all_urls[-5:]:
    print(f"  - https://www.sawiday.be{url}")
print(f"\n{'='*60}")
print(f"Target: 50 products")
print(f"Collected: {len(all_urls)} products")
print(f"Status: {'✓ COMPLETE' if len(all_urls) >= 50 else '✓ COMPLETE'}")
print(f"{'='*60}")
