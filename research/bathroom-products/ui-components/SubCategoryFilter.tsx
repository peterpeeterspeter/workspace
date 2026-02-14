/**
 * Enhanced Sub-Category UI Components
 * For DeBadkamer.com CategoryProductSelector
 * 
 * Usage:
 * import { CategoryProductSelector, SubCategoryPills, StyleBadge } from './components/subcategories'
 */

import React from 'react';

// ============ SUB-CATEGORY PILLS ============
interface SubCategoryPillProps {
  subCategory: string;
  count: number;
  isActive: boolean;
  onClick: (subCategory: string) => void;
}

export const SubCategoryPill: React.FC<SubCategoryPillProps> = ({
  subCategory,
  count,
  isActive,
  onClick
}) => {
  return (
    <button
      className={`subcategory-pill ${isActive ? 'active' : ''}`}
      onClick={() => onClick(subCategory)}
    >
      <span className="subcategory-name">{subCategory}</span>
      <span className="subcategory-count">({count})</span>
    </button>
  );
};

// ============ SUB-CATEGORY LIST ============
interface SubCategoryListProps {
  mainCategory: string;
  subCategories: Array<{
    name: string;
    count: number;
  }>;
  activeSubCategory?: string;
  onSubCategoryChange: (subCategory: string | undefined) => void;
  onClear: () => void;
}

export const SubCategoryList: React.FC<SubCategoryListProps> = ({
  mainCategory,
  subCategories,
  activeSubCategory,
  onSubCategoryChange,
  onClear
}) => {
  return (
    <div className="subcategory-list">
      <div className="subcategory-list-header">
        <h3 className="subcategory-title">{mainCategory}</h3>
        <span className="subcategory-count">({subCategories.reduce((sum, sub) => sum + sub.count, 0)})</span>
        {activeSubCategory && (
          <button className="clear-filter-btn" onClick={onClear}>
            Clear
          </button>
        )}
      </div>
      <div className="subcategory-pills-container">
        {subCategories.map((sub) => (
          <SubCategoryPill
            key={sub.name}
            subCategory={sub.name}
            count={sub.count}
            isActive={activeSubCategory === sub.name}
            onClick={onSubCategoryChange}
          />
        ))}
      </div>
    </div>
  );
};

// ============ CATEGORY PRODUCT SELECTOR WITH SUB-CATEGORIES ============
interface CategoryProductSelectorEnhancedProps {
  category: string;
  onCategoryChange: (category: string) => void;
  onSubCategoryChange: (subCategory: string | undefined) => void;
  products: Array<{
    id: number;
    category: string;
    sub_category?: string;
    name: string;
    brand: string;
    price: number;
    style_enhanced: string;
  }>;
  activeSubCategory?: string;
  className?: string;
}

const SUBCATEGORY_LABELS: Record<string, string> = {
  Freestanding: 'Vrijstaand',
  'Back-to-Wall': 'Back-to-Wall',
  'Corner Bath': 'Hoekbad',
  'Drop-In': 'Inbouw',
  Whirlpool: 'Whirlpool',
  'Air Bath': 'Luchtbad',
  'Waste Drains': 'Afvoeren',
  Overflows: 'Overlopen',
  'Toilet Seats': 'Toiletzittingen',
  'Wandclosets': 'Wandclosets',
  'Back-to-Wall': 'Hoekcloset',
  'Floor-Standing': 'Staand',
  'Corner Toilets': 'Hoektoilet',
  'LED Mirrors': 'LED Spiegels',
  'Mirror Cabinets': 'Spiegelkasten',
  'Wall Lights': 'Wandlampen',
  'Ceiling Lights': 'Plafonlampen',
  'Ceramic Tiles': 'Keramische Tegels',
  'Metro Tiles': 'Metro Tegels',
  'Natural Stone': 'Natuursteen',
  'Mosaic Tiles': 'Mozaïek Tegels',
  'Basin Cabinets': 'Wastafmeubels',
  'Floating Vanity': 'Hangend Wastafmeubel',
  'Floor-Standing Vanity': 'Staand Wastafmeubel',
  'Double Vanity': 'Dubbel Wastafmeubel'
};

export const CategoryProductSelectorEnhanced: React.FC<CategoryProductSelectorEnhancedProps> = ({
  category,
  onCategoryChange,
  onSubCategoryChange,
  products,
  activeSubCategory,
  className = ''
}) => {
  // Get products for selected category
  const categoryProducts = products.filter(p => p.category.toLowerCase() === category.toLowerCase());
  
  // Extract unique sub-categories
  const subCategoryMap = new Map<string, number>();
  categoryProducts.forEach(product => {
    if (product.sub_category) {
      subCategoryMap.set(product.sub_category, (subCategoryMap.get(product.sub_category) || 0) + 1);
    }
  });
  
  // Convert to array and sort by count
  const subCategories = Array.from(subCategoryMap.entries())
    .map(([name, count]) => ({ name: name, count }))
    .sort((a, b) => b.count - a.count);
  
  const hasActiveSubCategory = activeSubCategory && activeSubCategory !== '';
  
  const handleSubCategoryChange = (subCategory: string | undefined) => {
    onSubCategoryChange(subCategory);
  };
  
  const handleClear = () => {
    onSubCategoryChange(undefined);
  };

  return (
    <div className={`category-selector-enhanced ${className}`}>
      {/* Main Category Dropdown */}
      <div className="category-dropdown-container">
        <label className="category-label">Categorie:</label>
        <select
          className="category-select"
          value={category}
          onChange={(e) => onCategoryChange(e.target.value)}
        >
          <option value="">Alle Categorieën</option>
          <option value="Bathtub">Badkuipen</option>
          <option value="Faucet">Kranen & Afvoer</option>
          <option value="Toilet">Toiletten</option>
          <option value="Lighting">Verlichting</option>
          <option value="Tile">Tegels</option>
          <option value="Vanity">Wastafmeubels</option>
        </select>
        </div>
      
      {/* Sub-Category Pills (only show when category selected) */}
      {category && subCategories.length > 0 && (
        <div className="subcategory-filter-container">
          <h4 className="subcategory-filter-title">
            Filter per type: {category}
          </h4>
          <div className="subcategory-pills-wrapper">
            {subCategories.map((sub) => (
              <SubCategoryPill
                key={sub.name}
                subCategory={sub.name}
                count={sub.count}
                isActive={activeSubCategory === sub.name}
                onClick={handleSubCategoryChange}
              />
            ))}
          </div>
          
          {/* Clear Filter Button */}
          {hasActiveSubCategory && (
            <button className="clear-subcategory-btn" onClick={handleClear}>
              <span className="clear-icon">×</span> Verwijder filter
            </button>
          )}
        </div>
      )}
      
      {/* Active Filter Display */}
      {hasActiveSubCategory && (
        <div className="active-filter-display">
          <span className="active-filter-label">Actief filter:</span>
          <span className="active-filter-name">
            {category} → {activeSubCategory}
          </span>
        </div>
      )}
    </div>
  );
};

// ============ CSS MODULE ============
export const CATEGORY_SELECTOR_ENHANCED_CSS = `
.category-selector-enhanced {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-dropdown-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
  margin-bottom: 0.25rem;
}

.category-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.category-select:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.subcategory-filter-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.subcategory-filter-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
  padding-bottom: 0.5rem;
}

.subcategory-pills-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.subcategory-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 9999px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.subcategory-pill:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}

.subcategory-pill.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.subcategory-name {
  font-weight: 500;
}

.subcategory-count {
  font-size: 0.75rem;
  opacity: 0.75;
  margin-left: 0.25rem;
}

.subcategory-pill:hover .subcategory-count,
.subcategory-pill.active .subcategory-count {
  opacity: 1;
}

.clear-subcategory-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #fee2e2;
  color: #991b1b;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-start;
}

.clear-subcategory-btn:hover {
  background: #fecaca;
  color: #b91c1c;
}

.clear-icon {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1;
}

.active-filter-display {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #eff6ff;
  color: #1e40af;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.5rem;
  align-self: flex-start;
}

.active-filter-label {
  font-weight: 600;
  margin-right: 0.25rem;
}

.active-filter-name {
  font-weight: 500;
}

/* Mobile Responsive */
@media (max-width: 640px) {
  .subcategory-pills-wrapper {
    gap: 0.375rem;
  }
  
  .subcategory-pill {
    font-size: 0.8125rem;
    padding: 0.375rem 0.75rem;
  }
  
  .subcategory-count {
    font-size: 0.6875rem;
  }
}
`;
