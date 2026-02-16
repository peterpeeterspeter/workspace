# Yardage Calculator 🧶

Een moderne, responsive calculator om te bepalen hoeveel garen je nodig hebt voor je brei-/haakproject.

## Features

✅ **Project Presets** - Sjaal, muts, trui, sokken, deken, shawl, cardigan, wanten
✅ **Alle Garen Diktes** - Lace t/m Super Bully (8 categorieën)
✅ **Gauge/Steken Proef** - Accuraat door steken + toeren in te voeren
✅ **Veiligheidsmarge** - 0-30% overtrek (standaard 15%)
✅ **Direct Resultaat** - Meters, yards, aantal ballen (100g)
✅ **Mobile Friendly** - Werkt perfect op telefoon
✅ **Geen backend nodig** - 100% client-side JavaScript

## Deploy

### Optie 1: Direct Open (Lokaal)
```bash
cd /root/.openclaw/workspace/projects/yardage-calculator
python3 -m http.server 8080
# Open: http://localhost:8080
```

### Optie 2: Caddy (HTTPS)
```bash
cd /root/.openclaw/workspace/projects/yardage-calculator

# Caddyfile maken
cat > Caddyfile << 'EOF'
yardage.hobbycrafters.io {
    reverse_proxy localhost:8080
}
EOF

# Start Caddy
caddy run --config Caddyfile
```

### Optie 3: Vercel/Netlify
- Sleep de `index.html` naar Vercel/Netlify
- Done in 30 seconden

### Optie 4: Subdomain bestaande site
Upload naar `public/yardage/` map van elke site

## Formule

De calculator gebruikt een multi-step formule:

1. **Totale steken** = (Breedte ÷ 10 × Steken) × (Lengte ÷ 10 × Toeren)
2. **Garen lengte** = Totale steken × 2 × stoklengte factor
3. **Complexiteit factor** - Project type multiplier (1.0-1.35)
4. **Veiligheidsmarge** - +0-30%
5. **Output** - Meters, yards, ballen (100g)

## Next Steps

**V1.1 Mogelijkheden:**
- Stash calculator (hoeveel projecten kan ik maken met mijn garn?)
- Pattern library integratie
- Yarn database (brand reviews, substitutie)
- Affiliate links naar garnwinkels
- Print-friendly versie

**Monetisatie:**
- Affiliate links (garnwinkels, naalden, accessoires)
- Premium patterns ($5-15)
- Yarn brand partnerships
- Display ads (AdSense)

## Tech Stack

- HTML5 + Tailwind CSS (CDN)
- Vanilla JavaScript (geen framework nodig)
- Font Awesome icons
- Responsive design

**Gemaakt met ❤️ voor hobby crafters**
