<?php
/**
 * Template Name: Stash Calculator
 * Description: Ontdek wat je met je garen stash kunt maken
 */

get_header();
?>

<style>
    /* Reset voor WordPress theme conflicts */
    #stash-calculator * {
        box-sizing: border-box !important;
    }
    
    #stash-calculator {
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    #stash-calculator .sc-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    #stash-calculator .sc-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        color: white;
        font-size: 32px;
    }
    
    #stash-calculator h1 {
        font-size: 36px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 10px;
    }
    
    #stash-calculator .sc-subtitle {
        color: #718096;
        font-size: 18px;
    }
    
    #stash-calculator .sc-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    #stash-calculator .sc-form-group {
        margin-bottom: 24px;
    }
    
    #stash-calculator label {
        display: block;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    #stash-calculator .sc-icon-small {
        color: #f093fb;
        margin-right: 8px;
    }
    
    #stash-calculator select,
    #stash-calculator input[type="number"] {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 16px;
        transition: border-color 0.2s;
    }
    
    #stash-calculator select:focus,
    #stash-calculator input[type="number"]:focus {
        outline: none;
        border-color: #f093fb;
    }
    
    #stash-calculator .sc-btn {
        width: 100%;
        padding: 16px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 16px;
    }
    
    #stash-calculator .sc-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(240, 147, 251, 0.3);
    }
    
    #stash-calculator .sc-summary {
        display: none;
        margin-top: 32px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 16px;
        padding: 32px;
        color: white;
    }
    
    #stash-calculator .sc-summary.show {
        display: block;
    }
    
    #stash-calculator .sc-summary-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    
    #stash-calculator .sc-summary-title {
        font-size: 24px;
        font-weight: 700;
    }
    
    #stash-calculator .sc-reset-btn {
        padding: 8px 16px;
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 8px;
        color: white;
        cursor: pointer;
        font-size: 14px;
    }
    
    #stash-calculator .sc-summary-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 16px;
    }
    
    #stash-calculator .sc-summary-box {
        text-align: center;
    }
    
    #stash-calculator .sc-summary-label {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    
    #stash-calculator .sc-summary-value {
        font-size: 28px;
        font-weight: 700;
    }
    
    #stash-calculator .sc-projects-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a202c;
        margin: 32px 0 16px 0;
    }
    
    #stash-calculator .sc-project-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    
    #stash-calculator .sc-project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    #stash-calculator .sc-project-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    #stash-calculator .sc-project-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #f093fb;
    }
    
    #stash-calculator .sc-project-name {
        font-weight: 600;
        color: #1a202c;
        font-size: 16px;
    }
    
    #stash-calculator .sc-project-meta {
        font-size: 14px;
        color: #718096;
    }
    
    #stash-calculator .sc-project-right {
        text-align: right;
    }
    
    #stash-calculator .sc-project-possible {
        border-left: 4px solid #10b981;
    }
    
    #stash-calculator .sc-project-maybe {
        border-left: 4px solid #f59e0b;
    }
    
    #stash-calculator .sc-project-impossible {
        border-left: 4px solid #ef4444;
        opacity: 0.6;
    }
    
    #stash-calculator .sc-shopping {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-top: 24px;
    }
    
    #stash-calculator .sc-shopping h4 {
        font-weight: 700;
        color: #92400e;
        margin-bottom: 8px;
    }
    
    #stash-calculator .sc-shopping p {
        color: #78350f;
        font-size: 14px;
    }
    
    #stash-calculator .sc-tips {
        background: rgba(240, 147, 251, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-top: 32px;
    }
    
    #stash-calculator .sc-tips h3 {
        font-size: 18px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    #stash-calculator .sc-tips ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    #stash-calculator .sc-tips li {
        padding: 8px 0;
        color: #4a5568;
        font-size: 14px;
    }
    
    @media (max-width: 768px) {
        #stash-calculator .sc-summary-grid {
            grid-template-columns: 1fr;
        }
        
        #stash-calculator {
            padding: 16px;
        }
        
        #stash-calculator .sc-card {
            padding: 24px;
        }
        
        #stash-calculator .sc-project-left,
        #stash-calculator .sc-project-right {
            flex-direction: column;
            align-items: flex-start;
        }
        
        #stash-calculator .sc-project-card {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
        }
    }
</style>

<div id="stash-calculator">
    <!-- Header -->
    <div class="sc-header">
        <div class="sc-icon">📦</div>
        <h1>Stash Calculator</h1>
        <p class="sc-subtitle">Ontdek wat je met je garn kunt maken 🧶</p>
    </div>

    <!-- Calculator Form -->
    <div class="sc-card">
        <form id="sc-form">
            <!-- Number of Balls -->
            <div class="sc-form-group">
                <label>
                    <i class="sc-icon-small">⚪</i>Aantal Ballen
                </label>
                <input type="number" id="sc-num-balls" placeholder="5" min="1" value="5" required>
            </div>

            <!-- Weight per Ball -->
            <div class="sc-form-group">
                <label>
                    <i class="sc-icon-small">⚖️</i>Gewicht per Bal (gram)
                </label>
                <input type="number" id="sc-weight-per-ball" placeholder="100" min="1" value="100" required>
                <small style="color: #718096; font-size: 12px;">Standaard: 50g of 100g</small>
            </div>

            <!-- Yarn Weight -->
            <div class="sc-form-group">
                <label>
                    <i class="sc-icon-small">🧶</i>Garen Dikte
                </label>
                <select id="sc-yarn-weight" required>
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

            <!-- Submit -->
            <button type="submit" class="sc-btn">
                Bereken Mogelijke Projecten
            </button>
        </form>

        <!-- Summary Result -->
        <div id="sc-summary" class="sc-summary">
            <div class="sc-summary-header">
                <div class="sc-summary-title">✓ Je Stash</div>
                <button id="sc-reset" class="sc-reset-btn">↻ Opnieuw</button>
            </div>
            
            <div class="sc-summary-grid">
                <div class="sc-summary-box">
                    <div class="sc-summary-label">Totaal Gewicht</div>
                    <div id="sc-total-weight" class="sc-summary-value">0 g</div>
                </div>
                <div class="sc-summary-box">
                    <div class="sc-summary-label">Totaal Meters</div>
                    <div id="sc-total-meters" class="sc-summary-value">0 m</div>
                </div>
                <div class="sc-summary-box">
                    <div class="sc-summary-label">Categorie</div>
                    <div id="sc-yarn-category" class="sc-summary-value">DK</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Projects List -->
    <div id="sc-projects-container" style="display: none;">
        <h3 class="sc-projects-title">🎨 Mogelijke Projecten</h3>
        <div id="sc-projects-list"></div>

        <!-- Shopping Suggestion -->
        <div id="sc-shopping" class="sc-shopping">
            <h4>🛒 Meer Garn Nodig?</h4>
            <p id="sc-shopping-text"></p>
        </div>
    </div>

    <!-- Tips -->
    <div class="sc-tips">
        <h3>💡 Tips</h3>
        <ul>
            <li>• Hoeveelheid is indicatief - complexere patronen gebruiken meer garn</li>
            <li>• Combineer kleuren voor grotere projecten (deken, vest)</li>
            <li>• Rond altijd naar boven af bij twijfel</li>
            <li>• Bewaar restjes voor kleine projecten (wanten, sokken)</li>
        </ul>
    </div>
</div>

<script>
(function() {
    'use strict';
    
    // Prevent conflicts
    var sc = window.stashCalc = {};
    
    sc.yarnData = {
        lace: { avg: 900 },
        fingering: { avg: 425 },
        sport: { avg: 325 },
        dk: { avg: 275 },
        worsted: { avg: 212 },
        aran: { avg: 170 },
        bulky: { avg: 130 },
        superbulky: { avg: 90 }
    };
    
    sc.projects = [
        { name: "Muts", category: "Sieraccessoires", minMeters: 100, maxMeters: 200, icon: "🧢", level: "Beginner" },
        { name: "Sjaal", category: "Sieraccessoires", minMeters: 200, maxMeters: 400, icon: "🧣", level: "Beginner" },
        { name: "Cowl", category: "Sieraccessoires", minMeters: 150, maxMeters: 300, icon: "⭕", level: "Beginner" },
        { name: "Wanten", category: "Sieraccessoires", minMeters: 100, maxMeters: 200, icon: "🧤", level: "Beginner" },
        { name: "Muff", category: "Sieraccessoires", minMeters: 100, maxMeters: 150, icon: "🧤", level: "Beginner" },
        { name: "Sokken (paar)", category: "Sokken", minMeters: 300, maxMeters: 450, icon: "🧦", level: "Gemiddeld" },
        { name: "Mittens", category: "Sokken", minMeters: 150, maxMeters: 250, icon: "🧤", level: "Beginner" },
        { name: "Shawl", category: "Sieraccessoires", minMeters: 400, maxMeters: 800, icon: "🔺", level: "Gemiddeld" },
        { name: "Vest", category: "Kleding", minMeters: 600, maxMeters: 1000, icon: "🦺", level: "Gevorderd" },
        { name: "Trui", category: "Kleding", minMeters: 800, maxMeters: 1500, icon: "👕", level: "Gevorderd" },
        { name: "Cardigan", category: "Kleding", minMeters: 900, maxMeters: 1800, icon: "🦺", level: "Gevorderd" },
        { name: "Baby deken", category: "Dekens", minMeters: 400, maxMeters: 700, icon: "👶", level: "Gemiddeld" },
        { name: "Standaard deken", category: "Dekens", minMeters: 1200, maxMeters: 2500, icon: "🛏️", level: "Gevorderd" },
        { name: "Grote deken", category: "Dekens", minMeters: 2500, maxMeters: 4500, icon: "🛏️", level: "Expert" },
        { name: "Tasje", category: "Accessoires", minMeters: 150, maxMeters: 300, icon: "👜", level: "Gemiddeld" },
        { name: "Telefoonhoesje", category: "Accessoires", minMeters: 50, maxMeters: 100, icon: "📱", level: "Beginner" },
        { name: "Kussensloop", category: "Woonaccessoires", minMeters: 200, maxMeters: 400, icon: "🛋️", level: "Beginner" },
        { name: "Potholders (stel)", category: "Woonaccessoires", minMeters: 100, maxMeters: 150, icon: "🧤", level: "Beginner" },
        { name: "Koekjeszakje", category: "Woonaccessoires", minMeters: 50, maxMeters: 100, icon: "🍪", level: "Beginner" },
        { name: "Kerstsok", category: "Seizoensgebonden", minMeters: 150, maxMeters: 250, icon: "🎄", level: "Beginner" },
        { name: "Slippers", category: "Seizoensgebonden", minMeters: 200, maxMeters: 350, icon: "👟", level: "Gemiddeld" }
    ];
    
    // Elements
    var form = document.getElementById('sc-form');
    var summary = document.getElementById('sc-summary');
    var projectsContainer = document.getElementById('sc-projects-container');
    var projectsList = document.getElementById('sc-projects-list');
    var resetBtn = document.getElementById('sc-reset');
    
    // Calculate
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        var numBalls = parseInt(document.getElementById('sc-num-balls').value);
        var weightPerBall = parseInt(document.getElementById('sc-weight-per-ball').value);
        var yarnWeight = document.getElementById('sc-yarn-weight').value;
        
        // Calculate totals
        var totalWeight = numBalls * weightPerBall;
        var metersPer100g = sc.yarnData[yarnWeight].avg;
        var totalMeters = Math.round((totalWeight / 100) * metersPer100g);
        
        // Update summary
        document.getElementById('sc-total-weight').textContent = totalWeight + ' g';
        document.getElementById('sc-total-meters').textContent = totalMeters + ' m';
        document.getElementById('sc-yarn-category').textContent = yarnWeight.toUpperCase();
        
        // Clear projects list
        projectsList.innerHTML = '';
        
        var possibleCount = 0;
        var maybeCount = 0;
        
        // Sort and filter projects
        var sortedProjects = sc.projects.sort(function(a, b) {
            return a.maxMeters - b.maxMeters;
        });
        
        sortedProjects.forEach(function(project) {
            var status, statusClass, statusIcon;
            
            if (totalMeters >= project.maxMeters) {
                status = 'possible';
                statusClass = 'sc-project-possible';
                statusIcon = '✅';
                possibleCount++;
            } else if (totalMeters >= project.minMeters) {
                status = 'maybe';
                statusClass = 'sc-project-maybe';
                statusIcon = '⚠️';
                maybeCount++;
            } else {
                return; // Skip impossible projects
            }
            
            var projectCard = document.createElement('div');
            projectCard.className = 'sc-project-card ' + statusClass;
            
            var neededText = '';
            if (status === 'maybe') {
                neededText = '<small style="color: #f59e0b;">Nog ' + (project.maxMeters - totalMeters) + 'm nodig</small>';
            }
            
            projectCard.innerHTML = 
                '<div class="sc-project-left">' +
                    '<div class="sc-project-icon">' + project.icon + '</div>' +
                    '<div>' +
                        '<div class="sc-project-name">' + project.name + '</div>' +
                        '<div class="sc-project-meta">' + project.category + ' • ' + project.level + '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="sc-project-right">' +
                    '<div>' + statusIcon + '</div>' +
                    '<small style="color: #718096;">' + project.minMeters + '-' + project.maxMeters + 'm</small>' +
                    neededText +
                '</div>';
            
            projectsList.appendChild(projectCard);
        });
        
        // Shopping suggestion
        var shoppingText = document.getElementById('sc-shopping-text');
        if (possibleCount >= 3) {
            shoppingText.innerHTML = '🎉 Je hebt genoeg voor <strong>' + possibleCount + '+ projecten</strong>! Bekijk patroonwebsites zoals <a href="https://www.ravelry.com/patterns/search" target="_blank" style="text-decoration: underline;">Ravelry</a> of <a href="https://www.lovecrafts.com/nl-nl/search/yarn?pref_n1=100" target="_blank" style="text-decoration: underline;">LoveCrafts</a> voor inspiratie.';
        } else if (possibleCount > 0) {
            shoppingText.innerHTML = 'Je kunt <strong>' + possibleCount + ' project(en)</strong> maken. Voor meer opties, overweeg om <a href="https://www.lovecrafts.com/nl-nl/search/yarn?pref_n1=100" target="_blank" style="text-decoration: underline;">nog wat garn bij te kopen</a>.';
        } else {
            shoppingText.innerHTML = 'Je hebt helaas niet genoeg voor een compleet project. Overweeg om <a href="https://www.lovecrafts.com/nl-nl/search/yarn?pref_n1=100" target="_blank" style="text-decoration: underline;">nog wat bij te kopen</a> of combineer met een andere kleur!';
        }
        
        // Show results
        summary.classList.add('show');
        projectsContainer.style.display = 'block';
        projectsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    
    // Reset
    resetBtn.addEventListener('click', function() {
        summary.classList.remove('show');
        projectsContainer.style.display = 'none';
        form.reset();
        document.querySelector('.sc-header').scrollIntoView({ behavior: 'smooth' });
    });
    
})();
</script>

<?php get_footer(); ?>
