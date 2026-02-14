#!/usr/bin/env python3
import json
import subprocess
import os

with open('metadata/duravit-image-urls.json', 'r') as f:
    data = json.load(f)

shower_imgs = [img for img in data['images'] if 'shower' in img['url'].lower()][:10]
bath_imgs = [img for img in data['images'] if 'bath' in img['url'].lower() or 'tub' in img['url'].lower()][:10]

def download(images, category):
    downloaded = 0
    for img in images:
        if downloaded >= 6:
            break
        url = img['url']
        fname = url.split('/')[-1].split('?')[0][:35]
        path = f"raw-images/{category}/premium/duravit-{fname}"
        
        if os.path.exists(path):
            continue
        
        try:
            subprocess.run(['wget', '-q', '-O', path, url, '--timeout=8'], 
                           capture_output=True, timeout=12)
            if os.path.exists(path) and os.path.getsize(path) > 10000:
                downloaded += 1
                print(f"{category}: {downloaded}/6")
        except:
            pass

download(shower_imgs, 'showers')
download(bath_imgs, 'bathtub')
print("Done!")
