#!/usr/bin/env python3
"""
Create custom prompts for each article based on title analysis
Unique, specific prompts for every article
"""

import json

def create_custom_prompt(post):
    """Create unique prompt based on article title"""

    title = post['title']
    title_lower = title.lower()

    # Base quality
    base = "cinematic digital illustration, 4K, professional photography quality, commercial advertising style"

    # --- TRUST & FAIRNESS ARTICLES ---
    if 'rigged' in title_lower and 'fairness' in title_lower:
        prompt = f"""{base}. Wide establishing shot, eye-level camera. Soft blue-white professional lighting with subtle rim light.
Scene: Split composition showing two contrasting worlds - left side shows transparent blockchain verification with glowing green checkmarks and shield icons, right side shows murky suspicious elements with warning symbols. Central scale balancing truth vs deception. Cool blue and green color palette with warm amber accents on warning symbols. Trustworthy, authoritative mood."""

    elif 'how we rate' in title_lower and 'transparency' in title_lower:
        prompt = f"""{base}. Medium shot with straight-on camera, symmetrical composition. Studio lighting with softbox setup.
Scene: Professional review workspace with magnifying glass revealing detailed star rating system, transparency glass panels showing backend review process, clipboard with checklist visible, trust seals arranged in arc. Gold and white color scheme with blue accent. Authoritative, transparent mood."""

    elif 'verify crash game fairness' in title_lower:
        prompt = f"""{base}. Medium shot, slightly low angle conveying authority. Cool blue-white professional lighting.
Scene: Technical verification interface showing hash algorithm visualization, blockchain confirmation nodes, padlock unlocking mechanism, fairness certificate with holographic seal. Green and blue cyber aesthetic with glowing elements. Technical, secure mood."""

    elif 'crash gambling scams' in title_lower:
        prompt = f"""{base}. Dramatic low angle shot, Dutch tilt for tension. High contrast lighting with red warning glow.
Scene: Split scene - top shows red flag warnings, shield blocking threats, user protected behind safety glass; bottom shows scammer silhouettes being blocked. Alert system interface with threat indicators. Red, amber, and black color scheme. Protective, vigilant mood."""

    elif 'red flags' in title_lower or 'rogue site' in title_lower:
        prompt = f"""{base}. Medium close-up, direct eye contact. Dramatic side lighting creating shadows.
Scene: Seven red flags arranged in semi-circle, each flag showing different warning sign (fake license, no SSL, slow withdrawals, etc.), central shield protecting player. Warning symbols glowing red. Red, black, and amber palette. Alert, protective mood."""

    elif 'provably fair' in title_lower or 'game integrity' in title_lower:
        prompt = f"""{base}. Wide shot showing mathematical verification. Clean white lighting.
Scene: Blockchain hash visualization, mathematical formula floating in space, verification checkmark stamping document, transparency glass showing fair random number generation. Green and gold color scheme. Mathematical, transparent mood."""

    # --- BONUS & PROMO ARTICLES ---
    elif 'crash casino bonuses' in title_lower and 'maximize' in title_lower:
        prompt = f"""{base}. Dynamic low angle, energy and celebration. Warm golden lighting with sparkler effects.
Scene: Treasure chest overflowing with golden coins, bonus code letters floating upward, percentage symbols (100%, 200%, 300%) exploding like fireworks, player hand reaching for bonus. Gold and vibrant orange palette. Excitement, reward mood."""

    elif 'best crash casinos' in title_lower and 'verified' in title_lower:
        prompt = f"""{base}. Medium wide shot, balanced composition. Professional studio lighting.
Scene: Podium with top 3 casinos on medal stands (gold, silver, bronze), verification badges glowing, trust seals arranged below, five-star ratings floating above. Blue, gold, and white professional color scheme. Authoritative, trustworthy mood."""

    elif 'best crash bonus codes' in title_lower:
        prompt = f"""{base}. Close-up on bonus codes, shallow depth of field. Warm celebratory lighting.
Scene: Bonus code text (CB100, WELCOME500, etc.) glowing neon, gift boxes bursting open, golden coins cascading, percentage offers highlighted. Gold and bright green palette. Excitement, urgency mood."""

    # --- STRATEGY & TUTORIAL ARTICLES ---
    elif 'crash gambling mistakes' in title_lower and 'bankroll' in title_lower:
        prompt = f"""{base}. Medium shot, instructional viewpoint. Clean even lighting.
Scene: Split composition - left side showing 15 common mistakes as red X marks, right side showing corrections as green checkmarks. Learning curve graph going upward. Expert advisor figure pointing to solutions. Blue and orange educational palette. Teaching, corrective mood."""

    elif 'crash game variants' in title_lower:
        prompt = f"""{base}. Wide shot showing variety. Dynamic lighting with multiple colored zones.
Scene: 7 different crash game interfaces arranged in arc (classic rocket, airplane, spaceship, balloon, etc.), each with unique visual style showing diversity. Comparison arrows between games. Colorful, diverse palette showing variety. Informative, comparative mood."""

    elif 'cashout strategies' in title_lower or 'cash-out' in title_lower:
        prompt = f"""{base}. Medium shot, analytical viewpoint. Clean clinical lighting.
Scene: Multiplier graph with perfect timing indicator, optimal cashout zone highlighted in green, too early/too late zones in red. Profit calculator showing gains. Strategic dashboard with metrics. Blue and purple analytical palette. Strategic, analytical mood."""

    elif 'crash gambling 101' in title_lower or 'beginner' in title_lower:
        prompt = f"""{base}. Medium wide shot, friendly perspective. Warm approachable lighting.
Scene: Tutorial progression from left to right - basic concepts illustrated with simple icons, step-by-step numbered path, question marks turning into lightbulbs. Learning road map visible. Friendly blue and green palette. Educational, welcoming mood."""

    elif 'timing' in title_lower and 'cash-out' in title_lower:
        prompt = f"""{base}. Close-up on timing element. Dramatic lighting highlighting clock.
Scene: Stopwatch with precise timing marker, multiplier curve with perfect exit point highlighted in gold zone, split-second decision moment frozen. Time-lapse effect showing right vs wrong timing. Gold and red high-contrast palette. Urgent, strategic mood."""

    elif 'strategy breakdown' in title_lower or 'choosing the right style' in title_lower:
        prompt = f"""{base}. Medium shot showing options. Balanced lighting.
Scene: Decision tree diagram with different strategy branches (conservative, aggressive, balanced), player silhouette at decision point, outcomes showing for each path. Flowchart style visualization. Blue and purple analytical palette. Decision-focused mood."""

    elif 'comparing crash game and slots' in title_lower:
        prompt = f"""{base}. Side-by-side comparison shot. Even lighting.
Scene: Left side showing crash game with upward curve, right side showing slots with spinning reels. VS text in center. Comparison metrics visible below each. Dual-screen split composition. Contrasting color palettes (crash in blue, slots in orange). Comparative mood."""

    # --- CRYPTO & ANONYMITY ARTICLES ---
    elif 'anonymous crash gambling' in title_lower or 'no-kyc' in title_lower:
        prompt = f"""{base}. Futuristic camera angle, Dutch tilt. Neon purple and cyan lighting with glow.
Scene: Hooded figure silhouette (anonymous), privacy shield protecting identity, blockchain network nodes in background, cryptocurrency symbols floating, VPN connection visualization. Futuristic purple, cyan, and black palette. Privacy-focused, cyber mood."""

    elif 'bitcoin crash gambling' in title_lower:
        prompt = f"""{base}. Extreme wide shot, epic scale. Dramatic rim lighting.
Scene: Massive Bitcoin logo as centerpiece, crash game rocket trajectory curving around it, blockchain web connecting everything, futuristic crypto casino floor. Bitcoin orange and cyber blue palette. Epic, cryptocurrency mood."""

    elif 'best payment methods' in title_lower:
        prompt = f"""{base}. Medium shot showing variety. Professional studio lighting.
Scene: Payment method icons arranged in grid (credit cards, crypto, e-wallets, bank transfer), speed meters showing transaction times, fee comparison bars visible. Information dashboard style. Multi-colored but organized. Informative, comparative mood."""

    # --- GLOBAL/REGIONAL ARTICLES ---
    elif 'german players' in title_lower:
        prompt = f"""{base}. Wide establishing shot. Natural daylight with German flag colors subtly integrated.
Scene: German map outline with hotspots, German flag colors (black, red, gold) as subtle accents, beer garden aesthetic with crash game terminal, legal text with German seal. Culturally relevant but modern. Localized, legal-compliance mood."""

    elif 'chinese players' in title_lower:
        prompt = f"""{base}. Wide shot with cultural elements. Warm red and gold lighting.
Scene: Great Wall silhouette, Chinese dragon curve as multiplier, red lanterns, traditional architecture modernized with crash game interface. Red and gold celebratory palette with modern tech. Cultural fusion, celebratory mood."""

    elif 'india players' in title_lower:
        prompt = f"""{base}. Epic wide shot. Warm vibrant lighting.
Scene: Taj Mahal silhouette, crash game rocket ascending like Diwali rocket, rangoli patterns as decorative borders, Indian flag colors subtly integrated. Rich vibrant palette. Cultural celebration, modern gaming mood."""

    elif 'singapore' in title_lower:
        prompt = f"""{base}. Urban aerial view. Modern city lighting.
Scene: Singapore skyline with Marina Bay Sands, futuristic crash game interface, legal framework symbols, tropical modern aesthetic. Modern blue and green palette. Urban, legal-compliance mood."""

    elif 'is crash gambling legal' in title_lower:
        prompt = f"""{base}. Medium shot, authoritative. Balanced professional lighting.
Scene: Legal scale weighing regulations, gavel and law book, map of world with green (legal) and red (illegal) zones, compliance checklist. Professional blue with gold accents. Legal, informative mood."""

    # --- REVIEWS & RATINGS ---
    elif 'how to choose' in title_lower and 'safe' in title_lower:
        prompt = f"""{base}. Medium wide shot, instructional. Clean bright lighting.
Scene: Checklist with green checkmarks, safety inspection elements, magnifying glass revealing trust seals, decision tree for choosing casino. Educational blue and orange palette. Guide, decision-support mood."""

    elif 'rtp' in title_lower and 'house edge' in title_lower:
        prompt = f"""{base}. Medium shot, mathematical. Clean clinical lighting.
Scene: Percentage calculations visible, RTP meter showing high percentage, house edge visualization, mathematical formulas in background. Green (good RTP) and red (high edge) indicators. Educational, mathematical mood."""

    elif 'fast cash' in title_lower and 'payout speeds' in title_lower:
        prompt = f"""{base}. Dynamic speed-focused shot. Motion blur lighting.
Scene: Lightning bolt symbols, speedometer gauge, comparison bars showing crash vs slots payout times, hourglass with fast-flowing sand. Yellow and blue fast-paced palette. Speed, comparison mood."""

    # --- DEFAULT/GENERIC ---
    else:
        prompt = f"""{base}. Wide shot, eye-level. Professional balanced lighting.
Scene: Crash game rocket soaring upward, multiplier curve climbing steeply, casino chips flying, winning moment captured, player celebrating. Dynamic energetic composition. Blue and vibrant accent colors. Excitement, winning mood."""

    return prompt

def main():
    # Load posts
    input_file = '/root/.openclaw/workspace/temp/missing-images.json'

    with open(input_file, 'r') as f:
        posts = json.load(f)

    print("📝 Creating custom prompts for each article")
    print("=" * 70)
    print()

    # Generate custom prompts for each post
    for i, post in enumerate(posts, 1):
        custom_prompt = create_custom_prompt(post)

        post['custom_prompt'] = custom_prompt

        # Show samples
        if i <= 5 or i % 10 == 0:
            print(f"[{i}/{len(posts)}] {post['site']}/{post['post_id']}")
            print(f"  Title: {post['title'][:70]}")
            print(f"  Custom prompt preview: {custom_prompt[:120]}...")
            print()

    # Save custom prompts
    output_file = '/root/.openclaw/workspace/temp/missing-images-custom.json'
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print("=" * 70)
    print(f"✅ Custom prompts saved to: {output_file}")
    print()
    print("Each article now has a unique, specific prompt based on:")
    print("• Article topic and focus")
    print("• Target audience and intent")
    print("• Specific visual elements")
    print("• Appropriate mood and atmosphere")
    print("• Cultural/regional relevance (where applicable)")
    print()
    print(f"Total unique prompts: {len(posts)}")

if __name__ == '__main__':
    main()
