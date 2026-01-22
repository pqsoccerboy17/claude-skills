#!/bin/bash
#
# Mac Sync - Install Configuration
# Run this on a NEW Mac to set up your synced environment
#
# Usage: ./install-config.sh [dotfiles-directory]
#

set -e

DOTFILES_DIR="${1:-$(pwd)}"

echo "🖥️  Mac Sync - Install Configuration"
echo "====================================="
echo ""
echo "This script will:"
echo "  1. Create symlinks from your home directory to dotfiles"
echo "  2. Install Homebrew packages from Brewfile"
echo "  3. Set up VS Code extensions (if applicable)"
echo ""
echo "Dotfiles directory: $DOTFILES_DIR"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Helper function to create symlinks with backup
link_file() {
    local src="$1"
    local dest="$2"

    if [ ! -f "$src" ]; then
        return 0
    fi

    if [ -f "$dest" ] && [ ! -L "$dest" ]; then
        echo "   📋 Backing up existing: $dest"
        mv "$dest" "$dest.backup.$(date +%Y%m%d)"
    fi

    if [ -L "$dest" ]; then
        rm "$dest"
    fi

    ln -s "$src" "$dest"
    echo "   ✓ Linked: $(basename $dest)"
}

# ============================================
# Shell Configuration
# ============================================
echo ""
echo "🐚 Installing shell configuration..."

link_file "$DOTFILES_DIR/shell/zshrc" "$HOME/.zshrc"
link_file "$DOTFILES_DIR/shell/bashrc" "$HOME/.bashrc"
link_file "$DOTFILES_DIR/shell/bash_profile" "$HOME/.bash_profile"
link_file "$DOTFILES_DIR/shell/zprofile" "$HOME/.zprofile"
link_file "$DOTFILES_DIR/shell/aliases" "$HOME/.aliases"

# ============================================
# Git Configuration
# ============================================
echo ""
echo "🔧 Installing git configuration..."

link_file "$DOTFILES_DIR/git/gitconfig" "$HOME/.gitconfig"
link_file "$DOTFILES_DIR/git/gitignore_global" "$HOME/.gitignore_global"

# Note: You may want to update user.email in .gitconfig if different per machine

# ============================================
# SSH Configuration
# ============================================
echo ""
echo "🔐 Installing SSH config..."

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
link_file "$DOTFILES_DIR/ssh/config" "$HOME/.ssh/config"

echo ""
echo "   ⚠️  Remember: SSH keys are NOT synced. You need to:"
echo "      - Copy keys manually from a secure backup, OR"
echo "      - Generate new keys: ssh-keygen -t ed25519"
echo "      - Add the new public key to GitHub: gh ssh-key add ~/.ssh/id_ed25519.pub"

# ============================================
# Claude Code Configuration
# ============================================
echo ""
echo "🤖 Installing Claude Code configuration..."

mkdir -p "$HOME/.claude"

if [ -f "$DOTFILES_DIR/claude/settings.json" ]; then
    link_file "$DOTFILES_DIR/claude/settings.json" "$HOME/.claude/settings.json"
fi

# Claude Desktop app config
CLAUDE_APP_SUPPORT="$HOME/Library/Application Support/Claude"
if [ -d "$DOTFILES_DIR/claude/app-support" ]; then
    mkdir -p "$CLAUDE_APP_SUPPORT"
    if [ -f "$DOTFILES_DIR/claude/app-support/claude_desktop_config.json" ]; then
        link_file "$DOTFILES_DIR/claude/app-support/claude_desktop_config.json" "$CLAUDE_APP_SUPPORT/claude_desktop_config.json"
    fi
fi

# ============================================
# Homebrew
# ============================================
echo ""
echo "🍺 Installing Homebrew packages..."

if ! command -v brew &> /dev/null; then
    echo "   Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add brew to PATH for Apple Silicon
    if [ -f "/opt/homebrew/bin/brew" ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

if [ -f "$DOTFILES_DIR/Brewfile" ]; then
    echo "   Installing from Brewfile..."
    brew bundle --file="$DOTFILES_DIR/Brewfile" || echo "   ⚠️  Some packages may have failed"
    echo "   ✓ Homebrew packages installed"
else
    echo "   ⚠️  No Brewfile found, skipping..."
fi

# ============================================
# VS Code
# ============================================
echo ""
echo "📝 Installing VS Code configuration..."

VSCODE_DIR="$HOME/Library/Application Support/Code/User"
if [ -d "$DOTFILES_DIR/config/vscode" ]; then
    mkdir -p "$VSCODE_DIR"

    if [ -f "$DOTFILES_DIR/config/vscode/settings.json" ]; then
        link_file "$DOTFILES_DIR/config/vscode/settings.json" "$VSCODE_DIR/settings.json"
    fi
    if [ -f "$DOTFILES_DIR/config/vscode/keybindings.json" ]; then
        link_file "$DOTFILES_DIR/config/vscode/keybindings.json" "$VSCODE_DIR/keybindings.json"
    fi

    # Install extensions
    if [ -f "$DOTFILES_DIR/config/vscode/extensions.txt" ] && command -v code &> /dev/null; then
        echo "   Installing VS Code extensions..."
        while read extension; do
            code --install-extension "$extension" --force 2>/dev/null || true
        done < "$DOTFILES_DIR/config/vscode/extensions.txt"
        echo "   ✓ VS Code extensions installed"
    fi
else
    echo "   ⚠️  No VS Code config found, skipping..."
    echo "   💡 Tip: VS Code has built-in Settings Sync - consider using that instead"
fi

# ============================================
# Cursor (if config exists)
# ============================================
if [ -d "$DOTFILES_DIR/config/cursor" ]; then
    echo ""
    echo "📝 Installing Cursor configuration..."
    CURSOR_DIR="$HOME/Library/Application Support/Cursor/User"
    mkdir -p "$CURSOR_DIR"

    if [ -f "$DOTFILES_DIR/config/cursor/settings.json" ]; then
        link_file "$DOTFILES_DIR/config/cursor/settings.json" "$CURSOR_DIR/settings.json"
    fi
fi

# ============================================
# Summary
# ============================================
echo ""
echo "====================================="
echo "✅ Installation complete!"
echo "====================================="
echo ""
echo "What was set up:"
echo "  • Shell configuration (symlinked)"
echo "  • Git configuration (symlinked)"
echo "  • SSH config (symlinked)"
echo "  • Claude Code settings (symlinked)"
echo "  • Homebrew packages (installed)"
echo "  • VS Code settings & extensions (if found)"
echo ""
echo "⚠️  Action items:"
echo "  1. Restart your terminal for shell changes to take effect"
echo "  2. Set up SSH keys if you haven't already"
echo "  3. Run 'gh auth login' to authenticate with GitHub"
echo "  4. Review ~/.gitconfig and update email if needed"
echo ""
echo "📁 Your original files (if any) were backed up with .backup.YYYYMMDD extension"
echo ""
