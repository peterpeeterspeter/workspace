#!/bin/bash
# Auto-fix SEO metadata for CrashCasino articles

echo "=== Auto-fixing SEO Metadata ==="
echo ""

# Article 838
echo "Fixing article 838..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/838" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Discover how we rate crash casinos in 2026. Full transparency on our 9 crash-specific criteria, testing process, and affiliate disclosure.",
      "_yoast_wpseo_focuskw": "rate crash casinos",
      "_yoast_wpseo_title": "How We Rate Crash Casinos: Full 2026 Review Criteria"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 838 fixed" || echo "❌ 838 failed"

# Article 837
echo "Fixing article 837..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/837" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Learn how to verify crash game fairness in 2026. Step-by-step guides for checking provably fair algorithms at popular crash casinos.",
      "_yoast_wpseo_focuskw": "verify crash game fairness",
      "_yoast_wpseo_title": "How to Verify Crash Game Fairness: 2026 Guide"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 837 fixed" || echo "❌ 837 failed"

# Article 836
echo "Fixing article 836..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/836" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Protect yourself from crash gambling scams in 2026. Learn to spot, avoid, and report fake crash casinos with our 7 red flags guide.",
      "_yoast_wpseo_focuskw": "crash gambling scams",
      "_yoast_wpseo_title": "Crash Gambling Scams: 7 Red Flags to Avoid in 2026"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 836 fixed" || echo "❌ 836 failed"

# Article 835
echo "Fixing article 835..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/835" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Discover how we rate crash casinos in 2026. Full transparency on our 9 crash-specific criteria, testing process, and affiliate disclosure.",
      "_yoast_wpseo_focuskw": "rate crash casinos",
      "_yoast_wpseo_title": "How We Rate Crash Casinos: Full 2026 Review Criteria"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 835 fixed" || echo "❌ 835 failed"

# Article 834
echo "Fixing article 834..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/834" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Learn how to verify crash game fairness in 2026. Step-by-step guides for checking provably fair algorithms at popular crash casinos.",
      "_yoast_wpseo_focuskw": "verify crash game fairness",
      "_yoast_wpseo_title": "How to Verify Crash Game Fairness: 2026 Guide"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 834 fixed" || echo "❌ 834 failed"

# Article 833
echo "Fixing article 833..."
curl -X POST "https://crashcasino.io/wp-json/wp/v2/posts/833" \
  -u "peter:3vRhtTs2khfdLtTiDFqkdeXI" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_yoast_wpseo_metadesc": "Protect yourself from crash gambling scams in 2026. Learn to spot, avoid, and report fake crash casinos with our 7 red flags guide.",
      "_yoast_wpseo_focuskw": "crash gambling scams",
      "_yoast_wpseo_title": "Crash Gambling Scams: 7 Red Flags to Avoid in 2026"
    }
  }' 2>&1 | grep -q "id" && echo "✅ 833 fixed" || echo "❌ 833 failed"

echo ""
echo "=== SEO Metadata Added ==="
echo ""
echo "Checking improved scores..."
echo ""

for id in 838 837 836 835 834 833; do
  echo "Article $id:"
  /root/.openclaw/workspace/scripts/publish-gateway.sh check $id crashcasino 2>&1 | grep -E "Health Score:|Post:"
  echo ""
done
