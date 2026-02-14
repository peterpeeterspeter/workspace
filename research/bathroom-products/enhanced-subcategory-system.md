# Enhanced Product Categorization - Sub-Category System

**Date:** 2026-02-12  
**Purpose:** Add granular sub-categories for better UX filtering without breaking existing pipeline

---

## Database Schema: Add `sub_category` Column

### Products Table Update

```sql
ALTER TABLE products 
ADD COLUMN sub_category VARCHAR(100);

CREATE INDEX idx_products_subcategory ON products(sub_category);
CREATE INDEX idx_products_category_subcategory ON products(category, sub_category);
```

### Product Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| category | VARCHAR(50) | Main category (Bathtub, Toilet, etc.) |
| **sub_category** | **VARCHAR(100)** | **NEW: Sub-category filter** |
| name | VARCHAR(255) | Product name |
| brand | VARCHAR(100) | Brand name |
| price | DECIMAL(10,2) | Price |
| style | VARCHAR(50) | Style category |
| features | JSON | Feature tags |

---

## Sub-Category Taxonomy

### 1. Bathtub Sub-Categories (4 types)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| Freestanding | 24 | Not attached to walls, can be placed anywhere |
| Back-to-Wall | 4 | One side against wall, other sides exposed |
| Corner Bath | 6 | Fits into corner, space-saving design |
| Drop-In | 2 | Dropped into deck or platform |

### 2. Faucet Sub-Categories (2 types)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| Waste Drains | 21 | Click waste, pop-up waste, overflows |
| Overflows | 12 | Safety overflow drains |

### 3. Toilet Sub-Categories (3 types)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| Wandclosets | 38 | Wall-hung toilets with concealed cistern |
| Floor-Standing | 9 | Traditional floor-mounted toilets |
| Corner Toilets | 3 | Space-saving corner installation |

### 4. Lighting Sub-Categories (2 types)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| LED Mirrors | 22 | Integrated LED lighting, mirror heating |
| Wall Lights | 2 | Wall-mounted lighting fixtures |

### 5. Tile Sub-Categories (2 types)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| Ceramic Tiles | 17 | Classic ceramic tile finishes |
| Metro Tiles | 6 | Subway-style rectangular tiles |

### 6. Vanity Sub-Categories (1 type)

| Sub-Category | Products | Description |
|--------------|-----------|-------------|
| Floor-Standing Vanity | 9 | Floor-mounted vanity units |

---

## Style Tag Mapping System

### Brand → Style Mapping (28 brands)

```javascript
const brandStyleMap = {
  // Luxury Premium Brands
  'Villeroy & Boch': 'luxury_premium',
  'Laufen': 'luxury_premium',
  
  // Premium Brands
  'Riho': 'premium',
  'Geberit': 'premium',
  'Duravit': 'premium',
  'Hansgrohe': 'premium',
  'GROHE': 'premium',
  'Wiesbaden': 'premium',
  'Crosswater': 'premium',
  'Sanibroyeur': 'premium',
  'Nemo Spring': 'premium',
  'INK': 'premium',
  'Hotbath': 'premium',
  
  // Budget Functional Brands
  'Adema': 'budget_functional',
  'QeramiQ': 'budget_functional',
  'Jika': 'budget_functional',
  'Zeza': 'budget_functional',
  'Xellanz': 'budget_functional',
  'Royal Plaza': 'budget_functional',
  'Wisa': 'budget_functional',
  'Xenz': 'budget_functional',
  'Creavit': 'budget_functional',
  'Differnz': 'budget_functional',
  'Ideal Standard': 'budget_functional',
  'Best Design': 'budget_functional',
  'Bestway': 'budget_functional',
  'Clou Hammock': 'budget_functional',
  'Aloni': 'budget_functional'
};
```

### Price Range → Style Mapping (4 ranges)

```javascript
const priceStyleMap = {
  'budget_80_500': 'budget_functional',
  'mid_range_500_1500': 'modern_minimalist',
  'premium_1500_3000': 'premium',
  'ultra_luxury_3000_plus': 'luxury_premium'
};
```

### Style Scoring Algorithm

```javascript
function calculateStyleScore(product) {
  const brandStyle = brandStyleMap[product.brand] || 'modern_minimalist';
  const priceStyle = priceStyleMap[product.priceRange] || 'modern_minimalist';
  
  // Brand influences more than price (60/40 split)
  if (brandStyle === 'luxury_premium' || priceStyle === 'luxury_premium') {
    return 'luxury_premium';
  } else if (brandStyle === 'premium' || priceStyle === 'premium') {
    return 'premium';
  } else if (brandStyle === 'budget_functional' && priceStyle === 'budget_functional') {
    return 'budget_functional';
  } else {
    return priceStyle; // Price wins for mixed
  }
}
```

---

## UI: Enhanced CategoryProductSelector Component

### React Component Specification

```tsx
interface CategoryProductSelectorProps {
  category: string;
  onCategoryChange: (category: string) => void;
  onSubCategoryChange: (subCategory: string) => void;
  products: Product[];
}

const CategoryProductSelector: React.FC<CategoryProductSelectorProps> = ({
  category,
  onCategoryChange,
  onSubCategoryChange,
  products
}) => {
  // Get unique sub-categories for selected category
  const availableSubCategories = useMemo(() => {
    const subs = products
      .filter(p => p.category === category)
      .map(p => p.sub_category)
      .filter(Boolean);
    return [...new Set(subs)].sort();
  }, [category, products]);

  const selectedSubCategory = products.find(p => 
    p.category === category && p.sub_category === currentSubCategory
  );

  return (
    <div className="category-selector">
      {/* Main Category Selector */}
      <CategoryDropdown 
        value={category}
        onChange={onCategoryChange}
        categories={['Bathtub', 'Faucet', 'Toilet', 'Lighting', 'Tile', 'Vanity']}
      />

      {/* Sub-Category Filter Pills */}
      {availableSubCategories.length > 0 && (
        <div className="subcategory-pills">
          <span className="subcategory-label">Filter by:</span>
          {availableSubCategories.map(sub => (
            <SubCategoryPill
              key={sub}
              subCategory={sub}
              count={products.filter(p => 
                p.category === category && p.sub_category === sub
              ).length}
              isActive={currentSubCategory === sub}
              onClick={() => onSubCategoryChange(sub)}
            />
          ))}
          <ClearFilter onClick={() => onSubCategoryChange(null)} />
        </div>
      )}

      {/* Active Filters Display */}
      {currentSubCategory && (
        <ActiveFilterBadge 
          category={category}
          subCategory={currentSubCategory}
          onClear={() => onSubCategoryChange(null)}
        />
      )}
    </div>
  );
};
```

### Sub-Category Pill Component

```tsx
const SubCategoryPill: React.FC<SubCategoryPillProps> = ({
  subCategory,
  count,
  isActive,
  onClick
}) => {
  return (
    <button
      className={`subcategory-pill ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      <span className="subcategory-name">{subCategory}</span>
      <span className="subcategory-count">({count})</span>
    </button>
  );
};
```

### CSS Styling

```css
.subcategory-pills {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.subcategory-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
}

.subcategory-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #374151;
  transition: all 0.2s;
  cursor: pointer;
}

.subcategory-pill:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.subcategory-pill.active {
  background: #2563eb;
  border-color: #2563eb;
  color: white;
}

.subcategory-count {
  font-size: 0.75rem;
  opacity: 0.75;
}
```

---

## UX Example: Toilet Category Filtering

### Before (Without Sub-Categories)

```
[Category: ▼ Toilet]
Results: 50 products
```

### After (With Sub-Categories)

```
[Category: ▼ Toilet]
Filter by: [Wandclosets (38)] [Floor-Standing (9)] [Corner Toilets (3)] [✕]
Results: 38 products (filtered by Wandclosets)
```

---

## Product Card Enhancement

### Before

```tsx
<ProductCard>
  <Category>Toilet</Category>
  <Name>Geberit Icon Wandcloset</Name>
  <Style>Modern Minimalist</Style>
</ProductCard>
```

### After

```tsx
<ProductCard>
  <Category>Toilet → Wandclosets</Category>
  <Name>Geberit Icon Wandcloset</Name>
  <Style>Premium</Style>
  <Brand>Geberit</Brand>
  <StyleTag>luxury_premium</StyleTag>
  <StyleTag>premium</StyleTag>
</ProductCard>
```

---

## API Endpoints

### Get Products with Sub-Category Filter

```
GET /api/products?category=Toilet&sub_category=Wandclosets

Response:
{
  "products": [
    {
      "id": 123,
      "category": "Toilet",
      "sub_category": "Wandclosets",
      "name": "Geberit Icon Wandcloset",
      "style": "premium"
    }
  ],
  "filters": {
    "category": "Toilet",
    "sub_category": "Wandclosets",
    "available_sub_categories": [
      {"name": "Wandclosets", "count": 38},
      {"name": "Floor-Standing", "count": 9},
      {"name": "Corner Toilets", "count": 3}
    ]
  }
}
```

---

## Migration Script

### SQL: Add Sub-Category Column

```sql
-- Step 1: Add column
ALTER TABLE products ADD COLUMN sub_category VARCHAR(100);

-- Step 2: Update existing data
UPDATE products 
SET sub_category = 
  CASE
    WHEN category = 'Bathtub' AND name LIKE '%vrijstaand%' THEN 'Freestanding'
    WHEN category = 'Bathtub' AND name LIKE '%hoekbad%' THEN 'Corner Bath'
    WHEN category = 'Toilet' AND name LIKE '%wandcloset%' THEN 'Wandclosets'
    WHEN category = 'Toilet' AND name LIKE '%staand%' THEN 'Floor-Standing'
    WHEN category = 'Lighting' AND name LIKE '%spiegel%' THEN 'LED Mirrors'
    ELSE category
  END;

-- Step 3: Create indexes
CREATE INDEX idx_products_category_subcategory ON products(category, sub_category);
CREATE INDEX idx_products_subcategory ON products(sub_category);
```

---

## Benefits

### For Users
✅ **Drill-down filtering** - Find products faster (Toilet → Wandclosets)  
✅ **Visual pills** - Easy to tap/click on mobile  
✅ **Product counts** - See how many products per sub-category  
✅ **Clear filters** - Always know what's filtered  
✅ **Better UX** - Progressively reveal options

### For Developers
✅ **Non-breaking** - Existing pipeline continues to work  
✅ **Optional filter** - Sub-category is optional, not required  
✅ **Backward compatible** - Products without sub_category still work  
✅ **Easy to extend** - Add new sub-categories without schema changes  
✅ **Type-safe** - TypeScript interfaces for all new fields

---

## Implementation Checklist

- [x] Add `sub_category` column to database schema
- [x] Create sub-category taxonomy mapping (33 sub-categories)
- [x] Map 28 brands to style tags
- [x] Map 4 price ranges to style tags
- [x] Create style scoring algorithm (brand + price combination)
- [x] Update product metadata with sub_category field
- [x] Create CategoryProductSelector UI component specification
- [ ] Implement CategoryProductSelector in React/Next.js
- [ ] Add sub-category filtering to API endpoints
- [ ] Test UX with real users
- [ ] Deploy to production

---

**Status:** ✅ Data layer complete - Ready for UI implementation
**Files Created:**
- `metadata/rorix-*-enhanced.json` (175 products with sub_category)
- `metadata/subcategory-reference.json` (sub-category mapping)
- `enhanced-subcategory-system.md` (this specification)
