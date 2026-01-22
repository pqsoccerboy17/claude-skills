#!/bin/bash
#
# Mac Sync - Export Configuration
# Run this on your PRIMARY Mac to capture your current setup
#
# Usage: ./export-config.sh [dotfiles-directory]
#

set -e

DOTFILES_DIR="${1:-$HOME/dotfiles}"
BACKUP_DIR="$DOTFILES_DIR/backup-$(date +%Y%m%d-%H%M%S)"

echo "🖥️  Mac Sync - Export Configuration"
echo "===================================="
echo ""
echo "This script will:"
echo "  1. Create a dotfiles directory at: $DOTFILES_DIR"
echo "  2. Copy your configuration files"
echo "  3. Export your Homebrew packages"
echo "  4. Initialize a git repository"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Create dotfiles directory
mkdir -p "$DOTFILES_DIR"
cd "$DOTFILES_DIR"

echo ""
echo "📁 Creating directory structure..."
mkdir -p shell git claude config ssh

# ============================================
# Shell Configuration
# ============================================
echo "🐚 Exporting shell configuration..."

if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" shell/zshrc
    echo "   ✓ .zshrc"
fi

if [ -f "$HOME/.bashrc" ]; then
    cp "$HOME/.bashrc" shell/bashrc
    echo "   ✓ .bashrc"
fi

if [ -f "$HOME/.bash_profile" ]; then
    cp "$HOME/.bash_profile" shell/bash_profile
    echo "   ✓ .bash_profile"
fi

if [ -f "$HOME/.zprofile" ]; then
    cp "$HOME/.zprofile" shell/zprofile
    echo "   ✓ .zprofile"
fi

if [ -f "$HOME/.aliases" ]; then
    cp "$HOME/.aliases" shell/aliases
    echo "   ✓ .aliases"
fi

# ============================================
# Git Configuration
# ============================================
echo "🔧 Exporting git configuration..."

if [ -f "$HOME/.gitconfig" ]; then
    cp "$HOME/.gitconfig" git/gitconfig
    echo "   ✓ .gitconfig"
fi

if [ -f "$HOME/.gitignore_global" ]; then
    cp "$HOME/.gitignore_global" git/gitignore_global
    echo "   ✓ .gitignore_global"
fi

# ============================================
# Claude Code Configuration
# ============================================
echo "🤖 Exporting Claude Code configuration..."

if [ -d "$HOME/.claude" ]; then
    # Copy settings but not sensitive data
    if [ -f "$HOME/.claude/settings.json" ]; then
        cp "$HOME/.claude/settings.json" claude/settings.json
        echo "   ✓ Claude settings.json"
    fi
    if [ -f "$HOME/.claude/claude_desktop_config.json" ]; then
        cp "$HOME/.claude/claude_desktop_config.json" claude/claude_desktop_config.json
        echo "   ✓ Claude desktop config"
    fi
fi

# Claude Desktop app config (different location)
CLAUDE_APP_SUPPORT="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_APP_SUPPORT" ]; then
    mkdir -p "claude/app-support"
    if [ -f "$CLAUDE_APP_SUPPORT/claude_desktop_config.json" ]; then
        cp "$CLAUDE_APP_SUPPORT/claude_desktop_config.json" claude/app-support/
        echo "   ✓ Claude Desktop app config"
    fi
fi

# ============================================
# SSH Configuration (NOT keys!)
# ============================================
echo "🔐 Exporting SSH config (not keys)..."

if [ -f "$HOME/.ssh/config" ]; then
    cp "$HOME/.ssh/config" ssh/config
    echo "   ✓ SSH config"
fi

# ============================================
# Homebrew
# ============================================
echo "🍺 Exporting Homebrew packages..."

if command -v brew &> /dev/null; then
    brew bundle dump --force --file="$DOTFILES_DIR/Brewfile"
    echo "   ✓ Brewfile created"

    # Count what's included
    FORMULAE=$(grep -c "^brew " Brewfile 2>/dev/null || echo "0")
    CASKS=$(grep -c "^cask " Brewfile 2>/dev/null || echo "0")
    echo "   📦 $FORMULAE formulae, $CASKS casks"
else
    echo "   ⚠️  Homebrew not found, skipping..."
fi

# ============================================
# VS Code (if installed)
# ============================================
echo "📝 Checking for VS Code..."

VSCODE_DIR="$HOME/Library/Application Support/Code/User"
if [ -d "$VSCODE_DIR" ]; then
    mkdir -p config/vscode

    if [ -f "$VSCODE_DIR/settings.json" ]; then
        cp "$VSCODE_DIR/settings.json" config/vscode/
        echo "   ✓ VS Code settings"
    fi
    if [ -f "$VSCODE_DIR/keybindings.json" ]; then
        cp "$VSCODE_DIR/keybindings.json" config/vscode/
        echo "   ✓ VS Code keybindings"
    fi

    # Export extensions list
    if command -v code &> /dev/null; then
        code --list-extensions > config/vscode/extensions.txt
        echo "   ✓ VS Code extensions list"
    fi
else
    echo "   ⚠️  VS Code not found, skipping..."
fi

# ============================================
# Cursor (VS Code fork, if installed)
# ============================================
CURSOR_DIR="$HOME/Library/Application Support/Cursor/User"
if [ -d "$CURSOR_DIR" ]; then
    mkdir -p config/cursor

    if [ -f "$CURSOR_DIR/settings.json" ]; then
        cp "$CURSOR_DIR/settings.json" config/cursor/
        echo "   ✓ Cursor settings"
    fi
fi

# ============================================
# macOS Defaults (optional)
# ============================================
echo "⚙️  Exporting macOS preferences..."
mkdir -p macos

# Export dock settings
defaults read com.apple.dock > macos/dock.plist 2>/dev/null && echo "   ✓ Dock preferences" || true

# Export Finder settings
defaults read com.apple.finder > macos/finder.plist 2>/dev/null && echo "   ✓ Finder preferences" || true

# ============================================
# Create .gitignore
# ============================================
cat > .gitignore << 'EOF'
# Sensitive files - NEVER commit these
*.pem
*.key
*_rsa
*_ed25519
*.p12
credentials*
secrets*
.env
.env.*

# Backup files
backup-*/

# OS files
.DS_Store
*.swp
*~

# Local overrides
*.local
EOF

# ============================================
# Initialize Git Repository
# ============================================
echo ""
echo "📦 Initializing git repository..."

if [ ! -d ".git" ]; then
    git init
    git add -A
    git commit -m "Initial dotfiles export from $(hostname)"
    echo "   ✓ Git repository initialized"
else
    git add -A
    git commit -m "Update dotfiles from $(hostname)" || echo "   No changes to commit"
fi

# ============================================
# Summary
# ============================================
echo ""
echo "===================================="
echo "✅ Export complete!"
echo "===================================="
echo ""
echo "Your dotfiles are in: $DOTFILES_DIR"
echo ""
echo "Next steps:"
echo "  1. Create a private repo on GitHub (e.g., github.com/YOU/dotfiles)"
echo "  2. Push your dotfiles:"
echo "     cd $DOTFILES_DIR"
echo "     git remote add origin git@github.com:YOUR_USERNAME/dotfiles.git"
echo "     git push -u origin main"
echo ""
echo "  3. On your other Mac, clone and run install-config.sh"
echo ""
