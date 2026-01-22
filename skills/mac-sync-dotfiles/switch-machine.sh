#!/bin/bash
#
# Machine Switch Helper
# Run this BEFORE switching to your other Mac
#
# This script:
#   1. Shows status of all repos (uncommitted changes, unpushed commits)
#   2. Optionally commits and pushes everything
#   3. Syncs your dotfiles
#

set -e

# Multiple repo directories
REPOS_DIRS=("$HOME/dev" "$HOME/Projects")
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}🔄 Machine Switch Preparation${NC}"
echo "======================================"
echo ""
echo "Current machine: $(hostname)"
echo "Date: $(date)"
echo ""

# ============================================
# Helper function
# ============================================

# Iterate over all local repos (outputs: path|name)
for_each_local_repo() {
    for dir in "${REPOS_DIRS[@]}"; do
        [ -d "$dir" ] || continue
        for repo_dir in "$dir"/*/; do
            [ -d "$repo_dir/.git" ] || continue
            repo_name=$(basename "$repo_dir")
            echo "$repo_dir|$repo_name"
        done
    done
}

# ============================================
# Check for uncommitted changes
# ============================================
echo -e "${BOLD}📊 Checking repositories for uncommitted changes...${NC}"
echo ""

# Store repo paths for later (name|path format)
declare -A repo_paths
uncommitted_repos=()
unpushed_repos=()

while IFS='|' read -r repo_dir repo_name; do
    repo_paths["$repo_name"]="$repo_dir"
    cd "$repo_dir"

    # Check for uncommitted changes
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        uncommitted_repos+=("$repo_name")
        changes=$(git status --porcelain | wc -l | tr -d ' ')
        location=$(dirname "$repo_dir" | xargs basename)
        echo -e "  ${YELLOW}⚠️  $repo_name${NC} (~/$location) - $changes uncommitted changes"
    fi

    # Check for unpushed commits
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    ahead=$(git rev-list --count "origin/$branch..HEAD" 2>/dev/null || echo "0")
    if [ "$ahead" -gt 0 ]; then
        unpushed_repos+=("$repo_name")
        location=$(dirname "$repo_dir" | xargs basename)
        echo -e "  ${BLUE}📤 $repo_name${NC} (~/$location) - $ahead unpushed commits"
    fi
done < <(for_each_local_repo)

# Also check dotfiles
if [ -d "$DOTFILES_DIR/.git" ]; then
    cd "$DOTFILES_DIR"
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        uncommitted_repos+=("dotfiles")
        echo -e "  ${YELLOW}⚠️  dotfiles${NC} - uncommitted changes"
    fi
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    ahead=$(git rev-list --count "origin/$branch..HEAD" 2>/dev/null || echo "0")
    if [ "$ahead" -gt 0 ]; then
        unpushed_repos+=("dotfiles")
        echo -e "  ${BLUE}📤 dotfiles${NC} - $ahead unpushed commits"
    fi
fi

echo ""

# ============================================
# Summary and action
# ============================================
if [ ${#uncommitted_repos[@]} -eq 0 ] && [ ${#unpushed_repos[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ All repositories are clean and pushed!${NC}"
    echo ""
    echo "You're ready to switch machines. On your other Mac, run:"
    echo -e "  ${BOLD}cd ~/dev/claude-skills/skills/mac-sync-dotfiles && ./sync-repos.sh${NC}"
    exit 0
fi

echo -e "${BOLD}Summary:${NC}"
echo -e "  ${YELLOW}Uncommitted: ${#uncommitted_repos[@]} repos${NC}"
echo -e "  ${BLUE}Unpushed: ${#unpushed_repos[@]} repos${NC}"
echo ""

# ============================================
# Offer to fix
# ============================================
echo -e "${BOLD}What would you like to do?${NC}"
echo "  1) Commit and push all changes (auto WIP commit message)"
echo "  2) Show detailed status for each repo"
echo "  3) Exit (I'll handle it manually)"
echo ""
read -p "Choice [1/2/3]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Committing and pushing all changes...${NC}"
        echo ""

        for repo_name in "${uncommitted_repos[@]}"; do
            if [ "$repo_name" = "dotfiles" ]; then
                repo_dir="$DOTFILES_DIR"
            else
                repo_dir="${repo_paths[$repo_name]}"
            fi

            cd "$repo_dir"
            echo -e "  ${BLUE}📦 $repo_name${NC}"

            branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
            git add -A
            git commit -m "WIP: Sync from $(hostname) - $(date '+%Y-%m-%d %H:%M')"
            git push origin "$branch" 2>/dev/null || git push -u origin "$branch"

            echo -e "  ${GREEN}✓ $repo_name committed and pushed${NC}"
        done

        # Push any that only had unpushed commits
        for repo_name in "${unpushed_repos[@]}"; do
            # Skip if already handled above
            [[ " ${uncommitted_repos[*]} " =~ " ${repo_name} " ]] && continue

            if [ "$repo_name" = "dotfiles" ]; then
                repo_dir="$DOTFILES_DIR"
            else
                repo_dir="${repo_paths[$repo_name]}"
            fi

            cd "$repo_dir"
            echo -e "  ${BLUE}📤 $repo_name${NC}"

            branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
            git push origin "$branch" 2>/dev/null || git push -u origin "$branch"

            echo -e "  ${GREEN}✓ $repo_name pushed${NC}"
        done

        echo ""
        echo -e "${GREEN}✅ All done! Ready to switch machines.${NC}"
        echo ""
        echo "On your other Mac, run:"
        echo -e "  ${BOLD}cd ~/dev/claude-skills/skills/mac-sync-dotfiles && ./sync-repos.sh${NC}"
        ;;

    2)
        echo ""
        for repo_name in "${uncommitted_repos[@]}" "${unpushed_repos[@]}"; do
            # Remove duplicates
            if [ "$repo_name" = "dotfiles" ]; then
                repo_dir="$DOTFILES_DIR"
            else
                repo_dir="${repo_paths[$repo_name]}"
            fi

            [ -d "$repo_dir" ] || continue
            cd "$repo_dir"

            location=$(dirname "$repo_dir" | xargs basename)
            echo -e "${BOLD}━━━ $repo_name (~/$location) ━━━${NC}"
            git status -s
            echo ""
        done
        ;;

    *)
        echo "Exiting. Don't forget to commit and push before switching!"
        ;;
esac
