# Learnings Log

This file captures corrections, knowledge gaps, and best practices for continuous improvement.

---

## [LRN-20250213-001] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Locked Architecture Pattern for consistent AI-generated content

### Details
From Larry's TikTok automation system: When generating multiple images of the same space (e.g., room makeovers), lock ALL architectural elements and only change the style-specific variable.

**Example for room transformation:**
- **Locked**: Room dimensions, window count/position, door location, camera angle, furniture size, ceiling height, floor type
- **Variable ONLY**: Wall color, bedding, decor, lighting fixtures

**Why this matters:**
- Early prompts like "a nice modern kitchen" generated completely different rooms each time
- Windows appearing/disappearing, counters on different walls = looks fake
- Solution: obsessively specific about architecture, change only style

**Application:**
- Debadkamer.com: Lock bathroom architecture, only change product (toilet/sink/shower/faucet)
- Any content requiring visual consistency across variations

### Suggested Action
Create skill file `bathroom-product-generator` with locked bathroom architecture template. Only product element changes between images.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Related Files: `/root/.openclaw/workspace/research/bathroom-products/`
- Tags: content-generation, prompt-engineering, consistency, ai-images, locked-architecture
- See Also: LRN-20250213-002

---

## [LRN-20250213-002] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: high
**Status**: pending
**Area**: frontend

### Summary
Viral Hook Formula: [Another person] + [conflict/doubt] → showed them proof → they changed mind

### Details
From Larry's TikTok testing data:

**Hooks that FAILED (self-focused):**
- "Why does my flat look like a student loan" → 905 views
- "See your room in 12+ styles before you commit" → 879 views
- "The difference between $500 and $5000 taste" → 2,671 views

**Hooks that SUCCEEDED (story-focused):**
- "My landlord said I can't change anything so I showed her what AI thinks it could look like" → 234,000 views
- "I showed my mum what AI thinks our living room could be" → 167,000 views
- "My landlord wouldn't let me decorate until I showed her these" → 147,000 views

**Formula:**
> [Another person] + [conflict or doubt] → showed them AI → they changed their mind

**Why it works:**
- Creates a tiny story in viewer's head before they swipe
- They picture the landlord's face, the mum being impressed
- It's about the human moment, not the app/features

**For crash gambling niche:**
- "My wife thought crash games were rigged until I showed her the math"
- "My friend lost €5000 until I showed him this one strategy"
- "I almost quit crash gambling until I understood the house edge"

### Suggested Action
Adopt hook formula for all social content. Brainstorm by asking: "Who's the other person, and what's the conflict?" If no conflict, hook probably won't work.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: viral-content, hooks, social-media, storytelling, copywriting
- See Also: LRN-20250213-001

---

## [LRN-20250213-003] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Skill Files Are the Critical Component of AI Agent Systems

### Details
From Larry's system: Larry has a 500+ line TikTok skill file. It contains every rule, formatting spec, and lesson learned from every failure. The skill file has been rewritten ~20 times in the first week.

**Why skill files matter:**
- AI starts with zero context
- Every failure becomes a rule
- Every success becomes a formula
- Agent compounds knowledge over time

**What goes in skill files:**
- Image sizes and formats (e.g., 1024x1536 portrait, always)
- Prompt templates with locked architecture descriptions
- Text overlay rules (font size, positioning, line length)
- Caption formulas and hashtag strategy
- Hook formats that work in your niche
- Failure log so agent never repeats mistakes

**Write like training a new team member:**
- Incredibly capable but zero context
- Be obsessively specific
- Include examples
- Document every mistake

### Suggested Action
Create detailed skill files for each major workflow. Treat them as living documents - update immediately after learning lessons.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: skills, prompt-engineering, ai-agents, documentation, continuous-improvement
- See Also: LRN-20250213-001, LRN-20250213-002

---

## [LRN-20250213-004] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Hybrid Workflow: AI Does 95%, Human Does 5%

### Details
From Larry's system: The most effective workflow isn't full automation - it's strategic division of labor.

**AI does (95%, 15-30 minutes):**
- Generate images with locked architecture
- Add text overlays
- Write captions
- Upload to TikTok as drafts
- Research trends and analyze performance

**Human does (5%, 60 seconds):**
- Pick trending music (can't be automated, TikTok library requires manual browsing)
- Approve hooks
- Quality check on images
- Final publish decision

**Why this works:**
- AI handles repetitive, time-consuming tasks
- Human provides creative judgment that requires taste
- Human touches what algorithms can't do yet
- Partnership, not replacement

**Cost:** ~$0.50 per post in API calls, $0.25 with Batch API

### Suggested Action
Design workflows with clear 95/5 split. AI generates, human approves/finalizes.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: workflow, automation, human-ai-collaboration, efficiency
- See Also: LRN-20250213-003

---

## [LRN-20250213-005] knowledge_gap

**Logged**: 2025-02-13T18:31:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
OpenAI Batch API: Pre-generate Content Overnight for 50% Cost Savings

### Details
From Larry's system: Use OpenAI's Batch API to pre-generate content overnight.

**How it works:**
- Schedule batch generation to run during off-hours
- By morning, entire day's content is ready
- 50% cheaper than real-time generation ($0.25 vs $0.50 per image)

**Use cases:**
- Daily social media content (6 slideshows)
- Product image generation
- Any predictable, volume-based generation

**Implementation:**
- Set up cron job for overnight batch processing
- Store generated content in organized structure
- Human reviews and publishes next day

### Suggested Action
Explore Batch API implementation for high-volume content generation (bathroom products, social content).

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: cost-optimization, batch-processing, openai-api, automation
- See Also: LRN-20250213-001

---

## [LRN-20250213-006] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Obsessive Specificity in Prompt Engineering for Visual Consistency

### Details
From Larry's system: Early prompts were too vague ("a nice modern kitchen"), resulting in completely different rooms each time.

**Solution: Lock everything with obsessive detail**

**Example room description (bold = only variable):**
> iPhone photo of a small UK rental kitchen. Narrow galley style kitchen, roughly 2.5m x 4m. Shot from the doorway at the near end, looking straight down the length. Countertops along the right wall with base cabinets and wall cabinets above. Small window on the far wall, centered, single pane, white UPVC frame, about 80cm wide. Left wall bare except for a small fridge freezer near the far end. Vinyl flooring. White ceiling, fluorescent strip light. Natural phone camera quality, realistic lighting. Portrait orientation. **Beautiful modern country style.**

**What gets locked:**
- Room dimensions
- Window count and position
- Door location
- Camera angle
- Furniture size
- Ceiling height
- Floor type
- Lighting
- Photo quality markers

**What varies:**
- Style-specific elements only (wall color, bedding, decor, fixtures)

**Additional detail tip:**
- "Before" rooms need signs of life: flat screen TV, mugs on counter, remote on sofa
- Without everyday items, rooms look like empty show homes - nobody relates

### Suggested Action
Apply obsessive specificity to all prompt engineering. Lock architecture completely, vary only surface elements.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: prompt-engineering, specificity, visual-consistency, ai-images
- See Also: LRN-20250213-001

---

## [LRN-20250213-007] best_practice

**Logged**: 2025-02-13T18:31:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Performance Tracking: Log Every Piece of Content with Metrics

### Details
From Larry's system: Every post, view count, and insight gets logged to memory files. When brainstorming hooks, Larry references actual performance data - not guessing.

**What to track:**
- Post content/hook
- Publication date/time
- Platform
- Views, likes, shares, comments
- Engagement rate
- Conversion (downloads, signups)
- Cost (API usage)

**Why it matters:**
- Data-driven hook selection
- Identify what's working
- Learn from failures
- Compound knowledge over time

**Planning workflow:**
- Don't post reactively
- Brainstorm 10-15 hooks at once
- Reference performance data
- Pick best ones for next few days
- Schedule in advance

### Suggested Action
Implement performance tracking in content workflows. Log metrics for every published piece.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: analytics, performance-tracking, metrics, data-driven
- See Also: LRN-20250213-002

---

## [LRN-20250213-008] knowledge_gap

**Logged**: 2025-02-13T18:31:00Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Postiz: Social Media Scheduling Tool with API for AI Automation

### Details
From Larry's system: Postiz is used to post to TikTok via API.

**Why Postiz:**
- API included in plan (cheaper alternatives don't)
- Incredible documentation for AI to understand
- Allows uploading slideshows as drafts
- Privacy level: "SELF_ONLY" lands content in TikTok drafts folder

**Workflow:**
1. AI generates images, adds text overlays, writes caption
2. AI uploads to TikTok as draft via Postiz API
3. AI sends caption to human (can't add caption to draft via API)
4. Human opens TikTok, picks trending sound, pastes caption, publishes

**Peter's affiliate link:** https://postiz.com/?ref=peterpeters

**Limitations:**
- Music addition requires manual browsing of TikTok's library
- Can't add captions to drafts via API
- Trending sounds change constantly

### Suggested Action
Consider Postiz for social media automation if building TikTok/Instagram workflow.

### Metadata
- Source: user_feedback (article about Larry's TikTok system)
- Tags: social-media, automation, postiz, api, scheduling
- See Also: LRN-20250213-004

---

## [LRN-20250213-009] best_practice

**Logged**: 2025-02-13T18:42:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Socratic Prompting: Stack Expert Questions Before Execution

### Details
From Ryan Lazuka (@lazukars): Instead of asking AI to "do X", stack questions that force strategic thinking **before** taking action.

**Framework:**
1. Identify the expert role (growth marketer, SEO strategist, product manager, etc.)
2. Stack 3-5 strategic questions the expert would ask before acting
3. Have AI answer those questions first
4. Then execute the original task with strategic foundation

**Example:**
- **Traditional:** "Design a marketing funnel for my SaaS product"
- **Socratic:** "What would a top growth marketer ask before building a funnel? What data would they need? What assumptions would they validate first? Now answer those questions for my SaaS product, then design the funnel."

**When to use:**
✅ Strategic thinking, nuanced analysis, creative problem-solving, multi-step reasoning

❌ Simple factual queries, data formatting, basic code generation, quick rewrites

**Template:**
```
What would [EXPERT ROLE] ask before [TASK]?
What data would they need?
What assumptions would they validate first?
What context would they gather?

Now answer those questions for my [CONTEXT],
then [TASK].
```

**Why it works:**
- Transforms AI from task-executor to strategic thinking partner
- Forces expert perspective before execution
- Reduces "fights with ChatGPT" → more strategic conversations
- Compounds knowledge over time

### Suggested Action
Use socratic prompting for complex/strategic tasks. Start with one prompt today: turn your next instruction into 3 questions. Created skill: `/root/.openclaw/workspace/skills/socratic-prompting/SKILL.md`

### Metadata
- Source: user_feedback (Ryan Lazuka @lazukars Twitter thread)
- Tags: prompting, strategic-thinking, expert-perspective, question-stacking, ai-collaboration
- See Also: LRN-20250213-003 (skill files criticality)
