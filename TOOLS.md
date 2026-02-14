# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Browser Tool (OpenClaw)
**Executable:** `/usr/bin/google-chrome-stable` (NOT `/usr/bin/google-chrome`)
**CDP Port:** 18800
**Profile:** openclaw (isolated managed browser)
**Status:** ✅ Working (Chrome PID 3423483, installed 2026-02-09)

**Snapshot Parameters:**
- Full capture: `depth=5, maxChars=50000, compact=false`
- Quick scan: `depth=3, maxChars=15000, compact=true`
- Interactive: `depth=4, compact=true, interactive=true`

**Common Fixes:**
- If browser fails: Check `executablePath` uses `-stable` suffix
- If snapshot incomplete: Increase `depth` to 5, `maxChars` to 50000, `compact=false`
- For snap Chromium issues: Install Google Chrome .deb instead
