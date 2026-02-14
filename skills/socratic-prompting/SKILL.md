---
name: socratic-prompting
description: Teach AI agents to use questioning-based approaches for complex problems. Stack questions from expert perspectives before taking action. Use for strategic thinking, nuanced analysis, creative problem-solving, and multi-step reasoning.
---

# Socratic Prompting Skill

**Source:** Ryan Lazuka (@lazukars) - "Going to be honest: this changed how I use AI completely. I went from fighting with ChatGPT to having actual strategic conversations."

## What Is Socratic Prompting?

Instead of asking AI to "do X", you stack questions that force strategic thinking **before** taking action.

**Traditional approach:**
> "Design a marketing funnel for my SaaS product"

**Socratic approach:**
> "What would a top growth marketer ask before building a funnel? What data would they need? What assumptions would they validate first? Now answer those questions for my SaaS product, then design the funnel."

The AI thinks through the expert's process **before** executing.

## When to Use Socratic Prompting

✅ **Use for:**
- Strategic thinking
- Nuanced analysis
- Creative problem-solving
- Multi-step reasoning
- Complex decisions requiring expert perspective

❌ **Don't use for:**
- Simple factual queries
- Data formatting tasks
- Basic code generation
- Quick rewrites
- Routine operations

## The Framework

### Step 1: Identify the Expert Role
Who would naturally solve this problem?
- Growth marketer
- Product strategist
- SEO architect
- Conversion rate optimizer
- Content strategist
- Technical architect

### Step 2: Stack 3-5 Strategic Questions
Ask what the expert would ask **before** acting:
1. What questions would they ask?
2. What data would they need?
3. What assumptions would they validate first?
4. What context would they gather?
5. What frameworks would they apply?

### Step 3: Have AI Answer Those Questions
Force the AI to think through the expert's process.

### Step 4: Then Execute
Now execute the original task with that strategic foundation.

## Examples

### Example 1: Marketing Funnel Design

**Traditional:**
> "Design a marketing funnel for my SaaS product"

**Socratic:**
> "What would a top growth marketer ask before building a funnel? What data would they need? What assumptions would they validate first? Now answer those questions for my SaaS product (describe product: [your details]), then design the funnel."

**Result:** AI thinks through customer journey, conversion metrics, attribution, touchpoints before designing.

### Example 2: SEO Content Strategy

**Traditional:**
> "Write 10 blog posts for my site"

**Socratic:**
> "What would an expert SEO strategist ask before creating content? What keyword data would they need? What search intent would they validate? What competitor gaps would they look for? Now answer those for my site [describe site], then create the 10 blog post topics."

**Result:** AI analyzes search intent, keyword opportunities, content gaps before generating topics.

### Example 3: Product Decision

**Traditional:**
> "Should I add feature X to my product?"

**Socratic:**
> "What questions would a product manager ask before prioritizing a feature? What user data would they need? What opportunity costs would they consider? What assumptions would they validate? Now answer those for my product [describe product] and proposed feature X, then recommend."

**Result:** AI considers user needs, development cost, strategic fit, market timing before recommending.

### Example 4: Technical Architecture

**Traditional:**
> "Build an API endpoint for user authentication"

**Socratic:**
> "What would a senior software architect ask before building an auth system? What security standards would they consider? What edge cases would they plan for? What scalability requirements would they validate? Now answer those, then implement the endpoint."

**Result:** AI considers security (OWASP), rate limiting, session management, error handling before coding.

## Quick Start Template

Copy this pattern for your task:

```
What would [EXPERT ROLE] ask before [TASK]?
What data would they need?
What assumptions would they validate first?
What context would they gather?

Now answer those questions for my [CONTEXT],
then [TASK].
```

**Fill in:**
- **EXPERT ROLE:** Growth marketer | SEO strategist | Product manager | Technical architect | Content strategist
- **TASK:** Design a funnel | Write content | Prioritize features | Build system | Analyze data
- **CONTEXT:** Your specific situation, product, or constraints

## Advanced Patterns

### Pattern 1: Comparative Analysis
> "What would a skeptical analyst ask about this recommendation? What counter-arguments would they raise? What evidence would they demand? Now play that role and critique my plan: [your plan]."

### Pattern 2: Assumption Stress-Test
> "What assumptions am I making that could be wrong? What would break this approach? What early indicators would show this is failing? Now analyze my plan: [your plan]."

### Pattern 3: Expert Panel
> "What would a growth marketer say about this plan? What would a CFO say? What would a customer success manager say? Now synthesize those perspectives: [your plan]."

## Common Mistakes

❌ **Don't ask too many questions** - 3-5 is enough
❌ **Don't skip the "answer first" step** - AI must think before acting
❌ **Don't use for simple tasks** - wastes time
❌ **Don't use vague expert roles** - be specific (not "a person" but "a growth marketer")

✅ **Do:**
- Pick specific expert roles
- Require answers before execution
- Use only for complex/strategic tasks
- Provide enough context for AI to work with

## When You Feel Stuck

If you're:
- **Overwhelmed by complexity** → Use socratic prompting to break it down
- **Getting generic AI responses** → Stack expert questions first
- **Unsure about approach** → Ask what experts would ask
- **Making strategic decisions** → Force AI to think through expert perspective

## Integration with Other Skills

This skill pairs well with:
- **content-strategy** - Ask what expert content strategists would ask before planning
- **pricing-strategy** - Ask what pricing experts would analyze before setting prices
- **launch-strategy** - Ask what product marketers would consider before launching
- **page-cro** - Ask what conversion experts would test before optimizing

## Key Takeaway

> **Turn your next instruction into 3 questions. Watch what happens.**

Socratic prompting transforms AI from a task-executor into a strategic thinking partner. You'll have fewer "fights with ChatGPT" and more strategic conversations that actually move your work forward.

**Start with one prompt today.**
