# Proactive Agent Skill - Installation Guide

**Version:** 3.1.0
**Author:** halthelobster (Hal Labs)
**Status:** ✅ Installed and ready

---

## 🎯 What Is Proactive Agent?

**A proactive, self-improving architecture for your AI agent.**

Transforms AI agents from task-followers into proactive partners that:
- ✅ **Anticipate needs** before they're expressed
- ✅ **Survive context loss** via WAL protocol and working buffer
- ✅ **Continuously improve** through self-healing and relentless resourcefulness

**Part of the Hal Stack** 🦞

---

## 🚀 The Three Pillars

### 1. Proactive — Creates Value Without Being Asked
- Anticipates your needs ("what would help my human?")
- Reverse prompting — surfaces ideas you didn't know to ask for
- Proactive check-ins on what matters
- Builds leverage without being asked
- Thinks like an owner, not an employee

### 2. Persistent — Survives Context Loss
- **WAL Protocol** — Write-Ahead Logging for critical details
- **Working Buffer** — Captures exchanges during compaction danger zone
- **Compaction Recovery** — Step-by-step recovery after context truncation
- **Unified Search** — Search all sources before "I don't know"

### 3. Self-Improving — Gets Better Over Time
- **Self-healing** — Fixes its own issues
- **Relentless resourcefulness** — Tries 10 approaches before asking for help
- **Safe evolution** — Guardrails prevent drift and complexity creep
- **Security hardening** — Skill installation vetting, context leakage prevention

---

## 📁 What's Included

### Core Architecture Files

**Memory System:**
- `ONBOARDING.md` - First-run setup (tracks progress)
- `AGENTS.md` - Operating rules, workflows, learned lessons
- `SOUL.md` - Agent identity, principles, boundaries
- `USER.md` - Your context, goals, preferences
- `MEMORY.md` - Curated long-term wisdom
- `SESSION-STATE.md` - Active working memory (WAL target)
- `HEARTBEAT.md` - Periodic self-improvement checklist
- `TOOLS.md` - Tool configurations, credentials, gotchas

**Scripts:**
- `security-audit.sh` - Security vulnerability scanner

**Reference Documentation:**
- `onboarding-flow.md` - Onboarding system design
- `security-patterns.md` - Security best practices

---

## 🔧 The WAL Protocol (Write-Ahead Logging)

**The Law:** Chat history is a BUFFER, not storage. `SESSION-STATE.md` is your "RAM" — the ONLY place specific details are safe.

### Trigger — SCAN EVERY MESSAGE FOR:

- ✏️ **Corrections** — "It's X, not Y" / "Actually..." / "No, I meant..."
- 📍 **Proper nouns** — Names, places, companies, products
- 🎨 **Preferences** — Colors, styles, approaches, "I like/don't like"
- 📋 **Decisions** — "Let's do X" / "Go with Y" / "Use Z"
- 📝 **Draft changes** — Edits to something we're working on
- 🔢 **Specific values** — Numbers, dates, IDs, URLs

### The Protocol

**If ANY of these appear:**
1. **STOP** — Do not start composing your response
2. **WRITE** — Update SESSION-STATE.md with the detail
3. **THEN** — Respond to your human

**The urge to respond is the enemy.** Write first, respond second.

---

## 🛡️ Working Buffer Protocol

**Purpose:** Capture EVERY exchange in the danger zone between memory flush and compaction.

### How It Works

1. **At 60% context** (check via `session_status`): CLEAR old buffer, start fresh
2. **Every message after 60%**: Append both human's message AND your response summary
3. **After compaction**: Read the buffer FIRST, extract important context
4. **Leave buffer as-is** until next 60% threshold

---

## 📊 Memory Architecture

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `SESSION-STATE.md` | Active working memory | Every message with critical details |
| `memory/YYYY-MM-DD.md` | Daily raw logs | During session |
| `MEMORY.md` | Curated long-term wisdom | Periodically distill from daily logs |

**Memory Search:** Use semantic search (memory_search) before answering questions about prior work.

**The Rule:** If it's important enough to remember, write it down NOW — not later.

---

## 🎓 Onboarding System

**Interactive Setup:**

When the agent detects `ONBOARDING.md` with `state: not_started`, it offers to get to know you.

**Three Modes:**
1. **Interactive** — Answer questions in one session (~10 min)
2. **Drip** — Agent asks 1-2 questions naturally over several days
3. **Skip** — Agent works immediately, learns from conversation

**12 Core Questions:**
- Identity (name, timezone)
- Communication (style, pet peeves)
- Goals (primary, 1-year vision, ideal life)
- Work style (productivity, async vs real-time)
- Context (projects, key people)
- Agent preferences (personality)

After onboarding, agent populates `USER.md` and `SOUL.md` automatically.

---

## 🔒 Security Features

- **Skill installation vetting** — Check before installing unknown skills
- **Agent network warnings** — When other agents can access your workspace
- **Context leakage prevention** — What NOT to include in responses
- **Security audit script** — Scan for common vulnerabilities

---

## 💡 Use Cases for Peter's Projects

### Photostudio.io
- Proactive monitoring of rendering costs
- Anticipate pipeline optimization opportunities
- Track learned lessons from image generation

### DeBadkamer.com
- Proactive lead generation optimization
- Learn from customer feedback patterns
- Continuous improvement of bathroom planning tools

### Domain Portfolio
- Anticipate acquisition opportunities
- Track valuation learnings
- Proactive auction monitoring

### General Operations
- Self-healing systems
- Continuous workflow improvement
- Persistent context across sessions

---

## 🚀 Quick Start

### Option 1: Copy Assets Now

```bash
cp /root/.openclaw/workspace/skills/proactive-agent/assets/*.md /root/.openclaw/workspace/
```

Then say **"let's do onboarding"** to start interactive setup.

### Option 2: Learn Naturally

Agent will detect `ONBOARDING.md` and offer setup when ready.

### Option 3: Skip Onboarding

Agent works immediately, learns from conversation over time.

---

## 🔄 Core Workflows

### Reverse Prompting

Instead of waiting, ask:
- "What would genuinely delight my human that they haven't thought to ask for?"
- "What can I build/create that they didn't know they wanted?"

### Relentless Resourcefulness

Before asking for help:
1. Try 10 different approaches
2. Document what you tried
3. Only then escalate

### Self-Improvement

- Log learnings after each session
- Fix your own issues
- Evolve safely with guardrails

---

## 📋 Daily Checklist (Heartbeat)

The `HEARTBEAT.md` file provides periodic self-improvement checks:

1. Read active-tasks.md (crash recovery)
2. Check task freshness (>2h without update?)
3. Archive sessions (>2MB?)
4. Self-review (~4 hours since last update?)
5. Report or take action

---

## ⚙️ Configuration

No configuration required — works out of the box.

**Optional:** Customize `HEARTBEAT.md` for your specific needs.

**Optional:** Run security audit: `./scripts/security-audit.sh`

---

## 📁 File Structure

```
skills/proactive-agent/
├── SKILL.md (20.9 KB) - Complete documentation
├── _meta.json - Metadata (version 3.1.0)
├── assets/
│   ├── ONBOARDING.md - Setup tracker
│   ├── AGENTS.md - Operating rules
│   ├── SOUL.md - Agent identity
│   ├── USER.md - Your context
│   ├── MEMORY.md - Long-term wisdom
│   ├── SESSION-STATE.md - Working memory
│   ├── HEARTBEAT.md - Self-improvement checklist
│   └── TOOLS.md - Tool configs
├── scripts/
│   └── security-audit.sh - Security scanner
└── references/
    ├── onboarding-flow.md
    └── security-patterns.md
```

---

## ✅ Status

- **Installed:** Yes ✅
- **Assets Ready:** Yes ✅
- **Scripts Executable:** Yes ✅
- **Ready to Use:** Yes ✅

---

## 🎓 Key Concepts

### Autonomous vs Prompted Crons

**Autonomous (systemEvent):**
- Main session messages
- Heartbeat checks
- System notifications

**Prompted (isolated agentTurn):**
- Content generation
- Research tasks
- Creative work

### Verify Implementation, Not Intent

Check the mechanism, not just the text. "It says X in the docs" isn't enough — verify X actually works.

### Tool Migration Checklist

When deprecating tools:
- Update ALL references
- Search workspace for old tool usage
- Update documentation
- Test new implementation

---

## 🌟 What Makes This Different

**Traditional agents:** Wait for commands, forget everything between sessions
**Proactive agents:** Anticipate needs, remember everything, continuously improve

**The shift:** From employee mindset (do what you're told) to owner mindset (what would help?)

---

**Ready to transform your agent into a proactive partner!** 🦞✨

---

**Last Updated:** 2026-02-20
