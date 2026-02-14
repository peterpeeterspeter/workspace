#!/usr/bin/env python3
"""
Add Internal Links to Cardfair.com Posts
Updates posts to include internal links to pillar pages
"""

import requests
import json
import re

WP_URL = "https://cardfair.com/wp-json/wp/v2"
AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Internal links to add
INTERNAL_LINKS = {
    # Links to /secured-credit-cards/
    1333: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "consider"
    },
    1331: {
        "anchor": "secured cards for bad credit",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "rebuilding"
    },
    1327: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "tools"
    },
    1325: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "alternatives"
    },
    1318: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "solutions"
    },
    1312: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "options"
    },
    1300: {
        "anchor": "secured credit cards",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "consolidation"
    },
    1299: {
        "anchor": "secured cards for bad credit",
        "url": "https://www.cardfair.com/secured-credit-cards/",
        "context": "loans"
    },

    # Links to /rebuild-credit-after-bankruptcy/
    1326: {
        "anchor": "rebuild credit after bankruptcy",
        "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/",
        "context": "similar"
    },
    1309: {
        "anchor": "rebuild credit after bankruptcy",
        "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/",
        "context": "recovery"
    },
    1313: {
        "anchor": "rebuilding credit after bankruptcy",
        "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/",
        "context": "strategy"
    },
    1324: {
        "anchor": "rebuild credit after bankruptcy",
        "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/",
        "context": "credit"
    },
    1330: {
        "anchor": "rebuild credit after bankruptcy",
        "url": "https://www.cardfair.com/rebuild-credit-after-bankruptcy/",
        "context": "timeline"
    }
}

def get_post_content(post_id):
    """Fetch current post content"""
    url = f"{WP_URL}/posts/{post_id}"
    response = requests.get(url, auth=AUTH, timeout=10)

    if response.status_code == 200:
        return response.json()
    return None

def add_internal_link(content, link_data):
    """Smart internal link insertion - finds best context"""
    anchor = link_data["anchor"]
    url = link_data["url"]
    context = link_data["context"]

    # Create the link HTML
    link_html = f'<a href="{url}">{anchor}</a>'

    # Try to find a good insertion point
    # Look for paragraphs related to the context
    context_patterns = {
        "consider": r"(consider|look into|options include)",
        "rebuilding": r"(rebuilding|improving|boosting)",
        "tools": r"(tools|methods|strategies)",
        "alternatives": r"(alternatives|options|consider)",
        "solutions": r"(solutions|options|available)",
        "options": r"(options|choices|alternatives)",
        "consolidation": r"(consolidation|managing|debt)",
        "loans": r"(loans|credit|financing)",
        "similar": r"(similar|like|comparable)",
        "recovery": r"(recovery|recovering|after)",
        "strategy": r"(strategy|approach|method)",
        "credit": r"(credit|score|rating)",
        "timeline": r"(timeline|process|steps)"
    }

    pattern = context_patterns.get(context, r"(credit|score|rebuilding)")

    # Find a paragraph with the context word
    paragraphs = content.split('\n\n')
    for i, para in enumerate(paragraphs):
        if re.search(pattern, para, re.IGNORECASE) and len(para) > 100:
            # Insert link at end of a sentence in this paragraph
            if '.' in para:
                # Split by sentences and add link to first suitable sentence
                sentences = para.split('. ')
                if len(sentences) > 1:
                    # Add to first sentence that's not too short
                    for j, sent in enumerate(sentences):
                        if len(sent) > 30 and '<a' not in sent:
                            sentences[j] = sent + f' Learn more about {link_html}.'
                            paragraphs[i] = '. '.join(sentences)
                            return '\n\n'.join(paragraphs)

    # If no good spot found, append to content
    return f"{content}\n\n<p>Related: {link_html}</p>"

def update_post_with_link(post_id, link_data):
    """Update post with internal link"""
    post = get_post_content(post_id)

    if not post:
        return {
            "success": False,
            "post_id": post_id,
            "error": "Post not found"
        }

    # Get current content
    content = post.get('content', {}).get('rendered', '')
    title = post.get('title', {}).get('rendered', '')

    # Don't add if link already exists
    if link_data["url"] in content:
        return {
            "success": True,
            "post_id": post_id,
            "title": title[:50],
            "note": "Link already exists"
        }

    # Add the internal link
    updated_content = add_internal_link(content, link_data)

    # Update the post
    url = f"{WP_URL}/posts/{post_id}"
    payload = {
        "content": updated_content
    }

    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=10)

        if response.status_code == 200:
            return {
                "success": True,
                "post_id": post_id,
                "title": title[:50] + "...",
                "anchor": link_data["anchor"]
            }
        else:
            return {
                "success": False,
                "post_id": post_id,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "post_id": post_id,
            "error": str(e)
        }

def main():
    print("="*80)
    print("🔗 ADDING INTERNAL LINKS TO CARDFAIR.COM")
    print("="*80)
    print()

    results = []

    for post_id, link_data in INTERNAL_LINKS.items():
        print(f"Updating post {post_id}...")
        print(f"  Anchor: '{link_data['anchor']}'")
        print(f"  Target: {link_data['url']}")

        result = update_post_with_link(post_id, link_data)
        results.append(result)

        if result["success"]:
            print(f"  ✅ {result.get('note', 'SUCCESS')}")
        else:
            print(f"  ❌ ERROR: {result.get('error')}")

        print()

    print("="*80)
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Successfully added: {success_count}/{len(results)} internal links")
    print("="*80)

    # Save results
    with open('/root/.openclaw/workspace/internal_links_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Results saved to: internal_links_results.json")

    # Summary
    print("\n📋 LINKS ADDED:")
    print("-"*80)
    secured_count = sum(1 for r in results if r["success"] and "secured" in r.get("anchor", ""))
    rebuild_count = sum(1 for r in results if r["success"] and "rebuild" in r.get("anchor", ""))
    print(f"✅ Links to /secured-credit-cards/: {secured_count}")
    print(f"✅ Links to /rebuild-credit-after-bankruptcy/: {rebuild_count}")

if __name__ == "__main__":
    main()
