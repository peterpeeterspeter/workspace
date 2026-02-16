<?php
/**
 * Template Name: Yardage Calculator
 * Description: Garn calculator voor breien en haken
 */

get_header();
?>

<style>
    /* Reset voor WordPress theme conflicts */
    #yardage-calculator * {
        box-sizing: border-box !important;
    }
    
    #yardage-calculator {
        max-width: 800px;
        margin: 40px auto;
        padding: 20px;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    #yardage-calculator .yc-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    #yardage-calculator .yc-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        color: white;
        font-size: 32px;
    }
    
    #yardage-calculator h1 {
        font-size: 36px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 10px;
    }
    
    #yardage-calculator .yc-subtitle {
        color: #718096;
        font-size: 18px;
    }
    
    #yardage-calculator .yc-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    #yardage-calculator .yc-form-group {
        margin-bottom: 24px;
    }
    
    #yardage-calculator label {
        display: block;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    #yardage-calculator .yc-icon-small {
        color: #667eea;
        margin-right: 8px;
    }
    
    #yardage-calculator select,
    #yardage-calculator input[type="number"] {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 16px;
        transition: border-color 0.2s;
    }
    
    #yardage-calculator select:focus,
    #yardage-calculator input[type="number"]:focus {
        outline: none;
        border-color: #667eea;
    }
    
    #yardage-calculator .yc-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    
    #yardage-calculator .yc-btn {
        width: 100%;
        padding: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 16px;
    }
    
    #yardage-calculator .yc-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    #yardage-calculator .yc-result {
        display: none;
        margin-top: 32px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 16px;
        padding: 32px;
        color: white;
    }
    
    #yardage-calculator .yc-result.show {
        display: block;
    }
    
    #yardage-calculator .yc-result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    
    #yardage-calculator .yc-result-title {
        font-size: 24px;
        font-weight: 700;
    }
    
    #yardage-calculator .yc-reset-btn {
        padding: 8px 16px;
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 8px;
        color: white;
        cursor: pointer;
        font-size: 14px;
    }
    
    #yardage-calculator .yc-result-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    
    #yardage-calculator .yc-result-box {
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 20px;
    }
    
    #yardage-calculator .yc-result-label {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    
    #yardage-calculator .yc-result-value {
        font-size: 32px;
        font-weight: 700;
    }
    
    #yardage-calculator .yc-result-sub {
        font-size: 14px;
        opacity: 0.9;
    }
    
    #yardage-calculator .yc-result-info {
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-top: 16px;
        font-size: 14px;
    }
    
    #yardage-calculator .yc-tips {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-top: 32px;
    }
    
    #yardage-calculator .yc-tips h3 {
        font-size: 18px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    #yardage-calculator .yc-tips ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    #yardage-calculator .yc-tips li {
        padding: 8px 0;
        color: #4a5568;
        font-size: 14px;
    }
    
    #yardage-calculator .yc-margin-container {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    #yardage-calculator .yc-margin-slider {
        flex: 1;
        height: 8px;
        border-radius: 4px;
        background: #e2e8f0;
        outline: none;
    }
    
    #yardage-calculator .yc-margin-value {
        font-size: 18px;
        font-weight: 700;
        color: #667eea;
        min-width: 60px;
        text-align: center;
    }
    
    @media (max-width: 768px) {
        #yardage-calculator .yc-grid-2,
        #yardage-calculator .yc-result-grid {
            grid-template-columns: 1fr;
        }
        
        #yardage-calculator {
            padding: 16px;
        }
        
        #yardage-calculator .yc-card {
            padding: 24px;
        }
    }
</style>

<div id="yardage-calculator">
    <!-- Header -->
    <div class="yc-header">
        <div class="yc-icon">🧶</div>
        <h1>Yardage Calculator</h1>
        <p class="yc-subtitle">Bereken hoeveel garen je nodig hebt voor je project</p>
    </div>

    <!-- Calculator Form -->
    <div class="yc-card">
        <form id="yc-form">
            <!-- Project Type -->
            <div class="yc-form-group">
                <label>
                    <i class="yc-icon-small">📋</i>Project Type
                </label>
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

            <!-- Dimensions -->
            <div class="yc-grid-2">
                <div class="yc-form-group">
                    <label>
                        <i class="yc-icon-small">↔️</i>Breedte (cm)
                    </label>
                    <input type="number" id="yc-width" placeholder="25" min="1" step="0.1" required>
                </div>
                <div class="yc-form-group">
                    <label>
                        <i class="yc-icon-small">↕️</i>Lengte (cm)
                    </label>
                    <input type="number" id="yc-length" placeholder="150" min="1" step="0.1" required>
                </div>
            </div>

            <!-- Yarn Weight -->
            <div class="yc-form-group">
                <label>
                    <i class="yc-icon-small">⚖️</i>Garen Dikte
                </label>
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

            <!-- Gauge -->
            <div class="yc-grid-2">
                <div class="yc-form-group">
                    <label>
                        <i class="yc-icon-small">🔲</i>Steken (10 cm)
                    </label>
                    <input type="number" id="yc-stitches" placeholder="18" min="1" required>
                </div>
                <div class="yc-form-group">
                    <label>
                        <i class="yc-icon-small">📏</i>Toeren (10 cm)
                    </label>
                    <input type="number" id="yc-rows" placeholder="24" min="1" required>
                </div>
            </div>

            <!-- Safety Margin -->
            <div class="yc-form-group">
                <label>
                    <i class="yc-icon-small">🛡️</i>Veiligheidsmarge
                </label>
                <div class="yc-margin-container">
                    <input type="range" id="yc-margin" min="0" max="30" value="15" class="yc-margin-slider">
                    <span id="yc-margin-value" class="yc-margin-value">15%</span>
                </div>
            </div>

            <!-- Submit -->
            <button type="submit" class="yc-btn">
                Bereken Yardage
            </button>
        </form>

        <!-- Result -->
        <div id="yc-result" class="yc-result">
            <div class="yc-result-header">
                <div class="yc-result-title">✓ Resultaat</div>
                <button id="yc-reset" class="yc-reset-btn">↻ Nieuwe Berekening</button>
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
                <strong>Info:</strong> Inclusief <span id="yc-margin-display">15%</span> marge<br>
                <small id="yc-base-display">Basis: 0 m (zonder marge)</small>
            </div>
        </div>
    </div>

    <!-- Tips -->
    <div class="yc-tips">
        <h3>💡 Tips</h3>
        <ul>
            <li>• Maak altijd een gauge swatch voor accurate resultaten</li>
            <li>• Complexere patronen (kabels, lace) hebben meer garn nodig</li>
            <li>• Bij twijfel: rond altijd naar boven af</li>
            <li>• Grotere naalden/haken = meer garn verbruik</li>
        </ul>
    </div>
</div>

<script>
(function() {
    // Prevent conflicts with other scripts
    var yc = window.yardageCalc = {};
    
    yc.yarnData = {
        lace: { avg: 900 },
        fingering: { avg: 425 },
        sport: { avg: 325 },
        dk: { avg: 275 },
        worsted: { avg: 212 },
        aran: { avg: 170 },
        bulky: { avg: 130 },
        superbulky: { avg: 90 }
    };
    
    yc.presets = {
        scarf: { width: 25, length: 150, stitches: 18, rows: 24 },
        hat: { width: 55, length: 25, stitches: 20, rows: 28 },
        sweater: { width: 50, length: 65, stitches: 18, rows: 24 },
        cardigan: { width: 55, length: 70, stitches: 18, rows: 24 },
        socks: { width: 20, length: 60, stitches: 28, rows: 36 },
        blanket: { width: 100, length: 150, stitches: 16, rows: 20 },
        shawl: { width: 60, length: 180, stitches: 20, rows: 28 },
        mittens: { width: 18, length: 25, stitches: 24, rows: 32 },
        custom: { width: '', length: '', stitches: '', rows: '' }
    };
    
    yc.complexity = {
        scarf: 1.0,
        hat: 1.1,
        sweater: 1.3,
        cardigan: 1.35,
        socks: 1.15,
        blanket: 1.2,
        shawl: 1.25,
        mittens: 1.05,
        custom: 1.0
    };
    
    // Elements
    var form = document.getElementById('yc-form');
    var projectType = document.getElementById('yc-project-type');
    var marginSlider = document.getElementById('yc-margin');
    var marginDisplay = document.getElementById('yc-margin-value');
    var resultDiv = document.getElementById('yc-result');
    var resetBtn = document.getElementById('yc-reset');
    
    // Update margin display
    marginSlider.addEventListener('input', function() {
        marginDisplay.textContent = this.value + '%';
    });
    
    // Load preset on project type change
    projectType.addEventListener('change', function() {
        var preset = yc.presets[this.value];
        if (preset && this.value !== 'custom') {
            document.getElementById('yc-width').value = preset.width;
            document.getElementById('yc-length').value = preset.length;
            document.getElementById('yc-stitches').value = preset.stitches;
            document.getElementById('yc-rows').value = preset.rows;
        }
    });
    
    // Calculate
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        var width = parseFloat(document.getElementById('yc-width').value);
        var length = parseFloat(document.getElementById('yc-length').value);
        var stitches = parseInt(document.getElementById('yc-stitches').value);
        var rows = parseInt(document.getElementById('yc-rows').value);
        var yarnWeight = document.getElementById('yc-yarn-weight').value;
        var margin = parseInt(marginSlider.value) / 100;
        
        // Calculate
        var totalStitches = ((width / 10) * stitches) * ((length / 10) * rows);
        var metersPer100g = yc.yarnData[yarnWeight].avg;
        var stitchLength = 100 / metersPer100g;
        var baseMeters = totalStitches * stitchLength * 2 * yc.complexity[projectType.value];
        
        // Apply margin
        var totalMeters = Math.ceil(baseMeters * (1 + margin));
        var totalYards = Math.ceil(totalMeters * 1.09361);
        var gramsNeeded = (totalMeters / metersPer100g) * 100;
        var totalBalls = Math.ceil(gramsNeeded / 100);
        
        // Display
        document.getElementById('yc-meters').textContent = totalMeters + ' m';
        document.getElementById('yc-yards').textContent = totalYards + ' yards';
        document.getElementById('yc-balls').textContent = totalBalls;
        document.getElementById('yc-margin-display').textContent = (margin * 100) + '%';
        document.getElementById('yc-base-display').textContent = 'Basis: ' + Math.ceil(baseMeters) + ' m (zonder marge)';
        
        resultDiv.classList.add('show');
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    
    // Reset
    resetBtn.addEventListener('click', function() {
        resultDiv.classList.remove('show');
        form.reset();
        marginDisplay.textContent = '15%';
        document.querySelector('.yc-header').scrollIntoView({ behavior: 'smooth' });
    });
    
})();
</script>

<?php get_footer(); ?>
