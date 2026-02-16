<?php
/**
 * Template Name: Cost Calculator
 * Description: Bereken de echte kosten van je project
 */

get_header();
?>

<style>
    /* Reset voor WordPress theme conflicts */
    #cost-calculator * {
        box-sizing: border-box !important;
    }
    
    #cost-calculator {
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    #cost-calculator .cc-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    #cost-calculator .cc-icon {
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
    
    #cost-calculator h1 {
        font-size: 36px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 10px;
    }
    
    #cost-calculator .cc-subtitle {
        color: #718096;
        font-size: 18px;
    }
    
    #cost-calculator .cc-section {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 24px;
    }
    
    #cost-calculator .cc-section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 20px;
    }
    
    #cost-calculator .cc-form-group {
        margin-bottom: 20px;
    }
    
    #cost-calculator label {
        display: block;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    #cost-calculator .cc-icon-small {
        color: #667eea;
        margin-right: 8px;
    }
    
    #cost-calculator input[type="number"] {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 16px;
        transition: border-color 0.2s;
    }
    
    #cost-calculator input[type="number"]:focus {
        outline: none;
        border-color: #667eea;
    }
    
    #cost-calculator .cc-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    
    #cost-calculator .cc-btn {
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
    
    #cost-calculator .cc-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    #cost-calculator .cc-result {
        display: none;
    }
    
    #cost-calculator .cc-result.show {
        display: block;
    }
    
    #cost-calculator .cc-result-positive {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 16px;
        padding: 32px;
        color: white;
    }
    
    #cost-calculator .cc-result-negative {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 16px;
        padding: 32px;
        color: white;
    }
    
    #cost-calculator .cc-result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    
    #cost-calculator .cc-result-title {
        font-size: 24px;
        font-weight: 700;
    }
    
    #cost-calculator .cc-reset-btn {
        padding: 8px 16px;
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 8px;
        color: white;
        cursor: pointer;
        font-size: 14px;
    }
    
    #cost-calculator .cc-result-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    
    #cost-calculator .cc-result-box {
        text-align: center;
    }
    
    #cost-calculator .cc-result-label {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    
    #cost-calculator .cc-result-value {
        font-size: 28px;
        font-weight: 700;
    }
    
    #cost-calculator .cc-roi-section {
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 20px;
    }
    
    #cost-calculator .cc-breakdown {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    #cost-calculator .cc-breakdown-title {
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    #cost-calculator .cc-breakdown-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        background: #f7fafc;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    #cost-calculator .cc-breakdown-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    #cost-calculator .cc-breakdown-label {
        color: #2d3748;
    }
    
    #cost-calculator .cc-breakdown-value {
        font-weight: 700;
        color: #1a202c;
    }
    
    #cost-calculator .cc-insights {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        border: 2px solid #8b5cf6;
        border-radius: 16px;
        padding: 24px;
    }
    
    #cost-calculator .cc-insights-title {
        font-weight: 700;
        color: #5b21b6;
        margin-bottom: 12px;
    }
    
    #cost-calculator .cc-insights-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    #cost-calculator .cc-insights-list li {
        padding: 8px 0;
        color: #5b21b6;
        font-size: 14px;
    }
    
    @media (max-width: 768px) {
        #cost-calculator .cc-grid-2,
        #cost-calculator .cc-result-grid {
            grid-template-columns: 1fr;
        }
        
        #cost-calculator {
            padding: 16px;
        }
        
        #cost-calculator .cc-section {
            padding: 24px;
        }
        
        #cost-calculator .cc-result-grid {
            grid-template-columns: 1fr 1fr;
        }
    }
</style>

<div id="cost-calculator">
    <!-- Header -->
    <div class="cc-header">
        <div class="cc-icon">💰</div>
        <h1>Cost Calculator</h1>
        <p class="cc-subtitle">Bereken de echte kosten van je project 💸</p>
    </div>

    <!-- Calculator Form -->
    <form id="cc-form">
        <!-- Materials Section -->
        <div class="cc-section">
            <h3 class="cc-section-title"><i class="cc-icon-small">📦</i>Materialen</h3>
            
            <div class="cc-grid-2">
                <div class="cc-form-group">
                    <label>Garn (€)</label>
                    <input type="number" id="cc-yarn-cost" placeholder="25" min="0" step="0.01" required>
                </div>
                <div class="cc-form-group">
                    <label>Naalden/Haken (€)</label>
                    <input type="number" id="cc-needles-cost" placeholder="15" min="0" step="0.01" required>
                </div>
                <div class="cc-form-group">
                    <label>Accessoires (€)</label>
                    <input type="number" id="cc-accessories-cost" placeholder="5" min="0" step="0.01" required>
                    <small style="color: #718096; font-size: 12px;">Knopen, rits, label etc.</small>
                </div>
                <div class="cc-form-group">
                    <label>Overige (€)</label>
                    <input type="number" id="cc-other-cost" placeholder="0" min="0" step="0.01">
                </div>
            </div>
        </div>

        <!-- Time Section -->
        <div class="cc-section">
            <h3 class="cc-section-title"><i class="cc-icon-small">⏰</i>Tijd</h3>
            
            <div class="cc-grid-2">
                <div class="cc-form-group">
                    <label>Aantal Uur</label>
                    <input type="number" id="cc-hours-spent" placeholder="20" min="0" required>
                </div>
                <div class="cc-form-group">
                    <label>Uurloon (€)</label>
                    <input type="number" id="cc-hourly-rate" placeholder="15" min="0" step="0.01">
                    <small style="color: #718096; font-size: 12px;">Optioneel (voor verkoop/klanten)</small>
                </div>
            </div>
        </div>

        <!-- Comparison -->
        <div class="cc-section">
            <h3 class="cc-section-title"><i class="cc-icon-small">⚖️</i>Vergelijking</h3>
            
            <div class="cc-form-group">
                <label>Vergelijkbaar Product in Winkel (€)</label>
                <input type="number" id="cc-store-price" placeholder="89" min="0" step="0.01">
                <small style="color: #718096; font-size: 12px;">Optioneel - voor ROI berekening</small>
            </div>
        </div>

        <!-- Submit -->
        <button type="submit" class="cc-btn">Bereken Kosten</button>
    </form>

    <!-- Results -->
    <div id="cc-result" class="cc-result">
        <!-- Main Result Card -->
        <div id="cc-result-card">
            <div class="cc-result-header">
                <div class="cc-result-title"><i class="cc-icon-small">🧾</i>Kostenoverzicht</div>
                <button id="cc-reset" class="cc-reset-btn">↻ Opnieuw</button>
            </div>
            
            <div class="cc-result-grid">
                <div class="cc-result-box">
                    <div class="cc-result-label">Materialen</div>
                    <div id="cc-total-materials" class="cc-result-value">€0</div>
                </div>
                <div class="cc-result-box">
                    <div class="cc-result-label">Tijd (€)</div>
                    <div id="cc-time-value" class="cc-result-value">€0</div>
                </div>
                <div class="cc-result-box">
                    <div class="cc-result-label">Totaal</div>
                    <div id="cc-total-cost" class="cc-result-value">€0</div>
                </div>
                <div class="cc-result-box">
                    <div class="cc-result-label">Uurloon</div>
                    <div id="cc-effective-hourly-rate" class="cc-result-value">€0</div>
                </div>
            </div>

            <!-- ROI -->
            <div id="cc-roi-section" class="cc-roi-section" style="display: none;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 14px; opacity: 0.9;" id="cc-roi-label">ROI vs. Winkel</div>
                        <div id="cc-roi-value" style="font-size: 32px; font-weight: 700; margin-top: 4px;">€0</div>
                    </div>
                    <div id="cc-roi-icon" style="font-size: 48px;"></div>
                </div>
                <p id="cc-roi-explanation" style="font-size: 14px; margin-top: 12px; opacity: 0.9;"></p>
            </div>
        </div>

        <!-- Breakdown -->
        <div class="cc-breakdown">
            <h4 class="cc-breakdown-title">📋 Details</h4>
            <div id="cc-breakdown-list"></div>
        </div>

        <!-- Insights -->
        <div class="cc-insights">
            <h4 class="cc-insights-title">💡 Inzichten</h4>
            <ul id="cc-insights-list" class="cc-insights-list"></ul>
        </div>
    </div>
</div>

<script>
(function() {
    'use strict';
    
    var cc = window.costCalc = {};
    
    var form = document.getElementById('cc-form');
    var result = document.getElementById('cc-result');
    var resultCard = document.getElementById('cc-result-card');
    var roiSection = document.getElementById('cc-roi-section');
    var breakdownList = document.getElementById('cc-breakdown-list');
    var insightsList = document.getElementById('cc-insights-list');
    var resetBtn = document.getElementById('cc-reset');
    
    // Calculate
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        var yarnCost = parseFloat(document.getElementById('cc-yarn-cost').value) || 0;
        var needlesCost = parseFloat(document.getElementById('cc-needles-cost').value) || 0;
        var accessoriesCost = parseFloat(document.getElementById('cc-accessories-cost').value) || 0;
        var otherCost = parseFloat(document.getElementById('cc-other-cost').value) || 0;
        
        var hoursSpent = parseFloat(document.getElementById('cc-hours-spent').value) || 0;
        var hourlyRate = parseFloat(document.getElementById('cc-hourly-rate').value) || 0;
        var storePrice = parseFloat(document.getElementById('cc-store-price').value) || 0;
        
        // Calculate
        var totalMaterials = yarnCost + needlesCost + accessoriesCost + otherCost;
        var timeValue = hoursSpent * hourlyRate;
        var totalCost = totalMaterials + timeValue;
        var effectiveHourlyRate = (storePrice > 0 && hoursSpent > 0) ? 
            ((storePrice - totalMaterials) / hoursSpent).toFixed(2) : 0;
        
        // Update main result
        document.getElementById('cc-total-materials').textContent = '€' + totalMaterials.toFixed(2);
        document.getElementById('cc-time-value').textContent = '€' + timeValue.toFixed(2);
        document.getElementById('cc-total-cost').textContent = '€' + totalCost.toFixed(2);
        document.getElementById('cc-effective-hourly-rate').textContent = '€' + effectiveHourlyRate;
        
        // Determine card color
        if (hourlyRate > 0) {
            resultCard.className = 'cc-result-positive';
        } else {
            resultCard.className = 'cc-result-negative';
        }
        
        // ROI section
        if (storePrice > 0) {
            var roi = storePrice - totalCost;
            
            document.getElementById('cc-roi-label').textContent = 'ROI vs. Winkel:';
            document.getElementById('cc-roi-value').textContent = '€' + roi.toFixed(2);
            
            if (roi > 0) {
                document.getElementById('cc-roi-icon').textContent = '🎉';
                document.getElementById('cc-roi-explanation').textContent = 
                    'Door het zelf te maken bespaar je €' + roi.toFixed(2) + 
                    ' vergeleken met een vergelijkbaar product in de winkel van €' + storePrice.toFixed(2) + '.';
            } else {
                document.getElementById('cc-roi-icon').textContent = '💸';
                document.getElementById('cc-roi-explanation').textContent = 
                    'Dit project kost €' + Math.abs(roi).toFixed(2) + 
                    ' meer dan in de winkel. Maar je hebt wel een uniek, handgemaakt item!';
            }
            
            roiSection.style.display = 'block';
        } else {
            roiSection.style.display = 'none';
        }
        
        // Breakdown
        breakdownList.innerHTML = '';
        
        var items = [
            { label: 'Garn', value: yarnCost, icon: '⚪' },
            { label: 'Naalden/Haken', value: needlesCost, icon: '✏️' },
            { label: 'Accessoires', value: accessoriesCost, icon: '🧩' },
            { label: 'Overige', value: otherCost, icon: '➕' }
        ];
        
        items.forEach(function(item) {
            if (item.value > 0) {
                var div = document.createElement('div');
                div.className = 'cc-breakdown-item';
                div.innerHTML = 
                    '<div class="cc-breakdown-left">' +
                        '<span>' + item.icon + '</span>' +
                        '<span class="cc-breakdown-label">' + item.label + '</span>' +
                    '</div>' +
                    '<span class="cc-breakdown-value">€' + item.value.toFixed(2) + '</span>';
                breakdownList.appendChild(div);
            }
        });
        
        if (timeValue > 0) {
            var div = document.createElement('div');
            div.className = 'cc-breakdown-item';
            div.style.background = 'linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)';
            div.style.border = '2px solid #8b5cf6';
            div.innerHTML = 
                '<div class="cc-breakdown-left">' +
                    '<span>⏰</span>' +
                    '<span class="cc-breakdown-label">Tijd (' + hoursSpent + 'u × €' + hourlyRate + '/u)</span>' +
                '</div>' +
                '<span class="cc-breakdown-value">€' + timeValue.toFixed(2) + '</span>';
            breakdownList.appendChild(div);
        }
        
        // Insights
        insightsList.innerHTML = '';
        var insights = [];
        
        if (totalCost > 0) {
            var materialPercent = (totalMaterials / totalCost * 100).toFixed(0);
            insights.push('📊 Materialen maken <strong>' + materialPercent + '%</strong> uit van de totale kosten');
        }
        
        if (hourlyRate > 0) {
            insights.push('⏰ Met een uurloon van €' + hourlyRate + '/uur is je tijd <strong>€' + timeValue.toFixed(2) + '</strong> waard');
        } else {
            insights.push('⏰ Je besteedt <strong>' + hoursSpent + ' uur</strong> aan dit project (geen uurloon meegerekend)');
        }
        
        if (storePrice > 0) {
            var diff = storePrice - totalCost;
            var percent = (diff / storePrice * 100).toFixed(0);
            if (diff > 0) {
                insights.push('💰 Je bespaart <strong>' + percent + '%</strong> ten opzichte van de winkelprijs');
            } else {
                insights.push('💎 Handgemaakt kwaliteit - uniek en met liefde gemaakt');
            }
        }
        
        var yarnPercent = (yarnCost / totalMaterials * 100).toFixed(0);
        insights.push('🧶 Garn is <strong>' + yarnPercent + '%</strong> van je materiaalkosten');
        
        if (storePrice > 0 && hoursSpent > 0 && hourlyRate === 0) {
            var effective = (storePrice - totalMaterials) / hoursSpent;
            insights.push('💡 Als je dit voor €' + storePrice.toFixed(2) + ' zou verkopen, is je effectieve uurloon <strong>€' + effective.toFixed(2) + '/uur</strong>');
        }
        
        insights.forEach(function(insight) {
            var li = document.createElement('li');
            li.innerHTML = insight;
            insightsList.appendChild(li);
        });
        
        // Show result
        result.classList.add('show');
        result.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    
    // Reset
    resetBtn.addEventListener('click', function() {
        result.classList.remove('show');
        form.reset();
        document.querySelector('.cc-header').scrollIntoView({ behavior: 'smooth' });
    });
    
})();
</script>

<?php get_footer(); ?>
