#!/bin/bash
################################################################################
# Hobbysalon Daily Content Pipeline Automation
# Runs daily at 09:00 CET
# Creates 2 articles per day from topical authority plan
################################################################################

set -e

# Configuration
WORKSPACE="/root/.openclaw/workspace"
PLAN_FILE="$WORKSPACE/projects/hobbysalon/topical-authority-research.md"
PROJECT_ID="9d1d03ac7bc78ccf"
API_KEY="n-dffb15d9b58b0d132234ad90a17f794d"
SITE="hobbysalon"
LOG_DIR="$WORKSPACE/logs/hobbysalon-content-pipeline"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/pipeline-$DATE.log"

# Create log directory
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Hobbysalon Daily Content Pipeline Started ==="

################################################################################
# STEP 1: Extract topics from the topical authority plan
################################################################################

log "STEP 1: Extracting topics from topical authority plan..."

# This will be a simple random selection from priority clusters
# In production, this would track which topics have been covered

declare -a PRIORITY_KEYWORDS=(
    "hobbybeurs utrecht"
    "hobbybeurs rotterdam"
    "hobbybeurs amsterdam"
    "creabea groot bijgaarden"
    "creativa hasselt"
    "kerstmarkten nederland 2024"
    "kerstmarkten belgië 2024"
    "creatieve workshops amsterdam"
    "creatieve workshops rotterdam"
    "breicursus beginners"
    "haken workshop"
    "keramiek cursus"
    "kunstmarkt amsterdam"
    "kunstmarkt rotterdam"
    "ambachtmarkt"
    "hobbywinkel amsterdam"
    "hobbywinkel rotterdam"
    "breiwol kopen"
    "garen kopen online"
    "knutselspullen"
)

# Select 2 random topics for today
TOPIC_1=${PRIORITY_KEYWORDS[$RANDOM % ${#PRIORITY_KEYWORDS[@]}]}
TOPIC_2=${PRIORITY_KEYWORDS[$RANDOM % ${#PRIORITY_KEYWORDS[@]}]}

log "Selected Topic 1: $TOPIC_1"
log "Selected Topic 2: $TOPIC_2"

################################################################################
# STEP 2: Create NeuronWriter queries for both topics
################################################################################

log "STEP 2: Creating NeuronWriter queries..."

create_neuronwriter_query() {
    local keyword="$1"
    local response
    
    response=$(curl -s -X POST "https://app.neuronwriter.com/neuron-api/0.5/writer/new-query" \
        -H "X-API-KEY: $API_KEY" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -d "{
            \"project\": \"$PROJECT_ID\",
            \"keyword\": \"$keyword\",
            \"engine\": \"google.nl\",
            \"language\": \"Dutch\"
        }")
    
    # Extract query ID
    query_id=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('query', 'ERROR'))" 2>/dev/null || echo "ERROR")
    
    if [ "$query_id" = "ERROR" ]; then
        log "ERROR: Failed to create query for '$keyword'"
        return 1
    fi
    
    echo "$query_id"
}

QUERY_ID_1=$(create_neuronwriter_query "$TOPIC_1")
QUERY_ID_2=$(create_neuronwriter_query "$TOPIC_2")

if [ "$QUERY_ID_1" = "ERROR" ] || [ "$QUERY_ID_2" = "ERROR" ]; then
    log "FATAL: Failed to create NeuronWriter queries"
    exit 1
fi

log "Query 1 created: $QUERY_ID_1"
log "Query 2 created: $QUERY_ID_2"

# Wait 60 seconds for NeuronWriter analysis
log "Waiting 60 seconds for NeuronWriter analysis..."
sleep 60

################################################################################
# STEP 3: Get SEO briefs from NeuronWriter
################################################################################

log "STEP 3: Fetching SEO briefs from NeuronWriter..."

get_neuronwriter_brief() {
    local query_id="$1"
    local keyword="$2"
    local brief_file="$LOG_DIR/brief-${query_id}.json"
    
    # Wait for analysis to complete (max 5 attempts)
    for i in {1..5}; do
        response=$(curl -s -X POST "https://app.neuronwriter.com/neuron-api/0.5/writer/get-query" \
            -H "X-API-KEY: $API_KEY" \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -d "{\"query\": \"$query_id\"}")
        
        status=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status', 'ERROR'))" 2>/dev/null || echo "ERROR")
        
        if [ "$status" = "ready" ]; then
            echo "$response" > "$brief_file"
            log "Brief ready for '$keyword'"
            return 0
        fi
        
        log "Brief not ready yet (attempt $i/5), waiting 30s..."
        sleep 30
    done
    
    log "ERROR: Brief not ready for '$keyword' after 5 attempts"
    return 1
}

get_neuronwriter_brief "$QUERY_ID_1" "$TOPIC_1"
get_neuronwriter_brief "$QUERY_ID_2" "$TOPIC_2"

################################################################################
# STEP 4: Spawn sub-agents to write articles
################################################################################

log "STEP 4: Spawning writing agents..."

write_article() {
    local topic="$1"
    local query_id="$2"
    local brief_file="$LOG_DIR/brief-${query_id}.json"
    local article_html="$LOG_DIR/article-${query_id}.html"
    
    # Spawn sub-agent via sessions_spawn (this would be called via OpenClaw API)
    # For now, we'll create a task file that the coordinator can pick up
    
    log "Creating writing task for: $topic"
    
    # Create task file
    cat > "$LOG_DIR/task-${query_id}.json" << EOF
{
    "topic": "$topic",
    "query_id": "$query_id",
    "brief_file": "$brief_file",
    "output_file": "$article_html",
    "status": "pending",
    "created_at": "$(date -Iseconds)"
}
EOF
    
    log "Task created: $LOG_DIR/task-${query_id}.json"
}

write_article "$TOPIC_1" "$QUERY_ID_1"
write_article "$TOPIC_2" "$QUERY_ID_2"

# Note: In production, this would use sessions_spawn to create writer agents
# For this version, we're creating task files that can be processed manually
# or picked up by a coordinator agent

log "Writing tasks created. In production, sub-agents would be spawned here."

################################################################################
# STEP 5: Score content via NeuronWriter (after articles are written)
################################################################################

log "STEP 5: Content scoring (to be implemented after writing phase)"

# This step would happen after articles are written
# For now, we'll create a pending task

cat > "$LOG_DIR/scoring-pending.json" << EOF
{
    "query_1": "$QUERY_ID_1",
    "query_2": "$QUERY_ID_2",
    "status": "pending_writing",
    "created_at": "$(date -Iseconds)"
}
EOF

################################################################################
# STEP 6: Publish via pinch-to-post (after scoring ≥ 70)
################################################################################

log "STEP 6: Publishing (to be implemented after scoring ≥ 70)"

# This step would use pinch-to-post to publish articles that score 70+
# Articles below 70 would be sent back for revision

################################################################################
# Summary
################################################################################

log "=== Pipeline Summary ==="
log "Topic 1: $TOPIC_1 (Query: $QUERY_ID_1)"
log "Topic 2: $TOPIC_2 (Query: $QUERY_ID_2)"
log "Tasks created: $LOG_DIR/task-*.json"
log "Next steps:"
log "  1. Spawn writer agents to create articles"
log "  2. Score articles via NeuronWriter"
log "  3. Publish articles scoring 70+ via pinch-to-post"
log "=== Pipeline Complete ==="

# Send notification (via message tool or Telegram)
# This would notify Peter or the coordinator about the daily run

exit 0
