# Flooring Configurator

Visualize and customize flooring options for various room types.

## Features

- **13 Floor Styles**: Wood (oak, walnut, ash), stone (marble, terrazzo, concrete), and decorative options
- **5 Installation Patterns**: Straight lay, herringbone, chevron, basket weave, hexagon
- **6 Room Scenes**: Living room, bedroom, kitchen, hallway, bathroom, home office
- **Custom Sizing**: Adjustable room dimensions (200-600cm)
- **Board Configuration**: Width (10-40cm), length (60-200cm)
- **Border Options**: Add contrasting or matching borders (1-5 boards wide)
- **Surface Finishes**: Matt, silk matt, naturally oiled, high gloss
- **Surface Textures**: Smooth, brushed, handscraped, saw marked, planked

## Floor Styles

### Wood Flooring
- **Oak Natural** - Classic natural oak finish (base price)
- **Oak White Oiled** - Light, airy oak with white oil treatment (+€10/sqm)
- **Oak Smoked** - Dark, rich smoked oak (+€15/sqm)
- **Walnut Natural** - Premium walnut with deep tones (+€35/sqm)
- **Ash Bleached** - Light Scandinavian-style ash (+€5/sqm)

### Stone & Tile
- **Marble Carrara** - Classic Italian white marble (+€80/sqm)
- **Marble Calacatta** - Premium Calacatta with bold veining (+€120/sqm)
- **Terrazzo Grey** - Modern grey terrazzo (+€65/sqm)
- **Terrazzo Multicolor** - Colorful vintage terrazzo (+€85/sqm)
- **Concrete Polished** - Industrial polished concrete (+€40/sqm)
- **Brick Herringbone** - Traditional brick herringbone pattern (+€55/sqm)
- **Hexagon Marble** - Hexagonal marble tiles (+€95/sqm)

## Installation Patterns

1. **Straight Lay** - Classic parallel installation, most common
2. **Herringbone** - 90° angled zigzag pattern, traditional elegance
3. **Chevron** - 45° angled continuous V pattern, sophisticated
4. **Basket Weave** - Square basket weave pattern, geometric
5. **Hexagon** - Hexagonal tile layout, modern and unique

## Room Scenes

Each scene is optimized for specific flooring styles:

| Scene | Recommended Styles | Best For |
|-------|-------------------|----------|
| Living Room | Oak Natural, White Oiled, Walnut | General living spaces |
| Bedroom | Oak Natural, Ash Bleached, Smoked | Relaxing, warm spaces |
| Kitchen | White Oiled, Marble Carrara, Terrazzo | Clean, modern spaces |
| Hallway | Smoked Oak, Walnut, Brick Herringbone | High-traffic areas |
| Bathroom | Marble Carrara, Calacatta, Hexagon | Wet areas, luxury |
| Home Office | Oak Natural, Walnut, Concrete | Professional spaces |

## Pricing Structure

**Base Price**: €45/sqm

Additional costs:
- Style modifiers: €0-120/sqm
- Finish modifiers: €0-12/sqm
- Border work: Custom quote based on complexity

Example calculations:
- Oak Natural, Matt finish: €45/sqm
- Oak White Oiled, Naturally Oiled: €45 + €10 + €8 = €63/sqm
- Marble Calacatta, High Gloss: €45 + €120 + €12 = €177/sqm

## Configuration Options

### Sizing
- **Room Width**: 200-600cm (10cm steps)
- **Room Depth**: 200-600cm (10cm steps)

### Board Settings
- **Board Width**: 10-40cm (1cm steps)
- **Board Length**: 60-200cm (5cm steps)

### Visual Options
- **4 Grout Colors**: White, grey, black, beige
- **3 Orientations**: Horizontal, vertical, diagonal
- **4 Finishes**: Matt, silk matt, naturally oiled, high gloss
- **5 Surface Textures**: Smooth, brushed, handscraped, saw marked, planked

## Border Configuration

Add decorative borders with:
- Width: 1-5 boards
- Colors: Matching main floor, contrasting, or specific wood types
- Best for: Herringbone and straight lay patterns

## Rendering Quality

- **Anti-aliasing**: Enabled for smooth edges
- **Shadows**: Soft shadows at 30% intensity
- **Reflections**: Subtle reflections at 20% intensity
- **Lighting**: Adjustable ambient (60%) and directional (40%) at 45°

## File Structure

```
flooring/
├── config.json              # Product configuration
├── README.md               # This file
├── thumbnail.jpg           # Product thumbnail (to be added)
└── scenes/                 # Room scene images
    ├── living-room.jpg
    ├── living-room-floor-mask.png
    ├── living-room-thumb.jpg
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

## Usage

1. Select a room scene that matches your space
2. Choose your preferred floor style and pattern
3. Adjust board dimensions for realistic proportions
4. Customize grout color and surface finish
5. Add borders for decorative accent
6. Configure room dimensions to match your space
7. Generate high-quality renders for visualization

## Future Enhancements

- Custom image upload for room matching
- Additional wood species and finishes
- More pattern variations (diagonal herringbone, random width)
- Transition strips and threshold visualization
- In-floor heating compatibility indicators
- Installation cost estimator
- Material sample ordering integration

---

**Product Version**: 1.0.0
**Last Updated**: February 2026
