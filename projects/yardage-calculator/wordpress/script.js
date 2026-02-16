(function() {
    'use strict';
    
    // Wait for DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    function init() {
        var calc = document.getElementById('yardage-calculator');
        if (!calc) return;
        
        var data = {
            yarnData: {
                lace: { avg: 900 },
                fingering: { avg: 425 },
                sport: { avg: 325 },
                dk: { avg: 275 },
                worsted: { avg: 212 },
                aran: { avg: 170 },
                bulky: { avg: 130 },
                superbulky: { avg: 90 }
            },
            presets: {
                scarf: { width: 25, length: 150, stitches: 18, rows: 24 },
                hat: { width: 55, length: 25, stitches: 20, rows: 28 },
                sweater: { width: 50, length: 65, stitches: 18, rows: 24 },
                cardigan: { width: 55, length: 70, stitches: 18, rows: 24 },
                socks: { width: 20, length: 60, stitches: 28, rows: 36 },
                blanket: { width: 100, length: 150, stitches: 16, rows: 20 },
                shawl: { width: 60, length: 180, stitches: 20, rows: 28 },
                mittens: { width: 18, length: 25, stitches: 24, rows: 32 },
                custom: { width: '', length: '', stitches: '', rows: '' }
            },
            complexity: {
                scarf: 1.0,
                hat: 1.1,
                sweater: 1.3,
                cardigan: 1.35,
                socks: 1.15,
                blanket: 1.2,
                shawl: 1.25,
                mittens: 1.05,
                custom: 1.0
            }
        };
        
        var form = calc.querySelector('#yc-form');
        var projectType = calc.querySelector('#yc-project-type');
        var marginSlider = calc.querySelector('#yc-margin');
        var marginDisplay = calc.querySelector('#yc-margin-value');
        var resultDiv = calc.querySelector('#yc-result');
        var resetBtn = calc.querySelector('#yc-reset');
        
        // Margin slider
        if (marginSlider) {
            marginSlider.addEventListener('input', function() {
                marginDisplay.textContent = this.value + '%';
            });
        }
        
        // Project type preset
        if (projectType) {
            projectType.addEventListener('change', function() {
                var preset = data.presets[this.value];
                if (preset && this.value !== 'custom') {
                    calc.querySelector('#yc-width').value = preset.width;
                    calc.querySelector('#yc-length').value = preset.length;
                    calc.querySelector('#yc-stitches').value = preset.stitches;
                    calc.querySelector('#yc-rows').value = preset.rows;
                }
            });
        }
        
        // Calculate
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                var width = parseFloat(calc.querySelector('#yc-width').value);
                var length = parseFloat(calc.querySelector('#yc-length').value);
                var stitches = parseInt(calc.querySelector('#yc-stitches').value);
                var rows = parseInt(calc.querySelector('#yc-rows').value);
                var yarnWeight = calc.querySelector('#yc-yarn-weight').value;
                var margin = parseInt(marginSlider.value) / 100;
                
                // Calculate total stitches
                var totalStitches = ((width / 10) * stitches) * ((length / 10) * rows);
                
                // Calculate yarn needed
                var metersPer100g = data.yarnData[yarnWeight].avg;
                var stitchLength = 100 / metersPer100g;
                var baseMeters = totalStitches * stitchLength * 2 * data.complexity[projectType.value];
                
                // Apply margin
                var totalMeters = Math.ceil(baseMeters * (1 + margin));
                var totalYards = Math.ceil(totalMeters * 1.09361);
                var gramsNeeded = (totalMeters / metersPer100g) * 100;
                var totalBalls = Math.ceil(gramsNeeded / 100);
                
                // Display results
                calc.querySelector('#yc-meters').textContent = totalMeters + ' m';
                calc.querySelector('#yc-yards').textContent = totalYards + ' yards';
                calc.querySelector('#yc-balls').textContent = totalBalls;
                calc.querySelector('#yc-margin-display').textContent = (margin * 100) + '%';
                calc.querySelector('#yc-base-display').textContent = 'Basis: ' + Math.ceil(baseMeters) + ' m (zonder marge)';
                
                // Show result
                resultDiv.classList.add('show');
                
                // Smooth scroll to result
                if (resultDiv.scrollIntoView) {
                    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        }
        
        // Reset
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                resultDiv.classList.remove('show');
                form.reset();
                marginDisplay.textContent = '15%';
                
                // Scroll to top
                var header = calc.querySelector('.yc-header');
                if (header && header.scrollIntoView) {
                    header.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    }
})();
