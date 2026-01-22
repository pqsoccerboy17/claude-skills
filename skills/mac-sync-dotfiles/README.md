# Mac Sync Dotfiles

Synchronize your development environment between multiple Mac computers (e.g., Mac Mini and MacBook) using a Git-based dotfiles repository.

## Overview

This skill provides scripts for complete machine synchronization:

| Script | Purpose |
|--------|---------|
| **`export-config.sh`** | Capture your current Mac's configuration |
| **`install-config.sh`** | Set up a new Mac with your synced environment |
| **`sync-repos.sh`** | Clone/pull ALL your GitHub repositories |
| **`switch-machine.sh`** | Pre-flight check before switching Macs |

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

### Repository Structure

Repos are organized in two locations:

| Location | Purpose | Contents |
|----------|---------|----------|
| `~/dev/` | Development tools & automations | claude-skills, MCP servers, automation tools |
| `~/Projects/` | Client & business work | client-timelines, design-os, etc. |

New repos from `--clone-all` are cloned to `~/dev/` by default.

### On Your Primary Mac (Mac Mini)

```bash
# 1. Clone this skills repo
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/dev/claude-skills
cd ~/dev/claude-skills/skills/mac-sync-dotfiles

# 2. Export your configuration (creates ~/dotfiles)
./export-config.sh

# 3. Create a private GitHub repo for dotfiles and push
cd ~/dotfiles
git remote add origin git@github.com:YOUR_USERNAME/dotfiles.git
git push -u origin main

# 4. Sync ALL your GitHub repos (scans ~/dev + ~/Projects, clones missing to ~/dev)
cd ~/dev/claude-skills/skills/mac-sync-dotfiles
./sync-repos.sh --clone-all
```

### On Your Other Mac (MacBook)

```bash
# 1. Clone the skills repo
git clone https://github.com/pqsoccerboy17/claude-skills.git ~/dev/claude-skills
cd ~/dev/claude-skills/skills/mac-sync-dotfiles

# 2. Clone your dotfiles and install
git clone git@github.com:YOUR_USERNAME/dotfiles.git ~/dotfiles
./install-config.sh

# 3. Clone ALL your GitHub repos
./sync-repos.sh --clone-all
```

## Syncing All GitHub Repositories

The `sync-repos.sh` script manages ALL your GitHub repos (all 17+):

```bash
# Clone all repos you don't have locally
./sync-repos.sh --clone-all

# Pull latest on all repos
./sync-repos.sh --pull-all

# Smart sync: clone missing + pull existing
./sync-repos.sh

# Check status of all repos
./sync-repos.sh --status

# Push all uncommitted changes (with WIP message)
./sync-repos.sh --push-all
```

### Configuration

The script scans repos in `~/dev` and `~/Projects` by default. New repos are cloned to `~/dev`.

To customize, edit the `REPOS_DIRS` array in `sync-repos.sh`:

```bash
REPOS_DIRS=("$HOME/dev" "$HOME/Projects")
DEFAULT_CLONE_DIR="${REPOS_DIRS[0]}"
```

## Daily Workflow

### Before Switching Machines (Leaving Mac Mini)

Use the switch helper to check everything is pushed:

```bash
cd ~/dev/claude-skills/skills/mac-sync-dotfiles
./switch-machine.sh
```

This will:
1. Scan all 17 repos for uncommitted changes
2. Show any unpushed commits
3. Offer to auto-commit and push everything

Or do it manually:

```bash
# Push all repos with uncommitted changes
./sync-repos.sh --push-all
```

### When Starting on the Other Machine (MacBook)

```bash
cd ~/dev/claude-skills/skills/mac-sync-dotfiles

# Pull everything (scans ~/dev + ~/Projects)
./sync-repos.sh
```

### Quick Reference

| When | Command |
|------|---------|
| Leaving a machine | `./switch-machine.sh` |
| Arriving on new machine | `./sync-repos.sh` |
| Check status of all repos | `./sync-repos.sh --status` |

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
