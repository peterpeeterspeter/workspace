# Humanize AI Text - Installation Guide

**Version:** 1.0.0 (from ClawHub)
**Author:** moltbro
**Status:** ✅ Installed and tested

---

## 🎯 What It Does

**Humanize AI Text** detects and transforms AI-generated content to bypass AI detectors like:
- GPTZero
- Turnitin
- Originality.ai
- And other AI detection tools

**Based on:** Wikipedia's "Signs of AI Writing" guide

---

## 🔍 How It Works

### Detection (16 Pattern Categories)

**Critical (Immediate Detection):**
- Citation bugs (oaicite, turn0search, contentReference)
- Knowledge cutoff phrases ("as of my last training")
- Chatbot artifacts ("I hope this helps", "As an AI")
- Markdown formatting (**bold**, ## headers)

**High Signal:**
- AI vocabulary (delve, tapestry, landscape, pivotal)
- Significance inflation ("serves as a testament", "pivotal moment")
- Promotional language (vibrant, groundbreaking, nestled)
- Copula avoidance ("serves as" instead of "is")

**Medium Signal:**
- Superficial -ing ("highlighting the importance")
- Filler phrases ("in order to", "due to the fact that")
- Vague attributions ("experts believe")
- Challenges formula ("Despite these challenges")

**Style Signal:**
- Curly quotes ("") vs straight ("")
- Em dash overuse (—)
- Negative parallelisms ("Not only... but also")
- Rule of three (forced triplets)

---

## 🚀 Quick Start

### Detect AI Patterns

```bash
# Scan a file
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py document.txt

# Score only
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py document.txt -s

# JSON output
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py document.txt -j

# Pipe text
echo "Your text here" | python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py
```

### Transform to Human-Like

```bash
# Basic transformation
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py document.txt -o clean.txt

# Aggressive mode (more fixes)
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py document.txt -a -o clean.txt

# Quiet mode (less output)
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py document.txt -q
```

### Compare Before/After

```bash
# See improvement
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/compare.py document.txt -o clean.txt
```

---

## 📊 AI Probability Scoring

| Rating | Criteria |
|--------|----------|
| **Very High** | Citation bugs, knowledge cutoff, or chatbot artifacts present |
| **High** | >30 issues OR >5% issue density |
| **Medium** | >15 issues OR >2% issue density |
| **Low** | <15 issues AND <2% density |

---

## 🛠️ What Gets Auto-Fixed

**Automatic Fixes:**
- ✅ Citation bugs → Removed
- ✅ Markdown (**, ##, ```) → Plain text
- ✅ Chatbot sentences → Removed
- ✅ "Serves as" → "Is"
- ✅ "Boasts" → "Has"
- ✅ Filler phrases → Simplified
- ✅ Curly quotes → Straight quotes

**Aggressive Mode (-a):**
- ✅ Simplifies -ing clauses
- ✅ Reduces em dashes

**Manual Fixes Needed:**
- ⚠️ AI vocabulary (delve, tapestry, landscape)
- ⚠️ Significance inflation phrases
- ⚠️ Promotional language
- ⚠️ Rule of three patterns

---

## 💡 Use Cases for Peter's Projects

### Photostudio.io
- Humanize AI-generated product descriptions
- Make marketing copy sound natural
- Bypass AI detectors on content sites

### DeBadkamer.com
- Natural-sounding bathroom renovation tips
- Human-written looking blog content
- Avoid AI detection on SEO content

### Content Creation
- Transform ChatGPT/Claude output
- Make AI text undetectable
- Pass AI content detectors

### General
- Clean up LLM-generated content
- Make text sound human-written
- Bypass plagiarism/AI detectors

---

## 📋 Workflow Example

```bash
# 1. Check AI detection risk
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py article.txt

# 2. Transform with comparison
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/compare.py article.txt -o article_v2.txt

# 3. Verify improvement
python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py article_v2.txt -s

# 4. Manual review for remaining patterns
# (AI vocabulary, promotional language, etc.)
```

---

## 🔄 Batch Processing

```bash
# Scan multiple files
for f in *.txt; do
  echo "=== $f ==="
  python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/detect.py "$f" -s
done

# Transform all markdown files
for f in *.md; do
  python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py "$f" -a -o "${f%.md}_clean.md" -q
done
```

---

## ⚙️ Customization

Edit `/root/.openclaw/workspace/skills/humanize-ai-text/scripts/patterns.json` to:

- Add AI vocabulary words
- Modify significance inflation phrases
- Add promotional language patterns
- Customize copula replacements
- Add filler phrase replacements
- Add chatbot artifact phrases

---

## 📁 Files

```
skills/humanize-ai-text/
├── SKILL.md (5.2 KB) - Full documentation
├── README.md (this file) - Installation guide
├── scripts/
│   ├── detect.py (7.9 KB) - Scan for AI patterns
│   ├── transform.py (5.3 KB) - Transform text
│   ├── compare.py (2.3 KB) - Before/after comparison
│   └── patterns.json (6.6 KB) - AI pattern definitions
└── _meta.json - Skill metadata
```

---

## ✅ Status

- **Installed:** Yes ✅
- **Tested:** Yes ✅
- **Working:** Verified ✅
- **Python:** Python 3 ✅

---

**Ready to humanize AI-generated text!** ✨

---

**Last Updated:** 2026-02-20
