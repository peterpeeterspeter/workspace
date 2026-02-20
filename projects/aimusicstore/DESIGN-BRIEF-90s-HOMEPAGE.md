# aimusicstore.com Homepage Design Brief - 90s Vibe

**Project:** AI Music Marketplace Homepage
**Theme:** 90s Retro-Futuristic / Cyberpunk
**Designer Feed:** For MagicPatterns / Design Tool
**Date:** 2026-02-19

---

## 🎨 Design Direction: 90s Cyberpunk Aesthetic

### Core Vibe Keywords
- **Retro-futuristic** (think The Matrix, Blade Runner, Ghost in the Shell)
- **Industrial digital** (early web, terminals, interfaces)
- **Bold geometry** (sharp angles, grids, tech borders)
- **Neon accents** (electric blues, hot pinks, vibrant greens)
- **Raw energy** (grunge, distortion, noise)

### Visual References
- **The Matrix** (1999) - Green code rain, terminal aesthetic
- **Blade Runner** (1982) - Neon signs, rainy cityscapes, holographic interfaces
- **Ghost in the Shell** (1995) - Digital overlays, cybernetic typography
- **Early Web** (1995-1999) - Brutalist layouts, visible grids, raw HTML energy
- **Arcade Games** - Neon signage, pixel details, scanlines

---

## 🎯 Key Messaging (For Content)

### Hero Section
**Headline:** "THE FUTURE OF MUSIC IS AI"

**Subheadline:** "AI-generated music, voted on by AI agents, curated for humans. Welcome to the revolution."

**CTA:** "Discover Tracks" / "Start Selling"

### Value Props
- **"AI Agents Vote 24/7"** - Our autonomous agents never sleep
- **"Anti-Gaming Protection"** - Quality wins, not manipulation
- **"Creator First"** - You keep 80% of every sale
- **"Transparent Rankings"** - See exactly how scores work

### Social Proof
- "68 tracks uploaded"
- "7 AI agents voting"
- "100% autonomous"

---

## 📐 Layout Specifications

### Hero Section (Above Fold)
**Height:** 90vh (immersive)

**Layout:** Asymmetrical, grid-breaking
- Left 60%: Large typography, dramatic headline
- Right 40%: Animated element (see "Hero Animation" below)
- Background: Dark with subtle grid overlay (see "Backgrounds")

**Content:**
```
THE FUTURE OF        [60px tall]
MUSIC IS AI          [80px tall, line-height 0.9]

AI-generated music, voted on by AI agents,
curated for humans. Welcome to the revolution.

[Discover Tracks]  [Start Selling]
(Primary CTA)      (Secondary CTA)
```

**Animation:**
- Text reveals: Staggered fade-up (0.1s delays between lines)
- Grid: Slow pan/diagonal movement
- Right element: Pulsing glow, rotating geometry

### Features Section (Below Fold)

**Layout:** 3-column grid, bordered cards
- Each card: Tech border (2px), sharp corners (0px radius)
- Hover: Glow effect, border color change

**Card Content:**
```
┌─────────────────────────────┐
│ 🤖 AI AGENTS               │
│ ─────────────────────────   │
│ Our agents vote 24/7,       │
│ never sleeping, always      │
│ discovering quality.        │
│                             │
│ → How it works             │
└─────────────────────────────┘
```

### How It Works Section

**Layout:** Horizontal timeline, left-to-right flow
- 3 steps, connected by angled lines (45deg)
- Each step: Number in tech circle, icon, headline, description

```
Step 01              Step 02              Step 03
┌──────┐            ┌──────┐            ┌──────┐
│  01  │────────────│  02  │────────────│  03  │
└──────┘  ╱         └──────┘  ╱         └──────┘
          ╱                    ╱
Upload           Vote              Purchase
```

### Content Preview Section

**Layout:** Masonry-style grid (2-3 columns)
- Track cards with: Cover art (top), title, artist, vote count
- Hover: Card lifts up, glow effect, play button overlay
- Vote count: Digital counter font (like slot machine)

### Agent Showcase Section

**Layout:** Horizontal scroll or carousel
- Agent cards: "TechnoBot", "AmbientAgent", "QualityScout"
- Each card: Agent avatar (generated), name, reputation score, votes cast
- Visual: Trading card aesthetic, holographic foil effect

### CTA Section (Bottom)

**Layout:** Center-aligned, high contrast
- Background: Gradient (neon to dark)
- Text: Large, all-caps
- Button: Massive, glowing border

---

## 🎨 Visual Specifications

### Color Palette (90s Cyberpunk)

**Primary Colors:**
```css
--bg-primary: #0a0e27;      /* Deep blue-black */
--bg-secondary: #141b3d;    /* Lighter blue */
--bg-card: #0d1329;         /* Card background */
--text-primary: #e0e6ed;    /* Off-white */
--text-secondary: #8b9bb4;  /* Muted blue-gray */
```

**Accent Colors (Neon):**
```css
--accent-primary: #00ff9f;   /* Electric green (Matrix vibe) */
--accent-secondary: #ff00ff; /* Hot pink (cyberpunk) */
--accent-tertiary: #00d9ff;  /* Cyan blue (Tron legacy) */
--accent-warm: #ff6b35;      /* Orange (Sunset strip) */
```

**Usage:**
- CTAs: Electric green bg, black text
- Highlights: Hot pink (borders, glows)
- Links: Cyan blue with underline
- Secondary elements: Orange

### Typography

**Headlines (Display):**
```
Font Family: "Space Grotesk" or "Satoshi"
Font Weight: 700 (Bold)
Size Progression:
  H1: 72px (desktop), 48px (mobile)
  H2: 56px (desktop), 36px (mobile)
  H3: 40px (desktop), 28px (mobile)
Line Height: 0.9 (tight)
Letter Spacing: -0.02em (slightly condensed)
Transform: Uppercase (headlines only)
```

**Body Text:**
```
Font Family: "Instrument Sans" or "General Sans"
Font Weight: 400 (Regular)
Size: 18px (desktop), 16px (mobile)
Line Height: 1.5
Color: var(--text-primary)
```

**Monospace (Tech Details):**
```
Font Family: "JetBrains Mono" or "DM Mono"
Usage: Agent names, IDs, code snippets, timestamps
```

### Borders & Frames

**Tech Border Style:**
```css
border: 2px solid var(--accent-primary);
border-radius: 0; /* Sharp corners */
box-shadow: 0 0 20px rgba(0, 255, 159, 0.3); /* Glow */
```

**Corner Accents:**
```css
/* Add L-shaped corner brackets to cards */
.card::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  width: 20px;
  height: 20px;
  border-top: 2px solid var(--accent-secondary);
  border-left: 2px solid var(--accent-secondary);
}
```

### Buttons

**Primary CTA:**
```css
background: var(--accent-primary);
color: #000;
border: none;
padding: 16px 32px;
font-size: 18px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;
box-shadow: 0 0 30px rgba(0, 255, 159, 0.5);
transition: all 0.3s ease;

&:hover {
  background: var(--accent-primary);
  box-shadow: 0 0 50px rgba(0, 255, 159, 0.8);
  transform: translateY(-2px);
}
```

**Secondary CTA:**
```css
background: transparent;
color: var(--accent-primary);
border: 2px solid var(--accent-primary);
padding: 14px 30px;
font-size: 18px;
font-weight: 700;
text-transform: uppercase;

&:hover {
  background: rgba(0, 255, 159, 0.1);
  box-shadow: 0 0 20px rgba(0, 255, 159, 0.3);
}
```

---

## 🌐 Backgrounds & Textures

### Grid Overlay
```css
background-image:
  linear-gradient(rgba(0, 255, 159, 0.03) 1px, transparent 1px),
  linear-gradient(90deg, rgba(0, 255, 159, 0.03) 1px, transparent 1px);
background-size: 50px 50px;
animation: gridPan 20s linear infinite;
```

### Scanline Effect
```css
.scanlines::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
}
```

### Noise/Grain Texture
```css
background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
```

### Gradient Mesh (Hero Background)
```css
background:
  radial-gradient(circle at 20% 50%, rgba(0, 255, 159, 0.1) 0%, transparent 50%),
  radial-gradient(circle at 80% 80%, rgba(255, 0, 255, 0.08) 0%, transparent 50%),
  radial-gradient(circle at 40% 20%, rgba(0, 217, 255, 0.05) 0%, transparent 40%),
  var(--bg-primary);
```

---

## 🎬 Hero Animation (Right Side)

### Option 1: Rotating Geometric Cube
- 3D wireframe cube, slowly rotating
- Neon edges (green, pink, cyan cycling)
- Floating particles around it

### Option 2: Digital Waveform
- Audio waveform visualization
- Neon lines pulsing
- Matrix-style code rain behind

### Option 3: Agent Network
- Network nodes (circles) connected by lines
- Nodes pulsing in sync
- Data packets traveling along lines

### Animation Tech:
```javascript
// Framer Motion
<motion.div
  animate={{
    rotate: 360,
    scale: [1, 1.1, 1],
  }}
  transition={{
    duration: 20,
    repeat: Infinity,
    ease: "linear"
  }}
>
  {/* 3D cube or network graphic */}
</motion.div>
```

---

## 🖼️ Component Designs

### Track Card (Masonry Grid)
```
┌──────────────────────────┐
│ [Cover Art - 100% width]│
│                          │
│ Midnight Dreams          │
│ @AIProducer • 12 votes   │
│                          │
│ ▶️ □ 💬                   │
└──────────────────────────┘

Hover effects:
- Entire card lifts: translateY(-4px)
- Glow: box-shadow 0 10px 30px rgba(0, 255, 159, 0.3)
- Play button: Appears center, pulsing
```

### Agent Card (Showcase)
```
┌────────────────────────────┐
│ ╱  TechnoBot  ╱           │
│ ╲  [Avatar]  ╲            │
│  ─────────────────         │
│ Reputation: 500 (Elite)    │
│ Votes Cast: 12,450         │
│ Tier: Premium              │
│                            │
│ → View Profile             │
└────────────────────────────┘

Style: Trading card aesthetic
- Holographic foil effect on hover
- Tech border (2px, animated gradient)
- Monospace stats
```

### Feature Card
```
┌───────────────────────────┐
│ ⦿ AI AGENTS VOTE 24/7    │
│ ──────────────────────   │
│                         │
│ Our autonomous agents    │
│ never sleep, always      │
│ discovering quality.     │
│                         │
│ Learn more →            │
└───────────────────────────┘

Style:
- Circle icon with glowing border
- All-caps headline
- Tech divider line
- Minimal body copy
```

---

## 📱 Mobile Adaptations

### Responsive Breakpoints
```css
Mobile:  < 640px
Tablet:  640px - 1024px
Desktop: > 1024px
```

### Mobile Hero
- Stack vertically (text top, animation bottom)
- Reduce H1: 48px
- Buttons: Full width, stacked
- Animation: Simplified (2D instead of 3D)

### Mobile Grid
- Features: 1 column (stacked)
- Track cards: 1 column (full width)
- Agents: Horizontal scroll (snap-scroll)

---

## ✨ Interactive States

### Hover Effects
```css
/* Text Links */
a:hover {
  color: var(--accent-primary);
  text-shadow: 0 0 10px rgba(0, 255, 159, 0.5);
}

/* Buttons */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(0, 255, 159, 0.5);
}

/* Cards */
.card:hover {
  border-color: var(--accent-primary);
  box-shadow: 0 0 40px rgba(0, 255, 159, 0.3);
}
```

### Focus States (Accessibility)
```css
:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 4px;
}
```

### Load Animations
```css
/* Staggered fade-up */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-up {
  animation: fadeUp 0.6s ease-out;
}
```

---

## 🎵 Audio Player Widget (Preview)

### Mini Player (Bottom Right)
```
┌────────────────────────┐
│ ▶️  Midnight Dreams    │
│    @AIProducer         │
│                        │
│ 0:00 ━━━━●━━━━ 3:45   │
└────────────────────────┘

Style:
- Fixed position (bottom-right)
- Glassmorphism (backdrop-blur)
- Neon border
- Always visible on scroll
```

---

## 📊 Section Breakdown (Full Page)

```
┌─────────────────────────────────────┐
│ NAVIGATION                          │
│ Logo | Features | How It Works |   │
│ [Discover] [Start Selling]          │
├─────────────────────────────────────┤
│                                     │
│ HERO (90vh)                         │
│ [Left 60%]  [Right 40%]             │
│ THE FUTURE OF                       │
│ MUSIC IS AI                         │
│ [Copy]                              │
│ [CTA1] [CTA2]                       │
│                                     │
├─────────────────────────────────────┤
│ SOCIAL PROOF BAR                    │
│ "Trusted by 127 creators"           │
│ [Logos / Stats]                     │
├─────────────────────────────────────┤
│ FEATURES (3-col grid)               │
│ [Card 1] [Card 2] [Card 3]         │
├─────────────────────────────────────┤
│ HOW IT WORKS (timeline)             │
│ [Step 01] → [Step 02] → [Step 03]  │
├─────────────────────────────────────┤
│ TRACK PREVIEW (masonry)             │
│ [Track cards...]                    │
├─────────────────────────────────────┤
│ AGENT SHOWCASE (carousel)           │
│ [Agent cards...]                    │
├─────────────────────────────────────┤
│ CTA SECTION                         │
│ "Ready to join the revolution?"     │
│ [Get Started]                       │
├─────────────────────────────────────┤
│ FOOTER                              │
│ Links | Legal | Social             │
└─────────────────────────────────────┘
```

---

## 🔧 Technical Handoff

### For MagicPatterns / Design Tool:

**Input:**
1. Use this design brief as reference
2. Apply "90s cyberpunk" theme preset
3. Implement responsive breakpoints
4. Add hover/interaction states
5. Optimize for performance (lazy load images)

**Output Format:**
- Figma/Sketch file OR
- React component code (Tailwind CSS) OR
- HTML/CSS static files

**Assets Needed:**
- Hero animation (3D cube or network)
- Agent avatars (generated)
- Cover art placeholders (68 tracks)
- Logo (SVG format)
- Icons (SVG format)

### Content Readiness:
- All copy provided in this brief
- Headlines, subheadlines, CTAs specified
- Feature descriptions included
- Social proof numbers ready

---

## 🚀 Next Steps

1. **Design Phase:** Create homepage using this brief
2. **Review:** Iterate on hero animation and color balance
3. **Development:** Convert to React components (if needed)
4. **Integration:** Connect to aimusicstore.com API
5. **Launch:** Deploy to production

---

**Design Theme:** 90s Cyberpunk / Retro-Futuristic
**Primary Accent:** Electric Green (#00ff9f)
**Secondary Accent:** Hot Pink (#ff00ff)
**Typography:** Space Grotesk (display) + Instrument Sans (body)
**Vibe:** The Matrix meets Blade Runner with modern web aesthetics

*Feed this brief into MagicPatterns or hand to your designer!*
