#!/usr/bin/env python3
"""
Create all remaining landing pages and upload them
"""

import json
import subprocess

# Site configurations
SITES = {
    'freecrashgames': {
        'url': 'https://freecrashgames.com/wp-json',
        'user': '@peter',
        'pass': 'F8Mg yZXM qJy4 jQvp BMeZ FoMG',
        'page_id': None,  # Will fetch
        'file': '/root/.openclaw/workspace/tasks/freecrashgames-landing.html',
        'title': 'Free Crash Games - Play Crash Without Risk'
    },
    'cryptocrash': {
        'url': 'https://cryptocrashgambling.com/wp-json',
        'user': '@peter',
        'pass': 'R3kQ 6vRA UwYd x7Cn KEtT Pk83',
        'page_id': None,
        'file': '/root/.openclaw/workspace/tasks/cryptocrash-landing.html',
        'title': 'Crypto Crash Gambling - Bitcoin, ETH, USDT'
    },
    'crashgamegambling': {
        'url': 'https://crashgamegambling.com/wp-json',
        'user': '@peter',
        'pass': 'MioX SygN Xaz6 pK9o RUiK tBMF',
        'page_id': None,
        'file': '/root/.openclaw/workspace/tasks/crashgamegambling-landing.html',
        'title': 'Master Crash Gambling - From Beginner to Pro'
    }
}

def get_home_page_id(site_key):
    """Get the homepage ID for a site"""
    site = SITES[site_key]
    curl_command = [
        'curl', '-s',
        '-u', f"{site['user']}:{site['pass']}",
        f"{site['url']}/wp/v2/pages?slug=home&_fields=id"
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        pages = json.loads(result.stdout)
        if pages and len(pages) > 0:
            return pages[0]['id']
    except:
        pass
    
    return None

def upload_landing_page(site_key):
    """Upload landing page to WordPress"""
    site = SITES[site_key]
    
    # Read HTML file
    try:
        with open(site['file'], 'r') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ {site_key}: File not found - {site['file']}")
        return False
    
    # Get homepage ID if not set
    if not site['page_id']:
        page_id = get_home_page_id(site_key)
        if not page_id:
            print(f"❌ {site_key}: Could not find homepage")
            return False
        site['page_id'] = page_id
    
    # Upload to WordPress
    payload = {
        "title": site['title'],
        "content": html_content,
        "status": "publish"
    }
    
    curl_command = [
        'curl', '-s', '-X', 'POST',
        f"{site['url']}/wp/v2/pages/{site['page_id']}",
        '-u', f"{site['user']}:{site['pass']}",
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        
        if 'code' in response:
            print(f"❌ {site_key}: {response['message']}")
            return False
        
        print(f"✓ {site_key}: Uploaded successfully!")
        print(f"  Page ID: {response.get('id')}")
        print(f"  URL: {response.get('link')}")
        return True
        
    except Exception as e:
        print(f"❌ {site_key}: {e}")
        return False

# Create cryptocrash landing page
cryptocrash_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Crash Gambling - Bitcoin, ETH, USDT | CryptoCrashGambling.com</title>
    <meta name="description" content="Anonymous, instant withdrawals, provably fair. Play crash games with BTC, ETH, USDT and 10+ cryptocurrencies.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #050505; color: #e0e0e0; line-height: 1.6; }
        html { scroll-behavior: smooth; }
        .container { max-width: 1280px; margin: 0 auto; padding: 0 24px; }
        
        .hero { padding: 100px 24px; background: #050505; position: relative; overflow: hidden; }
        .hero::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at top, #0a3d0a 0%, transparent 50%); opacity: 0.3; }
        .badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 4px; background: #0a3d0a; color: #39ff14; margin-bottom: 24px; font-family: monospace; border: 1px solid #39ff14; }
        .hero-title { font-size: clamp(36px, 7vw, 56px); font-weight: 700; margin-bottom: 24px; }
        .hero-title .green { color: #39ff14; }
        .hero-subtitle { font-size: clamp(16px, 2.5vw, 20px); color: #9ca3af; max-width: 700px; margin: 0 auto 32px; }
        .ticker { display: flex; gap: 24px; justify-content: center; margin-bottom: 32px; font-family: monospace; font-size: 14px; }
        .ticker-item { padding: 8px 16px; background: #1a1a1a; border-radius: 4px; }
        .ticker-up { color: #39ff14; }
        
        .btn { display: inline-block; padding: 14px 28px; border-radius: 4px; font-weight: 600; text-align: center; transition: all 0.3s; font-family: monospace; }
        .btn-primary { background: #39ff14; color: #000; }
        .btn-primary:hover { background: #32d612; }
        .btn-secondary { border: 1px solid #39ff14; color: #39ff14; }
        .btn-secondary:hover { background: #39ff14; color: #000; }
        
        .section { padding: 80px 24px; }
        .section-dark { background: #0a0a0a; }
        .section-title { font-size: clamp(24px, 4vw, 36px); font-weight: 700; text-align: center; margin-bottom: 16px; }
        .section-subtitle { font-size: 16px; color: #9ca3af; text-align: center; margin-bottom: 48px; }
        
        .grid { display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
        .card { padding: 24px; border-radius: 8px; background: #1a1a1a; border: 1px solid #2a2a2a; transition: all 0.3s; }
        .card:hover { border-color: #39ff14; }
        .coin-icon { font-size: 32px; margin-bottom: 12px; }
        .card-title { font-size: 20px; font-weight: 600; margin-bottom: 8px; }
        .card-text { color: #9ca3af; font-size: 14px; }
        
        .footer { padding: 48px 24px; background: #030303; border-top: 1px solid #1a1a1a; text-align: center; }
        .footer-tagline { font-size: 20px; font-weight: 700; color: #39ff14; margin-bottom: 24px; }
    </style>
</head>
<body>
    <section class="hero">
        <div class="container" style="position: relative; z-index: 1;">
            <div class="badge">₿ Bitcoin Accepted</div>
            <h1 class="hero-title">Crypto Crash<br><span class="green">Gambling</span></h1>
            <p class="hero-subtitle">Anonymous, instant withdrawals, provably fair. Play crash games with BTC, ETH, USDT and 10+ cryptocurrencies.</p>
            <div class="ticker">
                <div class="ticker-item">BTC <span class="ticker-up">$97,234</span></div>
                <div class="ticker-item">ETH <span class="ticker-up">$3,456</span></div>
                <div class="ticker-item">USDT <span class="ticker-up">$1.00</span></div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
                <a href="#casinos" class="btn btn-primary" style="width: 200px;">Find Crypto Casinos</a>
            </div>
        </div>
    </section>

    <section class="section section-dark">
        <div class="container">
            <h2 class="section-title">Play with Your Favorite Coins</h2>
            <p class="section-subtitle">Every major cryptocurrency supported</p>
            <div class="grid">
                <div class="card">
                    <div class="coin-icon">₿</div>
                    <h3 class="card-title">Bitcoin (BTC)</h3>
                    <p class="card-text">The original crypto. Accepted everywhere, instant withdrawals, maximum anonymity.</p>
                </div>
                <div class="card">
                    <div class="coin-icon">Ξ</div>
                    <h3 class="card-title">Ethereum (ETH)</h3>
                    <p class="card-text">Fast transactions, smart contract integration, widely accepted at crash casinos.</p>
                </div>
                <div class="card">
                    <div class="coin-icon">₮</div>
                    <h3 class="card-title">Tether (USDT)</h3>
                    <p class="card-text">Stable value, TRC20 for low fees, perfect for bankroll management.</p>
                </div>
                <div class="card">
                    <div class="coin-icon">◎</div>
                    <h3 class="card-title">Litecoin (LTC)</h3>
                    <p class="card-text">Lightning-fast transactions, low fees, great for small bets.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="casinos" class="section">
        <div class="container">
            <h2 class="section-title">No-KYC Crypto Casinos</h2>
            <p class="section-subtitle">Play anonymously, no ID required</p>
            <div class="grid">
                <div class="card">
                    <h3 class="card-title">TrustDice</h3>
                    <p class="card-text" style="margin-bottom: 16px;">30% revenue share, no negative carryover. Provably fair, instant crypto payouts.</p>
                    <a href="https://trustdice.win/?ref=u_peterp" target="_blank" rel="nofollow noopener" class="btn btn-primary" style="width: 100%; display: block;">Play Now</a>
                </div>
                <div class="card">
                    <h3 class="card-title">Betfury</h3>
                    <p class="card-text" style="margin-bottom: 16px;">20% NGR, full crypto ecosystem. Staking, mining, and crash games in one place.</p>
                    <a href="https://betfury.bet/df1865703" target="_blank" rel="nofollow noopener" class="btn btn-primary" style="width: 100%; display: block;">Play Now</a>
                </div>
                <div class="card">
                    <h3 class="card-title">Betzrd</h3>
                    <p class="card-text" style="margin-bottom: 16px;">25-45% commission, no KYC required. VPN-friendly, crypto-native platform.</p>
                    <a href="https://betzrd.com/pyondmfcx" target="_blank" rel="nofollow noopener" class="btn btn-primary" style="width: 100%; display: block;">Play Now</a>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p class="footer-tagline">Provably Fair. Anonymous. Instant.</p>
            <p style="font-size: 14px; color: #6b7280;">© 2026 CryptoCrashGambling.com. Gamble responsibly. 18+ only.</p>
        </div>
    </footer>
</body>
</html>'''

with open(SITES['cryptocrash']['file'], 'w') as f:
    f.write(cryptocrash_html)

print("✓ Created cryptocrash-landing.html")

# Create crashgamegambling landing page
crashgamegambling_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Crash Gambling - From Beginner to Pro | CrashGameGambling.com</title>
    <meta name="description" content="From absolute beginner to advanced strategist. 50+ guides, strategies, and tools to maximize your EV in crash gambling.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f1f5f9; line-height: 1.6; }
        html { scroll-behavior: smooth; }
        .container { max-width: 1280px; margin: 0 auto; padding: 0 24px; }
        
        .hero { padding: 100px 24px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); position: relative; }
        .badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 9999px; background: #fbbf24/20; color: #fbbf24; margin-bottom: 24px; font-weight: 500; }
        .hero-title { font-size: clamp(40px, 8vw, 64px); font-weight: 700; margin-bottom: 24px; }
        .hero-title .gold { color: #fbbf24; }
        .hero-subtitle { font-size: clamp(18px, 3vw, 22px); color: #94a3b8; max-width: 700px; margin: 0 auto 32px; }
        
        .btn { display: inline-block; padding: 14px 28px; border-radius: 8px; font-weight: 600; text-align: center; transition: all 0.3s; }
        .btn-primary { background: #fbbf24; color: #0f172a; }
        .btn-primary:hover { background: #f59e0b; }
        
        .section { padding: 80px 24px; }
        .section-dark { background: #1e293b; }
        .section-title { font-size: clamp(28px, 5vw, 42px); font-weight: 700; text-align: center; margin-bottom: 16px; }
        .section-subtitle { font-size: 18px; color: #94a3b8; text-align: center; margin-bottom: 48px; max-width: 700px; margin-left: auto; margin-right: auto; }
        
        .path { display: flex; flex-direction: column; gap: 24px; max-width: 900px; margin: 0 auto; }
        .path-level { display: flex; gap: 24px; align-items: flex-start; }
        .path-marker { width: 60px; height: 60px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
        .path-content { flex: 1; }
        .path-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
        .path-text { color: #94a3b8; }
        
        .grid { display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
        .card { padding: 24px; border-radius: 12px; background: #1e293b; border: 1px solid #334155; transition: all 0.3s; }
        .card:hover { border-color: #fbbf24; }
        .card-number { font-size: 48px; font-weight: 700; color: #fbbf24/30; margin-bottom: -20px; }
        .card-title { font-size: 20px; font-weight: 600; margin-bottom: 8px; }
        .card-text { color: #94a3b8; }
        
        .footer { padding: 48px 24px; background: #0f172a; border-top: 1px solid #1e293b; text-align: center; }
        .footer-tagline { font-size: 24px; font-weight: 700; color: #fbbf24; margin-bottom: 24px; }
    </style>
</head>
<body>
    <section class="hero">
        <div class="container">
            <div class="badge">📚 Complete Learning Path</div>
            <h1 class="hero-title">Master Crash<br><span class="gold">Gambling</span></h1>
            <p class="hero-subtitle">From absolute beginner to advanced strategist. 50+ guides, strategies, and tools to maximize your EV in crash gambling.</p>
            <a href="#path" class="btn btn-primary">Start Learning (Free)</a>
        </div>
    </section>

    <section id="path" class="section">
        <div class="container">
            <h2 class="section-title">Your Learning Path</h2>
            <p class="section-subtitle">Follow our structured curriculum from basics to pro</p>
            <div class="path">
                <div class="path-level">
                    <div class="path-marker">1</div>
                    <div class="path-content">
                        <h3 class="path-title">Beginner</h3>
                        <p class="path-text">What is crash? How do multipliers work? Understanding provably fair. Your first rounds.</p>
                    </div>
                </div>
                <div class="path-level">
                    <div class="path-marker">2</div>
                    <div class="path-content">
                        <h3 class="path-title">Intermediate</h3>
                        <p class="path-text">Bankroll management. Auto-cashout strategies. Reading patterns. Bonus hunting.</p>
                    </div>
                </div>
                <div class="path-level">
                    <div class="path-marker">3</div>
                    <div class="path-content">
                        <h3 class="path-title">Advanced</h3>
                        <p class="path-text">Expected value calculations. Risk of ruin. Multi-account strategy. Arbitrage.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-dark">
        <div class="container">
            <h2 class="section-title">Popular Guides</h2>
            <p class="section-subtitle">Most-read crash gambling strategies</p>
            <div class="grid">
                <div class="card">
                    <div class="card-number">01</div>
                    <h3 class="card-title">Crash Gambling Cashout Strategies</h3>
                    <p class="card-text">When to cash out for maximum profit. Multiplier targets vs. holding longer.</p>
                </div>
                <div class="card">
                    <div class="card-number">02</div>
                    <h3 class="card-title">Bankroll Management Guide</h3>
                    <p class="card-text">Protect your funds. Bet sizing formulas. Stop-loss strategies.</p>
                </div>
                <div class="card">
                    <div class="card-number">03</div>
                    <h3 class="card-title">Odds Calculator</h3>
                    <p class="card-text">Calculate your edge. Expected value per round. Risk of ruin analysis.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p class="footer-tagline">Level Up Your Crash Game</p>
            <p style="font-size: 14px; color: #64748b;">© 2026 CrashGameGambling.com. Gamble responsibly. 18+ only.</p>
        </div>
    </footer>
</body>
</html>'''

with open(SITES['crashgamegambling']['file'], 'w') as f:
    f.write(crashgamegambling_html)

print("✓ Created crashgamegambling-landing.html")
print("\n" + "="*60)
print("All landing pages created!")
print("="*60)
print("\nNow uploading to WordPress...")
print()

# Upload all landing pages
for site_key in SITES:
    upload_landing_page(site_key)
    print()

print("="*60)
print("Landing pages deployment complete!")
print("="*60)
