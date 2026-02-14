<?php
/**
 * Template: Top Picks Grid
 */
?>

<div class="cardfair-top-picks">

    <?php foreach ($cards as $index => $card): ?>
        <?php
        $is_featured = $index === 0;
        $key_features = extract_top_features($card);
        ?>

        <div class="cardfair-pick-card<?php echo $is_featured ? ' featured' : ''; ?>">

            <div class="cardfair-pick-header">
                <h3 class="cardfair-pick-name"><?php echo esc_html($card['name']); ?></h3>
                <div class="cardfair-pick-issuer"><?php echo esc_html($card['issuer']); ?></div>
            </div>

            <?php if (!empty($key_features)): ?>
                <div class="cardfair-pick-features">
                    <?php foreach ($key_features as $feature): ?>
                        <div class="cardfair-pick-feature">
                            <span class="cardfair-pick-feature-icon">✓</span>
                            <span><?php echo esc_html($feature); ?></span>
                        </div>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>

            <div class="cardfair-pick-details">
                <div class="cardfair-pick-stat">
                    <span class="cardfair-stat-label">Annual Fee</span>
                    <span class="cardfair-stat-value <?php echo get_fee_value_class($card['annual_fee']); ?>">
                        <?php echo esc_html($card['annual_fee']); ?>
                    </span>
                </div>

                <?php if ($card['rewards']): ?>
                    <div class="cardfair-pick-stat">
                        <span class="cardfair-stat-label">Rewards</span>
                        <span class="cardfair-stat-value cardfair-value-good">
                            <?php echo esc_html(wp_trim_words($card['rewards'], 10)); ?>
                        </span>
                    </div>
                <?php endif; ?>

                <?php if ($card['credit_score_required']): ?>
                    <div class="cardfair-pick-stat">
                        <span class="cardfair-stat-label">Credit Needed</span>
                        <span class="cardfair-stat-value">
                            <?php echo esc_html($card['credit_score_required']); ?>
                        </span>
                    </div>
                <?php endif; ?>
            </div>

            <div class="cardfair-pick-cta">
                <a href="#apply-<?php echo esc_attr(sanitize_title($card['name'])); ?>"
                   class="cardfair-pick-apply-btn"
                   target="_blank"
                   rel="nofollow sponsored">
                    Apply Now →
                </a>
            </div>

        </div>

    <?php endforeach; ?>

</div>

<?php
/**
 * Extract top 3 features for card
 */
function extract_top_features($card) {
    $features = array();
    $text = strtolower($card['additional_features'] ?? '');

    // Intro APR offer
    if (preg_match('/0%.*?(\d+)\s*month/i', $text, $matches)) {
        $features[] = "0% for {$matches[1]} months";
    } elseif (strpos($text, '0% intro') !== false) {
        $features[] = '0% Intro APR';
    }

    // Sign-up bonus
    if (preg_match('/(\$?\d{3,})\s*(bonus|cash back|points)/i', $text, $matches)) {
        $features[] = "{$matches[1]} bonus";
    } elseif (preg_match('/earn?(\d{2,})\s*(bonus|points|miles)/i', $text, $matches)) {
        $features[] = "{$matches[1]} bonus";
    }

    // Rewards rate
    if ($card['rewards'] && preg_match('/(\d+%)/', $card['rewards'], $matches)) {
        $features[] = "{$matches[1]} rewards";
    }

    // Annual fee
    if (strpos($card['annual_fee'], '$0') !== false) {
        $features[] = 'No annual fee';
    }

    // Foreign fees
    if (strpos($text, 'no foreign transaction fee') !== false) {
        $features[] = 'No foreign fees';
    }

    // Return up to 3 features
    return array_slice($features, 0, 3);
}

/**
 * Get CSS class for annual fee value
 */
function get_fee_value_class($fee) {
    if (stripos($fee, '$0') !== false || stripos($fee, 'None') !== false) {
        return 'cardfair-value-good';
    } elseif (preg_match('/\$(\d+)/', $fee, $matches) && (int)$matches[1] >= 95) {
        return 'cardfair-value-premium';
    } else {
        return 'cardfair-value-warning';
    }
}
?>
