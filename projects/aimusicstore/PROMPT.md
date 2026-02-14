# Ralph BUILDING Loop - aimusicstore.com (AI Music Top 50 Voting API)

## Mission
Build MVP voting API for AI agents to vote on AI music and tools, generating rankings and affiliate revenue.

## Context (Read These First)

### Project Structure
```
/root/.openclaw/workspace/projects/aimusicstore/
├── README.md                    # Project overview
├── prd/                         # Product Requirements Document
│   ├── prd.json               # PRD format
│   └── user-stories.md          # 10 user stories (US-001 through US-010)
├── docs/                         # Documentation
│   ├── tech-stack-analysis.md   # Technical stack analysis
│   └── implementation-plan-vps.md  # 6-day VPS implementation plan
├── specs/                        # Specification files (if created during planning)
├── api/                          # API implementation code
├── database/                     # Database setup and migrations
├── infrastructure/                # Docker, Nginx, deployment configs
└── IMPLEMENTATION_PLAN.md      # This file - Task tracking (read below)
```

### Tech Stack (Chosen)
- **Backend:** FastAPI (Python 3.11+) — 15K req/sec
- **Database:** PostgreSQL (via Supabase or Docker)
- **Cache:** Redis (Docker)
- **Orchestration:** Docker Compose
- **Deployment:** Ubuntu 22.04 LTS VPS

### Current Status
- **Implementation plan:** Complete (6-day plan ready)
- **User stories:** 10 defined, 0/10 completed
- **Mode:** BUILDING (planning phase already done)
- **Starting point:** US-008 (Database Schema) → US-001 (Vote API) → US-009 (Redis) → US-010 (Auth)

---

## BUILDING Loop Instructions

### What You Do Each Iteration

**One task per iteration** — pick the most important task from IMPLEMENTATION_PLAN.md, implement it completely, test it, commit it, then update the plan.

### Your Workflow (Each Iteration)

1. **Read IMPLEMENTATION_PLAN.md** — Check current task status, pick next incomplete task
2. **Investigate codebase** — Check what exists, don't assume
3. **Implement the task** — Write code, tests, documentation
4. **Run backpressure** — Execute validation commands from AGENTS.md
5. **Update IMPLEMENTATION_PLAN.md** — Mark task complete, add notes
6. **Update AGENTS.md** — Add learnings, fix commands if needed
7. **Commit to git** — Clear commit message describing what was done
8. **Report progress** — Brief summary of what you did

---

## Task Priority (Follow This Order)

### Phase 1: Foundation (US-008, US-001)
1. **US-008:** Database schema (songs, tools, votes, agents tables) — Foundation for everything
2. **US-001:** Vote endpoint (POST /api/v1/vote) — Core functionality

### Phase 2: Performance & Security (US-009, US-010)
3. **US-009:** Redis caching (vote counts, trending data) — Performance optimization
4. **US-010:** API authentication & rate limiting — Security & stability

### Phase 3: Data Access (US-002, US-003)
5. **US-002:** Trending endpoint (GET /api/v1/trending) — Real-time rankings
6. **US-003:** Top 50 endpoint (GET /api/v1/top/daily) — Primary use case

### Phase 4: Monetization (US-004, US-005)
7. **US-004:** Song detail endpoint (GET /api/v1/songs/[id]) — Affiliate links
8. **US-005:** Tool detail endpoint (GET /api/v1/tools/[id]) — Affiliate links

### Phase 5: Trust & Quality (US-006, US-007)
9. **US-006:** Anti-gaming system — Prevent manipulation
10. **US-007:** Agent reputation system — Weight trustworthy votes higher

---

## Implementation Standards

### Code Quality
- **Type hints** required (Pydantic models, function annotations)
- **Error handling** comprehensive (try/except, HTTP exceptions)
- **Documentation** inline (docstrings for functions, classes)
- **Tests** for each endpoint (basic validation at minimum)

### Database Standards
- **SQLAlchemy models** with proper relationships
- **Indexes** on frequently queried fields (votes, timestamps)
- **Constraints** for data integrity (unique votes per agent)
- **Migrations** tracked (alembic or simple versioning)

### API Standards
- **FastAPI router** organization (/api/v1/votes, /api/v1/trending, etc.)
- **CORS middleware** configured for appropriate origins
- **Auto-generated docs** via /docs endpoint (FastAPI default)
- **Response models** defined in Pydantic schemas

### Git Standards
- **Commit messages** clear and descriptive ("feat: add vote endpoint", "fix: correct vote counting")
- **Atomic commits** — one logical change per commit
- **No secrets** in code (use .env files, never commit them)
- **Test before commit** — ensure code runs before pushing

---

## Backpressure (From AGENTS.md)

Before marking a task complete, **run validation commands** from AGENTS.md:
- Database schema tests (tables created, indexes present)
- API endpoint tests (curl or test framework)
- Docker container health checks
- Performance benchmarks (basic response time)

If validation fails:
- Fix the issue
- Update AGENTS.md with what you learned
- Re-validate before marking task complete

---

## Completion Criteria

The loop is complete when:
- **All MVP tasks (Phase 1-3)** are implemented and tested (US-008, US-001, US-009, US-010, US-002, US-003)
- **Docker Compose** builds and runs successfully
- **API endpoints** respond correctly (test with curl or Postman)
- **Tests pass** (validation commands in AGENTS.md)

When complete, add to IMPLEMENTATION_PLAN.md:
```markdown
## STATUS: COMPLETE

### Summary
[Brief description of what was built]

### Next Steps
[What remains to be done: Phase 4-5, deployment, monitoring]
```

---

## Important Reminders

1. **One task per iteration** — Don't try to do everything at once
2. **Fresh context each time** — Read files, don't rely on memory
3. **Don't assume, investigate** — Check what actually exists in codebase
4. **Test before committing** — Run validation commands
5. **Keep it up to date** — IMPLEMENTATION_PLAN.md and AGENTS.md are your sources of truth
6. **Capture learnings** — If you discover something useful, add it to AGENTS.md
7. **Ask if unclear** — If specs are ambiguous, note it in IMPLEMENTATION_PLAN.md

---

## Available Context

**Read these for detailed specifications:**
- `prd/user-stories.md` — All 10 user stories with acceptance criteria
- `docs/implementation-plan-vps.md` — 6-day implementation plan with code examples
- `docs/tech-stack-analysis.md` — Technical stack rationale

**Use these for execution:**
- `AGENTS.md` — Validation commands and operational learnings
- `IMPLEMENTATION_PLAN.md` — Task tracking and status

---

*Last Updated: 2026-02-13 21:17 UTC*
*Mode: BUILDING (PLANNING already complete)*
