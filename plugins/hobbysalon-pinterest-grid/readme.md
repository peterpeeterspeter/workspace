# Hobbysalon Pinterest Grid

A Pinterest-style masonry grid layout plugin for Hobbysalon.be - perfect for showcasing crafting projects, patterns, and DIY tutorials.

## Features

✨ **Pinterest-Style Layout**
- Responsive masonry grid (1-5 columns based on screen size)
- Smooth animations and hover effects
- Visual-heavy design optimized for crafting content

🎨 **Beautiful Card Design**
- Rounded corners with elegant shadows
- Image overlays with "View Project" call-to-action
- Category badges and metadata display
- Save/bookmark functionality for users

📱 **Fully Responsive**
- Desktop: 5 columns
- Laptop: 4 columns
- Tablet: 3 columns
- Mobile: 2 columns
- Small Mobile: 1 column

⚡ **Performance Optimized**
- Lazy loading images
- Smooth animations (60fps)
- Intersection Observer for scroll effects
- Optimized CSS and JavaScript

♿ **Accessible**
- Keyboard navigation support
- ARIA labels
- Reduced motion support
- Focus indicators

🌙 **Dark Mode Support**
- Automatic dark mode detection
- Optimized colors for low light

## Installation

### Method 1: WordPress Admin (Recommended)

1. Download `hobbysalon-pinterest-grid.zip`
2. Go to **WordPress Admin → Plugins → Add New**
3. Click **Upload Plugin**
4. Select the ZIP file and click **Install Now**
5. Activate the plugin

### Method 2: Manual FTP

1. Extract the ZIP file
2. Upload `hobbysalon-pinterest-grid` folder to `/wp-content/plugins/`
3. Go to **WordPress Admin → Plugins**
4. Find "Hobbysalon Pinterest Grid" and click **Activate**

## Usage

### Automatic Integration

Once activated, the plugin automatically applies the Pinterest grid layout to:
- Blog homepage (is_home)
- Category archives (is_archive)
- Front page (if showing posts)

### Shortcode Usage

You can also add a Pinterest grid anywhere using:

```
[pinterest_grid posts_per_page="12" columns="4" category="knitting"]
```

**Parameters:**
- `posts_per_page` - Number of posts to show (default: 12)
- `columns` - Number of columns 1-5 (default: responsive)
- `category` - Filter by category slug (optional)

**Examples:**

```
// Show 8 posts from crochet category
[pinterest_grid posts_per_page="8" category="crochet"]

// Show 16 posts in 3 columns
[pinterest_grid posts_per_page="16" columns="3"]

// Show all posts (no limit)
[pinterest_grid posts_per_page="-1"]
```

### Customization

#### Change Card Colors

Add to **WordPress Admin → Appearance → Customize → Additional CSS**:

```css
/* Primary color on hover */
.pinterest-card:hover .pinterest-card__title {
    color: #your-color;
}

/* Category badge color */
.pinterest-card__category {
    background: #your-color;
    color: #fff;
}

/* Save button color */
.pinterest-card__save.active {
    background: #your-color;
}
```

#### Adjust Spacing

```css
:root {
    --pinterest-gap: 32px; /* Increase spacing */
    --pinterest-card-radius: 20px; /* Rounder corners */
}
```

#### Hide Elements

```css
/* Hide author and date */
.pinterest-card__meta {
    display: none;
}

/* Hide save buttons */
.pinterest-card__save {
    display: none;
}

/* Hide category badges */
.pinterest-card__categories {
    display: none;
}
```

## Features Explained

### Save/Bookmark Functionality

Users can save posts to view later:
- Click the bookmark icon (top-right of card)
- Saved posts stored in browser localStorage
- Persists across sessions
- Optional backend integration for user accounts

### Hover Effects

- Image zooms slightly
- Overlay appears with "View Project" button
- Card lifts up with enhanced shadow
- Save button fades in

### Loading Animation

- Cards fade in sequentially
- Smooth upward movement
- Staggered delays for natural feel

## Performance

### Load Time Impact
- CSS: ~12KB (minified)
- JavaScript: ~8KB (minified)
- Uses WordPress core jQuery and Masonry
- No external dependencies

### Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

### Accessibility Score
- ARIA labels: ✅
- Keyboard navigation: ✅
- Screen reader friendly: ✅
- Focus indicators: ✅
- Reduced motion support: ✅

## Troubleshooting

### Grid Not Working

**Issue:** Posts appear in one column
**Solution:** 
- Clear browser cache
- Clear WordPress cache (LiteSpeed, etc.)
- Check for JavaScript errors in browser console

### Images Not Loading

**Issue:** Images show placeholder instead of actual images
**Solution:**
- Ensure posts have featured images set
- Check image file permissions
- Regenerate thumbnails if needed

### Masonry Layout Broken

**Issue:** Cards overlap or have gaps
**Solution:**
- Wait for images to fully load
- Check jQuery is loaded
- Disable other masonry plugins (conflict)

### Save Button Not Working

**Issue:** Clicking save does nothing
**Solution:**
- Check browser console for errors
- Ensure localStorage is enabled
- Clear browser cache

## Advanced Usage

### Custom Template Integration

To use in your theme template:

```php
<?php
echo do_shortcode('[pinterest_grid posts_per_page="12" category="knitting"]');
?>
```

### Programmatic Usage

```php
<?php
$grid = Hobbysalon_Pinterest_Grid::get_instance();
// Use the plugin methods
?>
```

### Filter Hooks

Available filters for customization:

```php
// Change card HTML
add_filter('hobbysalon_pinterest_card_html', function($html, $post_id) {
    // Modify $html
    return $html;
}, 10, 2);

// Change grid columns
add_filter('hobbysalon_pinterest_grid_columns', function($columns) {
    return 5; // Force 5 columns
});
```

## Changelog

### 1.0.0 (2026-02-16)
- Initial release
- Pinterest-style masonry layout
- Responsive design (1-5 columns)
- Save/bookmark functionality
- Shortcode support
- Dark mode support
- Accessibility features

## Support

For issues or questions:
- Website: https://hobbysalon.be
- Plugin folder: `/wp-content/plugins/hobbysalon-pinterest-grid/`

## Credits

- Developed by: Carlottta
- Inspired by: Pinterest grid layout
- Built for: Hobbysalon.be

## License

GPL v2 or later

---

**Enjoy your beautiful Pinterest-style grid! 🎨**
