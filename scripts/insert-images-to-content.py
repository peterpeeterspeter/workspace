#!/usr/bin/env python3
"""
Insert featured images into post content
Adds image at the beginning of each post
"""

import json
import os
import requests

# Site credentials
SITES = {
    'crashcasino': {
        'url': 'https://crashcasino.io/wp-json',
        'user': 'peter',
        'pass': '3vRhtTs2khfdLtTiDFqkdeXI'
    },
    'crashgame': {
        'url': 'https://crashgamegambling.com/wp-json',
        'user': '@peter',
        'pass': 'MioX SygN Xaz6 pK9o RUiK tBMF'
    },
    'freecrash': {
        'url': 'https://freecrashgames.com/wp-json',
        'user': '@peter',
        'pass': 'F8Mg yZXM qJy4 jQvp BMeZ FoMG'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'user': '@peter',
        'pass': 'R3kQ 6vRA UwYd x7Cn KEtT Pk83'
    }
}

def insert_image_to_content(site_key, media_id, post_id):
    """Insert featured image into post content"""

    if site_key not in SITES:
        return False, f"Unknown site: {site_key}"

    site = SITES[site_key]
    api_url = site['url']

    print(f"    → Inserting image into post {post_id}...")

    try:
        # Get current post
        post_url = f"{api_url}/wp/v2/posts/{post_id}"
        response = requests.get(post_url, auth=(site['user'], site['pass']), timeout=30)

        if response.status_code != 200:
            return False, f"Failed to fetch post: {response.status_code}"

        post_data = response.json()

        # Get media details
        media_url = f"{api_url}/wp/v2/media/{media_id}"
        media_response = requests.get(media_url, auth=(site['user'], site['pass']), timeout=30)

        if media_response.status_code != 200:
            return False, f"Failed to fetch media: {media_response.status_code}"

        media_data = media_response.json()
        image_url = media_data.get('source_url')
        alt_text = media_data.get('alt_text', '')

        # Build HTML for image insertion
        image_html = f'<figure class="featured-image-article"><img src="{image_url}" alt="{alt_text}" class="wp-post-image" /></figure>\n\n'

        # Get current content (raw, not rendered)
        current_content = post_data.get('content', {}).get('raw', '')

        # Check if image is already in content
        if image_url in current_content:
            print(f"    ✓ Image already in content")
            return True, "Already inserted"

        # Prepend image to content
        new_content = image_html + current_content

        # Update post
        update_response = requests.post(
            post_url,
            auth=(site['user'], site['pass']),
            headers={'Content-Type': 'application/json'},
            json={'content': new_content},
            timeout=30
        )

        if update_response.status_code == 200:
            print(f"    ✓ Image inserted into content")
            return True, "Success"
        else:
            return False, f"Update failed: {update_response.status_code} - {update_response.text}"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Load uploaded test batch JSON
    input_file = '/root/.openclaw/workspace/temp/missing-images-test-uploaded.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    # Filter posts that were uploaded successfully
    ready_posts = [p for p in posts if p.get('upload_status') == 'uploaded']

    print(f"📝 Inserting images into {len(ready_posts)} posts")
    print(f"Adding featured image HTML to post content")
    print()

    success_count = 0
    failed_posts = []

    for i, post in enumerate(ready_posts, 1):
        print(f"[{i}/{len(ready_posts)}] {post['site']} - Post {post['post_id']}")
        print(f"  Title: {post['title'][:60]}...")

        # Get media_id from the upload results
        # We need to fetch the post to get the featured_media ID
        site = SITES[post['site']]
        api_url = site['url']

        try:
            response = requests.get(
                f"{api_url}/wp/v2/posts/{post['post_id']}",
                auth=(site['user'], site['pass']),
                timeout=30
            )

            if response.status_code == 200:
                post_data = response.json()
                media_id = post_data.get('featured_media')

                if media_id and media_id > 0:
                    # Insert image into content
                    success, output = insert_image_to_content(
                        post['site'],
                        media_id,
                        post['post_id']
                    )

                    if success:
                        post['content_insertion'] = 'success'
                        success_count += 1
                    else:
                        post['content_insertion'] = 'failed'
                        post['insertion_error'] = output
                        failed_posts.append(post)
                else:
                    print(f"    ⚠️ No featured media set")
                    post['content_insertion'] = 'skipped'
                    post['insertion_error'] = 'No featured media'
            else:
                print(f"    ❌ Failed to fetch post")
                post['content_insertion'] = 'failed'
                post['insertion_error'] = 'Failed to fetch post'
                failed_posts.append(post)

        except Exception as e:
            print(f"    ❌ {str(e)}")
            post['content_insertion'] = 'failed'
            post['insertion_error'] = str(e)
            failed_posts.append(post)

        print()

    # Save updated JSON
    output_file = input_file.replace('-test-uploaded.json', '-test-complete.json')
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    # Summary
    print("=" * 50)
    print(f"✅ Successfully inserted: {success_count}/{len(ready_posts)} images")
    print(f"❌ Failed: {len(failed_posts)} insertions")
    print(f"📁 Log: {output_file}")
    print()

    if failed_posts:
        print("Failed insertions:")
        for post in failed_posts:
            print(f"  - {post['site']}/{post['post_id']}: {post.get('insertion_error', 'Unknown error')}")
    else:
        print("✨ All images inserted into post content!")
        print()
        print("Check the posts now - images should be visible:")
        for post in ready_posts:
            print(f"   - {post['url']}")

if __name__ == '__main__':
    main()
