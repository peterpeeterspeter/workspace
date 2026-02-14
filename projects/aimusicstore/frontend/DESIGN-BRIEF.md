# aimusicstore.com - Frontend Design Brief

**Project:** AI Music Top 50 Voting API
**Goal:** Production frontend with API integration
**Date:** 2026-02-14
**Stack:** React 18 + TypeScript + Tailwind CSS + shadcn/ui
**Build:** Vite (static, fast)

---

## Brand Identity

**Name:** aimusicstore.com
**Tagline:** "AI-Powered Music Rankings"
**Purpose:** Showcase top AI-generated music + tools, driven by community voting

**Target Audience:**
- Primary: AI music creators (Suno, Udio users)
- Secondary: Music enthusiasts discovering AI music
- Tertiary: Developers exploring AI music tools

---

## Design Direction: **Brutalist Tech**

**Why:** Bold, confident, trustworthy — like the technology it showcases

**Visual Language:**
- Strong geometric shapes (circles, hex patterns)
- High contrast typography
- Tech-forward aesthetic (not playful, not corporate)
- Anti-AI-slop: Purposeful details, not generic

**Keywords:** Bold, geometric, tech-forward, data-driven

---

## Color Palette

### Primary Colors
```css
--bg-primary: #0a0a0;      /* Deep purple - AI, creativity */
--bg-secondary: #7c3aed;   /* Vibrant purple - music energy */
--text-primary: #fafafa;   /* Near white - readability */
--text-secondary: #e0e7ff;   /* Light purple - soft accent */
--accent: #a855f7;          /* Electric purple - CTAs */
--accent-hover: #c975fb;    /* Bright purple - hover states */
```

### Supporting Colors
```css
--surface: #1a1a2e;        /* Cards, sections */
--surface-alt: #241432;     /* Alternating backgrounds */
--border: #37224a;          /* Subtle borders */
--success: #10b981;         /* Green for positive states */
--warning: #f59e0b;         /* Orange for attention */
--error: #ef4444;           /* Red for errors */
```

---

## Typography System

**Font Pairing:**
- **Display:** Space Grotesk (Bold personality)
- **Body:** Instrument Sans (Refined readability)

**Scale:**
- Hero: 64px (4rem) - Bold presence
- H1: 48px (3rem)
- H2: 36px (2.25rem)
- H3: 24px (1.5rem)
- Body: 16px (1rem)

**Hierarchy:**
```css
/* Display */
--font-display: 'Space Grotesk', sans-serif;

/* Body */
--font-body: 'Instrument Sans', sans-serif;
```

**Weights:**
- Hero title: 700 (Bold)
- Headlines: 600 (Semibold)
- Body: 400 (Regular)

---

## Unforgettable Element

**The Hexagon Background Pattern**

Subtle animated hexagon grid that:
- Creates tech texture without noise
- Supports "AI-generated" theme
- Performance-optimized (CSS-only animation)

---

## Page Structure

### Homepage (/)

**Hero Section:**
```
┌─────────────────────────────────────────────┐
│                                         │
│     [Trending Now]                      │
│                                         │
│   Top AI Music + Tools                   │
│     Powered by Community Voting             │
│                                         │
│         [Explore Rankings ▶]              │
└─────────────────────────────────────────────┘
```

**Content:**
- Badge: "Now Live" or "Beta"
- Title: "AI-Powered Music Rankings"
- Subtitle: "Discover top AI-generated tracks and tools"
- CTA: "Explore Rankings" → /trending
- Animated: Hexagon background (slow pan)

**Trending Section (Below Fold):**
- Top 5 songs carousel
- Top 5 tools grid
- "View All Trending" → /trending
- Update every 60s (poll API)

**Features Grid (3 columns):**
- Real-time voting
- Agent reputation scoring
- Tier-based API access
- Anti-gaming protection

**Footer:**
- API Documentation link
- GitHub link
- Social icons

---

### Trending Page (/trending)

**Hero:**
```
┌────────────────────────────────────────┐
│                                    │
│   Trending Now                 │
│   Top AI music + tools         │
│                                    │
└────────────────────────────────────────┘
```

**Content:**
- Title: "Trending"
- Subtitle: "What's popular right now"
- Animated pulse indicator

**Two Columns:**
```
┌────────────────┬────────────────┐
│  Top 10 Songs │ Top 10 Tools │
│  (carousel)      │   (grid)     │
└────────────────┴────────────────┘
```

**Updates:**
- Auto-refresh every 60s
- Smooth transitions
- Vote counts live

---

### Top 50 Page (/top)

**Hero:**
```
┌────────────────────────────────────┐
│                                │
│   Top 50 Rankings            │
│   AI Music + Tools           │
│                                │
└────────────────────────────────────┘
```

**Content:**
- Period tabs: Daily | Weekly | Monthly | All-Time
- Combined rankings (songs + tools mixed)
- "Last updated" timestamp

**Table:**
- Rank | Type | Name | Platform/Category | Score | Votes
- Weighted score badge (if reputation ≠ 0)
- Clickable rows → detail pages

**Pagination:**
- 50 items per page (already filtered)
- Sticky header on scroll

---

### Song Detail Page (/songs/{id})

**Header:**
- Back button ←
- Breadcrumb: Home → Trending → Song Title

**Hero:**
- Large album art (placeholder if none)
- Title + Artist
- Platform badge (Suno, Udio, etc.)
- Play button (if audio available)

**Details Grid:**
```
┌──────────────────────────────────────┐
│ Genre    │ Mood     │ Tempo │   Up/Down     │
│ Rock     │ Chill    │ 128 BPM │ ████████░░ │
└──────────────────────────────────────┘
```

**Vote Section:**
- Large thumb up/down buttons
- Vote count with live updates
- "Requires API key" note (future)

**Footer:**
- Platform link (open in new tab)
- Affiliate disclaimer
- Related songs carousel

---

### Tool Detail Page (/tools/{id})

**Header:** Same as song detail

**Hero:**
- Tool logo/icon
- Name + category badge
- Website link (prominent CTA)
- Commission rate badge

**Details Grid:**
```
┌───────────────────────────────────────────┐
│ Category      │ Features    │ Pricing   │
│ Text-to-Music │ • Free tier  │ • Free     │
│               │ • Pro tier   │ • $10/mo   │
└───────────────────────────────────────────┘
```

**Vote Section:** Same as song detail

**Footer:**
- Website link (affiliate)
- Rating + review count
- Similar tools carousel

---

## Component Library (shadcn/ui)

**Priority Components:**
1. Button (Primary, Secondary, Ghost, Icon)
2. Card (Song, Tool, Feature)
3. Badge (Platform, Category, Status)
4. Accordion (FAQ)
5. Tabs (Period selector on /top)
6. Carousel (Trending songs)
7. Avatar (Agent placeholder)
8. Skeleton loaders (while polling)

**Custom Components:**
- HexagonBackground (animated CSS)
- VoteButton (up/down with animation)
- ScoreDisplay (weighted vs raw)
- PlatformBadge (color-coded)

---

## Mobile-First Design

### Desktop (1280px+)
- Hero: Full animation
- Trending: 3-column features
- Top 50: Full table
- Detail: 2-column details grid

### Tablet (768px-1280px)
- Hero: Simplified animation
- Trending: 2-column grid
- Top 50: Scrollable cards (simplified)
- Detail: Stacked grid

### Mobile (<768px)
- Hero: Static image (no animation)
- Trending: Single column list
- Top 50: Compact table (rank only)
- Detail: Single column stack

---

## API Integration

### Endpoints to Call
- GET /health - System status
- GET /api/v1/trending - Top 10 each
- GET /api/v1/top/{period} - Top 50 combined
- GET /api/v1/songs/{id} - Song details
- GET /api/v1/tools/{id} - Tool details

### State Management
```typescript
// React Query or SWR
const { data, error, isLoading } = useSWR('/api/v1/trending')
const { data: songs } = useSWR('/api/v1/songs/abc123')
```

### Polling
- Trending page: Poll every 60s
- Vote counts: Real-time updates when user votes

---

## Content Strategy

### Homepage
- **Hero:** Value prop (AI music rankings)
- **Social proof:** "500+ votes cast yesterday"
- **Features:** 3 key benefits
- **CTA:** Primary "Explore Rankings", Secondary "Get API Key"

### /trending
- **Hero:** "What's hot right now"
- **Live indicator:** Pulse animation
- **Updates:** Auto-refresh notice

### /top
- **Tabs:** Period switcher (daily/weekly/monthly/alltime)
- **Transparency:** Show weighted scoring tooltip
- **Updates:** Timestamp with auto-refresh

### Detail Pages
- **Hero:** Strong visual identity
- **Social proof:** Vote count, rank trend
- **Affiliate:** Clear CTAs
- **Related:** Cross-link other items

---

## Performance Targets

- **Lighthouse Score:** 95+
- **First Contentful Paint:** <1.5s
- **Time to Interactive:** <3s
- **Bundle Size:** <150KB (gzipped)

---

## Next Steps

1. ✅ Initialize Vite project with React + Tailwind
2. ✅ Install shadcn/ui components
3. ✅ Build homepage with hero + features
4. ✅ Build /trending page with API integration
5. ✅ Build /top page with period tabs
6. ✅ Build detail pages for songs + tools
7. ✅ Add API integration layer
8. ✅ Optimize + deploy (static hosting)

---

*Design Brief Complete*
*Created: 2026-02-14 08:20 UTC*
*Next: Initialize frontend project*
