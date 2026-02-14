#!/usr/bin/env python3
"""
Create Multiple Comparison Pages via WordPress API
"""

import requests
import json
import re

AUTH = ("admin", "GyOC qXGg K82P hxRt ZjbY 2v9k")

# Load credit card data
with open('/root/.openclaw/media/inbound/file_0---1cf36a19-42d3-40ac-b404-b7ddc9c78914.json', 'r') as f:
    data = json.load(f)
    all_cards = data[0]['credit_cards']

# Filter cards by type
def filter_cards_by_type(cards, card_type):
    filtered = []
    for card in cards:
        name_lower = card['name'].lower()
        
        if card_type == 'student':
            if 'student' in name_lower:
                filtered.append(card)
        elif card_type == 'secured':
            if 'secured' in name_lower:
                filtered.append(card)
        elif card_type == 'travel':
            if 'travel' in name_lower or 'venture' in name_lower or 'explore' in name_lower:
                filtered.append(card)
        elif card_type == 'cashback':
            if card['rewards'] and 'cash' in card['rewards'].lower():
                filtered.append(card)
        elif card_type == 'business':
            if 'business' in name_lower:
                filtered.append(card)
    
    return filtered

# Generate HTML page for card type
def generate_comparison_page(card_type, cards, title, description):
    
    # Page HTML template
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Cardfair</title>
    <meta name="description" content="{description}">
    
    <style>
        /* Comparison Page Styles */
        :root {{
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --success: #10b981;
            --warning: #f59e0b;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-700: #374151;
            --gray-900: #111827;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--gray-700);
            background: var(--gray-50);
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        
        .hero {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 80px 0 60px;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.1;
        }}
        
        .hero-subtitle {{
            font-size: 1.25rem;
            opacity: 0.9;
            max-width: 700px;
            margin: 0 auto;
        }}
        
        .cards-section {{ padding: 60px 0; }}
        
        .section-title {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--gray-900);
            margin-bottom: 50px;
            text-align: center;
        }}
        
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }}
        
        .card-card {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .card-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }}
        
        .card-card.featured {{
            border: 3px solid var(--warning);
        }}
        
        .card-card.featured::before {{
            content: "⭐ BEST OVERALL";
            position: absolute;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--warning), #d97706);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            z-index: 10;
        }}
        
        .card-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 25px;
            position: relative;
        }}
        
        .card-name {{
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 8px;
            padding-right: 100px;
        }}
        
        .card-issuer {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .card-body {{ padding: 25px; }}
        
        .card-highlights {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }}
        
        .card-highlight {{
            background: var(--gray-100);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--gray-700);
        }}
        
        .card-highlight.good {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .card-features {{
            margin-bottom: 20px;
        }}
        
        .card-feature {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 12px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .card-feature-icon {{
            color: var(--success);
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
            padding: 20px;
            background: var(--gray-50);
            border-radius: 10px;
        }}
        
        .card-stat {{
            text-align: center;
        }}
        
        .card-stat-label {{
            font-size: 11px;
            font-weight: 700;
            color: var(--gray-700);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .card-stat-value {{
            font-size: 16px;
            font-weight: 800;
            color: var(--gray-900);
        }}
        
        .card-stat-value.good {{
            color: var(--success);
        }}
        
        .card-footer {{
            padding: 20px 25px;
            background: var(--gray-50);
        }}
        
        .card-apply-btn {{
            display: block;
            width: 100%;
            padding: 14px 24px;
            background: linear-gradient(135deg, var(--success), #059669);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            font-size: 15px;
            text-align: center;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .card-apply-btn:hover {{
            background: linear-gradient(135deg, #059669, #047857);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
        }}
        
        @media (max-width: 768px) {{
            .cards-grid {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 2rem; }}
        }}
    </style>
    
    <!-- Schema.org markup -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "{title}",
      "description": "{description}",
      "numberOfItems": {min(5, len(cards))},
      "itemListElement": [
    '''
    
    # Add schema for first 5 cards
    for i, card in enumerate(cards[:5], 1):
        html += f'''
        {{
          "@type": "ListItem",
          "position": {i},
          "item": {{
            "@type": "CreditCard",
            "name": "{card['name'].replace('"', '\\"')}",
            "issuer": {{
              "@type": "Organization",
              "name": "{card['issuer']}"
            }},
            "annualFee": "{card['annual_fee']}",
            "offers": {{
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "USD"
            }}
          }}
        }}
        ''' + ("," if i < min(5, len(cards)) else "")
    
    html += '''
      ]
    }
    </script>
</head>
<body>
    <section class="hero">
        <div class="container">
            <h1>{title}</h1>
            <p class="hero-subtitle">{description}</p>
        </div>
    </section>

    <section class="cards-section">
        <div class="container">
            <h2 class="section-title">Top {card_type.title()} Credit Cards</h2>
            <div class="cards-grid">
    '''
    
    # Add cards
    for i, card in enumerate(cards[:5], 1):
        is_featured = i == 1
        featured_class = ' featured' if is_featured else ''
        
        # Extract key features
        features_text = card.get('additional_features', '')
        has_no_fee = '$0' in card.get('annual_fee', '') or 'None' in card.get('annual_fee', '')
        
        html += f'''
                <div class="card-card{featured_class}">
                    <div class="card-header">
                        <div class="card-name">{card['name']}</div>
                        <div class="card-issuer">{card['issuer']}</div>
                    </div>
                    <div class="card-body">
                        <div class="card-highlights">
                            {'<span class="card-highlight good">No Annual Fee</span>' if has_no_fee else ''}
                            {'<span class="card-highlight good">' + card['rewards'][:30] + '</span>' if card.get('rewards') else ''}
                            <span class="card-highlight">{card['issuer']}</span>
                        </div>
                        
                        <div class="card-features">
                            <div class="card-feature">
                                <span class="card-feature-icon">✓</span>
                                <span>{features_text[:100]}...</span>
                            </div>
                        </div>
                        
                        <div class="card-stats">
                            <div class="card-stat">
                                <div class="card-stat-label">Annual Fee</div>
                                <div class="card-stat-value {' + 'good' if has_no_fee else '' + '"}>{card.get('annual_fee', 'N/A')}</div>
                            </div>
                            <div class="card-stat">
                                <div class="card-stat-label">APR</div>
                                <div class="card-stat-value">{card.get('interest_rate', 'Variable')}</div>
                            </div>
                            <div class="card-stat">
                                <div class="card-stat-label">Credit Needed</div>
                                <div class="card-stat-value">{card.get('credit_score_required', 'Varies')}</div>
                            </div>
                            <div class="card-stat">
                                <div class="card-stat-label">Rewards</div>
                                <div class="card-stat-value">{card.get('rewards', 'None')[:20]}</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <a href="#apply-{card['name'].lower().replace(' ', '-')}" class="card-apply-btn">
                            Apply Now →
                        </a>
                    </div>
                </div>
        '''
    
    html += '''
            </div>
        </div>
    </section>
</body>
</html>
    '''
    
    return html

# Create pages
pages_to_create = [
    {
        'type': 'student',
        'title': 'Best Student Credit Cards 2025 | No Credit Required | Cardfair',
        'description': 'Compare the best student credit cards for building credit with no credit history. Top picks from Discover, Capital One, and Journey Student Rewards.',
        'slug': 'best-student-credit-cards-2025'
    },
    {
        'type': 'cashback',
        'title': 'Best Cash Back Credit Cards 2025 | Maximize Rewards | Cardfair',
        'description': 'Compare the best cash back credit cards with up to 5% rewards. Top picks from Chase, Citi Double Cash, and Capital One for every purchase.',
        'slug': 'best-cash-back-credit-cards-2025'
    },
    {
        'type': 'travel',
        'title': 'Best Travel Credit Cards 2025 | Miles & Points | Cardfair',
        'description': 'Compare the best travel credit cards earning miles and points. Top picks from Chase Sapphire, Capital One Venture, and American Express for frequent travelers.',
        'slug': 'best-travel-credit-cards-2025'
    }
]

print("="*80)
print("📤 UPLOADING MULTIPLE COMPARISON PAGES")
print("="*80)
print()

results = []

for page_config in pages_to_create:
    card_type = page_config['type']
    
    print(f"Creating: {page_config['title']}")
    
    # Filter cards
    cards = filter_cards_by_type(all_cards, card_type)
    
    if len(cards) == 0:
        print(f"  ⚠️ No cards found for type: {card_type}")
        continue
    
    # Generate HTML
    html_content = generate_comparison_page(
        card_type,
        cards,
        page_config['title'],
        page_config['description']
    )
    
    # Create via API
    url = "https://cardfair.com/wp-json/wp/v2/pages"
    
    payload = {
        "title": page_config['title'],
        "content": html_content,
        "slug": page_config['slug'],
        "status": "publish",
        "meta": {
            "rank_math_title": page_config['title'],
            "rank_math_description": page_config['description']
        }
    }
    
    try:
        response = requests.post(url, auth=AUTH, json=payload, timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            page_url = result.get('link', '')
            
            print(f"  ✅ SUCCESS")
            print(f"  URL: {page_url}")
            
            results.append({
                'success': True,
                'title': page_config['title'],
                'url': page_url,
                'slug': page_config['slug']
            })
        else:
            print(f"  ❌ FAILED: HTTP {response.status_code}")
            results.append({
                'success': False,
                'title': page_config['title'],
                'error': f"HTTP {response.status_code}"
            })
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        results.append({
            'success': False,
            'title': page_config['title'],
            'error': str(e)
        })
    
    print()

print("="*80)
print(f"✅ UPLOAD COMPLETE: {sum(1 for r in results if r['success'])}/{len(results)} pages created")
print("="*80)
print()

print("📊 Created Pages:")
print("-"*80)
for result in results:
    if result['success']:
        print(f"✅ {result['title']}")
        print(f"   {result['url']}")
        print()

print("="*80)
print("🎯 NEXT STEPS:")
print("="*80)
print("1. Add affiliate links to all 'Apply Now' buttons")
print("2. Test all pages on mobile")
print("3. Submit to Google Search Console")
print("4. Add to navigation menu")

# Save results
with open('/root/.openclaw/workspace/multiple_pages_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n📁 Results saved: multiple_pages_results.json")
