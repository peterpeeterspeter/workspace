# Flooring Configurator Setup Guide

Complete guide for setting up and extending the Flooring Configurator in Studio Configurator.

## 📁 Directory Structure

```
studio-configurator/
├── public/
│   ├── index.html                    # Main entry point (product gallery)
│   ├── products.json                 # Product registry and metadata
│   └── products/
│       ├── flooring/                 # Flooring Configurator
│       │   ├── config.json          # Product configuration
│       │   ├── README.md            # Product documentation
│       │   ├── thumbnail.jpg        # Product thumbnail (to be added)
│       │   └── scenes/              # Room scene assets
│       │       ├── README.md        # Scene asset guide
│       │       ├── living-room.jpg
│       │       ├── living-room-floor-mask.png
│       │       ├── living-room-thumb.jpg
│       │       ├── bedroom.jpg
│       │       ├── bedroom-floor-mask.png
│       │       ├── bedroom-thumb.jpg
│       │       ├── kitchen.jpg
│       │       ├── kitchen-floor-mask.png
│       │       ├── kitchen-thumb.jpg
│       │       ├── hallway.jpg
│       │       ├── hallway-floor-mask.png
│       │       ├── hallway-thumb.jpg
│       │       ├── bathroom.jpg
│       │       ├── bathroom-floor-mask.png
│       │       ├── bathroom-thumb.jpg
│       │       ├── office.jpg
│       │       ├── office-floor-mask.png
│       │       └── office-thumb.jpg
│       └── tiling/                   # Wall Tiling Configurator (reference)
│           └── config.json
└── FLOORING_SETUP.md                 # This file
```

## 🚀 Quick Start

### 1. Verify Installation

All files have been created successfully:

```bash
cd /root/.openclaw/workspace/projects/photostudio-io/app/studio-configurator

# Check structure
ls -la public/products/flooring/
ls -la public/products/flooring/scenes/

# Verify configuration
cat public/products/flooring/config.json | jq '.name, .title, .options.style.enum'
```

### 2. Add Room Scene Assets

Before the configurator is fully functional, you need to add room scene images. See `public/products/flooring/scenes/README.md` for detailed requirements.

**Minimal setup for testing:**
```bash
cd public/products/flooring/scenes

# Add placeholder images (600x400 for base, 400x300 for thumbnails)
# You can use stock photos from Unsplash or Pexels for testing
```

### 3. Test the Configurator

Open `index.html` in a browser:
- View the product gallery
- Click on "Flooring Configurator" to see the launch alert
- Check browser console for loaded products data

## 📊 Configuration Overview

### Product Metadata (`config.json`)

```json
{
  "name": "flooring",              // Internal product ID
  "title": "Flooring Configurator", // Display name
  "category": "flooring",           // Product category
  "sizing": { ... },                // Dimension constraints
  "options": { ... },               // User-configurable options
  "roomScenes": { ... },            // Available room types
  "visualization": { ... },         // Render settings
  "pricing": { ... }                // Price calculation rules
}
```

### Sizing Configuration

Controls room dimensions users can set:

```json
"sizing": {
  "width": {
    "min": 200,      // Minimum room width (cm)
    "max": 600,      // Maximum room width (cm)
    "step": 10,      // Increment step
    "label": "Room Width (cm)"
  },
  "height": {
    "min": 200,      // Minimum room depth (cm)
    "max": 600,      // Maximum room depth (cm)
    "step": 10       // Increment step
  }
}
```

### Style Options

13 floor styles across three categories:

**Wood Flooring:**
- Oak Natural, Oak White Oiled, Oak Smoked
- Walnut Natural, Ash Bleached

**Stone & Tile:**
- Marble Carrara, Marble Calacatta
- Terrazzo Grey, Terrazzo Multicolor
- Concrete Polished, Brick Herringbone
- Hexagon Marble

### Installation Patterns

Five layout patterns:
- **Straight Lay**: Standard parallel installation
- **Herringbone**: 90° zigzag pattern
- **Chevron**: 45° continuous V pattern
- **Basket Weave**: Square geometric pattern
- **Hexagon**: Hexagonal tile layout

### Room Scenes

Six pre-configured rooms with optimized recommendations:

| Scene | Style | Best For |
|-------|-------|----------|
| Living Room | General living | Oak, Walnut |
| Bedroom | Warm, cozy | Light woods |
| Kitchen | Clean, bright | Tile, stone |
| Hallway | High-traffic | Durable materials |
| Bathroom | Waterproof | Marble, tile |
| Home Office | Professional | Wood, concrete |

## 💰 Pricing Structure

Base price + style modifier + finish modifier:

```
Total Price/sqm = Base (€45) + Style (€0-120) + Finish (€0-12)
```

**Examples:**
- Oak Natural, Matt: €45/sqm
- Oak White Oiled, Naturally Oiled: €63/sqm
- Marble Calacatta, High Gloss: €177/sqm

## 🎨 Customization Guide

### Adding a New Floor Style

1. Edit `config.json`:
```json
"options": {
  "style": {
    "enum": [
      "oak-natural",
      "oak-white-oiled",
      "your-new-style"  // Add internal ID
    ],
    "enumNames": [
      "Oak Natural",
      "Oak White Oiled",
      "Your New Style"  // Add display name
    ]
  }
}

"pricing": {
  "stylePriceModifier": {
    "your-new-style": 75  // Set price
  }
}
```

2. Add style rendering logic (in the app code)

### Adding a New Room Scene

1. Create three image files in `scenes/`:
   - `{room-name}.jpg` (base photo)
   - `{room-name}-floor-mask.png` (floor area mask)
   - `{room-name}-thumb.jpg` (thumbnail)

2. Add to `config.json`:
```json
"roomScenes": {
  "your-new-room": {
    "title": "Your New Room",
    "thumbnail": "scenes/your-new-room-thumb.jpg",
    "baseImage": "scenes/your-new-room.jpg",
    "floorMask": "scenes/your-new-room-floor-mask.png",
    "defaultPerspective": "perspective",
    "lighting": "warm",
    "wallColor": "#F5F5DC",
    "recommendedStyles": ["oak-natural", "walnut-natural"]
  }
}
```

### Adding a New Pattern

1. Add to pattern enum:
```json
"options": {
  "pattern": {
    "enum": ["straight", "herringbone", "your-pattern"],
    "enumNames": ["Straight Lay", "Herringbone", "Your Pattern"]
  }
}
```

2. Implement pattern rendering logic

### Adjusting Sizing Constraints

Modify `sizing` section in `config.json`:

```json
"sizing": {
  "width": {
    "min": 150,    // Change minimum
    "max": 800,    // Change maximum
    "step": 5      // Change increment
  }
}
```

## 🔧 Integration with Application

### Loading Product Config

```javascript
// Fetch product configuration
async function loadProduct(productId) {
  const response = await fetch(`products/${productId}/config.json`);
  const config = await response.json();
  return config;
}

// Usage
const flooringConfig = await loadProduct('flooring');
console.log(flooringConfig.options.style.enum);
```

### Listing Available Products

```javascript
// Fetch product registry
async function getProducts() {
  const response = await fetch('products.json');
  const data = await response.json();
  return data.products.filter(p => p.enabled);
}

// Usage
const products = await getProducts();
// Returns: [{ id: 'flooring', ... }, { id: 'tiling', ... }]
```

### Calculating Price

```javascript
function calculatePrice(config, selections) {
  const basePrice = config.pricing.basePrice;
  const stylePrice = config.pricing.stylePriceModifier[selections.style] || 0;
  const finishPrice = config.pricing.finishPriceModifier[selections.finish] || 0;

  const pricePerSqm = basePrice + stylePrice + finishPrice;
  const area = (selections.width * selections.height) / 10000; // cm² to m²
  const totalPrice = pricePerSqm * area;

  return {
    pricePerSqm,
    area,
    totalPrice
  };
}
```

## 📝 Asset Requirements

### Room Scene Images

**Base Photo:**
- Resolution: 1920x1080px minimum
- Format: JPEG (quality 85-95)
- Color space: sRGB
- Well-lit, professional photography
- Clear floor area visible

**Floor Mask:**
- Resolution: Same as base photo
- Format: PNG with transparency
- White/visible: Floor area
- Black/transparent: Walls, furniture
- Precise edges along walls

**Thumbnail:**
- Resolution: 400x300px
- Format: JPEG
- Representative room view
- Clear scene type identification

### Creating Floor Masks

**Option 1: Photoshop/GIMP**
1. Open base image
2. Create new layer
3. Pen tool to outline floor
4. Fill floor with white
5. Invert and fill rest with black
6. Save as PNG

**Option 2: AI Tools**
- Remove.bg
- Clipdrop
- Photoshop AI Remove Background

**Option 3: 3D Renders**
- Render floor as separate pass
- Use material ID buffer
- Convert to mask

## 🚀 Next Steps

### Immediate (Required for Full Functionality)

1. **Add Room Scene Assets**
   - Create or source room photos
   - Generate floor masks
   - Create thumbnails
   - Place in `scenes/` directory

2. **Create Product Thumbnail**
   - Add `thumbnail.jpg` to flooring directory
   - Recommended: 400x300px

3. **Build Configurator UI**
   - Create React/Vue component for product interface
   - Implement option selectors
   - Add live preview canvas
   - Integrate price calculator

### Enhancement Phase

1. **3D Visualization**
   - Three.js or Babylon.js for 3D room rendering
   - Realistic material textures
   - Dynamic lighting

2. **Additional Features**
   - Custom room image upload
   - Save/load configurations
   - Share configuration links
   - Export high-res renders
   - Sample ordering integration

3. **Performance**
   - Lazy loading for scenes
   - Web Workers for rendering
   - Progressive image loading
   - Caching strategies

## 🐛 Troubleshooting

### Config Not Loading

```javascript
// Check JSON syntax
cat public/products/flooring/config.json | jq .

// Verify file permissions
ls -la public/products/flooring/config.json

// Test in browser console
fetch('products/flooring/config.json')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

### Scenes Not Displaying

- Verify all three files exist per scene (base, mask, thumb)
- Check file formats (JPEG for photos, PNG for mask)
- Confirm mask has transparency
- Validate file paths in config.json

### Price Calculations Wrong

```javascript
// Test calculation
const config = /* loaded config */;
const selections = {
  style: 'oak-natural',
  finish: 'matt',
  width: 400,
  height: 400
};

console.log(calculatePrice(config, selections));
// Should output: { pricePerSqm: 45, area: 16, totalPrice: 720 }
```

## 📚 Reference

### File Locations

- **Product Config**: `public/products/flooring/config.json`
- **Product Registry**: `public/products.json`
- **Main Gallery**: `public/index.html`
- **Scene Guide**: `public/products/flooring/scenes/README.md`
- **Product Docs**: `public/products/flooring/README.md`

### Key Numbers

- **Room Size Range**: 200-600cm (2-6m)
- **Board Width**: 10-40cm
- **Board Length**: 60-200cm
- **Price Range**: €45-177/sqm
- **Number of Styles**: 13
- **Number of Patterns**: 5
- **Number of Rooms**: 6

---

**Status**: ✅ Structure complete, awaiting scene assets
**Version**: 1.0.0
**Last Updated**: February 3, 2026

For questions or support, refer to the individual README files in each directory.
