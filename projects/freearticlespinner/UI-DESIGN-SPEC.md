# freearticlespinner.com - Complete UI Design Specification

**For:** medo.dev (GPT-5 Nano)
**Designer:** Carlottta (frontend-design-ultimate skill)
**Date:** 2026-02-14
**Aesthetic:** Brutalist-Meets-Editorial (bold typography, high contrast, textural depth)

---

## 1. Design Direction & Aesthetic

### Design Philosophy
**Anti-AI-Slop Manifesto:**
- No generic gradients (purple-to-white is banned)
- No Inter/Roboto typography (use distinctive fonts)
- No centered hero on plain white background
- No generic feature grids with icon + text + "learn more"
- No 3-column layouts that break on mobile

### Chosen Aesthetic: **Industrial Editorial**

**Tone Characteristics:**
- Typography-forward (bold, condensed display fonts)
- High contrast borders (1px solid black on cream)
- Monospace accents (for code snippets, data, spin scores)
- Newsprint texture (subtle noise pattern, like printed paper)
- Stark shadows (hard 3px black, no blur)
- Raw, exposed structure (visible borders, grid lines)

**Unforgettable Element:**
Real-time "Spin Score" indicator that calculates as you type:
- Shows uniqueness percentage (0-100%)
- Animated counter (ticking up as AI processes)
- Color-coded: <60% red, 60-80% yellow, 80%+ green
- This is the hook that makes users remember the tool

---

## 2. Typography System

### Font Choices (Non-Negotiable)

```css
/* IMPORT THESE EXACT FONTS */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* CSS VARIABLES */
:root {
  --font-display: 'Space Grotesk', sans-serif;           /* Hero, headings, CTAs */
  --font-body: 'Instrument Sans', sans-serif;            /* Body text, explanations */
  --font-mono: 'JetBrains Mono', monospace;             /* Spin score, data, technical bits */
}
```

**Typography Hierarchy:**

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|----------|-------|-------|--------|--------------|-----------------|
| Hero H1 | Space Grotesk | 64px → 48px (mobile) | 700 | 1.1 | -0.02em |
| Section H2 | Space Grotesk | 48px → 32px (mobile) | 600 | 1.2 | -0.01em |
| Feature H3 | Space Grotesk | 24px → 20px (mobile) | 500 | 1.3 | 0 |
| Body text | Instrument Sans | 18px → 16px (mobile) | 400 | 1.6 | 0 |
| Small text | Instrument Sans | 14px | 400 | 1.5 | 0 |
| Spin score | JetBrains Mono | 72px → 56px (mobile) | 700 | 1 | 0 |

**Size Progression Rule:** Use 3x jumps (64 → 48 → 32 → 24), not timid 1.5x increments.

---

## 3. Color Palette (Industrial Editorial)

```css
:root {
  /* Primary Palette - Newsprint base */
  --bg-primary: #f4f1ea;        /* Cream, like aged paper */
  --bg-secondary: #ebe7de;      /* Slightly darker cream for sections */
  --bg-accent: #e8e4da;        /* Subtle border/line color */

  /* Typography - Stark black, no gray */
  --text-primary: #0d0d0d;      /* Nearly black, softer than #000 */
  --text-secondary: #3d3d3d;    /* Dark gray, not medium gray */
  --text-tertiary: #6b6b6b;     /* Muted text, timestamps */

  /* Accents - Industrial pops */
  --accent-primary: #ff4500;       /* Orange-red, bold CTAs */
  --accent-hover: #ff6a33;         /* Lighter orange */
  --accent-secondary: #2563eb;      /* Royal blue, secondary actions */
  --accent-success: #16a34a;       /* Green, spin score 80%+ */
  --accent-warning: #ca8a04;       /* Yellow, spin score 60-80% */
  --accent-error: #dc2626;         /* Red, spin score <60% */

  /* UI Elements - Hard borders, no blur */
  --border-primary: #0d0d0d;      /* 1px solid black borders */
  --border-light: #a1a1a1;         /* Lighter borders */
  --shadow-hard: 0px 3px 0px #0d0d0d;  /* Stark 3px shadow */
  --shadow-hover: 0px 6px 0px #0d0d0d;  /* Deeper on hover */
}
```

**70-20-10 Rule Applied:**
- 70% Cream backgrounds (dominant)
- 20% Stark black typography (primary)
- 10% Orange-red accents (pop)

---

## 4. Layout & Components (Section by Section)

### HERO SECTION (Above Fold)

**Layout:** Asymmetric, industrial grid
```jsx
<div className="min-h-screen bg-[--bg-primary] border-b-4 border-[--border-primary]">
  <!-- Background texture: newsprint grain -->
  <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
       style={{backgroundImage: 'url("data:image/svg+xml,...")'}} />

  <div className="relative z-10 max-w-7xl mx-auto px-6 py-20">
    <!-- Badge -->
    <div className="inline-flex items-center gap-2 px-4 py-2 
                bg-[--bg-secondary] border border-[--border-primary] 
                font-mono text-sm mb-8">
      <span className="w-2 h-2 bg-[--accent-success] rounded-full animate-pulse" />
      <span className="font-[--font-mono]">GPT-5 POWERED • TRULY FREE</span>
    </div>

    <!-- Main headline -->
    <h1 className="font-[--font-display] text-6xl md:text-7xl 
                 font-bold leading-[1.1] text-[--text-primary] 
                 tracking-tight mb-6 max-w-4xl">
      Spin Articles.
      <span className="text-[--accent-primary]">Actually Readable.</span>
    </h1>

    <!-- Subheadline -->
    <p className="font-[--font-body] text-xl md:text-2xl 
                 text-[--text-secondary] max-w-2xl mb-10 
                 leading-relaxed">
      AI-powered article rewriter. No signup. No daily limits. 
      Just paste your text and get unique, readable content in seconds.
    </p>

    <!-- CTAs -->
    <div className="flex flex-col sm:flex-row gap-4 max-w-xl">
      <button className="flex-1 px-8 py-4 bg-[--accent-primary] 
                      text-white font-[--font-display] font-semibold 
                      text-lg hover:bg-[--accent-hover] 
                      shadow-[0px_3px_0px_#0d0d0d] 
                      hover:shadow-[0px_6px_0px_#0d0d0d] 
                      transition-all">
        Start Spinning Free
      </button>
      <button className="flex-1 px-8 py-4 bg-[--bg-secondary] 
                      border border-[--border-primary] 
                      text-[--text-primary] font-[--font-display] 
                      font-semibold text-lg hover:bg-[--bg-accent] 
                      transition-colors">
        How It Works
      </button>
    </div>

    <!-- Social proof -->
    <div className="mt-16 flex items-center gap-6 text-[--text-tertiary]">
      <div className="flex items-center gap-2">
        <div className="flex -space-x-2">
          {[1,2,3,4,5].map(i => (
            <div key={i} className="w-8 h-8 rounded-full bg-gray-300 border-2 border-white" />
          ))}
        </div>
        <span className="font-[--font-mono] text-sm">12,487 spins today</span>
      </div>
      </div>
  </div>
</div>
```

---

### SPINNER TOOL (Core Feature)

**Layout:** Side-by-side split (desktop) / stacked (mobile)

```jsx
<div className="bg-[--bg-secondary] border-t-4 border-[--border-primary] py-16">
  <div className="max-w-7xl mx-auto px-6">
    
    <!-- Tool Header -->
    <div className="text-center mb-12">
      <h2 className="font-[--font-display] text-4xl md:text-5xl 
                   font-bold text-[--text-primary] mb-4">
        Paste, Spin, Publish
      </h2>
      <p className="font-[--font-body] text-lg text-[--text-secondary]">
        Enter your article below. GPT-5 Nano will rewrite it while preserving meaning.
      </p>
    </div>

    <div className="grid lg:grid-cols-2 gap-8">
      
      <!-- LEFT COLUMN: INPUT -->
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <label className="font-[--font-display] font-semibold 
                         text-lg text-[--text-primary]">
            Original Article
          </label>
          <div className="font-[--font-mono] text-sm text-[--text-tertiary]">
            <span id="charCount">0</span> / 10,000 characters
          </div>
        </div>

        <textarea
          id="inputText"
          className="flex-1 min-h-[400px] p-6 
                   bg-white border-3 border-[--border-primary] 
                   font-[--font-body] text-base text-[--text-primary] 
                   placeholder:text-[--text-tertiary] 
                   focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]
                   resize-none"
          placeholder="Paste your article here...

          Try spinning this paragraph to see how it works...

          Our AI rewrites your content while preserving the original meaning. 
          No signup required. No daily limits. Just paste and spin."
          maxLength={10000}
          onInput={(e) => {
            document.getElementById('charCount').textContent = 
              e.target.value.length.toLocaleString();
          }}
        />

        <div className="flex gap-4">
          <button 
            id="spinBtn"
            className="flex-1 px-6 py-4 bg-[--accent-primary] 
                   text-white font-[--font-display] font-bold text-xl 
                   hover:bg-[--accent-hover] 
                   shadow-[0px_3px_0px_#0d0d0d] 
                   hover:shadow-[0px_6px_0px_#0d0d0d] 
                   transition-all"
            onClick={handleSpin}>
            🔄 SPIN ARTICLE
          </button>
          <button 
            className="px-6 py-4 bg-white border-3 border-[--border-primary] 
                   text-[--text-primary] font-[--font-mono] font-semibold
                   hover:bg-[--bg-accent] transition-colors"
            onClick={handleSample}>
            Load Sample
          </button>
        </div>
      </div>

      <!-- RIGHT COLUMN: OUTPUT -->
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <label className="font-[--font-display] font-semibold 
                         text-lg text-[--text-primary]">
            Spun Article
          </label>
          
          <!-- SPIN SCORE (UNFORGETTABLE ELEMENT) -->
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                          uppercase tracking-wider">
                Spin Score
              </div>
              <div id="spinScore" 
                   className="font-[--font-mono] text-5xl md:text-6xl 
                          font-bold tabular-nums 
                          text-[--accent-success]">
                0%
              </div>
            </div>
            <div id="scoreIndicator" 
                 className="w-16 h-16 rounded-full border-4 
                        border-[--border-primary] bg-white 
                        flex items-center justify-center">
              <span className="text-2xl">⚡</span>
            </div>
          </div>
        </div>

        <textarea
          id="outputText"
          readOnly
          className="flex-1 min-h-[400px] p-6 
                   bg-[--bg-accent] border-3 border-[--border-primary] 
                   font-[--font-body] text-base text-[--text-primary] 
                   focus:outline-none resize-none"
          placeholder="Your spun article will appear here...
          
          The Spin Score shows uniqueness percentage. 
          Higher score = more unique from original."
        />

        <div className="flex gap-4">
          <button 
            id="copyBtn"
            className="flex-1 px-6 py-4 bg-[--accent-secondary] 
                   text-white font-[--font-display] font-semibold 
                   hover:bg-[#1d4ed8] transition-colors
                   disabled"
            onClick={handleCopy}>
            📋 Copy to Clipboard
          </button>
          <button 
            className="px-6 py-4 bg-white border-3 border-[--border-primary] 
                   text-[--text-primary] font-[--font-mono] font-semibold
                   hover:bg-[--bg-accent] transition-colors">
            Download .txt
          </button>
        </div>
      </div>

    </div>
  </div>
</div>
```

**Spin Score Animation (Critical):**
```javascript
// Animate spin score from 0% to final percentage
const animateScore = (targetScore) => {
  const scoreEl = document.getElementById('spinScore');
  const indicatorEl = document.getElementById('scoreIndicator');
  let current = 0;
  const duration = 1500; // 1.5 seconds
  const increment = targetScore / (duration / 16); // 60fps

  const timer = setInterval(() => {
    current += increment;
    if (current >= targetScore) {
      current = targetScore;
      clearInterval(timer);
    }

    // Update score display
    scoreEl.textContent = Math.round(current) + '%';

    // Color-coded feedback
    if (current < 60) {
      scoreEl.className = 'font-[--font-mono] text-5xl md:text-6xl font-bold tabular-nums text-[--accent-error]';
      indicatorEl.style.borderColor = 'var(--accent-error)';
    } else if (current < 80) {
      scoreEl.className = 'font-[--font-mono] text-5xl md:text-6xl font-bold tabular-nums text-[--accent-warning]';
      indicatorEl.style.borderColor = 'var(--accent-warning)';
    } else {
      scoreEl.className = 'font-[--font-mono] text-5xl md:text-6xl font-bold tabular-nums text-[--accent-success]';
      indicatorEl.style.borderColor = 'var(--accent-success)';
    }
  }, 16);
};
```

---

### FEATURES SECTION (3-Column Grid)

**Layout:** Industrial cards with hard borders

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-7xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-4">
      Why GPT-5 Nano?
    </h2>
    <p className="font-[--font-body] text-lg text-[--text-secondary] 
                 text-center max-w-2xl mx-auto mb-16">
      Fast. Cheap. High-quality. Everything you need for article spinning.
    </p>

    <div className="grid md:grid-cols-3 gap-8">
      {[
        {
          icon: '⚡',
          title: 'Lightning Fast',
          desc: 'GPT-5 Nano processes articles in 2-3 seconds. No waiting.'
        },
        {
          icon: '💰',
          title: 'Truly Free',
          desc: 'No signup. No daily limits. No credit card required. Forever free.'
        },
        {
          icon: '🎯',
          title: 'High Quality',
          desc: 'GPT-5 family model. Preserves meaning while changing words.'
        },
        {
          icon: '🔒',
          title: 'Private & Secure',
          desc: 'Your articles are processed once. Never stored or shared.'
        },
        {
          icon: '📊',
          title: 'Spin Score',
          desc: 'Real-time uniqueness indicator shows how different your content is.'
        },
        {
          icon: '🚀',
          title: 'Batch Ready',
          desc: 'Spin multiple articles in sequence. No API rate limits.'
        }
      ].map(feature => (
        <div key={feature.title} 
             className="p-8 bg-white border-3 border-[--border-primary] 
                    shadow-[0px_3px_0px_#0d0d0d] 
                    hover:shadow-[0px_6px_0px_#0d0d0d] 
                    hover:-translate-y-1 transition-all">
          <div className="text-5xl mb-4">{feature.icon}</div>
          <h3 className="font-[--font-display] text-xl font-semibold 
                       text-[--text-primary] mb-3">
            {feature.title}
          </h3>
          <p className="font-[--font-body] text-base text-[--text-secondary]">
            {feature.desc}
          </p>
        </div>
      ))}
    </div>
  </div>
</div>
```

---

### PRICING SECTION (No Brainer)

**Layout:** Stark comparison (Free vs Competitors)

```jsx
<div className="bg-[--bg-secondary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-4xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-4">
      The Choice is Obvious
    </h2>
    <p className="font-[--font-body] text-lg text-[--text-secondary] 
                 text-center mb-16">
      Why pay for article spinning when this is free?
    </p>

    <div className="grid md:grid-cols-2 gap-8">
      
      <!-- FREE (our product) -->
      <div className="p-8 bg-white border-3 border-[--border-primary] 
                    shadow-[0px_3px_0px_#0d0d0d] relative">
        <div className="absolute top-4 right-4 px-3 py-1 
                      bg-[--accent-success] text-white 
                      font-[--font-mono] text-xs font-bold uppercase">
          Best Value
        </div>
        <h3 className="font-[--font-display] text-2xl font-bold 
                     text-[--text-primary] mb-2">
          freearticlespinner.com
        </h3>
        <div className="font-[--font-mono] text-5xl font-bold 
                     text-[--accent-success] mb-6">
          FREE
          <span className="text-lg text-[--text-tertiary]">/forever</span>
        </div>
        <ul className="space-y-3 mb-8">
          {['Unlimited spins', 'No signup required', 'GPT-5 powered', 
            'Batch processing', 'Spin Score indicator'].map(item => (
            <li key={item} className="flex items-start gap-3">
              <span className="text-[--accent-success] text-xl mt-1">✓</span>
              <span className="font-[--font-body] text-[--text-primary]">{item}</span>
            </li>
          ))}
        </ul>
        <button className="w-full px-6 py-4 bg-[--accent-primary] 
                       text-white font-[--font-display] font-bold text-lg 
                       hover:bg-[--accent-hover] 
                       shadow-[0px_3px_0px_#0d0d0d] 
                       hover:shadow-[0px_6px_0px_#0d0d0d] 
                       transition-all">
          Start Spinning Now
        </button>
      </div>

      <!-- COMPETITORS (example) -->
      <div className="p-8 bg-[--bg-accent] border-3 border-[--border-light] 
                    opacity-60">
        <h3 className="font-[--font-display] text-2xl font-bold 
                     text-[--text-tertiary] mb-2">
          Others (Spinbot, QuillBot, etc.)
        </h3>
        <div className="font-[--font-mono] text-5xl font-bold 
                     text-[--text-tertiary] mb-6">
          $15-49
          <span className="text-lg text-[--text-tertiary]">/month</span>
        </div>
        <ul className="space-y-3 mb-8">
          {['Daily spin limits', 'Signup required', 'Old synonym tech', 
            'No batch processing', 'Basic output'].map(item => (
            <li key={item} className="flex items-start gap-3">
              <span className="text-[--text-tertiary] text-xl mt-1">✗</span>
              <span className="font-[--font-body] text-[--text-tertiary]">{item}</span>
            </li>
          ))}
        </ul>
        <button className="w-full px-6 py-4 bg-[--text-tertiary] 
                       text-[--bg-secondary] font-[--font-mono] font-bold 
                       cursor-not-allowed opacity-50" disabled>
          Limited Free Tier
        </button>
      </div>

    </div>
  </div>
</div>
```

---

### FAQ SECTION (Accordion)

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-3xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-16">
      Questions?
    </h2>

    <div className="space-y-4">
      {[
        {
          q: 'Is this really free forever?',
          a: 'Yes. No credit card. No signup. No limits. Paste your article and spin as many times as you want.'
        },
        {
          q: 'How does the Spin Score work?',
          a: 'GPT-5 Nano compares your spun text against the original. The percentage shows how unique the output is. Higher score = more different from source.'
        },
        {
          q: 'Will Google penalize spun content?',
          a: 'Our AI preserves meaning while rewriting content. Always review and edit spun articles before publishing. Use as a starting point, not final output.'
        },
        {
          q: 'What about long articles?',
          a: 'Up to 10,000 characters per spin. For longer content, split into sections and spin each part separately.'
        }
      ].map((faq, i) => (
        <details key={i} 
                 className="group border-3 border-[--border-primary] bg-white 
                          shadow-[0px_2px_0px_#0d0d0d] 
                          open:shadow-[0px_4px_0px_#0d0d0d]">
          <summary className="flex items-center justify-between 
                          p-6 cursor-pointer hover:bg-[--bg-accent] 
                          transition-colors">
            <span className="font-[--font-display] font-semibold 
                          text-lg text-[--text-primary]">
              {faq.q}
            </span>
            <span className="text-2xl text-[--text-primary] 
                          group-open:rotate-45 transition-transform">
              +
            </span>
          </summary>
          <div className="px-6 pb-6 font-[--font-body] 
                      text-[--text-secondary] leading-relaxed">
            {faq.a}
          </div>
        </details>
      ))}
    </div>
  </div>
</div>
```

---

### FOOTER (Minimal)

```jsx
<footer className="bg-[--text-primary] text-[--bg-primary] 
                    border-t-4 border-[--accent-primary] py-12">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex flex-col md:flex-row justify-between items-center gap-8">
      
      <div className="flex flex-col gap-4">
        <div className="font-[--font-display] font-bold text-2xl">
          freearticlespinner.com
        </div>
        <div className="font-[--font-mono] text-sm text-[--bg-secondary]">
          GPT-5 Nano Powered • Truly Free Article Rewriter
        </div>
      </div>

      <div className="flex gap-8">
        <a href="#" className="font-[--font-body] text-[--bg-secondary] 
                     hover:text-white transition-colors">
          Privacy
        </a>
        <a href="#" className="font-[--font-body] text-[--bg-secondary] 
                     hover:text-white transition-colors">
          Terms
        </a>
        <a href="#" className="font-[--font-body] text-[--bg-secondary] 
                     hover:text-white transition-colors">
          Contact
        </a>
      </div>

      <div className="font-[--font-mono] text-sm text-[--bg-secondary]">
        © 2026 freearticlespinner.com
      </div>
    </div>
  </div>
</footer>
```

---

## 5. Mobile Responsive Breakpoints

```css
/* STACK 2-COLUMN LAYOUTS */
@media (max-width: 1024px) {
  .lg\:grid-cols-2 {
    display: flex;
    flex-direction: column;
  }
}

/* STACK 3-COLUMN LAYOUTS */
@media (max-width: 768px) {
  .md\:grid-cols-3 {
    display: flex;
    flex-direction: column;
  }
  
  /* Hero text scaling */
  .text-6xl { font-size: 48px; }
  .text-7xl { font-size: 56px; }
  
  /* Spin score scaling */
  .text-5xl { font-size: 40px; }
  .text-6xl { font-size: 48px; }
}

/* COMPACT PADDING */
@media (max-width: 480px) {
  .px-6 { padding-left: 1rem; padding-right: 1rem; }
  .py-20 { padding-top: 3rem; padding-bottom: 3rem; }
  .py-16 { padding-top: 2rem; padding-bottom: 2rem; }
}
```

---

## 6. Background Texture (Newsprint Grain)

**SVG Data URI (copy-paste ready):**
```css
.newsprint::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  z-index: 0;
}
```

**Apply to hero:**
```jsx
<div className="relative min-h-screen bg-[--bg-primary] newsprint">
  <!-- Content goes here -->
</div>
```

---

## 7. Accessibility Checklist

- [ ] Color contrast: All text meets WCAG AA (4.5:1 for body, 3:1 for large text)
- [ ] Focus states: All interactive elements have visible focus (ring or outline)
- [ ] Semantic HTML: Use `<main>`, `<section>`, `<article>`, `<details>`, `<footer>`
- [ ] Alt text: All images have descriptive alt attributes
- [ ] Keyboard navigation: All features work without mouse (tabindex, enter/space handlers)
- [ ] Form labels: All inputs have associated `<label>` or `aria-label`
- [ ] Error messages: Validation errors announced via `aria-live` or `role="alert"`

---

## 8. Performance Targets

| Metric | Target | Measurement |
|--------|---------|---------------|
| First Contentful Paint (FCP) | <1.5s | Lighthouse |
| Largest Contentful Paint (LCP) | <2.5s | Lighthouse |
| Total Blocking Time (TBT) | <200ms | Lighthouse |
| Cumulative Layout Shift (CLS) | <0.1 | Lighthouse |
| Time to Interactive (TTI) | <3s | Lighthouse |

**Optimization Hints:**
- Defer non-critical CSS (fonts load asynchronously)
- Lazy-load feature cards below fold
- Minimize JavaScript bundle (tree-shake unused dependencies)
- Use system font stack fallback if Google Fonts fail to load

---

## 9. Copywriting Guidelines

### Hero Headline
**Current:** "Spin Articles. Actually Readable."
**Alternative A:** "Stop Writing. Start Spinning."
**Alternative B:** "Your Article, Reimagined."
**Alternative C:** "AI That Actually Writes Well."

### Hero Subheadline
**Current:** "AI-powered article rewriter. No signup. No daily limits. Just paste your text and get unique, readable content in seconds."

### Feature Descriptions
- Use active voice ("Spins articles" not "Articles are spun")
- Quantify benefits ("2-3 seconds" not "Fast")
- Avoid fluff words ("very", "really", "quite")
- One benefit per feature (not multiple)

---

## 10. Backend Integration Notes (for Peter)

**API Endpoint Expectation:**
```
POST /api/v1/spin
Request: { text: "original article..." }
Response: { 
  spun: "rewritten article...",
  score: 87,  // Spin score 0-100
  processingTime: 2.3  // seconds
}
```

**Error Handling:**
- Text too long (>10,000 chars): Show inline error, disable spin button
- API timeout: Show "Still spinning..." with loading spinner
- Empty input: Disable spin button until text entered

**Rate Limiting (Client-Side):**
- Debounce spin button clicks (500ms minimum between requests)
- Show cooldown after 10 spins: "Take a break! Come back in 5 minutes."

---

## 11. Testing Checklist

### Functional Testing
- [ ] Paste text works (100-10,000 chars)
- [ ] Character count updates in real-time
- [ ] Spin button triggers API call
- [ ] Output appears in right textarea
- [ ] Spin score animates from 0% to final
- [ ] Copy to clipboard works
- [ ] Download .txt works
- [ ] Sample text loads correctly
- [ ] FAQ accordions open/close

### Responsive Testing
- [ ] Hero centers on mobile (no empty space)
- [ ] Spinner tool stacks vertically (input on top, output below)
- [ ] Feature cards collapse to single column
- [ ] Pricing comparison stacks (free on top, competitors below)
- [ ] Footer stacks vertically

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest macOS/iOS)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS 16+)
- [ ] Chrome Mobile (Android 13+)

---

## 12. Launch Checklist

### Before Launch
- [ ] All fonts load (check Network tab)
- [ ] Spin score animation smooth (60fps)
- [ ] Copy/download functions work
- [ ] FAQ accordions function
- [ ] Mobile responsive (test on real device)
- [ ] Performance score 90+ (Lighthouse)
- [ ] Accessibility score 90+ (Lighthouse)

### Day 1 Launch
- [ ] Site accessible via domain
- [ ] API endpoint responding
- [ ] First 10 test spins successful
- [ ] Analytics tracking installed (Google Analytics or Plausible)

### Week 1 Post-Launch
- [ ] Monitor API errors (Sentry or similar)
- [ ] Track spin count (goal: 1,000+ spins/day 1)
- [ ] Gather feedback (add "Report Issue" button)
- [ ] SEO basics (meta description, og:image, sitemap.xml)

---

## FINAL NOTES FOR PETER

### Copy-Paste Ready
This entire spec is designed to be copy-pasted into medo.dev. The CSS classes are Tailwind utility classes that medo.dev should understand natively.

### Non-Negotiable Elements
These design decisions are critical to the anti-AI-slop aesthetic:
1. **Space Grotesk + Instrument Sans + JetBrains Mono** (no substitutions)
2. **Industrial Editorial color palette** (cream background, black borders, orange accents)
3. **Spin Score animation** (this is the unforgettable element)
4. **Newsprint grain texture** (subtle noise overlay)
5. **Hard 3px shadows** (no blur, stark depth)
6. **70-20-10 color rule** (70% cream, 20% black text, 10% orange accents)

### What to Customize
- Adjust padding/spacing to fit your container
- Add your own copywriting if my suggestions don't resonate
- Add additional features if needed (e.g., history, export options)
- Modify API endpoint structure if your backend differs

### What NOT to Change
- Typography system (this is the distinctive element)
- Color palette (proven high-contrast, memorable)
- Spin Score concept (this is the viral hook)
- Layout structure (hero → tool → features → pricing → FAQ → footer)

---

**Ready to build. Paste this into medo.dev and watch the magic happen.** 🎨

*Designed by Carlottta using frontend-design-ultimate skill*
*Industrial Editorial aesthetic: bold typography, stark borders, newsprint texture*
*Unforgettable element: Animated Spin Score indicator*
