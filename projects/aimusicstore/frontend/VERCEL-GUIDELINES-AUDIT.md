# aimusicstore Frontend - Vercel Guidelines Audit

**Date:** 2026-02-15 17:40 UTC
**Standard:** Vercel Web Interface Guidelines
**Status:** 🔍 AUDIT IN PROGRESS

---

## Critical Issues (Must Fix Before Production)

### src/pages/HomePage.tsx

- **Line ~18** - Missing `lang` attribute on `<html>` (add to index.html)
- **Line ~25** - Link uses bare `href="#"` instead of proper route or `onClick` handler
- **Typography** - `"..."` used instead of `"…"` (ellipsis character)
- **Accessibility** - No skip link for main content
- **Accessibility** - Headings hierarchy not validated (starts with h2 instead of h1)
- **Focus** - Custom focus states may not be visible enough
- **Images** - Emoji icons (🎵, 🛠️) should have `role="img"` and `aria-label`

### src/pages/ComingSoonPage.tsx

- **Forms** - Email input needs `autocomplete="email"`
- **Forms** - Input needs explicit `type="email"` and `inputmode="email"`
- **Forms** - Label needs `htmlFor` attribute (currently wrapping div)
- **Accessibility** - Submit button needs `aria-describedby` for error message
- **Typography** - Loading state uses `"..."` instead of `"…"`

### src/pages/TrendingPage.tsx

- **Typography** - `"..."` should be `"…"`
- **Accessibility** - Card links may need better focus indicators
- **Performance** - Large list not virtualized (if >50 items)

### src/pages/Top50Page.tsx

- **Typography** - `"..."` should be `"…"`
- **Performance** - Large list not virtualized

### src/pages/SongDetailPage.tsx

- **Images** - External images lack explicit `width` and `height` (CLS risk)
- **Links** - Affiliate links should open in new tab with `rel="noopener noreferrer"`
- **Accessibility** - Song metadata may need better labeling

### src/pages/ToolDetailPage.tsx

- **Images** - External images lack explicit `width` and `height` (CLS risk)
- **Links** - Affiliate links should open in new tab
- **Buttons** - CTA buttons may need better hover states

---

## High Priority Issues

### Global (index.html)

- **Meta tags** - Missing `theme-color` for mobile browser UI
- **Meta tags** - Missing `<link rel="preconnect">` for CDN domains
- **Accessibility** - No skip link for keyboard users
- **Dark mode** - `color-scheme: dark` not set on `<html>`

### Navigation

- **Links** - Some links use `href="#"` (should be `<Link>` or proper handlers)
- **Deep linking** - State not always in URL (tabs, filters)

### Typography (All pages)

- **Ellipsis** - Replace `"..."` with `"…"` throughout
- **Quotes** - Ensure curly quotes `""` not straight `""`
- **Numbers** - Use numerals: "8 votes" not "eight votes"
- **Loading** - Loading states should end with `"…"`

### Forms

- **Validation** - Inline errors needed (not just console logs)
- **Focus** - Focus first error on submit
- **Autocomplete** - Add appropriate `autocomplete` values
- **Labels** - All inputs need proper labels (not just placeholder)

---

## Medium Priority Issues

### Animation

- **prefers-reduced-motion** - No reduced-motion variant for animations
- **Pulse animation** - Loading pulse should respect motion preferences

### Performance

- **Large lists** - Top 50 list should use virtualization (virtua or similar)
- **Layout thrashing** - Check for DOM reads in render
- **Font loading** - Consider `<link rel="preload">` for critical fonts

### Touch & Mobile

- **Touch actions** - Add `touch-action: manipulation` to interactive elements
- **Tap highlight** - `-webkit-tap-highlight-color` not set
- **Zoom** - Ensure no `user-scalable=no` viewport restrictions

### Content Handling

- **Long text** - No truncation or line-clamp for user-generated content
- **Empty states** - Check handling for empty arrays/strings
- **Flex truncation** - Ensure `min-w: 0` on flex children that truncate

---

## Low Priority Issues

### Locale & i18n

- **Dates** - Use `Intl.DateTimeFormat` instead of hardcoded formats
- **Numbers** - Use `Intl.NumberFormat` for vote counts
- **Language** - No language detection (Accept-Language header)

### Hydration Safety

- **Date rendering** - Check for hydration mismatch in timestamps
- **Inputs** - Ensure `value` inputs have `onChange` or use `defaultValue`

---

## Quick Wins (Easy Fixes)

1. **Ellipsis:** Find/replace `"..."` → `"…"` (5 min)
2. **Theme color:** Add `<meta name="theme-color">` to index.html (2 min)
3. **Color scheme:** Add `color-scheme: dark` to `<html>` (2 min)
4. **Form types:** Add `type="email"` and `inputmode="email"` to email input (2 min)
5. **Autocomplete:** Add `autocomplete="email"` to email input (1 min)
6. **Link targets:** Add `target="_blank" rel="noopener noreferrer"` to external links (5 min)
7. **Preconnect:** Add `<link rel="preconnect">` for fonts/CDN (3 min)
8. **Skip link:** Add skip link for accessibility (10 min)

**Total time:** ~30 minutes for all quick wins

---

## Action Plan

### Phase 1: Critical & Quick Wins (30 min)
- Fix ellipsis characters throughout
- Add meta tags to index.html (theme-color, color-scheme)
- Fix form attributes (type, inputmode, autocomplete)
- Add skip link for accessibility
- Fix external link targets

### Phase 2: High Priority (1-2 hours)
- Improve accessibility (aria-labels, labels, focus states)
- Fix images (width/height, alt text)
- Improve form validation and error handling
- Add proper heading hierarchy

### Phase 3: Medium Priority (2-3 hours)
- Add prefers-reduced-motion support
- Implement list virtualization for large lists
- Improve touch interactions
- Add preconnect for performance

### Phase 4: Low Priority (Future)
- Implement i18n for dates/numbers
- Add language detection
- Improve hydration safety

---

## Next Steps

1. **Start with Phase 1** (Critical & Quick Wins)
2. **Test changes** in development
3. **Rebuild production bundle**
4. **Deploy to production**

Ready to proceed with fixes?
