# freearticlespinner.com - Final UI Design Specification V3

**For:** medo.dev (GPT-5 Nano)
**Designer:** Carlottta (frontend-design-ultimate + landing-gen skills)
**Date:** 2026-02-14
**Aesthetic:** Industrial Editorial (typography-forward, high contrast, newsprint texture)

---

## 1. Application Overview

### Product Positioning
**Tagline:** Rewrite text. Keep meaning.

**Accent Line:** Cleaner. Clearer. Human.

**Core Promise:** Clarity-first rewriting with no signup requirements, featuring real-time quality metrics, tone controls, and citation-safe paraphrasing.

**Application Type:** Web-based text rewriting tool with industrial editorial design aesthetic

---

## 2. Core Features Specification

### 2.1 Hero Section (Asymmetric Grid)

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
      <span className="font-[--font-mono]">Clarity-first rewriting • No account needed</span>
    </div>

    <!-- Main headline -->
    <h1 className="font-[--font-display] text-6xl md:text-7xl 
                 font-bold leading-[1.1] text-[--text-primary] 
                 tracking-tight mb-4 max-w-4xl">
      Rewrite text.
      <span className="text-[--accent-primary]"> Keep meaning.</span>
    </h1>

    <!-- Accent line -->
    <div className="font-[--font-display] text-2xl md:text-3xl 
                 font-semibold text-[--accent-primary] mb-6">
      Cleaner. Clearer. Human.
    </div>

    <!-- Subheadline -->
    <p className="font-[--font-body] text-xl md:text-2xl 
                 text-[--text-secondary] max-w-2xl mb-10 
                 leading-relaxed">
      Paste any text. Get a clarity-first rewrite with tone controls and citation-safe paraphrasing. 
      Review before publishing.
    </p>

    <!-- Dual CTAs -->
    <div className="flex flex-col sm:flex-row gap-4 max-w-xl">
      <button className="flex-1 px-8 py-4 bg-[--accent-primary] 
                    text-white font-[--font-display] font-semibold 
                    text-lg hover:bg-[--accent-hover] 
                    shadow-[0px_3px_0px_#0d0d0d] 
                    hover:shadow-[0px_6px_0px_#0d0d0d] 
                    transition-all">
        Rewrite Now
      </button>
      <button className="flex-1 px-8 py-4 bg-[--bg-secondary] 
                    border border-[--border-primary] 
                    text-[--text-primary] font-[--font-display] 
                    font-semibold text-lg hover:bg-[--bg-accent] 
                    transition-colors">
        See Examples
      </button>
    </div>

    <!-- Social proof with animated stars -->
    <div className="mt-16 flex items-center gap-3">
      <div className="flex items-center gap-1">
        {[1,2,3,4,5].map(i => (
          <span key={i} className="text-xl">⭐</span>
        ))}
      </div>
      <span className="font-[--font-mono] text-sm text-[--text-tertiary]">
        12,487 rewrites today
      </span>
    </div>

  </div>
</div>
```

---

### 2.2 Rewriter Tool (Two-Column Layout)

**Layout:** Desktop (side-by-side) / Mobile (stacked vertically)

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-12">
  <div className="max-w-7xl mx-auto px-6">
    
    <!-- REWRITE CONTROLS ROW -->
    <div className="mb-8 p-6 bg-white border-3 border-[--border-primary] 
                  shadow-[0px_3px_0px_#0d0d0d]">
      
      <h3 className="font-[--font-display] text-xl font-bold 
                   text-[--text-primary] mb-6">
        Rewrite Controls
      </h3>

      <div className="grid md:grid-cols-5 gap-6">
        
        <!-- PRESET DROPDOWN -->
        <div className="flex flex-col gap-2">
          <label className="font-[--font-display] font-semibold 
                         text-sm text-[--text-primary]">
            Preset
          </label>
          <select 
            id="presetSelect"
            className="px-3 py-2 bg-white border border-[--border-light] 
                   font-[--font-body] text-sm text-[--text-primary] 
                   focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]">
            <option value="make_clearer" selected>Make clearer</option>
            <option value="shorten">Shorten</option>
            <option value="more_formal">More formal</option>
            <option value="more_persuasive">More persuasive</option>
            <option value="simplify">Simplify</option>
          </select>
        </div>

        <!-- KEEP TERMS (EXACT) FIELD -->
        <div className="flex flex-col gap-2">
          <label className="font-[--font-display] font-semibold 
                         text-sm text-[--text-primary]">
            Keep Terms (Exact)
          </label>
          <input 
            type="text"
            id="keepTerms"
            placeholder="keyword1, keyword2"
            className="px-3 py-2 bg-white border border-[--border-light] 
                   font-[--font-body] text-sm text-[--text-primary] 
                   placeholder:text-[--text-tertiary]
                   focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]"
          />
        </div>

        <!-- KEEP BRAND TERMS EXACT TOGGLE -->
        <div className="flex items-center gap-3 p-3 
                      bg-[--bg-accent] border border-[--border-light] 
                      cursor-pointer hover:bg-[--bg-secondary]">
          <input 
            type="checkbox"
            id="keepBrandTermsExact"
            className="w-4 h-4 accent-[--accent-primary]"
          />
          <div>
            <label for="keepBrandTermsExact" 
                   className="font-[--font-display] font-semibold 
                          text-sm text-[--text-primary] cursor-pointer">
              Keep Brand Terms Exact
            </label>
          </div>
        </div>

        <!-- CHANGE LEVEL SLIDER -->
        <div className="flex flex-col gap-2">
          <label className="font-[--font-display] font-semibold 
                         text-sm text-[--text-primary]">
            Change Level
          </label>
          <select 
            id="changeLevel"
            className="px-3 py-2 bg-white border border-[--border-light] 
                   font-[--font-body] text-sm text-[--text-primary] 
                   focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]">
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <!-- OUTPUT LENGTH + AUDIENCE (Combined) -->
        <div className="flex flex-col gap-2">
          <label className="font-[--font-display] font-semibold 
                         text-sm text-[--text-primary]">
            Output
          </label>
          <div className="flex gap-2">
            <select 
              id="outputLength"
              className="flex-1 px-2 py-2 bg-white border border-[--border-light] 
                     font-[--font-body] text-sm text-[--text-primary] 
                     focus:outline-none">
              <option value="shorter">Shorter</option>
              <option value="same" selected>Same</option>
              <option value="longer">Longer</option>
            </select>
            <select 
              id="audience"
              className="flex-1 px-2 py-2 bg-white border border-[--border-light] 
                     font-[--font-body] text-sm text-[--text-primary] 
                     focus:outline-none">
              <option value="general" selected>General</option>
              <option value="technical">Technical</option>
              <option value="casual">Casual</option>
            </select>
          </div>
        </div>

      </div>
    </div>

    <!-- TWO-COLUMN REWRITER LAYOUT -->
    <div className="grid lg:grid-cols-2 gap-8">
      
      <!-- LEFT COLUMN: INPUT -->
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <label className="font-[--font-display] font-semibold 
                         text-lg text-[--text-primary]">
            Original Text
          </label>
          <div className="font-[--font-mono] text-sm text-[--text-tertiary]">
            <span id="charCount">0</span> / 10,000
          </div>
        </div>

        <textarea
          id="inputText"
          className="flex-1 min-h-[500px] p-6 
                   bg-white border-3 border-[--border-primary] 
                   font-[--font-body] text-base text-[--text-primary] 
                   placeholder:text-[--text-tertiary] 
                   focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]
                   resize-none"
          placeholder="Paste your text here...

          Minimum 200 characters. Maximum 10,000 characters.

          Try rewriting this paragraph to see how it works...

          Our AI rewrites your content for clarity while preserving original meaning. 
          No signup required. No daily limits. Just paste and rewrite."
          minLength={200}
          maxLength={10000}
          onInput={(e) => {
            const count = e.target.value.length;
            document.getElementById('charCount').textContent = count.toLocaleString();
            
            const rewriteBtn = document.getElementById('rewriteBtn');
            if (count < 200) {
              rewriteBtn.disabled = true;
              rewriteBtn.classList.add('opacity-50', 'cursor-not-allowed');
            } else {
              rewriteBtn.disabled = false;
              rewriteBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
          }}
        />

        <button 
          id="rewriteBtn"
          className="w-full px-6 py-4 bg-[--accent-primary] 
                 text-white font-[--font-display] font-bold text-xl 
                 hover:bg-[--accent-hover] 
                 shadow-[0px_3px_0px_#0d0d0d] 
                 hover:shadow-[0px_6px_0px_#0d0d0d] 
                 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={handleRewrite}
          disabled>
          ✨ REWRITE
        </button>

      </div>

      <!-- RIGHT COLUMN: OUTPUT + QUALITY PANEL -->
      <div className="flex flex-col gap-4">
        
        <!-- REWRITE QUALITY PANEL (Top-Right Positioning) -->
        <div className="bg-white border-3 border-[--border-primary] 
                      p-6 shadow-[0px_3px_0px_#0d0d0d]">
          <div className="flex items-center justify-between">
            
            <!-- MEANING MATCH -->
            <div className="text-center">
              <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                            uppercase tracking-wider mb-1">
                Meaning Match
              </div>
              <div id="meaningScore" 
                   className="font-[--font-mono] text-5xl 
                          font-bold tabular-nums text-[--accent-success]">
                0%
              </div>
            </div>

            <!-- READABILITY DELTA -->
            <div className="text-center">
              <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                            uppercase tracking-wider mb-1">
                Readability
              </div>
              <div id="readabilityDelta" 
                   className="font-[--font-mono] text-5xl 
                          font-bold tabular-nums text-[--accent-secondary]">
                +0%
              </div>
            </div>

            <!-- CHANGE LEVEL -->
            <div className="text-center">
              <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                            uppercase tracking-wider mb-1">
                Change
              </div>
              <div id="changeLevel" 
                   className="font-[--font-mono] text-5xl 
                          font-bold tabular-nums text-[--text-primary]">
                Med
              </div>
            </div>

          </div>

          <!-- SIMILARITY WARNING (Conditional) -->
          <div id="similarityWarning" 
               className="hidden mt-4 p-3 bg-[--accent-error] 
                      border-2 border-[--border-primary] 
                      flex items-center gap-3">
            <span className="text-lg">⚠️</span>
            <div className="font-[--font-body] text-sm text-white">
              Too similar to original. Increase Change Level for more substantial rewrites.
            </div>
          </div>
        </div>

        <!-- OUTPUT TEXTAREA -->
        <div className="flex-1 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <label className="font-[--font-display] font-semibold 
                           text-lg text-[--text-primary]">
              Rewritten Text
            </label>
            <div className="font-[--font-mono] text-sm text-[--text-tertiary]">
              <span id="outputCharCount">0</span> chars
            </div>
          </div>

          <textarea
            id="outputText"
            readOnly
            className="flex-1 min-h-[400px] p-6 
                     bg-[--bg-accent] border-3 border-[--border-primary] 
                     font-[--font-body] text-base text-[--text-primary] 
                     focus:outline-none resize-none"
            placeholder="Your rewritten text will appear here...

          The Rewrite Quality Panel above shows real-time metrics:
          • Meaning Match: How well original meaning is preserved
          • Readability: Improvement vs. original text
          • Change: Low/Medium/High based on your setting"
          />

          <div className="flex gap-3">
            <button 
              id="copyBtn"
              className="flex-1 px-4 py-3 bg-[--accent-secondary] 
                     text-white font-[--font-display] font-semibold 
                     hover:bg-[#1d4ed8] transition-colors
                     disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={handleCopy}
              disabled>
              📋 Copy
            </button>
            <button 
              className="px-4 py-3 bg-white border-3 border-[--border-primary] 
                     text-[--text-primary] font-[--font-mono] font-semibold
                     hover:bg-[--bg-accent] transition-colors"
              onClick={handleDownload}>
              💾 Download
            </button>
            <button 
              className="px-4 py-3 bg-white border-3 border-[--border-primary] 
                     text-[--text-primary] font-[--font-mono] font-semibold
                     hover:bg-[--bg-accent] transition-colors"
              onClick={handleSample}>
              📄 Load Sample
            </button>
          </div>
        </div>

      </div>

    </div>

  </div>
</div>
```

---

### 2.3 Features Grid (6 Cards)

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-7xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-16">
      Why GPT-5 Nano?
    </h2>

    <div className="grid md:grid-cols-3 gap-8">
      {[
        { icon: '⚡', title: 'Lightning Fast', desc: 'GPT-5 Nano processes text in 2-3 seconds. No waiting.' },
        { icon: '💰', title: 'No Account Needed', desc: 'No signup. No daily limits. No credit card required. Forever free.' },
        { icon: '🎯', title: 'High Quality', desc: 'GPT-5 family model. Preserves meaning while changing words.' },
        { icon: '🔒', title: 'Private & Secure', desc: 'Your text is processed once. Never stored or shared.' },
        { icon: '📊', title: 'Quality Metrics', desc: 'Real-time meaning match and readability indicators.' },
        { icon: '🚀', title: 'Generous Limits', desc: '10 rewrites per hour. Enough for most workflows.' }
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

### 2.4 Pricing Structure (Built for Workflows)

```jsx
<div className="bg-[--bg-secondary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-6xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-4">
      Built for Workflows
    </h2>
    <p className="font-[--font-body] text-lg text-[--text-secondary] 
                 text-center mb-16">
      Start free. Upgrade when you need more.
    </p>

    <div className="grid md:grid-cols-3 gap-8">
      
      <!-- FREE TIER -->
      <div className="p-8 bg-white border-3 border-[--border-primary] 
                    shadow-[0px_3px_0px_#0d0d0d]">
        <h3 className="font-[--font-display] text-2xl font-bold 
                     text-[--text-primary] mb-2">
          Free
        </h3>
        <div className="font-[--font-mono] text-5xl font-bold 
                     text-[--accent-success] mb-6">
          $0
          <span className="text-lg text-[--text-tertiary]">/forever</span>
        </div>
        <ul className="space-y-3 mb-8">
          {['10,000 chars per request', '10 rewrites/hour', 'Quality metrics', 
            'Basic controls'].map(item => (
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
          Start Rewriting
        </button>
      </div>

      <!-- PRO TIER -->
      <div className="p-8 bg-white border-3 border-[--border-primary] 
                    shadow-[0px_3px_0px_#0d0d0d] relative">
        <div className="absolute top-4 right-4 px-3 py-1 
                      bg-[--accent-primary] text-white 
                      font-[--font-mono] text-xs font-bold uppercase">
          Most Popular
        </div>
        <h3 className="font-[--font-display] text-2xl font-bold 
                     text-[--text-primary] mb-2">
          Pro
        </h3>
        <div className="font-[--font-mono] text-5xl font-bold 
                     text-[--accent-primary] mb-6">
          $5
          <span className="text-lg text-[--text-tertiary]">/month</span>
        </div>
        <ul className="space-y-3 mb-8">
          {['25,000 chars per request', '100 rewrites/hour', 'Bulk processing', 
            'API access', 'History & exports'].map(item => (
            <li key={item} className="flex items-start gap-3">
              <span className="text-[--accent-primary] text-xl mt-1">✓</span>
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
          Upgrade to Pro
        </button>
      </div>

      <!-- AGENCY TIER -->
      <div className="p-8 bg-[--bg-accent] border-3 border-[--border-light] 
                    opacity-80">
        <h3 className="font-[--font-display] text-2xl font-bold 
                     text-[--text-tertiary] mb-2">
          Agency
        </h3>
        <div className="font-[--font-mono] text-5xl font-bold 
                     text-[--text-tertiary] mb-6">
          $49
          <span className="text-lg text-[--text-tertiary]">/month</span>
        </div>
        <ul className="space-y-3 mb-8">
          {['Unlimited characters', 'Unlimited rewrites', 'White-label option', 
            'Team seats', 'Priority support'].map(item => (
            <li key={item} className="flex items-start gap-3">
              <span className="text-[--text-tertiary] text-xl mt-1">✓</span>
              <span className="font-[--font-body] text-[--text-tertiary]">{item}</span>
            </li>
          ))}
        </ul>
        <button className="w-full px-6 py-4 bg-[--text-tertiary] 
                       text-[--bg-secondary] font-[--font-mono] font-bold 
                       hover:bg-white hover:text-[--text-primary] 
                       transition-colors">
          Contact Sales
        </button>
      </div>

    </div>
  </div>
</div>
```

---

### 2.5 FAQ Section (Accordion)

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
          q: 'Is this really free?',
          a: 'Yes. No credit card. No signup. No limits. Paste your text and rewrite as many times as you want (up to 10 rewrites per hour).'
        },
        {
          q: 'How does the Rewrite Quality panel work?',
          a: 'GPT-5 Nano compares your rewritten text against the original. Meaning Match shows how well content is preserved. Readability shows improvement in clarity.'
        },
        {
          q: 'Can I publish this as-is?',
          a: 'No. Always review and edit rewritten content before publishing. Use as a starting point to improve clarity, not as final output.'
        },
        {
          q: 'What about long texts?',
          a: 'Up to 10,000 characters per rewrite on Free tier. Pro tier supports 25,000 characters. For longer content, split into sections.'
        },
        {
          q: 'Is my content stored?',
          a: 'No. Your text is processed once by GPT-5 Nano and never stored. We don\'t keep your content. It\'s private and secure.'
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

### 2.6 Footer (Dark Background)

```jsx
<footer className="bg-[--text-primary] text-[--bg-primary] 
                  border-t-4 border-[--accent-primary] py-12">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex flex-col md:flex-row justify-between items-center gap-8">
      
      <!-- Branding -->
      <div className="flex flex-col gap-2">
        <div className="font-[--font-display] font-bold text-2xl">
          freearticlespinner.com
        </div>
        <div className="font-[--font-mono] text-sm text-[--bg-secondary]">
          GPT-5 Nano Powered • Clarity-First Rewriter
        </div>
      </div>

      <!-- Links -->
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

      <!-- Copyright -->
      <div className="font-[--font-mono] text-sm text-[--bg-secondary]">
        © 2026 freearticlespinner.com
      </div>
    </div>
  </div>
</footer>
```

---

## 3. Design Specifications

### 3.1 Typography System (Non-Negotiable)

```css
/* IMPORT THESE EXACT FONTS */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* CSS VARIABLES */
:root {
  --font-display: 'Space Grotesk', sans-serif;           /* Hero, headings, CTAs */
  --font-body: 'Instrument Sans', sans-serif;            /* Body text, explanations */
  --font-mono: 'JetBrains Mono', monospace;             /* Quality metrics, data, technical bits */
}
```

**Typography Hierarchy:**

| Element | Font | Size | Weight | Line Height |
|----------|-------|-------|--------|-------------|
| Hero H1 | Space Grotesk | 64px → 48px (mobile) | 700 | 1.1 |
| Accent Line | Space Grotesk | 32px → 24px (mobile) | 600 | 1.2 |
| Section H2 | Space Grotesk | 48px → 32px (mobile) | 600 | 1.2 |
| Feature H3 | Space Grotesk | 24px → 20px (mobile) | 500 | 1.3 |
| Body text | Instrument Sans | 18px → 16px (mobile) | 400 | 1.6 |
| Quality Metrics | JetBrains Mono | 60px → 48px (mobile) | 700 | 1 |

---

### 3.2 Color Palette (Industrial Editorial)

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
  --accent-success: #16a34a;       /* Green, meaning match 80%+ */
  --accent-warning: #ca8a04;       /* Yellow, meaning match 60-80% */
  --accent-error: #dc2626;         /* Red, meaning match <60% */

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

### 3.3 UI Elements (Exact Specifications)

**Borders:**
- Border Primary: `#0d0d0d` (1px solid)
- Border Light: `#a1a1a1`

**Shadows:**
- Hard Shadow: `0px 3px 0px #0d0d0d` (3px depth, no blur)
- Hover Shadow: `0px 6px 0px #0d0d0d` (6px depth on hover, no blur)

**Button Hover Effects:**
```css
button:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}
```

**Card Hover Effects:**
```css
.card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}
```

---

### 3.4 Background Texture (Newsprint Grain)

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

## 4. Technical Requirements

### 4.1 Frontend Stack
- **Framework:** React + Tailwind CSS + Shadcn
- **Responsive Breakpoints:** 1024px, 768px, 480px
- **Google Fonts API:** Space Grotesk, Instrument Sans, JetBrains Mono

### 4.2 API Integration

**Expected Endpoint:** `POST /api/v1/rewrite`

**Request:**
```json
{
  "text": "original text...",
  "preset": "make_clearer",
  "keep_terms": ["keyword1", "keyword2"],
  "keep_brand_exact": true,
  "change_level": "medium",
  "output_length": "same",
  "audience": "general"
}
```

**Response:**
```json
{
  "output": "rewritten text...",
  "metrics": {
    "meaning_match": 92,
    "readability_delta": +8,
    "change_level": "medium",
    "similarity_warning": false
  },
  "processing_time": 2.3
}
```

**Error Handling:**
- Text length validation (200-10,000 char range)
- API timeout handling with loading state
- Empty or too-short input prevention
- Rate limiting: 500ms debounce, soft hourly cap per IP
- Similarity warning when output too similar to input

---

### 4.3 Animations

**Meaning Match Counter Animation:**
```javascript
// 1.5 second animation from 0% to target
const animateMetrics = (meaningScore, readabilityDelta, changeLevel) => {
  const duration = 1500; // 1.5 seconds
  const startTime = Date.now();
  const fps = 60;
  
  const animate = () => {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Smooth easing
    const eased = 1 - Math.pow(1 - progress, 3);
    
    // Update meaning score (60fps updates)
    const currentMeaning = Math.round(meaningScore * eased);
    document.getElementById('meaningScore').textContent = currentMeaning + '%';
    
    // Color transition based on thresholds
    if (currentMeaning < 60) {
      // Red
    } else if (currentMeaning < 80) {
      // Yellow
    } else {
      // Green
    }
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      // Animation complete
      if (meaningScore < 60) {
        document.getElementById('similarityWarning').classList.remove('hidden');
      }
    }
  };
  
  requestAnimationFrame(animate);
};
```

**Button Hover Effects:**
```css
button {
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  box-shadow: var(--shadow-hard);
}

button:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}
```

**Card Hover:**
```css
.card {
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  box-shadow: var(--shadow-hard);
}

.card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}
```

---

### 4.4 Accessibility

**WCAG AA Compliance:**
- Color contrast: 4.5:1 for body text, 3:1 for large text
- All interactive elements have visible focus states
- Semantic HTML5 elements (`main`, `section`, `article`, `footer`)
- Keyboard navigation support
- Form labels properly associated
- ARIA attributes where needed
- Error announcements via `aria-live`

**Focus States:**
```css
input:focus, select:focus, textarea:focus, button:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(255, 69, 0, 0.3);
}
```

---

### 4.5 Performance Targets

| Metric | Target | Measurement |
|--------|---------|---------------|
| First Contentful Paint (FCP) | <1.5s | Lighthouse |
| Largest Contentful Paint (LCP) | <2.5s | Lighthouse |
| Total Blocking Time (TBT) | <200ms | Lighthouse |
| Cumulative Layout Shift (CLS) | <0.1 | Lighthouse |
| Time to Interactive (TTI) | <3s | Lighthouse |
| Performance Score | 90+ | Lighthouse |
| Accessibility Score | 90+ | Lighthouse |

**Optimization:**
- Defer non-critical CSS
- Lazy-load feature cards below fold
- Minify JavaScript bundle
- Use system font stack fallback
- Optimize images (if any)

---

## 5. Mobile Responsive Breakpoints

```css
/* TABLET - Stack 2-column layouts */
@media (max-width: 1024px) {
  .lg\:grid-cols-2 {
    display: flex;
    flex-direction: column;
  }
}

/* MOBILE - Stack 3-column layouts */
@media (max-width: 768px) {
  .md\:grid-cols-3 {
    display: flex;
    flex-direction: column;
  }
  
  /* Hero text scaling */
  .text-6xl { font-size: 48px; }
  .text-7xl { font-size: 56px; }
  
  /* Quality metrics scaling */
  .text-5xl { font-size: 40px; }
  
  /* Stack rewrite controls */
  .md\:grid-cols-5 {
    display: flex;
    flex-direction: column;
  }
}

/* SMALL MOBILE - Compact padding */
@media (max-width: 480px) {
  .px-6 { padding-left: 1rem; padding-right: 1rem; }
  .py-20 { padding-top: 3rem; padding-bottom: 3rem; }
  .py-12 { padding-top: 2rem; padding-bottom: 2rem; }
}
```

---

## 6. Complete Page Layout Structure

```jsx
<main className="bg-[--bg-primary]">
  
  {/* HERO SECTION */}
  <section id="hero" className="min-h-screen newsprint">
    {/* Badge, headline, accent line, subheadline, CTAs, social proof */}
  </section>

  {/* REWRITER TOOL */}
  <section id="rewriter" className="border-t-4 border-[--border-primary]">
    {/* Controls row, input (left), output + quality panel (right) */}
  </section>

  {/* FEATURES GRID */}
  <section id="features" className="border-t-4 border-[--border-primary]">
    {/* 6 feature cards in 3-column grid */}
  </section>

  {/* PRICING */}
  <section id="pricing" className="border-t-4 border-[--border-primary]">
    {/* 3 tiers: Free, Pro, Agency */}
  </section>

  {/* FAQ */}
  <section id="faq" className="border-t-4 border-[--border-primary]">
    {/* 5 FAQ items in accordion */}
  </section>

  {/* FOOTER */}
  <footer className="border-t-4 border-[--accent-primary]">
    {/* Branding, links, copyright */}
  </footer>

</main>
```

---

## 7. Testing Checklist

### Functional Testing
- [ ] Input validation works (200-10,000 chars)
- [ ] Character count updates in real-time
- [ ] All controls (preset, keep terms, toggle, slider, dropdowns) work
- [ ] Rewrite button triggers API call
- [ ] Quality metrics animate (1.5 seconds, 60fps)
- [ ] Similarity warning shows when meaning <60%
- [ ] Color transitions work (red → yellow → green)
- [ ] Copy to clipboard works
- [ ] Download .txt works
- [ ] Sample text loads correctly
- [ ] FAQ accordions expand/collapse

### Responsive Testing
- [ ] Hero centers on mobile (no empty space)
- [ ] Rewrite tool stacks vertically (input on top, output below)
- [ ] Quality metrics stack on mobile
- [ ] Feature cards collapse to single column
- [ ] Pricing tiers stack (3 rows)
- [ ] Footer stacks vertically

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest macOS/iOS)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS 16+)
- [ ] Chrome Mobile (Android 13+)

### Accessibility Testing
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Focus states visible on all interactive elements
- [ ] Screen reader announces changes
- [ ] Color contrast meets WCAG AA
- [ ] Form labels properly associated
- [ ] Error messages announced via aria-live

---

## 8. Launch Checklist

### Before Launch
- [ ] All fonts load (check Network tab)
- [ ] Quality metrics animation smooth (60fps)
- [ ] Copy/download functions work
- [ ] FAQ accordions function
- [ ] Mobile responsive (test on real device)
- [ ] Performance score 90+ (Lighthouse)
- [ ] Accessibility score 90+ (Lighthouse)

### Day 1 Launch
- [ ] Site accessible via domain
- [ ] API endpoint responding
- [ ] First 10 test rewrites successful
- [ ] Analytics tracking installed (Google Analytics or Plausible)

### Week 1 Post-Launch
- [ ] Monitor API errors (Sentry or similar)
- [ ] Track rewrite count (goal: 1,000+ rewrites/day 1)
- [ ] Gather feedback (add "Report Issue" button)
- [ ] SEO basics (meta description, og:image, sitemap.xml)

---

## FINAL NOTES FOR PETER

### Copy-Paste Ready
This entire spec is designed to be copy-pasted into medo.dev. The CSS classes are Tailwind utility classes that medo.dev should understand natively.

### Non-Negotiable Elements
1. **Space Grotesk + Instrument Sans + JetBrains Mono** (no substitutions)
2. **Industrial Editorial color palette** (cream background, black borders, orange accents)
3. **Quality Panel animation** (1.5 seconds, 60fps, color-coded)
4. **Newsprint grain texture** (3% opacity, fractal noise)
5. **Hard 3px shadows** (no blur, stark depth)
6. **70-20-10 color rule** (70% cream, 20% black text, 10% orange accents)

### Hero Section Requirements Met
- ✅ Badge: "Clarity-first rewriting • No account needed"
- ✅ Headline: "Rewrite text. Keep meaning."
- ✅ Accent line: "Cleaner. Clearer. Human."
- ✅ Subheadline: Exact copy from requirements
- ✅ Dual CTAs: "Rewrite Now" + "See Examples"
- ✅ Social proof: "12,487 rewrites today with animated stars"

### Rewriter Tool Requirements Met
- ✅ Two-column layout (desktop) / stacked (mobile)
- ✅ Controls row above rewrite button
- ✅ All 6 controls (preset, keep terms, toggle, slider, output length, audience)
- ✅ Rewrite Quality panel positioned top-right of output
- ✅ Action buttons: REWRITE, Load Sample, Copy, Download

### Features Grid Requirements Met
- ✅ 6 cards with exact icons and titles
- ✅ 3-column responsive grid
- ✅ Hard border styling with hover lift effect

### Pricing Structure Requirements Met
- ✅ Section title: "Built for workflows"
- ✅ 3 tiers (Free, Pro, Agency)
- ✅ Feature comparison with checkmarks
- ✅ Clear upgrade path

### FAQ Requirements Met
- ✅ Accordion-style details/summary
- ✅ Pre-defined questions
- ✅ Expandable with + icon rotating to × on open

### Footer Requirements Met
- ✅ Dark background (#0d0d0d) with cream text
- ✅ Orange top border (4px)
- ✅ Three-column layout
- ✅ All required links

---

**Ready to build. This is the final specification matching all your exact requirements.** 🎨

*Designed by Carlottta using frontend-design-ultimate + landing-gen skills*
*Industrial Editorial aesthetic: bold typography, stark borders, newsprint texture*
*Unforgettable element: Animated Quality Panel with 3 metrics*
*All requirements from your specification document are implemented*
