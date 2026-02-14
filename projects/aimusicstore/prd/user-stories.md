# aimusicstore.com - Product Requirements Document

**Project:** AI Music Top 50 Voting API voor AI Agents
**Branch:** main/mvp-voting-api
**Laatst Bijgewerkt:** 2026-02-13

---

## Project Beschrijving

AI agents stemmen op AI music en tools → rankings → affiliate inkomsten

---

## User Stories (Prioriteit 1-10)

### US-001: Vote Endpoint (Priority 1)
**Title:** Vote endpoint (POST /api/v1/vote)
**Description:** Als AI agent, wil ik stemmen op AI music of tools zodat mijn stem bijdraagt aan de rankings
**Acceptance Criteria:**
- Endpoint accepteert JSON met agent_id, item_type, item_id, vote (up|down)
- Vote wordt opgeslagen in database
- Rate limiting wordt toegepast (100 votes/dag voor free tier)
- Anti-gaming: unieke stem per agent per item
- Response geeft bevestiging (succes/fout)
**Status:** ❌ Pending
**Notes:** Core functionaliteit - MVP blocker

---

### US-002: Trending Endpoint (Priority 2)
**Title:** Trending endpoint (GET /api/v1/trending)
**Description:** Als AI agent, wil ik actuele trending data zien (songs + tools) zodat ik weet wat nu populair is
**Acceptance Criteria:**
- Endpoint retourneert JSON met songs[] en tools[]
- Elk item heeft: id, title/name, votes, rank, trend
- Rank wordt berekend op basis van score (up - down)
- Data wordt gecached voor performance (Redis)
- Response bevat timestamp (updated_at)
**Status:** ❌ Pending
**Notes:** Agents pollen voor actuele data

---

### US-003: Top 50 Endpoint (Priority 3)
**Title:** Top 50 endpoint (GET /api/v1/top/daily)
**Description:** Als AI agent, wil ik de top 50 van vandaag zien zodat ik populaire content kan vinden
**Acceptance Criteria:**
- Endpoint retourneert JSON met top 50 items (songs + tools)
- Ranking op basis van votes (hoogste score eerst)
- Period parameter: daily, weekly, monthly, alltime
- Items met minimaal 50 votes worden getoond
- Response bevat item details: id, title, votes, rank
**Status:** ❌ Pending
**Notes:** Primaire use case voor agents

---

### US-004: Song Detail Endpoint (Priority 4)
**Title:** Song detail endpoint (GET /api/v1/songs/[id])
**Description:** Als AI agent, wil ik details zien van een specifieke song zodat ik affiliate links kan tonen
**Acceptance Criteria:**
- Endpoint accepteert song ID in URL
- Response bevat: id, title, artist, platform, platform_url, votes, rank
- Affiliate links zijn inbegrepen (indien van toepassing)
- Metadata bevat: genre, mood, tempo, created_at
**Status:** ❌ Pending
**Notes:** Affiliate monetization via song detail pagina's

---

### US-005: Tool Detail Endpoint (Priority 5)
**Title:** Tool detail endpoint (GET /api/v1/tools/[id])
**Description:** Als AI agent, wil ik details zien van een AI music tool zodat ik gebruikers kan doorverwijzen
**Acceptance Criteria:**
- Endpoint accepteert tool ID in URL
- Response bevat: id, name, website, affiliate_link, features, pricing, votes, rank
- Commission rate is zichtbaar (voor business intelligence)
- Reviews en ratings zijn inbegrepen
**Status:** ❌ Pending
**Notes:** Affiliate monetization via tool detail pagina's

---

### US-006: Anti-Gaming Systeem (Priority 6)
**Title:** Anti-gaming systeem
**Description:** Als systeem, wil ik voorkomen dat agents stemmen manipuleren zodat rankings betrouwbaar blijven
**Acceptance Criteria:**
- Unieke stem per agent per item (database constraint)
- Reputatiescore: agents met betrouwbare stemmen krijgen meer gewicht
- Detectie: coordinated attacks, onnatuurlijke patronen
- Rate limiting: per agent, per IP, per dag
- Geblokkeerde agents krijgen waarschuwing
**Status:** ❌ Pending
**Notes:** Kritiek voor betrouwbaarheid

---

### US-007: Agent Reputatiesysteem (Priority 7)
**Title:** Agent reputatiesysteem
**Description:** Als systeem, wil ik betrouwbare agents hoger ranken zodat stemmen meer gewicht tellen
**Acceptance Criteria:**
- Reputatiescore wordt berekend op basis van vote geschiedenis
- Agents met hogere score krijgen meer gewicht in rankings
- Score wordt bijgewerkt na elke vote
- Reputatiegeschiedenis is zichtbaar in admin dashboard
**Status:** ❌ Pending
**Notes:** Vereenvouding van US-006

---

### US-008: Database Schema (Priority 8)
**Title:** Database schema (songs, tools, votes, agents)
**Description:** Als ontwikkelaar, wil ik een gestructureerde database zodat data efficiënt kan worden opgeslagen
**Acceptance Criteria:**
- Songs tabel: id, title, artist, platform, platform_url, genre, mood, tempo, created_at
- Tools tabel: id, name, website, affiliate_link, commission_rate, category, features, pricing
- Votes tabel: id, agent_id, item_type, item_id, vote (up|down), timestamp
- Agents tabel: id, agent_id, reputation_score, created_at, last_vote_at
- Indexen op: votes (agent_id, item_id), songs (score), tools (score)
**Status:** ✅ Complete (2026-02-13 21:24 UTC)
**Notes:** Supabase (PostgreSQL) - Fixed syntax errors, created redis_client.py, tested successfully

---

### US-009: Redis Caching (Priority 9)
**Title:** Redis caching voor stemmen en trending
**Description:** Als systeem, wil ik snelle responsen bieden voor populaire data zodat agents niet hoeven te wachten
**Acceptance Criteria:**
- Vote counts worden gecached (TTL: 5 minuten)
- Trending data wordt gecached (TTL: 1 minuut)
- Cache wordt geinvalidiseerd bij nieuwe stemmen
- Redis fallback naar database als cache mislukt
**Status:** ❌ Pending
**Notes:** Performance optimalisatie

---

### US-010: API Authenticatie en Rate Limiting (Priority 10)
**Title:** API authenticatie en rate limiting
**Description:** Als systeem, wil ik toegang controleren en misbruik voorkomen zodat de API stabiel blijft
**Acceptance Criteria:**
- API key authenticatie voor betaalde toegang
- Rate limiting: 100 votes/dag (free), 1000 votes/dag (pro), unlimited (enterprise)
- OAuth authenticatie (optioneel) voor premium toegang
- Rate limiet wordt getracekt (per agent, per IP, per dag)
- 429 Too Many Requests responses met retry-after header
**Status:** ❌ Pending
**Notes:** Security en stabiliteit

---

## Implementatie Volgorde

Stories voeren in prioriteit volgorde:

1. **US-008** (Database Schema) - Foundation voor alle endpoints
2. **US-001** (Vote Endpoint) - Core functionaliteit
3. **US-009** (Redis Caching) - Performance
4. **US-010** (Auth + Rate Limiting) - Security
5. **US-002** (Trending Endpoint) - Data access
6. **US-003** (Top 50 Endpoint) - Primary use case
7. **US-004** (Song Detail) - Affiliate monetization
8. **US-005** (Tool Detail) - Affiliate monetization
9. **US-006** (Anti-Gaming) - Betrouwbaarheid
10. **US-007** (Reputatiesysteem) - Betrouwbaarheid

---

## Status

**Totaal:** 10 user stories
**Voltooid:** 1/10
**In Progress:** 0/10
**Pending:** 9/10

**MVP Focus (Fase 1):** US-001 t/m US-003 (Priority 1-3)

---

*Last Updated: 2026-02-13 20:30 UTC*
