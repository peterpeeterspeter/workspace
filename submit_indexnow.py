#!/usr/bin/env python3
"""
IndexNow Batch Submission Script
Submits all your sites to IndexNow after you've added the verification keys
"""

import requests
import json

# Load keys
with open('/root/.openclaw/workspace/indexnow_keys.json', 'r') as f:
    sites = json.load(f)

def submit_to_indexnow(domain, key, urls):
    """Submit URLs to IndexNow API"""
    endpoint = "https://www.indexnow.org/indexnow"

    payload = {
        "host": domain,
        "key": key,
        "urlList": urls
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        return {
            "success": response.status_code == 200,
            "status": response.status_code,
            "response": response.text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def submit_all_sites():
    """Submit all sites with their homepages"""
    results = {}

    print("🚀 SUBMITTING TO INDEXNOW")
    print("="*80)
    print()

    for domain, key in sites.items():
        # Submit homepage
        urls = [f"https://{domain}/"]

        print(f"Submitting: {domain}")
        print(f"Key: {key}")

        result = submit_to_indexnow(domain, key, urls)
        results[domain] = result

        if result.get("success"):
            print(f"✅ SUCCESS - HTTP 200")
        else:
            print(f"❌ FAILED - {result.get('error', result.get('status'))}")

        print()

    print("="*80)
    print(f"✅ Submitted: {sum(1 for r in results.values() if r.get('success'))}/{len(sites)}")
    print()

    # Save results
    with open('/root/.openclaw/workspace/indexnow_submission_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("📊 Results saved to: indexnow_submission_results.json")
    print()
    print("⏰ Expected indexing: 24-48 hours")
    print()

    return results

if __name__ == "__main__":
    print("INDEXNOW BATCH SUBMISSION")
    print("="*80)
    print()
    print("⚠️ BEFORE RUNNING:")
    print("   1. Add meta tags or .txt files to verify ownership")
    print("   2. Wait 5-10 minutes for verification to propagate")
    print("   3. Then run this script")
    print()
    print("="*80)
    print()

    # Show what will be submitted
    print("Sites to submit:")
    for domain, key in sites.items():
        print(f"  - {domain}")
    print()

    input("Press Enter to continue...")

    submit_all_sites()
