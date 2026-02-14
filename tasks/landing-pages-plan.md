# Landing Pages Design Plan

**Date:** 2026-02-02
**Goal:** Create distinctive, production-grade landing pages for 4 crash gambling sites

---

## Site 1: crashcasino.io → Trust & Safety Authority

**Positioning:** "Crash Gambling, Verified Fair"
**Tone:** Editorial/Magazine (investigative journalism aesthetic)

**Design Direction:**
- **Aesthetic:** Bold, authoritative, transparency-focused
- **Color Palette:** Deep black (#0a0a0a), electric green (#00ff88) accent
- **Typography:** Satoshi (display) + General Sans (body)
- **Unforgettable Element:** Animated "verified safe" badge that pulses

**Hero Section:**
```
Badge: "50 Sites Tested"
Title: "Is Crash Gambling Rigged?"
Subtitle: "We tested 50 crash casinos for provably fair verification,
         RTP transparency, and real payout audits."
CTA: "See Which Sites Passed" (primary)
Secondary: "How We Test" (outline)
```

**Key Sections:**
1. Testing methodology (transparency)
2. Verified safe casinos table (with affiliate links)
3. Red flags warning (rogue casinos)
4. State legality breakdown
5. FAQ accordion

---

## Site 2: freecrashgames.com → Global Free Play Hub

**Positioning:** "Free Crash Games for Everyone, Everywhere"
**Tone:** Playful, accessible, borderless

**Design Direction:**
- **Aesthetic:** Global, vibrant, demo-focused
- **Color Palette:** Off-white base (#fafafa), gradient world map accents
- **Typography:** Space Grotesk (display) + Instrument Sans (body)
- **Unforgettable Element:** Interactive world map with hotspots

**Hero Section:**
```
Badge: "No Deposit Required"
Title: "Play Crash Games Free"
Subtitle: "Try top crash games without risking real money.
         Find demo versions from trusted casinos worldwide."
CTA: "Find Games for Your Country"
Interactive Element: World map with country selector
```

**Key Sections:**
1. Country-specific game finder (geo-selector)
2. Top free crash games (demo links)
3. "Why play free?" benefits
4. Tutorial section (how to play)
5. VPN-friendly casinos guide

---

## Site 3: cryptocrashgambling.com → Crypto Crash Expert

**Positioning:** "Crash Gambling with Your Favorite Coins"
**Tone:** Retro-futuristic, crypto-native

**Design Direction:**
- **Aesthetic:** Dark mode, neon accents, terminal elements
- **Color Palette:** Near-black (#050505), matrix green (#39ff14), bitcoin orange
- **Typography:** IBM Plex Mono (headings) + General Sans (body)
- **Unforgettable Element:** Live crypto price tickers in hero

**Hero Section:**
```
Badge: "Bitcoin Accepted"
Title: "Crypto Crash Gambling"
Subtitle: "Anonymous, instant withdrawals, provably fair.
         Play with BTC, ETH, USDT and 10+ coins."
CTA: "Find Crypto-Friendly Casinos"
Live Element: Scrolling ticker with BTC/ETH/USDT prices
```

**Key Sections:**
1. Coin-by-coin breakdown (BTC, ETH, USDT, etc.)
2. No-KYC casino recommendations
3. Privacy features (VPN, anonymous)
4. Blockchain verification explainer
5. Crypto bonus comparison

---

## Site 4: crashgamegambling.com → Crash Gambling Academy

**Positioning:** "Master Crash Gambling: From Beginner to Pro"
**Tone:** Educational, structured, professional

**Design Direction:**
- **Aesthetic:** Academic but modern (learning platform vibe)
- **Color Palette:** Navy (#1e293b) + gold (#fbbf24) accents
- **Typography:** Clash Display (headlines) + Plus Jakarta Sans (body)
- **Unforgettable Element:** Animated learning path visualization

**Hero Section:**
```
Badge: "Complete Learning Path"
Title: "Master Crash Gambling"
Subtitle: "From absolute beginner to advanced strategist.
         50+ guides, strategies, and tools to maximize your EV."
CTA: "Start Learning (Free)"
Visual: Skill tree showing progression path
```

**Key Sections:**
1. Learning path (beginner → intermediate → advanced)
2. Popular guides (strategy, bankroll, odds)
3. Interactive tools (calculator, simulator)
4. Expert tips section
5. Community/discord CTA

---

## Implementation Order

1. ✅ **crashcasino.io** (highest priority - trust angle unique)
2. **freecrashgames.com** (geo-angle working, double down)
3. **cryptocrashgambling.com** (crypto niche, rebuild needed)
4. **crashgamegambling.com** (educational, content-rich)

## Technical Approach

**Framework:** Vite (React + TypeScript + Tailwind)
**Deployment:** Export as static HTML → Upload to WordPress via REST API
**Bundle Size:** Single HTML file per landing page
**Mobile:** Fully responsive (test on 375px breakpoint)

## File Structure

```
landing-pages/
├── crashcasino/
│   ├── src/
│   │   ├── config/site.ts
│   │   ├── components/
│   │   └── App.tsx
│   └── index.html
├── freecrashgames/
├── cryptocrash/
└── crashgamegambling/
```

---

*Created: 2026-02-02*
