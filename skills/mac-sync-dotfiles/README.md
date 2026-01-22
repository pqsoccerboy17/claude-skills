# Mac Sync Dotfiles

Synchronize your development environment between multiple Mac computers (e.g., Mac Mini and MacBook) using a Git-based dotfiles repository.

## Overview

This skill provides two scripts:
- **`export-config.sh`** - Run on your primary Mac to capture your current setup
- **`install-config.sh`** - Run on a new Mac to set up your synced environment

## What Gets Synced

| Category | Files | Notes |
|----------|-------|-------|
| **Shell** | `.zshrc`, `.bashrc`, `.bash_profile`, `.zprofile`, `.aliases` | All shell configs |
| **Git** | `.gitconfig`, `.gitignore_global` | Git settings |
| **SSH** | `~/.ssh/config` | SSH config only, NOT keys |
| **Claude Code** | `~/.claude/settings.json`, desktop config | Claude Code settings |
| **Homebrew** | `Brewfile` | All packages, casks, taps |
| **VS Code** | `settings.json`, `keybindings.json`, extensions list | Editor config |
| **Cursor** | `settings.json` | If installed |
| **macOS** | Dock, Finder preferences | Optional |

## Quick Start

### On Your Primary Mac (Mac Mini)

```bash
# 1. Download and run the export script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/claude-skills/main/skills/mac-sync-dotfiles/export-config.sh
chmod +x export-config.sh
./export-config.sh

# 2. Create a private GitHub repo and push
cd ~/dotfiles
git remote add origin git@github.com:YOUR_USERNAME/dotfiles.git
git push -u origin main
```

### On Your Other Mac (MacBook)

```bash
# 1. Clone your dotfiles
git clone git@github.com:YOUR_USERNAME/dotfiles.git ~/dotfiles
cd ~/dotfiles

# 2. Download and run the install script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/claude-skills/main/skills/mac-sync-dotfiles/install-config.sh
chmod +x install-config.sh
./install-config.sh
```

## Daily Workflow

### Before Switching Machines

```bash
# On the machine you're leaving
cd ~/your-project
git add . && git commit -m "WIP" && git push

# For dotfiles changes
cd ~/dotfiles
git add . && git commit -m "Update config" && git push
```

### When Starting on the Other Machine

```bash
# Pull latest dotfiles
cd ~/dotfiles
git pull

# Pull your project
cd ~/your-project
git pull
```

## What's NOT Synced (Intentionally)

- **SSH Keys** - Generate new ones or copy from secure backup
- **Credentials/Secrets** - Use a password manager (1Password, etc.)
- **API Keys** - Use environment variables or secrets manager
- **node_modules, venv** - Regenerate these with `npm install`, etc.

## Handling Machine-Specific Differences

### Git Email

If you use different emails on different machines, create a local override:

```bash
# In any repo, set local email
git config user.email "work@company.com"

# Or use conditional includes in .gitconfig
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```

### Local Overrides

Create a `~/.zshrc.local` for machine-specific settings:

```bash
# In your synced .zshrc, add at the end:
[ -f ~/.zshrc.local ] && source ~/.zshrc.local
```

## SSH Key Options

1. **Copy from secure backup** - If you have keys backed up securely
2. **Generate new keys** on each machine:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   gh ssh-key add ~/.ssh/id_ed25519.pub
   ```
3. **Use 1Password SSH Agent** - Manages keys across machines

## Troubleshooting

### Symlink Conflicts

The install script backs up existing files with `.backup.YYYYMMDD`. If you have issues:

```bash
# Check what was backed up
ls -la ~/*.backup.*

# Restore if needed
mv ~/.zshrc.backup.20240115 ~/.zshrc
```

### Homebrew Failures

Some casks require passwords or may fail on certain macOS versions:

```bash
# Install only what works
brew bundle --file=~/dotfiles/Brewfile || true

# See what failed
brew bundle check --file=~/dotfiles/Brewfile
```

## Alternative: Mackup

If you prefer a more automated approach, consider [Mackup](https://github.com/lra/mackup):

```bash
brew install mackup
mackup backup    # on primary Mac
mackup restore   # on new Mac
```

Mackup supports many more applications but requires iCloud/Dropbox for syncing.

## Files Structure

After running `export-config.sh`, your dotfiles directory will look like:

```
~/dotfiles/
├── Brewfile
├── .gitignore
├── shell/
│   ├── zshrc
│   ├── bashrc
│   └── aliases
├── git/
│   ├── gitconfig
│   └── gitignore_global
├── claude/
│   ├── settings.json
│   └── app-support/
├── ssh/
│   └── config
├── config/
│   ├── vscode/
│   │   ├── settings.json
│   │   ├── keybindings.json
│   │   └── extensions.txt
│   └── cursor/
└── macos/
    ├── dock.plist
    └── finder.plist
```
