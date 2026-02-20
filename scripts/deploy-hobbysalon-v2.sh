#!/bin/bash
################################################################################
# Deploy Hobbysalon Content Pipeline v2
# Replaces v1 with the fully automated v2 script
################################################################################

set -e

echo "=========================================="
echo "Hobbysalon Automation v2 Deployment"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}ERROR: Please run as root${NC}"
    exit 1
fi

WORKSPACE="/root/.openclaw/workspace"
V1_SCRIPT="$WORKSPACE/scripts/hobbysalon-fully-automated-pipeline.sh"
V2_SCRIPT="$WORKSPACE/scripts/hobbysalon-fully-automated-pipeline-v2.sh"
BACKUP_DIR="$WORKSPACE/backups"
BACKUP_FILE="$BACKUP_DIR/crontab-backup-$(date +%Y%m%d_%H%M%S).txt"

# Step 1: Verify v2 script exists
echo -e "${YELLOW}Step 1: Verifying v2 script...${NC}"
if [ ! -f "$V2_SCRIPT" ]; then
    echo -e "${RED}ERROR: v2 script not found at $V2_SCRIPT${NC}"
    exit 1
fi

if [ ! -x "$V2_SCRIPT" ]; then
    echo "Making v2 script executable..."
    chmod +x "$V2_SCRIPT"
fi

echo -e "${GREEN}✓ v2 script found and executable${NC}"
echo ""

# Step 2: Backup current crontab
echo -e "${YELLOW}Step 2: Backing up current crontab...${NC}"
mkdir -p "$BACKUP_DIR"
crontab -l > "$BACKUP_FILE" 2>/dev/null || true
echo -e "${GREEN}✓ Crontab backed up to: $BACKUP_FILE${NC}"
echo ""

# Step 3: Show current cron entries
echo -e "${YELLOW}Step 3: Current hobbysalon cron entries:${NC}"
crontab -l | grep hobbysalon || echo "No hobbysalon cron jobs found"
echo ""

# Step 4: Confirm with user
echo -e "${YELLOW}Step 4: Deployment confirmation${NC}"
echo ""
echo "This will:"
echo "  1. Replace v1 script with v2 in crontab"
echo "  2. Keep v1 script as backup"
echo "  3. v2 will run at 09:00 CET daily"
echo ""
echo -e "${GREEN}v2 improvements:${NC}"
echo "  ✓ Actually writes articles (Python executor)"
echo "  ✓ Scores via NeuronWriter"
echo "  ✓ Publishes via pinch-to-post"
echo "  ✓ Full end-to-end automation"
echo ""
read -p "Deploy v2? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

# Step 5: Update crontab
echo ""
echo -e "${YELLOW}Step 5: Updating crontab...${NC}"

# Remove old hobbysalon cron entry and add new one
crontab -l 2>/dev/null | grep -v "hobbysalon-fully-automated-pipeline.sh" | crontab -

# Add v2 entry
(crontab -l 2>/dev/null; echo "0 9 * * * $V2_SCRIPT >> /root/.openclaw/workspace/logs/hobbysalon-v2.log 2>&1") | crontab -

echo -e "${GREEN}✓ Crontab updated${NC}"
echo ""

# Step 6: Verify deployment
echo -e "${YELLOW}Step 6: Verifying deployment...${NC}"
echo ""
echo "New crontab entry:"
crontab -l | grep hobbysalon-v2
echo ""

# Step 7: Test run (optional)
echo -e "${YELLOW}Step 7: Test run (optional)${NC}"
echo ""
read -p "Run v2 script now for testing? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running v2 script..."
    echo "Log file: /root/.openclaw/workspace/logs/hobbysalon-content-pipeline/pipeline-$(date +%Y-%m-%d).log"
    echo ""
    $V2_SCRIPT
    echo ""
    echo -e "${GREEN}✓ Test run complete${NC}"
    echo ""
    echo "Check the log for details:"
    echo "  tail -50 /root/.openclaw/workspace/logs/hobbysalon-content-pipeline/pipeline-$(date +%Y-%m-%d).log"
else
    echo "Skipping test run"
    echo ""
    echo "v2 will run automatically at 09:00 CET tomorrow"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "What changed:"
echo "  • v1 script: $V1_SCRIPT (kept as backup)"
echo "  • v2 script: $V2_SCRIPT (now active)"
echo "  • Crontab backup: $BACKUP_FILE"
echo ""
echo "Next run: Tomorrow 09:00 CET"
echo "Log location: /root/.openclaw/workspace/logs/hobbysalon-v2.log"
echo ""
echo "To revert to v1:"
echo "  crontab $BACKUP_FILE"
echo ""
echo "To monitor next run:"
echo "  tail -f /root/.openclaw/workspace/logs/hobbysalon-v2.log"
echo ""
