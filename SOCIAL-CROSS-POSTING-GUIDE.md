# 📱 Social Cross-Posting - Setup Guide

**From:** Pinch-to-Post v3.1.2 Feature Documentation

---

## Feature Overview

**Social Cross-Posting** - One post. Three platforms. Zero extra work.

Automatically publish your WordPress content to:
- ✅ Twitter/X
- ✅ LinkedIn
- ✅ Mastodon

---

## Current Status

### ✅ Helper Script Installed
- **Location:** `/root/.openclaw/workspace/scripts/pinch-to-post-helpers/social-post.sh`
- **Master command:** `pinch-to-post social-post <platform> <message> [url]`

### ❌ Social Credentials NOT Configured
- Twitter API: Not configured
- LinkedIn API: Not configured
- Mastodon API: Not configured

---

## How It Works

### Twitter/X
```bash
pinch-to-post social-post twitter "New article!" "https://crashcasino.io/post"
```

**Requirements:**
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_SECRET

**Best with:** `twurl` gem installed

### LinkedIn
```bash
pinch-to-post social-post linkedin "Check out our latest post" "https://crashcasino.io/post"
```

**Requirements:**
- LINKEDIN_ACCESS_TOKEN
- LINKEDIN_PERSON_ID

**Posts to:** Your LinkedIn profile feed

### Mastodon
```bash
pinch-to-post social-post mastodon "Fresh content!" "https://crashcasino.io/post"
```

**Requirements:**
- MASTODON_INSTANCE (e.g., https://mastodon.social)
- MASTODON_ACCESS_TOKEN

**Posts to:** Your Mastodon account

---

## Configuration

To enable social cross-posting, add to `/root/.openclaw/workspace/.env`:

```bash
# Twitter/X API
TWITTER_API_KEY="your_api_key"
TWITTER_API_SECRET="your_api_secret"
TWITTER_ACCESS_TOKEN="your_access_token"
TWITTER_ACCESS_SECRET="your_access_secret"

# LinkedIn API
LINKEDIN_ACCESS_TOKEN="your_linkedin_token"
LINKEDIN_PERSON_ID="urn:li:person:YOUR_ID"

# Mastodon API
MASTODON_INSTANCE="https://mastodon.social"
MASTODON_ACCESS_TOKEN="your_mastodon_token"
```

---

## Integration with Automated Workflows

### Vision's Enhanced Workflow
After publishing articles, can auto-share to social:

```bash
# After bulk publish
for url in "${PUBLISHED_URLS[@]}"; do
  pinch-to-post social-post twitter "New crash casino guide!" "$url"
  pinch-to-post social-post linkedin "Latest insights" "$url"
done
```

### Quill's Enhanced Workflow
Coordinate social media distribution:

```bash
# Weekly content promotion
pinch-to-post social-post twitter "Week 2 content recap!" "https://crashcasino.io/week-2"
```

---

## Use Cases

### Immediate Sharing
Publish article → immediately share to all platforms

```bash
# Publish
pinch-to-post publish crashcasino 838

# Share to social
pinch-to-post social-post twitter "🎰 New: How We Rate Crash Casinos" "https://crashcasino.io/rate-crash-casinos"
pinch-to-post social-post linkedin "Just published: Crash casino rating methodology" "https://crashcasino.io/rate-crash-casinos"
pinch-to-post social-post mastodon "Fresh from the keyboard: transparency in crash gambling reviews" "https://crashcasino.io/rate-crash-casinos"
```

### Batch Promotion
Share multiple articles at once

```bash
for id in 838 837 836; do
  URL=$(curl -s "https://crashcasino.io/wp-json/wp/v2/posts/$id" -u "peter:PASSWORD" | jq -r '.link')
  pinch-to-post social-post twitter "New crash gambling guide!" "$URL"
done
```

### Scheduled Sharing
Schedule social posts via cron:

```bash
# Morning tweet
0 9 * * * pinch-to-post social-post twitter "Morning crash game tips!" "https://crashcasino.io/tips"

# Evening LinkedIn
0 18 * * * pinch-to-post social-post linkedin "Evening crash gambling insights" "https://crashcasino.io/insights"
```

---

## Platform-Specific Best Practices

### Twitter/X
- **Length:** Keep it short (under 280 chars)
- **Hashtags:** Use 2-3 relevant tags (#CrashGambling #OnlineCasino)
- **Emojis:** ✅ Use them (🎰💰🎲)
- **Frequency:** 1-3 posts per day
- **Timing:** Post when audience is active (test and adjust)

**Example tweet:**
```
🎰 New: How We Rate Crash Casinos: Full Transparency on Our 2026 Review Process

We tested 50+ crash casinos using 9 crash-specific criteria. Here's what we found.

#CrashGambling #OnlineCasino #ResponsibleGambling

Read: https://crashcasino.io/rate-crash-casinos
```

### LinkedIn
- **Style:** Professional but conversational
- **Length:** Can be longer (up to 3000 chars)
- **Format:** Use line breaks for readability
- **Hashtags:** 3-5 relevant tags
- **Frequency:** 2-3 posts per week
- **Timing:** Business hours (9-5 weekdays)

**Example LinkedIn post:**
```
I just published a comprehensive analysis of how we rate crash casinos in 2026.

Key highlights:
• 9 crash-specific criteria
• Full transparency on our process
• Real money testing results
• Affiliate disclosure

The goal? Help you find safe, fair crash gambling sites.

Link in comments 👇

#iGaming #OnlineGaming #CasinoIndustry #ResponsibleGambling
```

### Mastodon
- **Style:** Community-focused, conversational
- **Length:** 500 chars
- **Format:** Conversational, use CW for sensitive topics
- **Hashtags:** Don't overuse
- **Frequency:** 1-2 posts per day
- **Timing:** When your followers are active

**Example Mastodon post:**
```
Fresh from the keyboard: A deep dive into crash game casino ratings.

We tested 50+ sites using crash-specific criteria: RTP, provably fair algorithms, withdrawal speeds, and more.

Full transparency + affiliate disclosure.

https://crashcasino.io/rate-crash-casinos

#crashgambling #casinos
```

---

## Benefits

### Without Social Cross-Posting
- Publish article → manually copy URL → open Twitter → compose tweet → post
- Repeat for LinkedIn
- Repeat for Mastodon
- **Time per article:** 5-10 minutes

### With Social Cross-Posting
- Publish article → one command → posted to all 3 platforms
- **Time per article:** 30 seconds

**Time saved:** 90%+

---

## Next Steps

### Option 1: Configure Full Social Integration
Set up API credentials for all 3 platforms (recommended if you have existing social presence)

### Option 2: Start with One Platform
Begin with Twitter (easiest to set up), expand later

### Option 3: Use Manual Sharing
Continue posting links manually (current approach)

---

## Want to Enable?

To configure social cross-posting, I need:

1. **Twitter API credentials** (if you have them)
   - Twitter Developer account
   - API key + secret
   - Access token + secret

2. **LinkedIn credentials** (optional)
   - LinkedIn access token
   - Your LinkedIn person ID

3. **Mastodon instance** (optional)
   - Your Mastodon server URL
   - Access token

**Or:** I can help you set up Twitter Developer account to get credentials.

---

**The feature is built and ready. Just need credentials to activate.** 🚀

---

*Feature documented: 2026-02-03 16:15 UTC*
*Status: Ready to configure*
