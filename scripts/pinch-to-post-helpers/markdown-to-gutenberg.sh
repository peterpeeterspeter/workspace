#!/bin/bash

# Markdown to Gutenberg Converter for WordPress
# Converts markdown files to proper Gutenberg block format

set -e

# Check arguments
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <site> <post_id> <markdown_file>"
  echo ""
  echo "Example: $0 crashgame 12345 /path/to/article.md"
  exit 1
fi

SITE="$1"
POST_ID="$2"
MD_FILE="$3"

# Validate inputs
if [[ ! -f "$MD_FILE" ]]; then
  echo "Error: File not found: $MD_FILE"
  exit 1
fi

# Get site credentials
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_CREDS=$($SCRIPT_DIR/get-site-creds.sh "$SITE")

if [[ -z "$SITE_CREDS" ]]; then
  echo "Error: Unknown site '$SITE'"
  exit 1
fi

# Parse credentials
SITE_URL=$(echo "$SITE_CREDS" | cut -d' ' -f1)
USERNAME=$(echo "$SITE_CREDS" | cut -d' ' -f2)
PASSWORD=$(echo "$SITE_CREDS" | cut -d' ' -f3-)

echo "📝 Converting markdown to Gutenberg blocks..."
echo "   Site: $SITE"
echo "   Post ID: $POST_ID"
echo "   File: $MD_FILE"

# Read markdown file
MD_CONTENT=$(cat "$MD_FILE")

# Convert markdown to HTML with proper Gutenberg blocks
GUTENBERG_CONTENT=$(python3 - "$MD_FILE" << 'PYTHON'
import sys
import re
import html

def escape_html(text):
    """Escape HTML special characters"""
    return html.escape(text)

def convert_to_gutenberg(md_text):
    """Convert markdown to Gutenberg block format"""
    
    # Split into lines
    lines = md_text.split('\n')
    
    blocks = []
    current_list = []
    in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Empty line - close any open blocks
        if not line:
            if current_list:
                # Close list
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            i += 1
            continue
        
        # H1 heading
        if line.startswith('# '):
            if current_list:
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            text = line[2:].strip()
            text = escape_html(text)
            blocks.append(f'<!-- wp:heading {"level":1} -->\n<h1>{text}</h1>\n<!-- /wp:heading -->')
        
        # H2 heading
        elif line.startswith('## '):
            if current_list:
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            text = line[3:].strip()
            text = escape_html(text)
            blocks.append(f'<!-- wp:heading {"level":2} -->\n<h2>{text}</h2>\n<!-- /wp:heading -->')
        
        # H3 heading
        elif line.startswith('### '):
            if current_list:
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            text = line[4:].strip()
            text = escape_html(text)
            blocks.append(f'<!-- wp:heading {"level":3} -->\n<h3>{text}</h3>\n<!-- /wp:heading -->')
        
        # Bold text (inline)
        elif '**' in line and not line.startswith('*'):
            # Close list if open
            if current_list and not line.startswith('- ') and not line.startswith('* '):
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            
            # Convert bold markers
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            line = escape_html(line)
            blocks.append(f'<!-- wp:paragraph -->\n<p>{line}</p>\n<!-- /wp:paragraph -->')
        
        # List item
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Handle inline bold
            text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
            # Handle inline links
            text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
            text = escape_html(text)
            current_list.append(f'<li>{text}</li>')
            in_list = True
        
        # Regular paragraph
        else:
            if current_list:
                list_items = '\n'.join(current_list)
                blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
                current_list = []
                in_list = False
            
            # Convert inline formatting
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
            line = escape_html(line)
            blocks.append(f'<!-- wp:paragraph -->\n<p>{line}</p>\n<!-- /wp:paragraph -->')
        
        i += 1
    
    # Close any remaining list
    if current_list:
        list_items = '\n'.join(current_list)
        blocks.append(f'<!-- wp:list -->\n{list_items}\n<!-- /wp:list -->')
    
    return '\n\n'.join(blocks)

# Read markdown from stdin or file
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        markdown_text = f.read()
else:
    markdown_text = sys.stdin.read()

# Convert and output
gutenberg_blocks = convert_to_gutenberg(markdown_text)
print(gutenberg_blocks)
PYTHON
)

if [[ -z "$GUTENBERG_CONTENT" ]]; then
  echo "❌ Error: Failed to convert markdown"
  exit 1
fi

# Update the post via WordPress REST API
echo "📤 Updating post $POST_ID..."
RESPONSE=$(curl -s -X POST \
  "${SITE_URL}/wp/v2/posts/${POST_ID}" \
  -u "${USERNAME}:${PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": $(echo "$GUTENBERG_CONTENT" | jq -Rs .)
  }")

# Check response
if echo "$RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
  echo "✅ Successfully updated post $POST_ID with Gutenberg blocks"
  echo "   View: $(echo "$RESPONSE" | jq -r '.link')"
else
  echo "❌ Error updating post:"
  echo "$RESPONSE" | jq -r '.message // .'
  exit 1
fi
