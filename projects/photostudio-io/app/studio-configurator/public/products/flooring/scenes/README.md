# Flooring Scene Assets

This directory contains room scene images for the flooring configurator.

## Required Assets

For each room scene, you need three images:

### 1. Base Image (Room Photo)
- **Filename**: `{room-name}.jpg`
- **Purpose**: High-quality photo of the room
- **Requirements**:
  - Resolution: 1920x1080px minimum
  - Well-lit, professional photography
  - Neutral floor area clearly visible
  - Camera angle: Eye-level or slightly elevated

### 2. Floor Mask (Alpha Layer)
- **Filename**: `{room-name}-floor-mask.png`
- **Purpose**: Defines where flooring should be rendered
- **Requirements**:
  - Same resolution as base image
  - PNG format with transparency
  - White/visible areas: floor area (flooring renders here)
  - Black/transparent areas: walls, furniture, objects
  - Precise edges along walls and fixtures

### 3. Thumbnail
- **Filename**: `{room-name}-thumb.jpg`
- **Purpose**: Preview image in scene selector
- **Requirements**:
  - Resolution: 400x300px
  - Shows representative view of the room
  - Clear, recognizable room type

## Room Scenes

### Living Room
- **Style**: Warm, inviting, general living space
- **Recommended**: Wood floors (oak, walnut)
- **Lighting**: Warm (2700K-3000K)
- **Wall Color**: Beige/Cream (#F5F5DC)

### Bedroom
- **Style**: Serene, relaxing, cozy
- **Recommended**: Light woods, carpet alternatives
- **Lighting**: Soft (2500K-2800K)
- **Wall Color**: Warm white/cream (#FFF8E7)

### Kitchen
- **Style**: Clean, modern, bright
- **Recommended**: Tile, stone, polished wood
- **Lighting**: Bright (3000K-4000K)
- **Wall Color**: Pure white (#FFFFFF)

### Hallway
- **Style**: Transitional, high-traffic
- **Recommended**: Durable wood, stone, brick
- **Lighting**: Neutral (3000K)
- **Wall Color**: Light grey (#E8E8E8)

### Bathroom
- **Style**: Clean, sanitary, spa-like
- **Recommended**: Waterproof materials (tile, stone)
- **Lighting**: Bright (3500K-4000K)
- **Wall Color**: White (#FFFFFF)

### Home Office
- **Style**: Professional, focused
- **Recommended**: Wood, concrete
- **Lighting**: Neutral (3000K-3500K)
- **Wall Color**: Light grey/white (#F0F0F0)

## Creating Floor Masks

### Option 1: Photoshop/GIMP
1. Open base image
2. Create new layer
3. Use pen tool or selection tools to outline floor area
4. Fill selection with white
5. Invert selection and fill with black
6. Save as PNG with transparency

### Option 2: AI Background Removal
1. Use tools like Remove.bg, Clipdrop, or Photoshop AI
2. Remove floor from image
3. Invert the result to get floor mask
4. Fine-tune edges manually

### Option 3: 3D Renders
If using 3D room renders:
1. Render floor material as separate pass
2. Use material ID or object buffer
3. Convert to mask format

## Image Specifications

### Technical Requirements
- **Color Space**: sRGB
- **Bit Depth**: 8-bit per channel
- **Compression**: JPEG (quality 85-95), PNG (lossless for masks)
- **File Size**: Base images < 2MB, thumbnails < 100KB

### Photography Guidelines
- Avoid wide-angle distortion
- Maintain consistent perspective across scenes
- Include natural depth of field
- Show realistic room proportions
- Include scale references (furniture, doors)

## Asset Naming Convention

```
scenes/
├── living-room.jpg              # Base photo
├── living-room-floor-mask.png   # Floor area mask
├── living-room-thumb.jpg        # Scene selector thumbnail
├── bedroom.jpg
├── bedroom-floor-mask.png
├── bedroom-thumb.jpg
├── kitchen.jpg
├── kitchen-floor-mask.png
├── kitchen-thumb.jpg
├── hallway.jpg
├── hallway-floor-mask.png
├── hallway-thumb.jpg
├── bathroom.jpg
├── bathroom-floor-mask.png
├── bathroom-thumb.jpg
├── office.jpg
├── office-floor-mask.png
└── office-thumb.jpg
```

## Placeholder Generation

Before real assets are available, use:
- Stock photos from Unsplash/Pexels for base images
- Simple gradient backgrounds for testing
- Procedurally generated masks for development

## Optimization Tips

1. **Batch Processing**: Process all scenes consistently
2. **Mask Quality**: Ensure masks align perfectly with base images
3. **Color Grading**: Match color temperature across scenes
4. **Resolution**: Use 2x resolution for retina displays
5. **Lazy Loading**: Implement loading states for large images

## Testing Checklist

- [ ] Mask aligns perfectly with base image
- [ ] Floor area is completely covered by mask
- [ ] No gaps or overlaps in mask edges
- [ ] Thumbnail represents scene accurately
- [ ] File sizes are optimized
- [ ] All scenes load without errors
- [ ] Consistent lighting and color temperature

---

**Note**: This is a temporary structure. Replace with actual room photography and professionally created masks for production use.
