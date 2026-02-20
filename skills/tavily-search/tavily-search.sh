#!/bin/bash
#
# Tavily Search Helper Script
# Usage: ./tavily-search.sh "<query>" [basic|advanced] [max_results]
#

set -e

# Configuration
API_KEY="${TAVILY_API_KEY:-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}"
QUERY="$1"
DEPTH="${2:-basic}"
MAX_RESULTS="${3:-10}"

# Validate
if [ -z "$QUERY" ]; then
  echo "❌ Error: Query required"
  echo ""
  echo "Usage: $0 \"<query>\" [basic|advanced] [max_results]"
  echo ""
  echo "Examples:"
  echo "  $0 \"AI trends 2026\""
  echo "  $0 \"best e-commerce platform\" advanced 15"
  echo "  $0 \"Photostudio competitors\" basic 5"
  exit 1
fi

# Validate depth
if [[ ! "$DEPTH" =~ ^(basic|advanced)$ ]]; then
  echo "❌ Error: depth must be 'basic' or 'advanced'"
  exit 1
fi

# Validate max_results
if ! [[ "$MAX_RESULTS" =~ ^[0-9]+$ ]] || [ "$MAX_RESULTS" -lt 1 ] || [ "$MAX_RESULTS" -gt 100 ]; then
  echo "❌ Error: max_results must be between 1 and 100"
  exit 1
fi

# Make request
echo "🔍 Tavily Search"
echo "Query: $QUERY"
echo "Depth: $DEPTH"
echo "Max Results: $MAX_RESULTS"
echo ""

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"$DEPTH\",
    \"max_results\": $MAX_RESULTS,
    \"include_answer\": true,
    \"include_images\": false,
    \"include_image_descriptions\": false
  }" | jq '.'

echo ""
echo "✅ Search complete"
