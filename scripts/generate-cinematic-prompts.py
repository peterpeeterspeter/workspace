#!/usr/bin/env python3
"""
Generate cinematic, detailed prompts for Nano Banana Pro (Gemini 3 Pro Image Preview)
Includes camera angles, lighting, scene composition, mood
"""

import json
import random

def get_camerawork(topic_type):
    """Define camera angle and shot type based on topic"""

    cameras = {
        'trust': [
            "wide angle shot, eye-level camera, balanced composition",
            "medium shot, slightly low angle to convey authority",
            "establishing shot, sweeping camera movement from left to right"
        ],
        'bonus': [
            "dynamic angle, low camera looking up at celebration, energetic feel",
            "close-up on falling coins, shallow depth of field",
            "overhead shot looking down on gift boxes, bird's eye view"
        ],
        'strategy': [
            "medium shot, straight-on camera, analytical viewpoint",
            "slightly elevated angle looking down at charts, professional perspective",
            "two-shot composition showing both player and screen, side angle"
        ],
        'crypto': [
            "futuristic camera angle, Dutch tilt for dynamic energy",
            "extreme wide shot showing blockchain network, epic scale",
            "macro shot on Bitcoin symbol, intricate detail focus"
        ],
        'global': [
            "epic wide shot, globe-centered composition, cinematic scope",
            "aerial view, high angle showing world map, grand perspective",
            "establishing shot with camera pan across diverse scenes"
        ],
        'review': [
            "medium close-up, centered composition, professional headshot style",
            "three-quarter angle, product photography lighting",
            "straight-on camera, symmetrical balance, authoritative feel"
        ],
        'tutorial': [
            "medium shot, instructional viewpoint, clear visibility",
            "slightly high angle, teacher-to-student perspective",
            "over-the-shoulder shot, relatable learning context"
        ]
    }

    return random.choice(cameras.get(topic_type, cameras['trust']))

def get_lighting(topic_type):
    """Define lighting based on topic mood"""

    lighting = {
        'trust': "soft professional lighting, cool blue-white key light, subtle rim light for depth",
        'bonus': "warm golden lighting, celebratory bright key light, sparkler bokeh effects",
        'strategy': "clean clinical lighting, neutral white balance, high contrast for data clarity",
        'crypto': "neon purple and cyan lighting, cyberpunk glow, dramatic rim lighting",
        'global': "natural daylight simulation, soft global illumination, warm ambient fill",
        'review': "studio lighting, softbox setup, professional product photography quality",
        'tutorial': "bright even lighting, classroom-style illumination, friendly and approachable"
    }

    return lighting.get(topic_type, lighting['trust'])

def get_scene_description(title, topic_type):
    """Describe the scene with specific visual elements"""

    title_lower = title.lower()

    if topic_type == 'trust':
        if any(kw in title_lower for kw in ['rigged', 'scam']):
            return "central shield emblem with padlock, background of blockchain network nodes, verification checkmarks floating around, holographic data streams, secure fortress imagery, protective bubble effect"
        else:
            return "trust scale balancing weights, fairness gavel and scales, secure vault door opening, certification badges arranged in arc, hand shaking illustration, transparency glass panel with data visible"

    elif topic_type == 'bonus':
        return "golden coins and bonus symbols raining from top, gift boxes exploding with confetti, celebratory fireworks in background, treasure chest overflowing, winning moment freeze-frame, jackpot machine display showing big win, champagne bottle popping"

    elif topic_type == 'strategy':
        return "multiplier graph climbing steeply upward, player hand hovering over cashout button, profit calculator dashboard with green numbers, strategy whiteboard with diagrams, winning trajectory line chart, analytical metrics overlay, timing stopwatch visual"

    elif topic_type == 'crypto':
        return "Bitcoin logo glowing with neon outline, Ethereum symbol nearby, blockchain network web connecting nodes, cryptocurrency wallet interface, futuristic digital casino floor, holographic coin displays, QR code patterns, decentralized network visualization"

    elif topic_type == 'global':
        return "rotating Earth globe with connection lines, diverse player silhouettes from different cultures, world map with hotspots, flags of major countries subtly integrated, international airport departure board style, multilingual welcome signs, global community gathering"

    elif topic_type == 'review':
        return "trophy pedestal with gold medal, five-star rating display prominent, comparison table visual, podium with top 3 positions, expert reviewer silhouette with clipboard, award ribbon graphics, 'BEST' badge centerpiece, trust seal stamps"

    elif topic_type == 'tutorial':
        return "step-by-step infographic flowchart, numbered checklist items, help question mark icons, tutorial progress bar, easy-to-read font hierarchy, beginner-friendly icons, learning path roadmap, hand-drawn arrow indicators, 'how-to' book open"

    else:
        return "crash game rocket launching upward, multiplier curve soaring, casino chips flying, betting grid visible, player winning moment, explosive energy, dynamic motion lines, action-packed gaming scene"

def generate_cinematic_prompt(title, site):
    """Generate full cinematic prompt with camera, lighting, and scene"""

    title_lower = title.lower()

    # Determine topic type
    if any(kw in title_lower for kw in ['rigged', 'fairness', 'verify', 'scam', 'legit', 'safe', 'trust']):
        topic_type = 'trust'
    elif any(kw in title_lower for kw in ['bonus', 'codes', 'free', 'promo', 'offer']):
        topic_type = 'bonus'
    elif any(kw in title_lower for kw in ['strategy', 'cashout', 'mistakes', 'win', 'profit', 'how to', 'guide']):
        topic_type = 'strategy'
    elif any(kw in title_lower for kw in ['bitcoin', 'crypto', 'no-kyc', 'anonymous', 'vpn', 'blockchain']):
        topic_type = 'crypto'
    elif any(kw in title_lower for kw in ['india', 'chinese', 'german', 'global', 'worldwide', 'singapore']):
        topic_type = 'global'
    elif any(kw in title_lower for kw in ['rate', 'review', 'best', 'top', 'ranking']):
        topic_type = 'review'
    elif any(kw in title_lower for kw in ['beginner', '101', 'tutorial', 'learn']):
        topic_type = 'tutorial'
    else:
        topic_type = 'trust'  # default

    # Build cinematic prompt
    camerawork = get_camerawork(topic_type)
    lighting = get_lighting(topic_type)
    scene = get_scene_description(title, topic_type)

    # Combine into full prompt
    prompt = f"""cinematic digital illustration, {camerawork}. {lighting}. Scene: {scene}. High-end production quality, 4K resolution, photorealistic rendering, professional photography aesthetic. Crisp focus, vibrant colors, polished finish. Commercial advertising photography style, premium brand quality."""

    return prompt

def main():
    # Load original posts
    input_file = '/root/.openclaw/workspace/temp/missing-images.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    print("🎬 Generating cinematic prompts for Nano Banana Pro")
    print("=" * 70)
    print()

    # Update each post with cinematic prompt
    for i, post in enumerate(posts, 1):
        cinematic_prompt = generate_cinematic_prompt(post['title'], post['site'])

        post['cinematic_prompt'] = cinematic_prompt

        # Show sample
        if i <= 3 or i % 10 == 0:  # Show first 3 and every 10th
            print(f"[{i}/{len(posts)}] {post['site']}/{post['post_id']}")
            print(f"  Title: {post['title'][:70]}...")
            print(f"  Prompt: {cinematic_prompt[:150]}...")
            print()

    # Save cinematic prompts
    output_file = '/root/.openclaw/workspace/temp/missing-images-cinematic.json'
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print("=" * 70)
    print(f"✅ Cinematic prompts saved to: {output_file}")
    print()
    print("Cinematic elements added:")
    print("• Camera angles and shot types (wide, close-up, overhead, Dutch tilt)")
    print("• Professional lighting setups (softbox, neon, studio, natural)")
    print("• Detailed scene descriptions with specific visual elements")
    print("• Photorealistic rendering and production quality")
    print()
    print("Ready for Nano Banana Pro generation:")
    print("  python3 /root/.openclaw/workspace/scripts/generate-images-cinematic.py")

if __name__ == '__main__':
    main()
