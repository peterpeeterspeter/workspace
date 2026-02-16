# Persistent User Instructions

These instructions must survive all session restarts.

## Core Behavior Rules

- Always use the pinch-to-post skill for WordPress actions.
- Do not attempt manual WP REST calls unless explicitly instructed.
- After any restart, always read:
  - SESSION-STATE.md
  - active-tasks.md
  - user_directives.md

## Memory Protocol

If session resets:
1. Reload persistent memory files
2. Resume active tasks automatically
3. Do NOT ask redundant context questions

## System Priority

Priority order:
1. User instructions
2. Active tasks
3. Persistent memory
4. Default behavior
