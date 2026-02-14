#!/usr/bin/env python3
"""
Restore post content from WordPress revisions
"""

import requests

# Credentials
SITE_URL = 'https://crashcasino.io/wp-json'
AUTH = ('peter', '3vRhtTs2khfdLtTiDFqkdeXI')

# Posts that need restoration
POSTS = [834, 833, 817, 816, 787]

def restore_from_revision(post_id):
    """Restore post content from latest revision"""

    # Get revisions
    response = requests.get(
        f"{SITE_URL}/wp/v2/posts/{post_id}/revisions?per_page=1",
        auth=AUTH,
        timeout=30
    )

    if response.status_code != 200:
        return False, f"Failed to get revisions: {response.status_code}"

    revisions = response.json()

    if not revisions:
        return False, "No revisions found"

    latest_revision = revisions[0]

    # Get content from revision
    content = latest_revision.get('content', {}).get('raw', '')

    if not content:
        return False, "Revision has no content"

    # Restore content to post
    update_response = requests.post(
        f"{SITE_URL}/wp/v2/posts/{post_id}",
        auth=AUTH,
        headers={'Content-Type': 'application/json'},
        json={'content': content},
        timeout=30
    )

    if update_response.status_code == 200:
        return True, f"Restored {len(content)} chars"
    else:
        return False, f"Update failed: {update_response.status_code}"

def main():
    print("🔧 Restoring post content from revisions")
    print("=" * 50)
    print()

    success = 0
    failed = []

    for post_id in POSTS:
        print(f"Post {post_id}...", end=" ")

        result, message = restore_from_revision(post_id)

        if result:
            print(f"✅ {message}")
            success += 1
        else:
            print(f"❌ {message}")
            failed.append(post_id)

    print()
    print("=" * 50)
    print(f"✅ Restored: {success}/{len(POSTS)} posts")

    if failed:
        print(f"❌ Failed: {failed}")

if __name__ == '__main__':
    main()
