#!/usr/bin/env python3
"""
Debug and upload remaining landing pages
"""

import json
import subprocess

def upload_with_debug(site_name, url, user, password, page_id, html_file, title):
    """Upload landing page with detailed debugging"""
    print(f"\n{'='*60}")
    print(f"Uploading: {site_name}")
    print(f"{'='*60}")

    # Read HTML
    with open(html_file, 'r') as f:
        html_content = f.read()

    print(f"HTML file: {html_file}")
    print(f"HTML length: {len(html_content)} chars")
    print(f"Page ID: {page_id}")

    # Prepare payload
    payload = {
        "title": title,
        "content": html_content,
        "status": "publish"
    }

    # Build curl command
    curl_cmd = [
        'curl', '-v',  # Verbose to see what's happening
        '-X', 'POST',
        f"{url}/wp/v2/pages/{page_id}",
        '-u', f"{user}:{password}",
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]

    print(f"\nExecuting curl...")
    print(f"URL: {url}/wp/v2/pages/{page_id}")

    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)

    print(f"\nReturn code: {result.returncode}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"Stderr length: {len(result.stderr)}")

    if result.stderr:
        print(f"\nStderr (first 500 chars):")
        print(result.stderr[:500])

    if result.stdout:
        print(f"\nStdout (first 500 chars):")
        print(result.stdout[:500])

    # Try to parse response
    try:
        if result.stdout.strip():
            response = json.loads(result.stdout)
            if 'id' in response:
                print(f"\n✅ SUCCESS!")
                print(f"   Page ID: {response['id']}")
                print(f"   URL: {response.get('link', 'N/A')}")
                return True
            else:
                print(f"\n❌ API Error: {response}")
                return False
        else:
            print(f"\n❌ Empty response from server")
            print(f"   Return code: {result.returncode}")
            return False
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Parse Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

# Upload cryptocrash
success1 = upload_with_debug(
    "cryptocrashgambling.com",
    "https://cryptocrashgambling.com/wp-json",
    "@peter",
    "R3kQ 6vRA UwYd x7Cn KEtT Pk83",
    "17869",
    "/root/.openclaw/workspace/tasks/cryptocrash-landing.html",
    "Crypto Crash Gambling - Bitcoin, ETH, USDT"
)

# Upload crashgamegambling
success2 = upload_with_debug(
    "crashgamegambling.com",
    "https://crashgamegambling.com/wp-json",
    "@peter",
    "MioX SygN Xaz6 pK9o RUiK tBMF",
    "49036",
    "/root/.openclaw/workspace/tasks/crashgamegambling-landing.html",
    "Master Crash Gambling - From Beginner to Pro"
)

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"cryptocrash: {'✅ Success' if success1 else '❌ Failed'}")
print(f"crashgamegambling: {'✅ Success' if success2 else '❌ Failed'}")
