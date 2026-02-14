<?php
/*
Plugin Name: Cardfair Credit Card Comparison
Description: Interactive credit card comparison tool with 338+ cards, filtering, and affiliate link support
Version: 1.0.0
Author: Cardfair
*/

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

class Cardfair_Credit_Card_Comparison {

    private static $instance = null;
    private $cards_data = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('cardfair_comparison', array($this, 'render_comparison_table'));
    }

    public function enqueue_scripts() {
        wp_enqueue_style(
            'cardfair-comparison-css',
            plugin_dir_url(__FILE__) . 'cardfair-comparison.css',
            array(),
            '1.0.0'
        );

        wp_enqueue_script(
            'cardfair-comparison-js',
            plugin_dir_url(__FILE__) . 'cardfair-comparison.js',
            array('jquery'),
            '1.0.0',
            true
        );

        wp_localize_script('cardfair-comparison-js', 'cardfairData', array(
            'cards' => $this->get_cards_data(),
            'ajaxUrl' => admin_url('admin-ajax.php')
        ));
    }

    private function get_cards_data() {
        if (null !== $this->cards_data) {
            return $this->cards_data;
        }

        // Load JSON data
        $json_file = plugin_dir_path(__FILE__) . 'credit-cards.json';

        if (!file_exists($json_file)) {
            return array();
        }

        $json_data = file_get_contents($json_file);
        $data = json_decode($json_data, true);

        if (isset($data[0]['credit_cards'])) {
            $this->cards_data = $data[0]['credit_cards'];
        } else {
            $this->cards_data = array();
        }

        return $this->cards_data;
    }

    public function render_comparison_table($atts) {
        $atts = shortcode_atts(array(
            'type' => 'all', // all, secured, student, business, travel, cashback
            'limit' => -1,
            'issuer' => '',
            'fee' => 'all' // all, no-fee, low-fee, premium
        ), $atts);

        $cards = $this->filter_cards($atts);

        ob_start();
        include plugin_dir_path(__FILE__) . 'template-comparison.php';
        return ob_get_clean();
    }

    private function filter_cards($atts) {
        $cards = $this->get_cards_data();
        $filtered = array();

        foreach ($cards as $card) {
            // Filter by type
            if ($atts['type'] !== 'all') {
                $name_lower = strtolower($card['name']);
                switch ($atts['type']) {
                    case 'secured':
                        if (strpos($name_lower, 'secured') === false) continue 2;
                        break;
                    case 'student':
                        if (strpos($name_lower, 'student') === false) continue 2;
                        break;
                    case 'business':
                        if (strpos($name_lower, 'business') === false) continue 2;
                        break;
                }
            }

            // Filter by issuer
            if (!empty($atts['issuer'])) {
                if (strtolower($card['issuer']) !== strtolower($atts['issuer'])) {
                    continue;
                }
            }

            // Filter by annual fee
            if ($atts['fee'] !== 'all') {
                $fee = $card['annual_fee'];
                switch ($atts['fee']) {
                    case 'no-fee':
                        if (strpos($fee, '$0') === false && strpos($fee, 'None') === false) continue 2;
                        break;
                    case 'low-fee':
                        if (preg_match('/\$(\d+)/', $fee, $matches)) {
                            if ((int)$matches[1] > 95) continue 2;
                        }
                        break;
                    case 'premium':
                        if (preg_match('/\$(\d+)/', $fee, $matches)) {
                            if ((int)$matches[1] < 95) continue 2;
                        }
                        break;
                }
            }

            $filtered[] = $card;
        }

        // Apply limit
        if ($atts['limit'] > 0) {
            $filtered = array_slice($filtered, 0, $atts['limit']);
        }

        return $filtered;
    }

    public function get_card_count($type = 'all') {
        $cards = $this->filter_cards(array('type' => $type));
        return count($cards);
    }
}

// Initialize the plugin
function cardfair_ccc_init() {
    return Cardfair_Credit_Card_Comparison::get_instance();
}
add_action('plugins_loaded', 'cardfair_ccc_init');

// Activation hook
register_activation_hook(__FILE__, 'cardfair_ccc_activate');
function cardfair_ccc_activate() {
    // Copy JSON data to plugin directory
    $source_file = '/root/.openclaw/workspace/credit-cards.json';
    $dest_file = plugin_dir_path(__FILE__) . 'credit-cards.json';

    if (file_exists($source_file) && !file_exists($dest_file)) {
        copy($source_file, $dest_file);
    }
}
