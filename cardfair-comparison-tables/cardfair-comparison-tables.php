<?php
/*
Plugin Name: Cardfair Comparison Tables
Description: Side-by-side credit card comparison tables for WordPress
Version: 1.0.0
Author: Cardfair
*/

if (!defined('ABSPATH')) {
    exit;
}

class Cardfair_Comparison_Tables {

    private static $instance = null;
    private $cards_data = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_assets'));
        add_shortcode('cardfair_compare', array($this, 'render_comparison_table'));
        add_shortcode('cardfair_top_picks', array($this, 'render_top_picks'));
    }

    public function enqueue_assets() {
        wp_enqueue_style(
            'cardfair-tables-css',
            plugin_dir_url(__FILE__) . 'comparison-tables.css',
            array(),
            '1.0.0'
        );

        wp_enqueue_script(
            'cardfair-tables-js',
            plugin_dir_url(__FILE__) . 'comparison-tables.js',
            array('jquery'),
            '1.0.0',
            true
        );
    }

    private function get_cards_data() {
        if (null !== $this->cards_data) {
            return $this->cards_data;
        }

        $json_file = plugin_dir_path(__FILE__) . 'credit-cards.json';

        if (!file_exists($json_file)) {
            return array();
        }

        $json_data = file_get_contents($json_file);
        $data = json_decode($json_data, true);

        $this->cards_data = isset($data[0]['credit_cards']) ? $data[0]['credit_cards'] : array();
        return $this->cards_data;
    }

    /**
     * Shortcode: [cardfair_compare cards="Chase Sapphire,Amex Gold,Citi Double" features="annual_fee,rewards,apr"]
     */
    public function render_comparison_table($atts) {
        $atts = shortcode_atts(array(
            'cards' => '', // Comma-separated card names
            'limit' => 3,  // Number of cards to compare
            'type' => '',  // Filter by type (secured, student, travel, etc.)
            'features' => 'annual_fee,rewards,interest_rate,credit_score' // Features to show
        ), $atts);

        $cards = $this->get_cards_for_comparison($atts);
        $features = explode(',', $atts['features']);

        if (empty($cards)) {
            return '<p class="cardfair-no-cards">No cards found for comparison.</p>';
        }

        ob_start();
        include plugin_dir_path(__FILE__) . 'template-comparison-table.php';
        return ob_get_clean();
    }

    /**
     * Shortcode: [cardfair_top_picks type="secured" limit="5"]
     */
    public function render_top_picks($atts) {
        $atts = shortcode_atts(array(
            'type' => 'all',
            'limit' => 5,
            'sort' => 'featured'
        ), $atts);

        $cards = $this->get_top_picks($atts);

        ob_start();
        include plugin_dir_path(__FILE__) . 'template-top-picks.php';
        return ob_get_clean();
    }

    private function get_cards_for_comparison($atts) {
        $all_cards = $this->get_cards_data();
        $selected_cards = array();

        // If specific cards named, find them
        if (!empty($atts['cards'])) {
            $card_names = array_map('trim', explode(',', $atts['cards']));

            foreach ($all_cards as $card) {
                foreach ($card_names as $name) {
                    if (stripos($card['name'], $name) !== false) {
                        $selected_cards[] = $card;
                        break;
                    }
                }

                if (count($selected_cards) >= $atts['limit']) {
                    break;
                }
            }
        }

        // If not enough cards, add by type
        if (count($selected_cards) < $atts['limit'] && !empty($atts['type'])) {
            foreach ($all_cards as $card) {
                if (in_array($card, $selected_cards)) {
                    continue;
                }

                $name_lower = strtolower($card['name']);

                switch ($atts['type']) {
                    case 'secured':
                        if (strpos($name_lower, 'secured') !== false) {
                            $selected_cards[] = $card;
                        }
                        break;
                    case 'student':
                        if (strpos($name_lower, 'student') !== false) {
                            $selected_cards[] = $card;
                        }
                        break;
                    case 'travel':
                        if (strpos($name_lower, 'travel') !== false ||
                            strpos($name_lower, 'venture') !== false) {
                            $selected_cards[] = $card;
                        }
                        break;
                    case 'cashback':
                        if (stripos($card['rewards'], 'cash') !== false) {
                            $selected_cards[] = $card;
                        }
                        break;
                }

                if (count($selected_cards) >= $atts['limit']) {
                    break;
                }
            }
        }

        // Fill with first cards if still empty
        if (empty($selected_cards) && count($all_cards) > 0) {
            $selected_cards = array_slice($all_cards, 0, $atts['limit']);
        }

        return $selected_cards;
    }

    private function get_top_picks($atts) {
        $all_cards = $this->get_cards_data();
        $picks = array();

        // Filter by type
        if (!empty($atts['type']) && $atts['type'] !== 'all') {
            foreach ($all_cards as $card) {
                $name_lower = strtolower($card['name']);

                if ($atts['type'] === 'secured' && strpos($name_lower, 'secured') !== false) {
                    $picks[] = $card;
                } elseif ($atts['type'] === 'student' && strpos($name_lower, 'student') !== false) {
                    $picks[] = $card;
                } elseif ($atts['type'] === 'no-fee' &&
                         (stripos($card['annual_fee'], '$0') !== false ||
                          stripos($card['annual_fee'], 'None') !== false)) {
                    $picks[] = $card;
                }
            }
        } else {
            $picks = $all_cards;
        }

        // Sort and limit
        if ($atts['sort'] === 'featured') {
            // Put well-known cards first
            $featured_issuers = array('American Express', 'Chase', 'Capital One', 'Citi');
            usort($picks, function($a, $b) use ($featured_issuers) {
                $a_index = array_search($a['issuer'], $featured_issuers);
                $b_index = array_search($b['issuer'], $featured_issuers);

                if ($a_index === false && $b_index === false) return 0;
                if ($a_index === false) return 1;
                if ($b_index === false) return -1;

                return $a_index - $b_index;
            });
        }

        return array_slice($picks, 0, $atts['limit']);
    }

    public function get_feature_value($card, $feature) {
        switch ($feature) {
            case 'annual_fee':
                return $card['annual_fee'];
            case 'rewards':
                return $card['rewards'];
            case 'interest_rate':
            case 'apr':
                return $card['interest_rate'];
            case 'credit_score':
                return $card['credit_score_required'];
            case 'features':
                return wp_trim_words($card['additional_features'], 20);
            default:
                return '';
        }
    }

    public function get_feature_label($feature) {
        $labels = array(
            'annual_fee' => 'Annual Fee',
            'rewards' => 'Rewards',
            'interest_rate' => 'Interest Rate',
            'apr' => 'APR',
            'credit_score' => 'Credit Required',
            'features' => 'Key Features'
        );

        return isset($labels[$feature]) ? $labels[$feature] : ucfirst(str_replace('_', ' ', $feature));
    }
}

// Initialize
function cardfair_tables_init() {
    return Cardfair_Comparison_Tables::get_instance();
}
add_action('plugins_loaded', 'cardfair_tables_init');

// Copy data on activation
register_activation_hook(__FILE__, 'cardfair_tables_activate');
function cardfair_tables_activate() {
    $source = '/root/.openclaw/media/inbound/file_0---1cf36a19-42d3-40ac-b404-b7ddc9c78914.json';
    $dest = plugin_dir_path(__FILE__) . 'credit-cards.json';

    if (file_exists($source) && !file_exists($dest)) {
        copy($source, $dest);
    }
}
