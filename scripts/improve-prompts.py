#!/usr/bin/env python3
"""
Generate improved prompts for crash casino featured images
More descriptive, thematic, and visually specific
"""

import json

def generate_improved_prompt(title, site):
    """Generate detailed, high-quality prompt based on article topic"""

    title_lower = title.lower()

    # Base style and quality keywords
    base_quality = "professional digital illustration, high quality, 4K, vibrant colors, modern design"

    # Crash game visual elements
    crash_elements = "crash game multiplier curve, rocket trajectory ascending, graph showing exponential growth, casino chips, betting interface"

    # Topic-specific prompts
    if any(kw in title_lower for kw in ['rigged', 'fairness', 'verify', 'scam', 'legit']):
        return f"{base_quality}, {crash_elements}, trust and security theme. Shield icon, padlock, verification checkmark, green and blue color palette representing trust and safety. Professional infographic style with blockchain network pattern in background. Clean, authoritative design."

    elif any(kw in title_lower for kw in ['bonus', 'codes', 'free', 'promo', 'offer']):
        return f"{base_quality}, {crash_elements}, celebration and rewards theme. Gift boxes, golden coins falling, bonus confetti, vibrant gold and green colors. Exciting promotional atmosphere with sparkle effects and winning celebration imagery."

    elif any(kw in title_lower for kw in ['strategy', 'cashout', 'mistakes', 'win', 'profit', 'how to']):
        return f"{base_quality}, {crash_elements}, strategic gameplay theme. Upward trending charts, profit arrows, successful cashout moment, player winning. Professional business illustration with data visualization, analytics dashboard style, blue and purple gradient."

    elif any(kw in title_lower for kw in ['bitcoin', 'crypto', 'no-kyc', 'anonymous', 'vpn', 'blockchain']):
        return f"{base_quality}, {crash_elements}, cryptocurrency theme. Bitcoin symbols, blockchain network nodes, futuristic tech aesthetic, purple and teal neon colors. Modern crypto gambling platform interface with digital currency elements."

    elif any(kw in title_lower for kw in ['india', 'chinese', 'german', 'global', 'worldwide', 'players']):
        return f"{base_quality}, {crash_elements}, international gaming theme. Globe with connection lines, diverse players, multicultural elements, world map background. Inclusive, global community atmosphere with warm welcoming colors."

    elif any(kw in title_lower for kw in ['rate', 'review', 'best', 'top', 'ranking']):
        return f"{base_quality}, {crash_elements}, expert review and rating theme. Star ratings, trophy icons, ranking podium, award badges. Professional review site aesthetic with gold medals and premium quality indicators. Trustworthy comparison style."

    elif any(kw in title_lower for kw in ['beginner', 'guide', '101', 'tutorial', 'learn', 'how to']):
        return f"{base_quality}, {crash_elements}, educational guide theme. Tutorial infographic style, step-by-step visual indicators, help icons, clean organized layout. Learning-friendly design with soft approachable colors, instructional diagrams."

    else:
        # Generic crash casino theme
        return f"{base_quality}, {crash_elements}, dynamic crash gambling scene. Multiplier graph soaring, exciting gameplay moment, casino gaming atmosphere. Energetic composition with action-packed visuals, modern gambling platform aesthetic."

def main():
    # Load original posts
    input_file = '/root/.openclaw/workspace/temp/missing-images.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    print("📝 Improving prompts for better image quality")
    print("=" * 60)
    print()

    # Update each post with improved prompt
    for i, post in enumerate(posts, 1):
        old_prompt = post['prompt']
        new_prompt = generate_improved_prompt(post['title'], post['site'])

        post['original_prompt'] = old_prompt
        post['prompt'] = new_prompt

        print(f"[{i}/{len(posts)}] {post['site']}/{post['post_id']}")
        print(f"  Title: {post['title'][:70]}...")
        print(f"  OLD: {old_prompt[:80]}...")
        print(f"  NEW: {new_prompt[:100]}...")
        print()

    # Save improved prompts
    output_file = '/root/.openclaw/workspace/temp/missing-images-improved.json'
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print("=" * 60)
    print(f"✅ Improved prompts saved to: {output_file}")
    print()
    print("Key improvements:")
    print("• More descriptive visual elements")
    print("• Topic-specific styling and colors")
    print("• Better mood and atmosphere")
    print("• Higher quality keywords")
    print()
    print("Next: Regenerate images with improved prompts")
    print("  python3 /root/.openclaw/workspace/scripts/generate-images-improved.py")

if __name__ == '__main__':
    main()
