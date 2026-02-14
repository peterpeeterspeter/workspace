#!/usr/bin/env python3
"""
Extract product URLs from Sawiday.be snapshot text.
Processes browser snapshot output to extract /nl-be/p/[id]/[slug] URLs.
"""

import re
import json
from pathlib import Path

def extract_urls_from_text(text):
    """Extract product URLs from snapshot text."""
    pattern = r'/nl-be/p/\d+/[a-zA-Z0-9\-\_]+'
    matches = re.findall(pattern, text)
    
    # Deduplicate and sort
    unique_urls = sorted(list(set(matches)))
    
    return unique_urls

def save_urls(category_name, urls, target_count):
    """Save URLs to JSON file."""
    # Trim to target count
    final_urls = urls[:target_count]
    
    filename = f"/root/.openclaw/workspace/output/sawiday_{category_name}_urls.json"
    
    data = {
        "category": category_name,
        "target_count": target_count,
        "total_collected": len(final_urls),
        "urls": ["https://www.sawiday.be" + url for url in final_urls]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename, len(final_urls)

# Example snapshot text from page 1
page1_text = """
/nl-be/p/77549622/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom
/nl-be/p/77549624/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom
/nl-be/p/77549625/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart
/nl-be/p/77549626/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart
/nl-be/p/77969582/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77134462/fortifura-calvi-regendoucheset-thermostatisch-25cm-ronde-hoofddouche-staafhanddouche-zwart-mat
/nl-be/p/77969620/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77969594/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-zwart-mat
/nl-be/p/77969588/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd
/nl-be/p/77134471/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart
/nl-be/p/77969586/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd
/nl-be/p/77969601/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-chroom
/nl-be/p/77557703/fortifura-calvi-regendoucheset-thermostatisch-met-25cm-ronde-hoofddouche-en-staafhanddouche-geborsteld-messing-pvd-goud
/nl-be/p/77969583/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77969587/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-gunmetal-pvd
/nl-be/p/77969613/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs
/nl-be/p/77969589/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs
/nl-be/p/77969623/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969619/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77969625/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969577/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969622/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969592/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs
"""

# Page 2 URLs
page2_text = """
/nl-be/p/77969618/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/78180208/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-goud-mat
/nl-be/p/77969596/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-zwart-mat
/nl-be/p/78015515/fortifura-calvi-inbouw-regendoucheset-rond-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-slang-geborsteld-messing-pvd
/nl-be/p/77969609/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-zwart-mat
/nl-be/p/77969579/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-ronde-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969578/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969621/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77969584/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-messing-pvd-goud
/nl-be/p/77969595/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-zwart-mat
/nl-be/p/76681289/grohe-euphoria-xxl-310-douchesysteem-supersteel
/nl-be/p/77969605/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-metalen-slang-staaf-handdouche-chroom
/nl-be/p/77134439/fortifura-calvi-regendoucheset-thermostatisch-25cm-ronde-hoofddouche-staafhanddouche-chroom
/nl-be/p/77969585/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-gunmetal-pvd
/nl-be/p/77495063/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-metalen-doucheslang-geborsteld-messing-pvd-goud
/nl-be/p/77969580/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-koper-pvd-koper
/nl-be/p/77969600/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-chroom
/nl-be/p/77969624/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-25cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart
/nl-be/p/77583605/fortifura-calvi-douchekraan-met-glijstangset-met-ronde-handdouche,-gladde-doucheslang-mat-zwart
/nl-be/p/77969610/fortifura-calvi-regendoucheset-thermostatisch-30cm-hoofddouche-gladde-slang-staaf-handdouche-geborsteld-rvs-pvd-rvs
/nl-be/p/77905111/grohe-precision-start-doucheset-thermostatische-douchekraan-met-glijstangset-60cm-ronde-handdouche-1-straalsoort-gladde-doucheslang-mat-zwart
"""

def main():
    """Extract and save URLs."""
    print("Extracting product URLs from Sawiday.be...\n")
    
    # Extract from both pages
    page1_urls = extract_urls_from_text(page1_text)
    page2_urls = extract_urls_from_text(page2_text)
    
    # Combine and deduplicate
    all_urls = sorted(list(set(page1_urls + page2_urls)))
    
    print(f"Found {len(all_urls)} unique product URLs")
    print(f"  - Page 1: {len(page1_urls)} URLs")
    print(f"  - Page 2: {len(page2_urls)} URLs")
    print(f"  - Combined: {len(all_urls)} URLs\n")
    
    # Save douchesets URLs (need 50)
    filename, count = save_urls("douchesets", all_urls, 50)
    print(f"✓ Saved {count} doucheset URLs to {filename}")
    
    # Show first 5 URLs as sample
    print("\nFirst 5 product URLs:")
    for url in all_urls[:5]:
        print(f"  - https://www.sawiday.be{url}")
    
    print(f"\n{'='*60}")
    print(f"Total URLs saved: {count}")
    print(f"Target: 50")
    print(f"Need more: {max(0, 50 - count)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
