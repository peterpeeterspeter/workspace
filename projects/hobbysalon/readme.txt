=== Hobbysalon Performance Optimizer ===
Contributors: carlottta
Tags: performance, speed, optimization, cache, lazy-loading, webp
Requires at least: 5.0
Tested up to: 6.7
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Advanced performance optimizations for hobbysalon.be following WordPress coding standards.

== Description ==

Custom performance optimization plugin built specifically for hobbysalon.be. Implements WordPress best practices for speed and efficiency.

== Features ==

* **Deferred JavaScript Loading** - Non-critical scripts load after page render
* **Lazy Loading Images** - Images load as you scroll, saving bandwidth
* **WebP Support** - Automatically serves WebP images when available
* **Preconnect Headers** - Speeds up connections to external resources
* **Database Optimization** - Reduces expensive queries on frontend
* **Asset Optimization** - Removes version strings, enables better caching
* **WordPress Head Cleanup** - Removes unnecessary bloat
* **Performance Dashboard** - Monitor site performance from WordPress admin
* **Cache Headers** - Long-term caching for static assets
* **Heartbeat Optimization** - Reduces server load from admin-ajax

== Installation ==

1. Upload the plugin files to `/wp-content/plugins/hobbysalon-performance-optimizer/`
2. Activate the plugin through the 'Plugins' screen in WordPress
3. Check the Performance Stats widget in your dashboard

== Configuration ==

No configuration needed! The plugin works automatically once activated.

To see performance stats:
1. Go to Dashboard
2. Look for the "🚀 Performance Stats" widget

== Frequently Asked Questions ==

= Will this conflict with LiteSpeed Cache? =

No, it's designed to work alongside LiteSpeed Cache and complement its features.

= Can I disable specific optimizations? =

Yes, you can comment out specific filters in the plugin file if needed.

= Does this work with page builders? =

Yes, tested with Elementor and Elementor Pro. Defers non-critical Elementor scripts.

= Is this safe for production? =

Yes. Follows WordPress coding standards, uses proper sanitization, and includes safety checks.

== Changelog ==

= 1.0.0 =
* Initial release
* Deferred JavaScript loading
* Lazy loading for images
* WebP image support
* Database query optimization
* Performance dashboard widget
* WordPress head cleanup
* Preconnect headers
* Asset version removal

== Upgrade Notice ==

= 1.0.0 =
Initial release. Install and activate for instant performance improvements.

== Screenshots ==

1. Dashboard widget showing performance statistics
2. Network tab showing deferred JavaScript loading
3. Lighthouse score improvements

== Credits ==

Developed by Carlottta (OpenClaw AI)
Based on WordPress performance best practices

== License ==

GPLv2 or later

== Plugin URI ==

https://www.hobbysalon.be
