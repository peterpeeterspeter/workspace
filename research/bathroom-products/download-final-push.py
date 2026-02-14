#!/usr/bin/env python3
import requests, os, time

base = "/root/.openclaw/workspace/research/bathroom-products/raw-images"

# Even more URLs to push toward better balance
final_urls = {
    'faucets': [
        'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=800',
        'https://images.unsplash.com/photo-1585704032871-d6afa36313c4?w=800',
        'https://images.unsplash.com/photo-1604762584865-43b6e2b9b5d5?w=800',
        'https://images.unsplash.com/photo-1584622650111-996317b8d101?w=800',
    ],
    'showers': [
        'https://images.unsplash.com/photo-1584622650345-67b45c1d1f2a?w=800',
        'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=800',
        'https://images.unsplash.com/photo-1584622650123-8b45c9fc7ef8?w=800',
        'https://images.unsplash.com/photo-1584622650456-9c85e0a1e6f3?w=800',
    ],
    'lighting': [
        'https://images.unsplash.com/photo-1513506003781-012925fcd71c?w=800',
        'https://images.unsplash.com/photo-1560387644718-e1b96c649ed?w=800',
        'https://images.unsplash.com/photo-1558171993-7ab85c8892c1?w=800',
        'https://images.unsplash.com/photo-1558171993-7ab85c8892c1?w=800',
    ],
    'tile': [
        'https://images.unsplash.com/photo-1600585154045-a3e8a8a6d36?w=800',
        'https://images.unsplash.com/photo-1600585154567-8e8f8b7d5c3?w=800',
        'https://images.unsplash.com/photo-1600566753600-5d7e8c18ea9?w=800',
        'https://images.unsplash.com/photo-1600585154432-c008f0ad7e8?w=800',
    ],
    'bathtub': [
        'https://images.unsplash.com/photo-1600217438822-5c40d6617d89?w=800',
        'https://images.unsplash.com/photo-1584622650456-9c85e0a1e6f3?w=800',
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
        'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',
    ]
}

def download(url, path):
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200 and len(r.content) > 10000:
            open(path, 'wb').write(r.content)
            return True
    except: pass
    return False

downloaded = 0
for cat, urls in final_urls.items():
    cat_dir = f"{base}/{cat}/budget"
    os.makedirs(cat_dir, exist_ok=True)

    for url in urls:
        existing = len([f for f in os.listdir(cat_dir) if f.startswith('essential-line')])
        fname = f"essential-line-{cat}-{existing+1}.jpg"
        path = os.path.join(cat_dir, fname)

        if os.path.exists(path):
            continue

        if download(url, path):
            downloaded += 1
            print(f"✓ {cat}: {existing+1}")
        time.sleep(0.25)

print(f"\n✅ Downloaded {downloaded} images")
