# Errors - Bathroom Products Project

This file captures command failures, exceptions, and unexpected behaviors encountered during the bathroom products research and transformation pipeline work.

---

## [ERR-20250213-001] transform_data.py

**Logged**: 2025-02-13T15:15:00Z
**Priority**: high
**Status**: resolved
**Area**: data_processing

### Summary
AttributeError: 'str' object has no attribute 'get' during JSON flattening

### Error
```
Traceback (most recent call last):
  File "/root/.openclaw/workspace/research/bathroom-products/transform_data.py", line 195, in flatten_data
    "name": product.get("name", ""),
            ^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'get'
```

### Context
- Command: `python3 transform_data.py`
- Input: 33 JSON files from scraper
- Issue: Assumed uniform JSON structure across all files
- Discovery: Some files had nested structure: `{"Baden": {"baden": {Zeza: [products]}}}`
- Original code expected: `{"baden": {Zeza: [products]}}`

### Suggested Fix
Check JSON structure before flattening:
```python
def flatten_data(raw_data):
    for category_dutch, brands_or_nested in raw_data.items():
        first_val = next(iter(brands_or_nested.values())) if brands_or_nested else None
        
        if first_val and isinstance(first_val, dict):
            # Nested structure - go one level deeper
            for nested_key, brands in brands_or_nested.items():
                # ... process brands
        elif first_val and isinstance(first_val, list):
            # Flat structure - brands directly map to product lists
            for brand, products in brands_or_nested.items():
                # ... process products
```

### Resolution
- **Resolved**: 2025-02-13T15:20:00Z
- **Commit/PR**: Fixed in transform_data.py
- **Notes**: Added nested structure detection. Now handles 3 JSON formats correctly. Reduced 232 raw products to 80 unique models.

### Metadata
- Reproducible: yes
- Related Files: `/root/.openclaw/workspace/research/bathroom-products/transform_data.py`
- See Also: LRN-20250213-001 (best_practice for flexible data loading)

---

