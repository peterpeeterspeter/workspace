# freearticlespinner.com - Enhanced UI Design Specification V2

**For:** medo.dev (GPT-5 Nano)
**Designer:** Carlottta (frontend-design-ultimate + landing-gen skills)
**Date:** 2026-02-14
**Aesthetic:** Industrial Editorial (typography-forward, high contrast, newsprint texture)

---

## 1. Application Overview

### Product Positioning
**What it is:** A GPT-5 Nano powered text rewriting tool that transforms original content into clearer, more readable versions while preserving meaning.

**Core Promise:** Clarity-first rewriting with no signup requirements, featuring a real-time Rewrite Quality panel that shows meaning match, readability improvements, and change level metrics.

**Application Type:** Web-based text rewriting tool with industrial editorial design aesthetic

---

## 2. Core Features Specification

### 2.1 Text Rewriting Engine

**Input Area:**
```jsx
<div className="flex flex-col gap-4">
  <div className="flex items-center justify-between">
    <label className="font-[--font-display] font-semibold text-lg text-[--text-primary]">
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

    Minimum 200 characters to prevent spam. Maximum 10,000 characters per request.

    Try rewriting this paragraph to see how it works...

    Our AI rewrites your content for clarity while preserving original meaning. 
    No signup required. No daily limits. Just paste and rewrite."
    minLength={200}
    maxLength={10000}
    onInput={(e) => {
      const count = e.target.value.length;
      document.getElementById('charCount').textContent = count.toLocaleString();
      
      // Enable/disable rewrite button based on minimum length
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

  <div className="flex gap-4">
    <button 
      id="rewriteBtn"
      className="flex-1 px-6 py-4 bg-[--accent-primary] 
             text-white font-[--font-display] font-bold text-xl 
             hover:bg-[--accent-hover] 
             shadow-[0px_3px_0px_#0d0d0d] 
             hover:shadow-[0px_6px_0px_#0d0d0d] 
             transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      onClick={handleRewrite}
      disabled>
      ✨ REWRITE ARTICLE
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
```

**Validation Rules:**
- **Minimum:** 200 characters (prevent spam/empty submissions)
- **Maximum:** 10,000 characters per request
- **Real-time counter:** Shows current count with visual feedback
- **Button state:** Disabled when <200 chars, enabled when ≥200 chars

**Soft Cap Per Hour:**
- 10 rewrites per hour per IP (generous usage limits)
- Client-side debouncing: 500ms minimum between requests
- Show cooldown indicator after 10 rewrites: "Take a break! Come back in 5 minutes."

---

### 2.2 Rewrite Quality Panel (UNFORGETTABLE ELEMENT)

**Layout:** Prominently displayed above output area

```jsx
<div className="bg-[--bg-accent] border-t-4 border-[--border-primary] py-8">
  <div className="max-w-7xl mx-auto px-6">
    
    <div className="text-center mb-8">
      <h2 className="font-[--font-display] text-3xl md:text-4xl 
                   font-bold text-[--text-primary] mb-2">
        Rewrite Quality Panel
      </h2>
      <p className="font-[--font-body] text-base text-[--text-secondary]">
        Real-time metrics showing how your rewritten content compares to the original.
      </p>
    </div>

    <div className="grid md:grid-cols-3 gap-6 mb-8">
      
      <!-- MEANING MATCH SCORE -->
      <div className="bg-white border-3 border-[--border-primary] 
                    p-6 shadow-[0px_3px_0px_#0d0d0d]">
        <div className="text-center">
          <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                        uppercase tracking-wider mb-2">
                Meaning Match
          </div>
          <div className="flex items-center justify-center gap-4">
            <div className="text-right">
              <div id="meaningScore" 
                   className="font-[--font-mono] text-6xl md:text-7xl 
                          font-bold tabular-nums text-[--accent-success]">
                0%
              </div>
              <div className="font-[--font-body] text-sm text-[--text-tertiary]">
                How well meaning is preserved
              </div>
            </div>
            <div id="meaningIndicator" 
                 className="w-20 h-20 rounded-full border-4 border-[--border-primary] 
                        bg-white flex items-center justify-center">
              <span className="text-3xl">🎯</span>
            </div>
          </div>
        </div>
      </div>

      <!-- READABILITY DELTA -->
      <div className="bg-white border-3 border-[--border-primary] 
                    p-6 shadow-[0px_3px_0px_#0d0d0d]">
        <div className="text-center">
          <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                        uppercase tracking-wider mb-2">
                Readability Delta
          </div>
          <div id="readabilityDelta" 
               className="font-[--font-mono] text-5xl md:text-6xl 
                      font-bold tabular-nums text-[--accent-secondary]">
            +0%
          </div>
          <div className="flex items-center justify-center gap-2 mt-3">
            <span id="readabilityIcon" className="text-2xl">➡️</span>
            <div className="font-[--font-body] text-sm text-[--text-tertiary] text-left">
              Improvement vs. original
            </div>
          </div>
        </div>
      </div>

      <!-- CHANGE LEVEL -->
      <div className="bg-white border-3 border-[--border-primary] 
                    p-6 shadow-[0px_3px_0px_#0d0d0d]">
        <div className="text-center">
          <div className="font-[--font-mono] text-xs text-[--text-tertiary] 
                        uppercase tracking-wider mb-2">
                Change Level
          </div>
          <div id="changeLevel" 
               className="font-[--font-mono] text-5xl md:text-6xl 
                      font-bold tabular-nums text-[--text-primary]">
            Medium
          </div>
          <div className="flex items-center justify-center gap-2 mt-3">
            <span className="text-2xl">📊</span>
            <div className="font-[--font-body] text-sm text-[--text-tertiary] text-left">
              Controlled by slider below
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- SIMILARITY WARNING (Conditional) -->
    <div id="similarityWarning" 
         className="hidden mt-6 p-4 bg-[--accent-error] 
                        border-3 border-[--border-primary] 
                        flex items-center gap-4">
      <span className="text-2xl">⚠️</span>
      <div className="flex-1">
        <div className="font-[--font-display] font-semibold 
                      text-lg text-white mb-1">
          Too Similar to Original
        </div>
        <div className="font-[--font-body] text-base text-white">
          Your rewritten content is very close to the original. 
          Consider increasing the Change Level slider for more substantial rewrites.
        </div>
      </div>
    </div>

  </div>
</div>
```

**Animated Counter Implementation:**
```javascript
// Animate all three metrics from 0% to final values over 1.5 seconds
const animateQualityMetrics = (meaningScore, readabilityDelta, changeLevel) => {
  const duration = 1500; // 1.5 seconds
  const startTime = Date.now();
  
  const meaningEl = document.getElementById('meaningScore');
  const readabilityEl = document.getElementById('readabilityDelta');
  const changeLevelEl = document.getElementById('changeLevel');
  const meaningIndicatorEl = document.getElementById('meaningIndicator');
  
  const animate = () => {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function for smooth animation
    const eased = 1 - Math.pow(1 - progress, 3);
    
    // Update meaning score
    const currentMeaning = Math.round(meaningScore * eased);
    meaningEl.textContent = currentMeaning + '%';
    
    // Color-coded meaning score
    if (currentMeaning < 60) {
      meaningEl.className = 'font-[--font-mono] text-6xl md:text-7xl font-bold tabular-nums text-[--accent-error]';
      meaningIndicatorEl.style.borderColor = 'var(--accent-error)';
    } else if (currentMeaning < 80) {
      meaningEl.className = 'font-[--font-mono] text-6xl md:text-7xl font-bold tabular-nums text-[--accent-warning]';
      meaningIndicatorEl.style.borderColor = 'var(--accent-warning)';
    } else {
      meaningEl.className = 'font-[--font-mono] text-6xl md:text-7xl font-bold tabular-nums text-[--accent-success]';
      meaningIndicatorEl.style.borderColor = 'var(--accent-success)';
    }
    
    // Update readability delta
    const currentReadability = Math.round(readabilityDelta * eased);
    readabilityEl.textContent = (currentReadability >= 0 ? '+' : '') + currentReadability + '%';
    
    // Update change level display
    const levels = ['Low', 'Medium', 'High'];
    const currentLevelIndex = Math.round((changeLevel - 1) / 2 * eased); // Map 1-3 to 0-2
    changeLevelEl.textContent = levels[Math.min(Math.round(currentLevelIndex), 2)];
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      // Animation complete - show similarity warning if needed
      if (meaningScore < 60) {
        document.getElementById('similarityWarning').classList.remove('hidden');
      }
    }
  };
  
  requestAnimationFrame(animate);
};
```

---

### 2.3 Rewrite Controls (Advanced Options)

**Layout:** Control panel above input area

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-8">
  <div className="max-w-7xl mx-auto px-6">
    
    <h3 className="font-[--font-display] text-2xl font-bold 
                 text-[--text-primary] mb-6">
      Rewrite Controls
    </h3>

    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- PRESET DROPDOWN -->
      <div className="flex flex-col gap-3">
        <label className="font-[--font-display] font-semibold 
                       text-base text-[--text-primary]">
          Rewrite Preset
        </label>
        <select 
          id="presetSelect"
          className="px-4 py-3 bg-white border-3 border-[--border-primary] 
                 font-[--font-body] text-base text-[--text-primary] 
                 focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]">
          <option value="shorten">✂️ Shorten (more concise)</option>
          <option value="clarify" selected>💡 Make clearer (improve flow)</option>
          <option value="formal">📝 More formal (professional tone)</option>
          <option value="persuade">😊 More persuasive (convincing)</option>
          <option value="simplify">🔨 Simplify (easier language)</option>
        </select>
      </div>

      <!-- KEEP TERMS EXACT TOGGLE -->
      <div className="flex items-center gap-3 p-4 
                    bg-white border-3 border-[--border-primary] 
                    cursor-pointer hover:bg-[--bg-accent]">
        <input 
          type="checkbox"
          id="keepTermsExact"
          className="w-5 h-5 accent-[--accent-primary]"
        />
        <div className="flex flex-col">
          <label for="keepTermsExact" 
                 className="font-[--font-display] font-semibold 
                        text-base text-[--text-primary] cursor-pointer">
            Keep Terms Exact
          </label>
          <div className="font-[--font-body] text-sm text-[--text-tertiary]">
            Preserve brand names, technical terms, proper nouns
          </div>
        </div>
      </div>

      <!-- CHANGE LEVEL SLIDER -->
      <div className="flex flex-col gap-3">
        <label className="font-[--font-display] font-semibold 
                       text-base text-[--text-primary]">
          Change Level
        </label>
        <div className="flex items-center gap-4">
          <span className="font-[--font-mono] text-sm text-[--text-tertiary]">
            Conservative
          </span>
          <input 
            type="range"
            id="changeLevelSlider"
            min="1"
            max="3"
            value="2"
            className="flex-1 h-3 accent-[--accent-primary]"
          />
          <span className="font-[--font-mono] text-sm text-[--text-tertiary]">
            Aggressive
          </span>
        </div>
        <div className="flex justify-between font-[--font-mono] text-sm 
                      text-[--text-tertiary] mt-1">
          <span>Low</span>
          <span id="changeLevelLabel">Medium</span>
          <span>High</span>
        </div>
      </div>

      <!-- OUTPUT LENGTH CONTROL -->
      <div className="flex flex-col gap-3">
        <label className="font-[--font-display] font-semibold 
                       text-base text-[--text-primary]">
          Output Length
        </label>
        <select 
          id="outputLength"
          className="px-4 py-3 bg-white border-3 border-[--border-primary] 
                 font-[--font-body] text-base text-[--text-primary] 
                 focus:outline-none focus:shadow-[0px_0px_0px_4px_#ff4500]">
          <option value="shorter">📉 Shorter (~10% less)</option>
          <option value="same" selected>📏 Same length (~original)</option>
          <option value="longer">📈 Longer (~10% more)</option>
        </select>
      </div>

    </div>

    <!-- AUDIENCE SELECTOR -->
    <div className="mt-6">
      <label className="font-[--font-display] font-semibold 
                     text-base text-[--text-primary] mb-3">
        Target Audience
      </label>
      <div className="flex gap-4">
        {[
          { value: 'general', label: '👥 General', desc: 'Broad audience, clear language' },
          { value: 'technical', label: '👓 Technical', desc: 'Industry-specific terminology' },
          { value: 'casual', label: '😊 Casual', desc: 'Conversational, friendly tone' }
        ].map(option => (
          <label key={option.value} 
                 className="flex-1 cursor-pointer">
            <input 
              type="radio"
              name="audience"
              value={option.value}
              className="sr-only accent-[--accent-primary]"
            />
            <div className="p-4 bg-white border-3 border-[--border-primary] 
                          hover:bg-[--bg-accent] transition-colors">
              <div className="font-[--font-display] font-semibold 
                            text-base text-[--text-primary]">
                {option.label}
              </div>
              <div className="font-[--font-body] text-sm text-[--text-tertiary]">
                {option.desc}
              </div>
            </div>
          </label>
        ))}
      </div>
    </div>

  </div>
</div>
```

---

### 2.4 Content Management

**Output Area with Actions:**

```jsx
<div className="bg-[--bg-secondary] border-t-4 border-[--border-primary] py-8">
  <div className="max-w-7xl mx-auto px-6">
    
    <div className="flex items-center justify-between mb-4">
      <label className="font-[--font-display] font-semibold 
                     text-lg text-[--text-primary]">
        Rewritten Article
      </label>
      
      <!-- CHARACTER COUNT TRACKING -->
      <div className="font-[--font-mono] text-sm text-[--text-tertiary]">
        <span id="outputCharCount">0</span> characters
      </div>
    </div>

    <textarea
      id="outputText"
      readOnly
      className="flex-1 min-h-[400px] p-6 
               bg-[--bg-accent] border-3 border-[--border-primary] 
               font-[--font-body] text-base text-[--text-primary] 
               focus:outline-none resize-none"
      placeholder="Your rewritten article will appear here...

      The Rewrite Quality Panel above shows real-time metrics:
      • Meaning Match: How well original meaning is preserved
      • Readability Delta: Improvement vs. original text
      • Change Level: Low/Medium/High based on your slider setting"
    />

    <div className="flex gap-4 mt-4">
      <button 
        id="copyBtn"
        className="flex-1 px-6 py-4 bg-[--accent-secondary] 
               text-white font-[--font-display] font-semibold 
               hover:bg-[#1d4ed8] transition-colors
               disabled:opacity-50 disabled:cursor-not-allowed"
        onClick={handleCopy}
        disabled>
        📋 Copy to Clipboard
      </button>
      <button 
        className="px-6 py-4 bg-white border-3 border-[--border-primary] 
               text-[--text-primary] font-[--font-mono] font-semibold
               hover:bg-[--bg-accent] transition-colors"
        onClick={handleDownload}>
        💾 Download .txt
      </button>
    </div>

  </div>
</div>
```

---

## 3. User Interface Sections

### 3.1 Hero Section (Industrial Asymmetric Grid)

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
      <span className="font-[--font-mono]">GPT-5 POWERED • NO SIGNUP REQUIRED</span>
    </div>

    <!-- Main headline -->
    <h1 className="font-[--font-display] text-6xl md:text-7xl 
                 font-bold leading-[1.1] text-[--text-primary] 
                 tracking-tight mb-6 max-w-4xl">
      Rewrite Articles.
      <span className="text-[--accent-primary]">Actually Readable.</span>
    </h1>

    <!-- Subheadline -->
    <p className="font-[--font-body] text-xl md:text-2xl 
                 text-[--text-secondary] max-w-2xl mb-10 
                 leading-relaxed">
      GPT-5 Nano powered article rewriter. See real-time quality metrics. 
      No signup. No daily limits. Just paste your text.
    </p>

    <!-- CTAs -->
    <div className="flex flex-col sm:flex-row gap-4 max-w-xl">
      <button className="flex-1 px-8 py-4 bg-[--accent-primary] 
                    text-white font-[--font-display] font-semibold 
                    text-lg hover:bg-[--accent-hover] 
                    shadow-[0px_3px_0px_#0d0d0d] 
                    hover:shadow-[0px_6px_0px_#0d0d0d] 
                    transition-all">
        Start Rewriting Free
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
        <span className="font-[--font-mono] text-sm">12,487 rewrites today</span>
      </div>
    </div>
  </div>
</div>
```

---

### 3.2 Features Showcase (3-Column Grid)

```jsx
<div className="bg-[--bg-primary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-7xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-4">
      Why GPT-5 Nano?
    </h2>
    <p className="font-[--font-body] text-lg text-[--text-secondary] 
                 text-center max-w-2xl mx-auto mb-16">
      Fast. Cheap. High-quality. Everything you need for article rewriting.
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
          title: 'Quality Metrics',
          desc: 'Real-time meaning match and readability indicators.'
        },
        {
          icon: '🚀',
          title: 'Advanced Controls',
          desc: 'Preset styles, change level slider, audience targeting.'
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

### 3.3 Pricing Structure (Free/Pro/Agency)

```jsx
<div className="bg-[--bg-secondary] border-t-4 border-[--border-primary] py-20">
  <div className="max-w-6xl mx-auto px-6">
    
    <h2 className="font-[--font-display] text-4xl md:text-5xl 
                 font-bold text-[--text-primary] text-center mb-4">
      Simple Pricing
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
          {['10 rewrites/hour', 'Quality metrics', 'Basic controls'].map(item => (
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
          {['100 rewrites/hour', 'Advanced controls', 'Priority support', 
            'Batch processing'].map(item => (
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
          {['Unlimited rewrites', 'API access', 'White-label option', 
            'Dedicated support'].map(item => (
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

### 3.4 FAQ Section (Accordion)

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
          a: 'Yes. No credit card. No signup. No limits. Paste your article and rewrite as many times as you want.'
        },
        {
          q: 'How does the Quality Panel work?',
          a: 'GPT-5 Nano compares your rewritten text against the original. Meaning Match shows how well content is preserved. Readability Delta shows improvement in clarity.'
        },
        {
          q: 'What does Change Level do?',
          a: 'Low = Minimal changes, mostly synonyms. Medium = Balanced rewriting. High = Substantial restructuring while preserving meaning.'
        },
        {
          q: 'Will Google penalize rewritten content?',
          a: 'Our AI preserves meaning while rewriting content for clarity. Always review and edit rewritten articles before publishing. Use as a starting point, not final output.'
        },
        {
          q: 'Can I rewrite long articles?',
          a: 'Up to 10,000 characters per rewrite. For longer content, split into sections and rewrite each part separately.'
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

### 3.5 Footer (Minimal)

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
          GPT-5 Nano Powered • Clarity-First Rewriter
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

## 4. Design Specifications

### 4.1 Typography System (Non-Negotiable)

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
| Section H2 | Space Grotesk | 48px → 32px (mobile) | 600 | 1.2 |
| Feature H3 | Space Grotesk | 24px → 20px (mobile) | 500 | 1.3 |
| Body text | Instrument Sans | 18px → 16px (mobile) | 400 | 1.6 |
| Small text | Instrument Sans | 14px | 400 | 1.5 |
| Quality Metrics | JetBrains Mono | 72px → 56px (mobile) | 700 | 1 |

---

### 4.2 Color Palette (Industrial Editorial)

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

### 4.3 Background Texture (Newsprint Grain)

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
  
  /* Quality metrics stack */
  .md\:grid-cols-3 {
    display: flex;
    flex-direction: column;
  }
  
  /* Hero text scaling */
  .text-6xl { font-size: 48px; }
  .text-7xl { font-size: 56px; }
  
  /* Quality metrics scaling */
  .text-5xl { font-size: 40px; }
  .text-6xl { font-size: 48px; }
  .text-7xl { font-size: 56px; }
}

/* COMPACT PADDING */
@media (max-width: 480px) {
  .px-6 { padding-left: 1rem; padding-right: 1rem; }
  .py-20 { padding-top: 3rem; padding-bottom: 3rem; }
  .py-16 { padding-top: 2rem; padding-bottom: 2rem; }
}
```

---

## 6. Backend Integration Notes

### API Endpoint Expectation
```
POST /api/v1/rewrite

Request:
{
  "text": "original article...",
  "preset": "clarify",           // shorten|clarify|formal|persuade|simplify
  "keepTermsExact": false,      // boolean
  "changeLevel": 2,              // 1=low, 2=medium, 3=high
  "outputLength": "same",         // shorter|same|longer
  "audience": "general"           // general|technical|casual
}

Response:
{
  "rewritten": "rewritten article...",
  "meaningScore": 87,            // 0-100
  "readabilityDelta": 15,         // percentage improvement
  "processingTime": 2.3           // seconds
}
```

### Error Handling
- Text too short (<200 chars): Show inline error "Minimum 200 characters required"
- Text too long (>10,000 chars): Show inline error "Maximum 10,000 characters"
- API timeout: Show "Still rewriting..." with loading spinner
- Empty input: Disable rewrite button until text entered

### Rate Limiting (Client-Side)
```javascript
// Debounce rewrite button clicks (500ms minimum between requests)
let lastRequest = 0;
const rewriteDebounced = () => {
  const now = Date.now();
  if (now - lastRequest < 500) {
    alert('Please wait before rewriting again.');
    return;
  }
  lastRequest = now;
  // Proceed with API call...
};
```

---

## 7. Complete Page Layout Structure

```jsx
<main className="bg-[--bg-primary]">
  
  {/* HERO SECTION */}
  <section id="hero" className="min-h-screen newsprint">
    {/* Asymmetric grid, badge, headline, CTAs, social proof */}
  </section>

  {/* REWRITE CONTROLS */}
  <section id="controls" className="border-t-4 border-[--border-primary]">
    {/* Preset dropdown, keep terms toggle, change level slider, 
         output length, audience selector */}
  </section>

  {/* REWRITE TOOL */}
  <section id="rewriter" className="border-t-4 border-[--border-primary]">
    {/* Input area (left), output area (right) */}
  </section>

  {/* QUALITY PANEL */}
  <section id="quality" className="border-t-4 border-[--border-primary]">
    {/* Meaning match, readability delta, change level metrics */}
  </section>

  {/* FEATURES SHOWCASE */}
  <section id="features" className="border-t-4 border-[--border-primary]">
    {/* 6 feature cards in 3-column grid */}
  </section>

  {/* PRICING TIERS */}
  <section id="pricing" className="border-t-4 border-[--border-primary]">
    {/* Free, Pro, Agency cards */}
  </section>

  {/* FAQ ACCORDION */}
  <section id="faq" className="border-t-4 border-[--border-primary]">
    {/* 5 FAQ items in accordion */}
  </section>

  {/* FOOTER */}
  <footer className="border-t-4 border-[--accent-primary]">
    {/* Logo, links, copyright */}
  </footer>

</main>
```

---

## 8. Testing Checklist

### Functional Testing
- [ ] Input validation works (200-10,000 chars)
- [ ] Character count updates in real-time
- [ ] Rewrite button triggers API call
- [ ] Output appears in right textarea
- [ ] Quality metrics animate from 0% to final
- [ ] All controls (preset, toggle, slider, dropdowns) update state
- [ ] Similarity warning shows when meaning score <60%
- [ ] Copy to clipboard works
- [ ] Download .txt works
- [ ] Sample text loads correctly
- [ ] FAQ accordions open/close

### Responsive Testing
- [ ] Quality metrics stack vertically on mobile
- [ ] Rewrite tool stacks vertically (input on top, output below)
- [ ] Feature cards collapse to single column
- [ ] Pricing tiers stack (3 rows on mobile)
- [ ] Footer stacks vertically

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest macOS/iOS)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS 16+)
- [ ] Chrome Mobile (Android 13+)

---

## 9. Launch Checklist

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

### What's New in V2
- **Quality Panel:** Replaced "Spin Score" with 3-metric panel (Meaning Match, Readability Delta, Change Level)
- **Advanced Controls:** Added preset dropdown, keep terms toggle, change level slider, output length, audience selector
- **Better Validation:** Minimum 200 characters (was 0 in V1)
- **Enhanced UX:** Similarity warning, more granular feedback
- **Pricing Structure:** 3 tiers (Free/Pro/Agency) instead of V1's 2-tier comparison

### Copy-Paste Ready
This entire spec is designed to be copy-pasted into medo.dev. The CSS classes are Tailwind utility classes that medo.dev should understand natively.

### Non-Negotiable Elements
These design decisions are critical to the anti-AI-slop aesthetic:
1. **Space Grotesk + Instrument Sans + JetBrains Mono** (no substitutions)
2. **Industrial Editorial color palette** (cream background, black borders, orange accents)
3. **Quality Panel animation** (this is the unforgettable element)
4. **Newsprint grain texture** (subtle noise overlay)
5. **Hard 3px shadows** (no blur, stark depth)
6. **70-20-10 color rule** (70% cream, 20% black text, 10% orange accents)

### What to Customize
- Adjust padding/spacing to fit your container
- Add your own copywriting if my suggestions don't resonate
- Modify API endpoint structure if your backend differs
- Add more preset options if needed

### What NOT to Change
- Typography system (this is the distinctive element)
- Color palette (proven high-contrast, memorable)
- Quality Panel concept (this is the viral hook)
- Layout structure (hero → controls → tool → quality → features → pricing → FAQ → footer)

---

**Ready to build. Paste this into medo.dev and watch the magic happen.** 🎨

*Designed by Carlottta using frontend-design-ultimate + landing-gen skills*
*Industrial Editorial aesthetic: bold typography, stark borders, newsprint texture*
*Unforgettable element: Animated Quality Panel with 3 metrics*
*Enhanced UX: Advanced controls, similarity warnings, granular feedback*
