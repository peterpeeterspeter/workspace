#!/bin/bash
# Hobbysalon.be Plugin Installation via FTP
# Author: Carlottta
# Date: 2026-02-16

# Note: This requires FTP credentials or direct file access
# Alternative: Copy-paste into functions.php or use plugin installer

echo "=== Hobbysalon Performance Optimizer Installation ==="
echo ""
echo "This plugin needs to be installed manually via WordPress admin or FTP."
echo ""
echo "Method 1: WordPress Admin (Recommended)"
echo "1. Go to: https://www.hobbysalon.be/wp-admin/plugin-install.php"
echo "2. Click 'Upload Plugin'"
echo "3. Select: hobbysalon-performance-optimizer.zip"
echo "4. Click 'Install Now' and activate"
echo ""
echo "Method 2: FTP"
echo "1. Upload to: /wp-content/plugins/hobbysalon-performance-optimizer/"
echo "2. Activate in WordPress admin"
echo ""
echo "Method 3: functions.php (Quick test)"
echo "Copy the code to: /wp-content/themes/YOUR-THEME/functions.php"
echo ""
echo "Creating ZIP file..."

# Create plugin directory structure
mkdir -p /tmp/hobbysalon-performance-optimizer
cp /root/.openclaw/workspace/projects/hobbysalon/hobbysalon-performance-optimizer.php \
   /tmp/hobbysalon-performance-optimizer/

# Create readme
cat > /tmp/hobbysalon-performance-optimizer/readme.txt << 'EOF'
=== Hobbysalon Performance Optimizer ===
Contributors: carlottta
Tags: performance, speed, optimization, cache
Requires at least: 5.0
Tested up to: 6.7
Requires PHP: 7.4
Stable tag: 1.0.0

Custom performance optimizations for hobbysalon.be

== Installation ==

1. Upload the plugin files to /wp-content/plugins/hobbysalon-performance-optimizer/
2. Activate the plugin through the 'Plugins' screen in WordPress
3. Check performance in Dashboard > Performance Stats widget

== Features ==

* Defers non-critical JavaScript
* Removes emoji scripts
* Adds preconnect headers
* Optimizes database queries
* Lazy loads images
* Removes WordPress bloat
* Adds performance monitoring widget

== Changelog ==

= 1.0.0 =
* Initial release
EOF

# Create ZIP
cd /tmp
zip -r hobbysalon-performance-optimizer.zip hobbysalon-performance-optimizer/

echo ""
echo "✓ ZIP created: /tmp/hobbysalon-performance-optimizer.zip"
echo ""
echo "Download and install via WordPress admin:"
echo "https://www.hobbysalon.be/wp-admin/plugin-install.php?tab=upload"
