#!/usr/bin/env python3
"""
Automated Indexing Submission Script
Submits sitemaps and URLs to Google, Bing, and IndexNow
"""

import requests
import json
from typing import List

class IndexingSubmitter:
    def __init__(self):
        self.sites = [
            "https://devismaison.com",
            "https://sostoitures.com",
            "https://comparateurdepret.com",
            "https://pintoresdecasas.com",
            "https://abogadospenal.com"
        ]

    def submit_google_ping(self, sitemap_url: str) -> bool:
        """Submit sitemap to Google via ping"""
        ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
        try:
            response = requests.get(ping_url, timeout=10)
            return response.status_code == 200
        except:
            return False

    def submit_indexnow(self, url: str, key: str) -> bool:
        """Submit URL to IndexNow"""
        endpoint = "https://www.indexnow.org/indexnow"
        payload = {
            "host": url.replace('https://', '').replace('http://', ''),
            "key": key,
            "urlList": [url]
        }
        try:
            response = requests.post(endpoint, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False

    def batch_submit_indexnow(self, key: str) -> dict:
        """Submit all sites to IndexNow in batch"""
        results = {}
        for site in self.sites:
            success = self.submit_indexnow(site, key)
            results[site] = success
        return results

    def submit_all_google_pings(self) -> dict:
        """Submit all sitemaps to Google"""
        results = {}
        for site in self.sites:
            sitemap = f"{site}/sitemap.xml"
            success = self.submit_google_ping(sitemap)
            results[site] = success
        return results

    def generate_indexnow_batch(self, key: str) -> str:
        """Generate IndexNow batch submission for all URLs"""
        url_list = []
        for site in self.sites:
            url_list.append(site)
            url_list.append(f"{site}/about")
            url_list.append(f"{site}/contact")

        payload = {
            "host": self.sites[0].replace('https://', '').replace('http://', ''),
            "key": key,
            "urlList": url_list
        }

        return json.dumps(payload, indent=2)

# Instructions
if __name__ == "__main__":
    print("="*80)
    print("AUTOMATED INDEXING SUBMISSION TOOL")
    print("="*80)
    print()
    print("This script will:")
    print("1. Submit all 5 sitemaps to Google via ping")
    print("2. Generate IndexNow batch submission")
    print("3. Provide instructions for Search Console")
    print()
    print("="*80)
    print()
    print("STEP 1: GOOGLE PING (Automatic)")
    print("-"*80)
    print()
    print("Run this to submit sitemaps to Google:")
    print()
    print("python3 indexing_submitter.py --google-ping")
    print()
    print("="*80)
    print()
    print("STEP 2: INDEXNOW (Needs API Key)")
    print("-"*80)
    print()
    print("1. Get IndexNow key: https://www.indexnow.org/")
    print("2. Add key to your sites (meta tag or file)")
    print("3. Run: python3 indexing_submitter.py --indexnow YOUR_KEY")
    print()
    print("="*80)
    print()
    print("STEP 3: SEARCH CONSOLE (Manual - Required)")
    print("-"*80)
    print()
    print("For each site:")
    print("1. Go to: https://search.google.com/search-console")
    print("2. Add property")
    print("3. Verify ownership (HTML file recommended)")
    print("4. Submit sitemap: /sitemap.xml")
    print()
    print("="*80)
    print()
    print("Sites to index:")
    print()
    for site in ["https://devismaison.com", "https://sostoitures.com",
                 "https://comparateurdepret.com", "https://pintoresdecasas.com",
                 "https://abogadospenal.com"]:
        print(f"  - {site}")
    print()
    print("Sitemaps:")
    print()
    for site in ["https://devismaison.com", "https://sostoitures.com",
                 "https://comparateurdepret.com", "https://pintoresdecasas.com",
                 "https://abogadospenal.com"]:
        print(f"  - {site}/sitemap.xml")
    print()
