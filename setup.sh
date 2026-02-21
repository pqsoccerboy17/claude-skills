#!/bin/bash
#
# Claude Skills Setup Script
# Configures Claude Code to use skills from this repository
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_CONFIG_DIR="$HOME/.claude"
CLAUDE_SETTINGS="$CLAUDE_CONFIG_DIR/settings.json"

echo "========================================"
echo "Claude Skills Setup"
echo "========================================"
echo ""
echo "Skills directory: $SCRIPT_DIR"
echo ""

# Check for required tools
echo "Checking dependencies..."

# Check for Python
if command -v python3 &> /dev/null; then
    echo "✓ Python3 found: $(python3 --version)"
else
    echo "✗ Python3 not found. Please install Python 3."
    exit 1
fi

# Check for pip packages
echo ""
echo "Installing Python dependencies..."
pip3 install --quiet pypdf pdfplumber reportlab Pillow openpyxl pandas pytest 2>/dev/null || {
    echo "Note: Some packages may need manual installation"
}
echo "✓ Python packages checked"

# Check for Node.js
if command -v node &> /dev/null; then
    echo "✓ Node.js found: $(node --version)"
else
    echo "✗ Node.js not found. Required for agent-dashboard."
    echo "  Install with: brew install node"
fi

# Check for LibreOffice (needed for Excel formula recalculation)
if command -v soffice &> /dev/null; then
    echo "✓ LibreOffice found"
else
    echo "⚠ LibreOffice not found. Install with: brew install --cask libreoffice"
    echo "  (Required for Excel formula recalculation)"
fi

# Create Claude config directory if needed
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo ""
    echo "Creating Claude config directory..."
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

# Configure Claude Code settings
echo ""
echo "Configuring Claude Code..."

if [ -f "$CLAUDE_SETTINGS" ]; then
    # Backup existing settings
    cp "$CLAUDE_SETTINGS" "$CLAUDE_SETTINGS.backup"
    echo "✓ Backed up existing settings to $CLAUDE_SETTINGS.backup"

    # Check if skills path already configured
    if grep -q "claude-skills" "$CLAUDE_SETTINGS" 2>/dev/null; then
        echo "✓ Skills path already configured in settings"
    else
        echo "⚠ Please add this to your $CLAUDE_SETTINGS manually:"
        echo ""
        echo '  "skills": {'
        echo "    \"paths\": [\"$SCRIPT_DIR\"]"
        echo '  }'
        echo ""
    fi
else
    # Create new settings file
    cat > "$CLAUDE_SETTINGS" << EOF
{
  "skills": {
    "paths": ["$SCRIPT_DIR"]
  }
}
EOF
    echo "✓ Created $CLAUDE_SETTINGS"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
find "$SCRIPT_DIR" -name "*.py" -exec chmod +x {} \;
find "$SCRIPT_DIR" -name "*.sh" -exec chmod +x {} \;
echo "✓ Scripts are executable"

# Install Node.js dependencies for agent-dashboard
echo ""
echo "Installing agent-dashboard dependencies..."
DASHBOARD_DIR="$SCRIPT_DIR/dev-tools/agent-dashboard/app"
if [ -d "$DASHBOARD_DIR" ] && [ ! -d "$DASHBOARD_DIR/node_modules" ]; then
    cd "$DASHBOARD_DIR" && npm install --quiet && cd "$SCRIPT_DIR"
    echo "✓ Agent dashboard dependencies installed"
elif [ -d "$DASHBOARD_DIR/node_modules" ]; then
    echo "✓ Agent dashboard dependencies already installed"
fi

# Create symlinks to ~/scripts/ for dual-install scripts
echo ""
echo "Setting up script symlinks..."
SCRIPTS_DIR="$HOME/scripts"
mkdir -p "$SCRIPTS_DIR"

SYMLINKS=(
    "$SCRIPT_DIR/productivity/ecosystem-status/scripts/ecosystem_status.py:$SCRIPTS_DIR/ecosystem_status.py"
    "$SCRIPT_DIR/productivity/notifications/scripts/notify.py:$SCRIPTS_DIR/notify.py"
)

for pair in "${SYMLINKS[@]}"; do
    src="${pair%%:*}"
    dest="${pair##*:}"
    if [ -f "$src" ]; then
        ln -sf "$src" "$dest"
        echo "✓ Linked $(basename "$dest") → ~/scripts/"
    else
        echo "⚠ Source not found: $src"
    fi
done

# Summary
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Skills installed:"
echo "  • pdf                 - PDF processing and form filling"
echo "  • xlsx                - Excel spreadsheet manipulation"
echo "  • csv-data-summarizer - Data analysis"
echo "  • file-organizer      - Document organization"
echo "  • internal-comms      - Communication templates"
echo "  • notion-api          - Direct Notion API for Code mode"
echo "  • ecosystem-status    - Automation system monitoring"
echo "  • notifications       - Unified push notifications"
echo "  • ecosystem-config    - Central configuration"
echo "  • gemini              - Google Gemini API integration"
echo "  • mcp-builder         - MCP server development"
echo "  • factory-pm          - Spec-before-code PM agent"
echo "  • agent-dashboard    - Real-time Agent Teams monitoring"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code to load skills"
echo "  2. Test by asking Claude to use a skill"
echo "  3. Run 'git pull' periodically to get updates"
echo ""
echo "To sync to another machine:"
echo "  git clone https://github.com/pqsoccerboy17/claude-skills.git ~/claude-skills"
echo "  cd ~/claude-skills && ./setup.sh"
echo ""
