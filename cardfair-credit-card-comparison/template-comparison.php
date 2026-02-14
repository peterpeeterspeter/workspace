<?php
/**
 * Cardfair Credit Card Comparison Template
 */

$wrapper_class = 'cardfair-comparison-wrapper';

// Get unique values for filters
$issuers = array();
foreach ($cards as $card) {
    $issuers[$card['issuer']] = true;
}
$issuers = array_keys($issuers);
sort($issuers);
?>

<div class="<?php echo esc_attr($wrapper_class); ?>">

    <!-- Filter Bar -->
    <div class="cardfair-filters">

        <div class="cardfair-search-box">
            <input
                type="text"
                class="cardfair-search-input"
                placeholder="🔍 Search cards..."
                value="<?php echo esc_attr($atts['search'] ?? ''); ?>"
            />
        </div>

        <div class="cardfair-filter-group">
            <label for="cardfair-type-filter">Card Type</label>
            <select id="cardfair-type-filter" class="cardfair-type-filter">
                <option value="all">All Cards</option>
                <option value="secured" <?php selected($atts['type'], 'secured'); ?>>Secured Cards</option>
                <option value="student" <?php selected($atts['type'], 'student'); ?>>Student Cards</option>
                <option value="business" <?php selected($atts['type'], 'business'); ?>>Business Cards</option>
                <option value="travel" <?php selected($atts['type'], 'travel'); ?>>Travel Cards</option>
                <option value="cashback" <?php selected($atts['type'], 'cashback'); ?>>Cash Back Cards</option>
            </select>
        </div>

        <div class="cardfair-filter-group">
            <label for="cardfair-issuer-filter">Issuer</label>
            <select id="cardfair-issuer-filter" class="cardfair-issuer-filter">
                <option value="all">All Issuers</option>
                <?php foreach ($issuers as $issuer): ?>
                    <option value="<?php echo esc_attr($issuer); ?>" <?php selected($atts['issuer'], $issuer); ?>>
                        <?php echo esc_html($issuer); ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="cardfair-filter-group">
            <label for="cardfair-fee-filter">Annual Fee</label>
            <select id="cardfair-fee-filter" class="cardfair-fee-filter">
                <option value="all">All Fees</option>
                <option value="no-fee" <?php selected($atts['fee'], 'no-fee'); ?>>No Annual Fee</option>
                <option value="low-fee" <?php selected($atts['fee'], 'low-fee'); ?>>Under $95</option>
                <option value="premium" <?php selected($atts['fee'], 'premium'); ?>>Premium ($95+)</option>
            </select>
        </div>

    </div>

    <!-- Results Count -->
    <div class="cardfair-results-count">
        Showing <strong><?php echo count($cards); ?></strong> credit cards
    </div>

    <!-- Cards Grid -->
    <div class="cardfair-cards-grid">
        <?php if (empty($cards)): ?>

            <!-- Empty State -->
            <div class="cardfair-empty-state">
                <div class="cardfair-empty-state-icon">🔍</div>
                <h3 class="cardfair-empty-state-title">No cards found</h3>
                <p class="cardfair-empty-state-text">Try adjusting your filters to see more results</p>
            </div>

        <?php else: ?>

            <!-- Loading indicator (removed by JS) -->
            <div class="cardfair-loading" style="display: none;">
                <div class="cardfair-loading-spinner"></div>
                <p>Loading cards...</p>
            </div>

        <?php endif; ?>
    </div>

</div>

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        <?php
        $count = 0;
        foreach ($cards as $card):
            $count++;
            ?>
            {
                "@type": "ListItem",
                "position": <?php echo $count; ?>,
                "item": {
                    "@type": "FinancialProduct",
                    "name": "<?php echo esc_js($card['name']); ?>",
                    "description": "<?php echo esc_js(wp_trim_words($card['additional_features'] ?? '', 30)); ?>",
                    "brand": {
                        "@type": "Organization",
                        "name": "<?php echo esc_js($card['issuer']); ?>"
                    },
                    "offers": {
                        "@type": "Offer",
                        "price": "<?php echo esc_js($card['annual_fee']); ?>",
                        "priceCurrency": "USD"
                    }
                }
            }<?php echo $count < count($cards) ? ',' : ''; ?>
        <?php endforeach; ?>
    ]
}
</script>
