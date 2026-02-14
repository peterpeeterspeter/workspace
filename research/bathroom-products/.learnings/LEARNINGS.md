# Learnings - Bathroom Products Project

This file captures corrections, knowledge gaps, and best practices discovered during the bathroom products research and transformation pipeline work.

---

## [LRN-20250213-004] best_practice

**Logged**: 2025-02-13T18:14:00Z
**Priority**: medium
**Status**: pending
**Area**: domain_research

### Summary
Domeinmarktonderzoek vereist multidisciplinaire aanpak: markttrends, business model analyse, concurrentieanalyse

### Details
Peter vroeg om ResidentialLeases.com domein te onderzoeken voor mogelijke aankoop. Methode:
1. **Domeinstatus check:** Web fetch toont domein staat op DropCatch (marktplaats)
2. **Markttrends onderzoek:** Web search naar "domain leasing" business model, trends 2025
3. **Business model analyse:** Revenue modellen (€200-500/maand), lease-to-own, marktgroei ($1.025B 2027)
4. **Concurrentie research:** Identificeer soortgelijke domeinen (PropertyLease.com, LeaseHomes.net)
5. **Strategische aanbeveling:** 3 business opties met ROI projecties
6. **Documentatie:** Creër uitgebreid markdown rapport met alle bevindingen

**Gevonden:**
- Dictionary domeinnaam (Residential + Leases) = 5/5 SEO score
- Residentaal lease markt groeit wereldwijd
- Domeinverhuur wordt populairder dan verkoop bij startups
- Unieke niche met weinig concurrentie
- Aanbeveling: koop met doel €7,500 (realistische marktwaarde)

**Leerdpunt:**
- DataForSEO API niet geconfigureerd (kon geen zoekvolume data)
- Moest vertrouwen op web search en industrierapportages

### Suggested Action
Voor domeinanalyses: combineer meerdere tools:
1. Web fetch (domein status check)
2. Web search (markttrends, concurrentie)
3. Vaardigheden: seo-dataforseo (zoekvolume), seo-audit (concurrentie SEO)
4. Documenteer altijd als markdown met business case, ROI projecties

### Metadata
- Source: user_request
- Related Files: `/root/.openclaw/workspace/research/residentialleases-domain-analysis.md`
- Tags: domain-investing, marktonderzoek, business-case, domeinverhuur, concurrentieanalyse

---

## [LRN-20250213-001] best_practice

**Logged**: 2025-02-13T17:49:00Z
**Priority**: high
**Status**: pending
**Area**: data_processing

### Summary
Multiple JSON file formats exist from scraper - need flexible data loading

### Details
The Sawiday scraper produced different JSON structures across different runs:
1. Multi-category format: `{"Baden": {"baden": {brand: [products]}}}`
2. Brand-level format: `{brand: [products]}`
3. List format: `[{products}]`

Original code assumed single structure, causing AttributeError when products were strings instead of dicts.

### Suggested Action
Always inspect JSON file structure first with `type(data)` checks. Handle multiple formats explicitly:
- Check if dict → examine first value type
- If first value is dict → nested structure
- If first value is list → flat structure
- If data is list → already flattened

### Metadata
- Source: error_analysis
- Related Files: `/root/.openclaw/workspace/research/bathroom-products/transform_data.py`
- Tags: json, data-loading, flexible-parsing, scraper

---

## [LRN-20250213-002] best_practice

**Logged**: 2025-02-13T17:49:00Z
**Priority**: medium
**Status**: pending
**Area**: deduplication

### Summary
Deduplicate by base model name, not just product URLs

### Details
Products come in size variants (e.g., "Zeza Oval ligbad 190x90cm", "Zeza Oval ligbad 170x70cm"). These are the same base model in different sizes. 

Original deduplication by URL kept all size variants as separate products. Fixed by:
1. Extract base model name: remove dimensions (e.g., "190x90cm")
2. Group by base model name
3. Keep first variant (one size per model)
4. Color/material variants have different base names → preserved

Result: 232 raw products → 80 unique models (152 size variants removed)

### Suggested Action
Implement `extract_model_name()` to strip dimension patterns:
```python
import re
def extract_model_name(name: str) -> str:
    # Remove dimensions (e.g., 190x90cm, 60x46x55cm)
    model = re.sub(r'\d+[xX]\d+(?:[xX]\d+)?(?:cm)?', '', name)
    model = ' '.join(model.split())
    return model
```

### Metadata
- Source: pipeline_development
- Related Files: `/root/.openclaw/workspace/research/bathroom-products/transform_data.py`
- Tags: deduplication, model-extraction, size-variants, data-quality

---

## [LRN-20250213-003] best_practice

**Logged**: 2025-02-13T17:49:00Z
**Priority**: medium
**Status**: pending
**Area**: classification

### Summary
Tier classification works best when category-specific

### Details
Price varies dramatically by product category. A €300 bathtub is "budget" while a €300 mirror is "premium".

Implemented tier thresholds by category:
- Bathtub: budget<€300, mid<€600, premium≥€600
- Shower: budget<€200, mid<€400, premium≥€400
- Toilet: budget<€150, mid<€300, premium≥€300
- Vanity: budget<€200, mid<€500, premium≥€500

Result: 17 budget, 22 mid, 41 premium products (realistic distribution)

### Suggested Action
Store tier thresholds in config dict, not hardcoded:
```python
TIER_THRESHOLDS = {
    "Bathtub": {"budget": 300, "mid": 600},
    "Shower": {"budget": 200, "mid": 400},
    # ... other categories
}
```

### Metadata
- Source: pipeline_development
- Related Files: `/root/.openclaw/workspace/research/bathroom-products/transform_data.py`
- Tags: classification, tier-system, category-specific, price-segmentation

---

