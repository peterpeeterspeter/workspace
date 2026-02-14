# Specialist Agent Configuration

**Status:** 2026-02-02 08:03 UTC

## Current Situation

The squad architecture was designed with 4 specialist agents:
- Carlottta (Coordinator) → This session ✅
- Fury (Research) → Not configured as spawnable agent
- Vision (SEO/Content) → Not configured as spawnable agent
- Quill (Marketing) → Not configured as spawnable agent

## Agent Availability

Current `agents_list` output:
```json
{
  "requester": "main",
  "allowAny": false,
  "agents": [
    {
      "id": "main",
      "configured": false
    }
  ]
}
```

**Only `main` agent is available.** Fury, Vision, Quill are not configured as separate spawnable agents.

## Two Options

### Option 1: Configure Specialist Agents (Proper Setup)
Create/configure Fury, Vision, Quill as separate agent profiles so they can be spawned via `sessions_spawn`.

**Requires:**
- Agent configuration files (likely in OpenClaw config)
- Each agent needs: id, model, tools, session key, SOUL.md reference
- Allowlist configuration for agent spawning

**Benefit:** True multi-agent system with independent sessions

### Option 2: Carlottta Performs Specialist Work (Interim)
Carlottta (current session) does the work of all specialists by:
- Reading each specialist's SOUL.md before working
- Embodying their personality and approach
- Delivering specialist outputs

**Benefit:** Can proceed immediately
**Drawback:** Not true multi-agent coordination (single session doing all work)

## Recommended Path

**Short-term (NOW):** Option 2
- Carlottta performs Fury's competitor research
- Then Vision's content strategy
- Then Quill's brand identity work
- Uses each SOUL.md as guidance for persona/approach

**Medium-term:** Option 1
- Properly configure Fury, Vision, Quill as spawnable agents
- Enable true multi-agent coordination
- Specialists can work in parallel

---

**Proceeding with Option 2 for now.** Carlottta will execute Fury's research phase.
