<?php
/**
 * Plugin Name: Hobbysalon Performance Optimizer
 * Plugin URI: https://www.hobbysalon.be
 * Description: Advanced performance optimizations for hobbysalon.be following WordPress coding standards
 * Version: 1.0.0
 * Author: Carlottta
 * Author URI: https://openclaw.ai
 * License: GPL v2 or later
 * Text Domain: hobbysalon-perf
 * Domain Path: /languages
 *
 * @package Hobbysalon_Performance
 */

// Exit if accessed directly
defined('ABSPATH') || exit;

/**
 * Main plugin class
 *
 * @class Hobbysalon_Performance_Optimizer
 */
class Hobbysalon_Performance_Optimizer {

	/**
	 * Plugin version
	 *
	 * @var string
	 */
	const VERSION = '1.0.0';

	/**
	 * Singleton instance
	 *
	 * @var Hobbysalon_Performance_Optimizer|null
	 */
	private static $instance = null;

	/**
	 * Get singleton instance
	 *
	 * @return Hobbysalon_Performance_Optimizer
	 */
	public static function get_instance() {
		if (null === self::$instance) {
			self::$instance = new self();
		}
		return self::$instance;
	}

	/**
	 * Constructor
	 */
	private function __construct() {
		// Defer non-critical JavaScript
		add_filter('script_loader_tag', [$this, 'defer_non_critical_scripts'], 10, 3);

		// Remove emoji scripts (performance optimization)
		remove_action('wp_head', 'print_emoji_detection_script', 7);
		remove_action('wp_print_styles', 'print_emoji_styles');
		remove_action('admin_print_scripts', 'print_emoji_detection_script');
		remove_action('admin_print_styles', 'print_emoji_styles');

		// Add preconnect headers for external resources
		add_action('wp_head', [$this, 'add_preconnect_headers'], 1);

		// Clean up WordPress head
		add_action('init', [$this, 'cleanup_head']);

		// Optimize database queries
		add_action('wp_loaded', [$this, 'optimize_database_queries']);

		// Add lazy loading to images
		add_filter('wp_get_attachment_image_attributes', [$this, 'add_lazy_loading'], 10, 3);

		// Optimize menu queries
		add_filter('wp_nav_menu_args', [$this, 'optimize_nav_menus']);

		// Add version removal for static assets
		add_filter('style_loader_src', [$this, 'remove_asset_version'], 9999);
		add_filter('script_loader_src', [$this, 'remove_asset_version'], 9999);

		// Defer jQuery for logged-out users
		add_action('wp_enqueue_scripts', [$this, 'optimize_jquery_loading'], 100);

		// Remove unnecessary CSS on frontend
		add_action('wp_enqueue_scripts', [$this, 'dequeue_unnecessary_styles'], 100);

		// Add performance monitoring widget
		add_action('wp_dashboard_setup', [$this, 'add_performance_dashboard_widget']);

		// Disable heartbeat except where needed
		add_action('init', [$this, 'optimize_heartbeat']);

		// Add cache headers for static assets
		add_action('template_redirect', [$this, 'add_static_asset_cache_headers']);
	}

	/**
	 * Defer non-critical JavaScript loading
	 *
	 * @param string $tag    The script tag.
	 * @param string $handle The script handle.
	 * @param string $src    The script source URL.
	 * @return string Modified script tag
	 */
	public function defer_non_critical_scripts($tag, $handle, $src) {
		// Scripts to defer (non-critical for render)
		$defer_scripts = [
			'jquery-core',
			'jquery-migrate',
			'wp-embed',
			'elementor-frontend-modules',
			'elementor-pro-frontend',
			'dokan',
		];

		// Scripts to load async (analytics, tracking)
		$async_scripts = [
			'google-analytics',
			'gtag',
			'analytics',
			'facebook-pixel',
		];

		// Defer non-critical scripts
		foreach ($defer_scripts as $defer_handle) {
			if (strpos($handle, $defer_handle) !== false) {
				return str_replace(' src', ' defer src', $tag);
			}
		}

		// Async tracking scripts
		foreach ($async_scripts as $async_handle) {
			if (strpos($handle, $async_handle) !== false) {
				return str_replace(' src', ' async src', $tag);
			}
		}

		return $tag;
	}

	/**
	 * Add preconnect headers for external resources
	 *
	 * Preconnect to external domains to speed up connections
	 */
	public function add_preconnect_headers() {
		echo '<!-- Performance: Preconnect headers -->' . "\n";
		echo '<link rel="preconnect" href="https://www.google.com">' . "\n";
		echo '<link rel="preconnect" href="https://www.gstatic.com" crossorigin>' . "\n";
		echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
		echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
		echo '<link rel="preconnect" href="https://www.googletagmanager.com">' . "\n";
		echo '<link rel="dns-prefetch" href="https://www.google-analytics.com">' . "\n";
		echo '<link rel="dns-prefetch" href="https://stats.g.doubleclick.net">' . "\n";
	}

	/**
	 * Clean up WordPress head
	 *
	 * Remove unnecessary bloat from wp_head()
	 */
	public function cleanup_head() {
		// Remove RSS feeds (if not needed)
		remove_action('wp_head', 'feed_links', 2);
		remove_action('wp_head', 'feed_links_extra', 3);

		// Remove RSD and WLW manifest
		remove_action('wp_head', 'rsd_link');
		remove_action('wp_head', 'wlwmanifest_link');

		// Remove shortlink
		remove_action('wp_head', 'wp_shortlink_wp_head', 10, 0);

		// Remove WordPress version
		remove_action('wp_head', 'wp_generator');

		// Remove REST API link (if not using)
		remove_action('wp_head', 'rest_output_link_wp_head', 10);
		remove_action('wp_head', 'wp_oembed_add_discovery_links');

		// Remove oEmbed discovery links
		remove_action('wp_head', 'wp_oembed_add_discovery_links');
		remove_action('wp_head', 'wp_oembed_add_host_js');
	}

	/**
	 * Remove version numbers from static assets for better caching
	 *
	 * @param string $src Asset source URL.
	 * @return string Modified source URL
	 */
	public function remove_asset_version($src) {
		if (strpos($src, 'ver=')) {
			return remove_query_arg('ver', $src);
		}
		return $src;
	}

	/**
	 * Optimize database queries
	 *
	 * Disable term counting for large taxonomies on frontend
	 */
	public function optimize_database_queries() {
		if (!is_admin()) {
			// Disable term counting (can be expensive)
			wp_defer_term_counting(true);
			wp_defer_comment_counting(true);
		}
	}

	/**
	 * Add lazy loading to images
	 *
	 * @param array        $attr       Image attributes.
	 * @param WP_Post      $attachment Attachment post object.
	 * @param string|array $size       Image size.
	 * @return array Modified attributes
	 */
	public function add_lazy_loading($attr, $attachment, $size) {
		// Skip lazy loading for critical above-fold images
		if (is_front_page() && isset($attr['class'])) {
			if (strpos($attr['class'], 'hero') !== false ||
			    strpos($attr['class'], 'above-fold') !== false) {
				return $attr;
			}
		}

		// Add loading and decoding attributes
		$attr['loading'] = 'lazy';
		$attr['decoding'] = 'async';

		return $attr;
	}

	/**
	 * Optimize navigation menu queries
	 *
	 * @param array $args Nav menu arguments.
	 * @return array Modified arguments
	 */
	public function optimize_nav_menus($args) {
		// Don't fallback to default menu if not needed
		if (isset($args['theme_location']) && !has_nav_menu($args['theme_location'])) {
			$args['fallback_cb'] = false;
		}

		return $args;
	}

	/**
	 * Optimize jQuery loading for logged-out users
	 *
	 * Move jQuery to footer for non-admin pages
	 */
	public function optimize_jquery_loading() {
		if (!is_admin() && !is_user_logged_in()) {
			// Move jQuery to footer
			wp_scripts()->add_data('jquery', 'group', 1);
			wp_scripts()->add_data('jquery-core', 'group', 1);
			wp_scripts()->add_data('jquery-migrate', 'group', 1);
		}
	}

	/**
	 * Dequeue unnecessary styles on frontend
	 *
	 * Remove block library CSS if not using blocks
	 */
	public function dequeue_unnecessary_styles() {
		// Remove Gutenberg block library if not using blocks
		if (!is_singular() && !is_page()) {
			wp_dequeue_style('wp-block-library');
			wp_dequeue_style('wp-block-library-theme');
			wp_dequeue_style('global-styles');
		}
	}

	/**
	 * Optimize WordPress Heartbeat API
	 *
	 * Disable heartbeat except for post editing
	 */
	public function optimize_heartbeat() {
		wp_deregister_script('heartbeat');

		// Only enable in admin
		if (is_admin()) {
			wp_register_script('heartbeat', includes_url('/js/heartbeat.min.js'), [], false, true);
		}
	}

	/**
	 * Add cache headers for static assets
	 *
	 * Long caching for CSS/JS files
	 */
	public function add_static_asset_cache_headers() {
		if (!is_admin() && !is_user_logged_in()) {
			// Check if this is a static asset request
			$request_uri = isset($_SERVER['REQUEST_URI']) ? sanitize_text_field(wp_unslash($_SERVER['REQUEST_URI'])) : '';

			if (strpos($request_uri, '.css') !== false ||
			    strpos($request_uri, '.js') !== false) {
				// Cache for 1 year
				header('Cache-Control: public, max-age=31536000, immutable');
			}
		}
	}

	/**
	 * Add performance monitoring widget to dashboard
	 *
	 * Only visible to administrators
	 */
	public function add_performance_dashboard_widget() {
		if (current_user_can('manage_options')) {
			wp_add_dashboard_widget(
				'hobbysalon_performance_widget',
				esc_html__('🚀 Performance Stats', 'hobbysalon-perf'),
				[$this, 'render_performance_widget']
			);
		}
	}

	/**
	 * Render performance dashboard widget
	 *
	 * Display database and cache statistics
	 */
	public function render_performance_widget() {
		global $wpdb;

		// Get database size
		$db_size = $wpdb->get_var(
			"SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2)
			FROM information_schema.TABLES
			WHERE table_schema = DATABASE()"
		);

		// Get content statistics
		$post_count = wp_count_posts();
		$published = isset($post_count->publish) ? $post_count->publish : 0;
		$drafts = isset($post_count->draft) ? $post_count->draft : 0;

		// Get option and transient counts
		$option_count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->options}");
		$transient_count = $wpdb->get_var(
			"SELECT COUNT(*) FROM {$wpdb->options}
			WHERE option_name LIKE '_transient_%'"
		);

		// Calculate autoload options size
		$autoload_size = $wpdb->get_var(
			"SELECT ROUND(LENGTH(option_value) / 1024 / 1024, 2)
			FROM {$wpdb->options}
			WHERE autoload = 'yes'
			ORDER BY LENGTH(option_value) DESC
			LIMIT 100"
		);

		// Output widget content
		echo '<div class="hobbysalon-perf-widget" style="padding: 12px;">';

		// Database stats
		echo '<h4 style="margin: 0 0 10px;">📊 Database</h4>';
		echo '<p style="margin: 5px 0;"><strong>Database Size:</strong> ' . esc_html($db_size) . ' MB</p>';
		echo '<p style="margin: 5px 0;"><strong>Published Posts:</strong> ' . esc_html($published) . '</p>';
		echo '<p style="margin: 5px 0;"><strong>Drafts:</strong> ' . esc_html($drafts) . '</p>';
		echo '<p style="margin: 5px 0;"><strong>Options:</strong> ' . esc_html($option_count) . '</p>';
		echo '<p style="margin: 5px 0;"><strong>Transients:</strong> ' . esc_html($transient_count) . '</p>';
		echo '<p style="margin: 5px 0;"><strong>Autoload Size:</strong> ' . esc_html($autoload_size) . ' MB</p>';

		echo '<hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">';

		// Recommendations
		echo '<h4 style="margin: 0 0 10px;">💡 Recommendations</h4>';

		if ($transient_count > 100) {
			echo '<p style="margin: 5px 0; color: #d63638;">⚠️ <strong>Clean up expired transients</strong> (' . esc_html($transient_count) . ' found)</p>';
		}

		if ($db_size > 100) {
			echo '<p style="margin: 5px 0; color: #d63638;">⚠️ <strong>Database is large</strong> - Consider cleanup</p>';
		}

		if ($autoload_size > 1) {
			echo '<p style="margin: 5px 0; color: #d63638;">⚠️ <strong>Reduce autoload options</strong> (' . esc_html($autoload_size) . ' MB)</p>';
		}

		if ($transient_count <= 100 && $db_size <= 100 && $autoload_size <= 1) {
			echo '<p style="margin: 5px 0; color: #00a32a;">✅ <strong>All good!</strong> No urgent optimizations needed</p>';
		}

		echo '<hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">';

		// Quick actions
		echo '<h4 style="margin: 0 0 10px;">🔧 Quick Actions</h4>';
		echo '<p style="margin: 5px 0;"><a href="' . esc_url(admin_url('options-general.php?page=litespeed-cache')) . '">LiteSpeed Cache Settings</a></p>';
		echo '<p style="margin: 5px 0;"><a href="' . esc_url(admin_url('tools.php?page=database-tools')) . '">Database Tools</a></p>';

		echo '</div>';
	}
}

/**
 * Image optimization: Serve WebP with fallback
 *
 * Automatically serve WebP images if available and browser supports it
 *
 * @param array|false $image           Array of image data, or false if no image.
 * @param int         $attachment_id   Attachment ID.
 * @param string|array $size            Image size.
 * @return array|false Modified image array
 */
add_filter('wp_get_attachment_image_src', function($image, $attachment_id, $size) {
	if (!$image) {
		return $image;
	}

	// Check if WebP version exists
	$webp_url = preg_replace('/\.(jpe?g|png)$/i', '.webp', $image[0]);
	$webp_path = str_replace(
		wp_upload_dir()['baseurl'],
		wp_upload_dir()['basedir'],
		$webp_url
	);

	// Serve WebP if available and browser supports it
	if (file_exists($webp_path) && isset($_SERVER['HTTP_ACCEPT'])) {
		$http_accept = sanitize_text_field(wp_unslash($_SERVER['HTTP_ACCEPT']));
		if (strpos($http_accept, 'image/webp') !== false) {
			$image[0] = $webp_url;
		}
	}

	return $image;
}, 10, 3);

/**
 * Limit post revisions to prevent database bloat
 *
 * @param int $num Number of revisions to keep.
 * @param bool $post Whether to limit revisions for this post type.
 */
add_filter('wp_revisions_to_keep', function($num, $post) {
	// Keep only 3 revisions for all post types
	return 3;
}, 10, 2);

/**
 * Automatically empty trash after 7 days
 */
define('EMPTY_TRASH_DAYS', 7);

/**
 * Disable XML-RPC if not needed (security + performance)
 */
add_filter('xmlrpc_enabled', '__return_false');

/**
 * Hide login errors for security
 */
add_filter('login_errors', function() {
	return esc_html__('Invalid login credentials.', 'hobbysalon-perf');
});

/**
 * Disable unneeded REST API endpoints for logged-out users
 */
add_filter('rest_authentication_errors', function($result) {
	if (!is_user_logged_in() && !current_user_can('edit_posts')) {
		return new WP_Error('rest_disabled', esc_html__('REST API restricted.', 'hobbysalon-perf'), ['status' => 401]);
	}
	return $result;
});

// Initialize plugin
Hobbysalon_Performance_Optimizer::get_instance();

/**
 * Plugin activation hook
 */
register_activation_hook(__FILE__, function() {
	// Set default options
	add_option('hobbysalon_perf_version', Hobbysalon_Performance_Optimizer::VERSION);

	// Flush cache to ensure changes take effect
	if (function_exists('litespeed_purge_all')) {
		litespeed_purge_all();
	}
});

/**
 * Plugin deactivation hook
 */
register_deactivation_hook(__FILE__, function() {
	// Flush cache on deactivation
	if (function_exists('litespeed_purge_all')) {
		litespeed_purge_all();
	}
});
