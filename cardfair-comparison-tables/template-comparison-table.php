<?php
/**
 * Template: Side-by-Side Comparison Table
 */

$features_map = array(
    'annual_fee' => 'Annual Fee',
    'rewards' => 'Rewards Rate',
    'interest_rate' => 'APR',
    'credit_score' => 'Credit Needed'
);
?>

<div class="cardfair-comparison-wrapper">

    <table class="cardfair-comparison-table">
        <thead>
            <tr>
                <th class="cardfair-feature-column">Feature</th>
                <?php foreach ($cards as $card): ?>
                    <th class="cardfair-card-column">
                        <span class="cardfair-card-name"><?php echo esc_html($card['name']); ?></span>
                        <span class="cardfair-card-issuer-badge"><?php echo esc_html($card['issuer']); ?></span>
                    </th>
                <?php endforeach; ?>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($features as $feature): ?>
                <tr>
                    <td class="cardfair-feature-label" data-label="<?php echo esc_attr($this->get_feature_label($feature)); ?>">
                        <?php echo esc_html($this->get_feature_label($feature)); ?>
                    </td>
                    <?php foreach ($cards as $card): ?>
                        <td class="cardfair-feature-value" data-label="<?php echo esc_attr($this->get_feature_label($feature)); ?>">
                            <?php
                            $value = $this->get_feature_value($card, $feature);
                            $value_class = $this->get_value_class($feature, $value);
                            ?>
                            <span class="<?php echo esc_attr($value_class); ?>">
                                <?php echo esc_html($value ?: 'N/A'); ?>
                            </span>
                        </td>
                    <?php endforeach; ?>
                </tr>
            <?php endforeach; ?>

            <!-- Key Features Row -->
            <tr>
                <td class="cardfair-feature-label" data-label="Key Features">
                    Key Features
                </td>
                <?php foreach ($cards as $card): ?>
                    <td class="cardfair-feature-value" data-label="Key Features">
                        <div class="cardfair-features-list">
                            <?php
                            $key_features = $this->extract_key_features($card);
                            foreach ($key_features as $feature):
                            ?>
                                <div class="cardfair-key-feature">
                                    ✓ <?php echo esc_html($feature); ?>
                                </div>
                            <?php endforeach; ?>
                        </div>
                    </td>
                <?php endforeach; ?>
            </tr>

            <!-- Pros/Cons Row -->
            <tr>
                <td class="cardfair-feature-label" data-label="Highlights">
                    Highlights
                </td>
                <?php foreach ($cards as $card): ?>
                    <td class="cardfair-feature-value" data-label="Highlights">
                        <div class="cardfair-highlights">
                            <?php echo esc_html(wp_trim_words($card['additional_features'], 15)); ?>
                        </div>
                    </td>
                <?php endforeach; ?>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td></td>
                <?php foreach ($cards as $index => $card): ?>
                    <td>
                        <a href="#apply-<?php echo esc_attr(sanitize_title($card['name'])); ?>"
                           class="cardfair-apply-btn"
                           target="_blank"
                           rel="nofollow sponsored">
                            Apply Now
                        </a>
                    </td>
                <?php endforeach; ?>
            </tr>
        </tfoot>
    </table>

</div>

<?php
/**
 * Helper to get CSS class for values
 */
function get_value_class($feature, $value) {
    $value_lower = strtolower($value);

    if ($feature === 'annual_fee') {
        if (strpos($value_lower, '$0') !== false || strpos($value_lower, 'none') !== false) {
            return 'cardfair-value-good';
        } elseif (preg_match('/\$(\d+)/', $value, $matches) && (int)$matches[1] >= 95) {
            return 'cardfair-value-premium';
        } else {
            return 'cardfair-value-warning';
        }
    }

    if ($feature === 'rewards') {
        if (preg_match('/(\d+%)/', $value)) {
            return 'cardfair-value-good';
        }
    }

    return 'cardfair-value-neutral';
}

/**
 * Extract key features from card
 */
function extract_key_features($card) {
    $features = array();
    $text = strtolower($card['additional_features'] ?? '');
    $name = strtolower($card['name']);

    // Check for common features
    if (strpos($text, '0% intro') !== false) {
        $features[] = '0% Intro APR';
    }

    if ($card['rewards'] && preg_match('/(\d+%)/', $card['rewards'], $matches)) {
        $features[] = $matches[1] . ' Rewards';
    }

    if (strpos($card['annual_fee'], '$0') !== false || strpos($card['annual_fee'], 'None') !== false) {
        $features[] = 'No Annual Fee';
    }

    if (strpos($text, 'no foreign') !== false) {
        $features[] = 'No Foreign Fees';
    }

    if (strpos($name, 'secured') !== false) {
        $features[] = 'Secured Card';
    }

    if (strpos($text, 'sign-up bonus') !== false || strpos($text, 'welcome offer') !== false) {
        $features[] = 'Welcome Bonus';
    }

    // Limit to 5 features
    return array_slice($features, 0, 5);
}
?>
