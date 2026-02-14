# Learning Entry

**Date:** 2026-02-03
**Category:** best_practice
**Priority:** high
**Related Issue:** WordPress publishing integration

## Learning: Don't Build Custom Implementations When Dedicated Skills Exist

**Context:**
While debugging WordPress publishing, I started building a custom implementation (preprocess_markdown.py, md2gutenberg.py, wp-publish-final.sh) instead of properly integrating the existing pinch-to-post skill.

**User Feedback:**
"Use pinch to post, use learning skill to not use custom skills when other dedicated are available"

**Root Cause:**
- Encountered environment variable issues with wp-rest.sh
- Instead of debugging the root cause, built parallel custom code
- Violated the "use dedicated skills first" principle (LRN-20260203-001)

**Correct Approach:**
1. Identify that pinch-to-post skill already exists for WordPress automation
2. Debug the actual issue (set -e causing silent failures)
3. Fix the skill's issue, not replace the skill
4. Document the fix in skill documentation

**Prevention:**
- Before writing custom code, search workspace/skills/ for existing implementations
- Read skill documentation (SKILL.md) to understand capabilities
- Debug existing tools before replacing them
- Follow AGENTS.md guidance on using dedicated skills

**See Also:**
- LRN-20260203-001: Use dedicated skills first
- /root/.openclaw/workspace/skills/pinch-to-post/SKILL.md

## Technical Finding: wp-rest.sh Silent Failures with set -e

**Context:**
wp-rest.sh has `set -e` at line 4, which causes silent failures when the script is called via command substitution in certain contexts.

**Symptoms:**
- Script exits with code 0 or 1
- No output returned
- No error messages
- bash -x shows successful check_env but no curl execution

**Root Cause:**
`set -e` causes bash to exit immediately on any command failure. In complex pipelines with command substitution, this can cause premature exit before output is captured.

**Fix:**
Remove or comment out `set -e` in wp-rest.sh:
```bash
# set -e  # Commented out - causes silent failures in command substitution
```

**Verification:**
After removing `set -e`, wp-rest.sh successfully:
- Converts markdown to Gutenberg blocks
- Publishes to WordPress REST API
- Returns proper JSON responses

**See Also:**
- /root/.openclaw/workspace/skills/pinch-to-post/wp-rest.sh:4
- Bash set -e documentation
