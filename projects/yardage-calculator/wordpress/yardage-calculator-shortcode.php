<?php
/**
 * Plugin Name: Yardage Calculator Shortcode
 * Description: Embed de yardage calculator met [yardage_calculator]
 * Version: 1.0
 * Author: HobbyCrafters
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Register shortcode
function yardage_calculator_shortcode($atts) {
    // Enqueue styles
    wp_enqueue_style('yardage-calculator', plugins_url('style.css', __FILE__));
    
    // Enqueue script
    wp_enqueue_script('yardage-calculator', plugins_url('script.js', __FILE__), array(), '1.0', true);
    
    // Output calculator
    ob_start();
    ?>
    <div id="yardage-calculator">
        <div class="yc-header">
            <div class="yc-icon">🧶</div>
            <h1>Yardage Calculator</h1>
            <p class="yc-subtitle">Bereken hoeveel garn je nodig hebt</p>
        </div>

        <div class="yc-card">
            <form id="yc-form">
                <div class="yc-form-group">
                    <label><i class="yc-icon-small">📋</i>Project Type</label>
                    <select id="yc-project-type" required>
                        <option value="scarf">Sjaal</option>
                        <option value="hat">Muts</option>
                        <option value="sweater">Trui</option>
                        <option value="cardigan">Cardigan</option>
                        <option value="socks">Sokken</option>
                        <option value="blanket">Deken</option>
                        <option value="shawl">Shawl</option>
                        <option value="mittens">Wanten</option>
                        <option value="custom">Eigen Ontwerp</option>
                    </select>
                </div>

                <div class="yc-grid-2">
                    <div class="yc-form-group">
                        <label><i class="yc-icon-small">↔️</i>Breedte (cm)</label>
                        <input type="number" id="yc-width" placeholder="25" min="1" step="0.1" required>
                    </div>
                    <div class="yc-form-group">
                        <label><i class="yc-icon-small">↕️</i>Lengte (cm)</label>
                        <input type="number" id="yc-length" placeholder="150" min="1" step="0.1" required>
                    </div>
                </div>

                <div class="yc-form-group">
                    <label><i class="yc-icon-small">⚖️</i>Garen Dikte</label>
                    <select id="yc-yarn-weight" required>
                        <option value="lace">Lace (2-ply) - 800-1000 m/100g</option>
                        <option value="fingering">Fingering (4-ply) - 400-450 m/100g</option>
                        <option value="sport">Sport (5-ply) - 300-350 m/100g</option>
                        <option value="dk" selected>DK (8-ply) - 250-300 m/100g</option>
                        <option value="worsted">Worsted (10-ply) - 200-225 m/100g</option>
                        <option value="aran">Aran (10-ply) - 160-180 m/100g</option>
                        <option value="bulky">Bulky (12-ply) - 120-140 m/100g</option>
                        <option value="superbulky">Super Bulky (14-ply) - 80-100 m/100g</option>
                    </select>
                </div>

                <div class="yc-grid-2">
                    <div class="yc-form-group">
                        <label><i class="yc-icon-small">🔲</i>Steken (10 cm)</label>
                        <input type="number" id="yc-stitches" placeholder="18" min="1" required>
                    </div>
                    <div class="yc-form-group">
                        <label><i class="yc-icon-small">📏</i>Toeren (10 cm)</label>
                        <input type="number" id="yc-rows" placeholder="24" min="1" required>
                    </div>
                </div>

                <div class="yc-form-group">
                    <label><i class="yc-icon-small">🛡️</i>Veiligheidsmarge</label>
                    <div class="yc-margin-container">
                        <input type="range" id="yc-margin" min="0" max="30" value="15" class="yc-margin-slider">
                        <span id="yc-margin-value" class="yc-margin-value">15%</span>
                    </div>
                </div>

                <button type="submit" class="yc-btn">Bereken Yardage</button>
            </form>

            <div id="yc-result" class="yc-result">
                <div class="yc-result-header">
                    <div class="yc-result-title">✓ Resultaat</div>
                    <button id="yc-reset" class="yc-reset-btn">↻ Nieuw</button>
                </div>
                <div class="yc-result-grid">
                    <div class="yc-result-box">
                        <div class="yc-result-label">Benodigd Garen</div>
                        <div id="yc-meters" class="yc-result-value">0 m</div>
                        <div id="yc-yards" class="yc-result-sub">0 yards</div>
                    </div>
                    <div class="yc-result-box">
                        <div class="yc-result-label">Aantal Ballen</div>
                        <div id="yc-balls" class="yc-result-value">0</div>
                        <div class="yc-result-sub">100g/bal</div>
                    </div>
                </div>
                <div class="yc-result-info">
                    <strong>Inclusief <span id="yc-margin-display">15%</span> marge</strong><br>
                    <small id="yc-base-display">Basis: 0 m (zonder marge)</small>
                </div>
            </div>
        </div>

        <div class="yc-tips">
            <h3>💡 Tips</h3>
            <ul>
                <li>• Maak altijd een gauge swatch</li>
                <li>• Complexere patronen = meer garn</li>
                <li>• Bij twijfel: rond naar boven af</li>
            </ul>
        </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('yardage_calculator', 'yardage_calculator_shortcode');
