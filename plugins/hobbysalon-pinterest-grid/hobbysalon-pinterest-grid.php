<?php
/**
 * Plugin Name: Hobbysalon Pinterest Grid
 * Plugin URI: https://hobbysalon.be
 * Description: Pinterest-style masonry grid layout for hobbysalon.be blog posts
 * Version: 1.0.0
 * Author: Carlottta
 * License: GPL v2 or later
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

class Hobbysalon_Pinterest_Grid {

    private static $instance = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_head', array($this, 'custom_css'));
        add_filter('body_class', array($this, 'add_body_class'));
        add_shortcode('pinterest_grid', array($this, 'pinterest_grid_shortcode'));
    }

    public function enqueue_scripts() {
        // Only load on blog pages
        if (is_home() || is_archive() || is_front_page()) {
            // Masonry.js from WordPress core
            wp_enqueue_script('jquery-masonry');
            
            // Custom script
            wp_enqueue_script(
                'hobbysalon-pinterest-js',
                plugin_dir_url(__FILE__) . 'pinterest-grid.js',
                array('jquery-masonry'),
                '1.0.0',
                true
            );
            
            // Custom styles
            wp_enqueue_style(
                'hobbysalon-pinterest-css',
                plugin_dir_url(__FILE__) . 'pinterest-grid.css',
                array(),
                '1.0.0'
            );
        }
    }

    public function add_body_class($classes) {
        if (is_home() || is_archive()) {
            $classes[] = 'pinterest-grid-layout';
        }
        return $classes;
    }

    public function custom_css() {
        ?>
        <style id="hobbysalon-pinterest-inline-css">
            /* Pinterest Grid - Inline Customizations */
            :root {
                --pinterest-card-radius: 16px;
                --pinterest-card-shadow: 0 4px 12px rgba(0,0,0,0.08);
                --pinterest-card-shadow-hover: 0 8px 24px rgba(0,0,0,0.15);
                --pinterest-gap: 24px;
                --pinterest-overlay-bg: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%);
            }

            .pinterest-grid-layout .site-main {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
            }

            /* Adjust based on screen size */
            @media (max-width: 768px) {
                .pinterest-grid-layout .site-main {
                    padding: 0 15px;
                }
                :root {
                    --pinterest-gap: 16px;
                }
            }
        </style>
        <?php
    }

    public function pinterest_grid_shortcode($atts) {
        $atts = shortcode_atts(array(
            'posts_per_page' => 12,
            'columns' => 4,
            'category' => '',
        ), $atts);

        $args = array(
            'post_type' => 'post',
            'posts_per_page' => $atts['posts_per_page'],
            'post_status' => 'publish',
        );

        if (!empty($atts['category'])) {
            $args['category_name'] = $atts['category'];
        }

        $query = new WP_Query($args);

        if (!$query->have_posts()) {
            return '<p>No posts found.</p>';
        }

        ob_start();
        ?>
        <div class="pinterest-grid-shortcode" data-columns="<?php echo esc_attr($atts['columns']); ?>">
            <?php
            while ($query->have_posts()) {
                $query->the_post();
                $this->render_pinterest_card();
            }
            wp_reset_postdata();
            ?>
        </div>
        <?php
        return ob_get_clean();
    }

    private function render_pinterest_card() {
        $post_id = get_the_ID();
        $thumbnail = get_the_post_thumbnail_url($post_id, 'large');
        $title = get_the_title();
        $excerpt = get_the_excerpt();
        $permalink = get_permalink();
        $categories = get_the_category();
        $date = get_the_date();
        $author = get_the_author();
        
        // Fallback image if no thumbnail
        if (!$thumbnail) {
            $thumbnail = 'https://via.placeholder.com/600x800/1a1a1a/ffffff?text=No+Image';
        }
        ?>
        <article class="pinterest-card" data-id="<?php echo esc_attr($post_id); ?>">
            <div class="pinterest-card__inner">
                <a href="<?php echo esc_url($permalink); ?>" class="pinterest-card__link">
                    <div class="pinterest-card__image">
                        <img src="<?php echo esc_url($thumbnail); ?>" 
                             alt="<?php echo esc_attr($title); ?>"
                             loading="lazy"
                             onerror="this.src='https://via.placeholder.com/600x800/1a1a1a/ffffff?text=No+Image'">
                        <div class="pinterest-card__overlay">
                            <div class="pinterest-card__overlay-content">
                                <span class="pinterest-card__view">View Project</span>
                            </div>
                        </div>
                    </div>
                    <div class="pinterest-card__content">
                        <?php if (!empty($categories)): ?>
                        <div class="pinterest-card__categories">
                            <?php foreach (array_slice($categories, 0, 2) as $category): ?>
                                <span class="pinterest-card__category"><?php echo esc_html($category->name); ?></span>
                            <?php endforeach; ?>
                        </div>
                        <?php endif; ?>
                        
                        <h2 class="pinterest-card__title"><?php echo esc_html($title); ?></h2>
                        
                        <p class="pinterest-card__excerpt"><?php echo esc_html(wp_trim_words($excerpt, 15)); ?></p>
                        
                        <div class="pinterest-card__meta">
                            <span class="pinterest-card__author">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                                </svg>
                                <?php echo esc_html($author); ?>
                            </span>
                            <span class="pinterest-card__date"><?php echo esc_html($date); ?></span>
                        </div>
                    </div>
                </a>
                
                <div class="pinterest-card__actions">
                    <button class="pinterest-card__save" data-post-id="<?php echo esc_attr($post_id); ?>">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </article>
        <?php
    }
}

// Initialize the plugin
function hobbysalon_pinterest_grid_init() {
    return Hobbysalon_Pinterest_Grid::get_instance();
}
add_action('plugins_loaded', 'hobbysalon_pinterest_grid_init');

// Activation hook
register_activation_hook(__FILE__, 'hobbysalon_pinterest_grid_activate');
function hobbysalon_pinterest_grid_activate() {
    // Set default options
    add_option('hobbysalon_pinterest_grid_enabled', true);
}

// Deactivation hook
register_deactivation_hook(__FILE__, 'hobbysalon_pinterest_grid_deactivate');
function hobbysalon_pinterest_grid_deactivate() {
    // Clean up if needed
}
