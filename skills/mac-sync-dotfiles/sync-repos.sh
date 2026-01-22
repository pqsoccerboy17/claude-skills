#!/bin/bash
#
# GitHub Repos Sync
# Syncs ALL your GitHub repositories between machines
#
# Usage:
#   ./sync-repos.sh              # Sync all repos (clone missing, pull existing)
#   ./sync-repos.sh --clone-all  # Initial clone of all repos
#   ./sync-repos.sh --pull-all   # Pull latest on all existing repos
#   ./sync-repos.sh --status     # Show status of all repos
#   ./sync-repos.sh --export     # Export repo list to repos.txt
#

set -e

# Configuration - customize these
GITHUB_USERNAME="${GITHUB_USERNAME:-$(gh api user --jq .login 2>/dev/null || echo '')}"
REPOS_DIR="${REPOS_DIR:-$HOME/repos}"
REPOS_MANIFEST="$HOME/dotfiles/repos.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 GitHub Repos Sync${NC}"
echo "================================"
echo ""

# Check prerequisites
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) not found${NC}"
    echo "Install it with: brew install gh"
    echo "Then authenticate: gh auth login"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get username if not set
if [ -z "$GITHUB_USERNAME" ]; then
    GITHUB_USERNAME=$(gh api user --jq .login)
fi

echo "GitHub User: $GITHUB_USERNAME"
echo "Repos Directory: $REPOS_DIR"
echo ""

# ============================================
# Functions
# ============================================

get_all_repos() {
    gh repo list "$GITHUB_USERNAME" --limit 100 --json name,sshUrl,isPrivate,updatedAt \
        --jq '.[] | "\(.name)|\(.sshUrl)|\(.isPrivate)"'
}

export_repos() {
    echo -e "${BLUE}📋 Exporting repository list...${NC}"

    mkdir -p "$(dirname "$REPOS_MANIFEST")"

    echo "# GitHub Repositories for $GITHUB_USERNAME" > "$REPOS_MANIFEST"
    echo "# Generated: $(date)" >> "$REPOS_MANIFEST"
    echo "# Format: name|ssh_url|is_private" >> "$REPOS_MANIFEST"
    echo "" >> "$REPOS_MANIFEST"

    get_all_repos >> "$REPOS_MANIFEST"

    REPO_COUNT=$(grep -v "^#" "$REPOS_MANIFEST" | grep -v "^$" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ Exported $REPO_COUNT repositories to $REPOS_MANIFEST${NC}"
}

clone_all() {
    echo -e "${BLUE}📥 Cloning all repositories...${NC}"
    echo ""

    mkdir -p "$REPOS_DIR"
    cd "$REPOS_DIR"

    local cloned=0
    local skipped=0
    local failed=0

    while IFS='|' read -r name ssh_url is_private; do
        # Skip comments and empty lines
        [[ "$name" =~ ^#.*$ ]] && continue
        [[ -z "$name" ]] && continue

        if [ -d "$REPOS_DIR/$name" ]; then
            echo -e "  ${YELLOW}⏭️  $name${NC} (already exists)"
            ((skipped++))
        else
            echo -e "  ${BLUE}📦 Cloning $name...${NC}"
            if git clone "$ssh_url" "$REPOS_DIR/$name" 2>/dev/null; then
                echo -e "  ${GREEN}✓ $name${NC}"
                ((cloned++))
            else
                echo -e "  ${RED}✗ Failed to clone $name${NC}"
                ((failed++))
            fi
        fi
    done < <(get_all_repos)

    echo ""
    echo "================================"
    echo -e "${GREEN}Cloned: $cloned${NC} | ${YELLOW}Skipped: $skipped${NC} | ${RED}Failed: $failed${NC}"
}

pull_all() {
    echo -e "${BLUE}📥 Pulling latest on all repositories...${NC}"
    echo ""

    if [ ! -d "$REPOS_DIR" ]; then
        echo -e "${RED}Error: Repos directory not found: $REPOS_DIR${NC}"
        exit 1
    fi

    local updated=0
    local unchanged=0
    local failed=0

    for repo_dir in "$REPOS_DIR"/*/; do
        [ -d "$repo_dir" ] || continue

        repo_name=$(basename "$repo_dir")

        if [ -d "$repo_dir/.git" ]; then
            cd "$repo_dir"

            # Get current branch
            branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

            # Fetch and check if updates available
            git fetch origin "$branch" 2>/dev/null

            local_commit=$(git rev-parse HEAD 2>/dev/null)
            remote_commit=$(git rev-parse "origin/$branch" 2>/dev/null || echo "")

            if [ "$local_commit" != "$remote_commit" ] && [ -n "$remote_commit" ]; then
                echo -e "  ${BLUE}⬇️  $repo_name${NC} (pulling...)"
                if git pull origin "$branch" 2>/dev/null; then
                    echo -e "  ${GREEN}✓ $repo_name${NC}"
                    ((updated++))
                else
                    echo -e "  ${RED}✗ $repo_name (merge conflict or error)${NC}"
                    ((failed++))
                fi
            else
                echo -e "  ${GREEN}✓ $repo_name${NC} (up to date)"
                ((unchanged++))
            fi

            cd "$REPOS_DIR"
        fi
    done

    echo ""
    echo "================================"
    echo -e "${GREEN}Updated: $updated${NC} | Unchanged: $unchanged | ${RED}Failed: $failed${NC}"
}

sync_all() {
    echo -e "${BLUE}🔄 Syncing all repositories...${NC}"
    echo ""

    mkdir -p "$REPOS_DIR"

    local cloned=0
    local updated=0
    local unchanged=0
    local failed=0

    while IFS='|' read -r name ssh_url is_private; do
        [[ "$name" =~ ^#.*$ ]] && continue
        [[ -z "$name" ]] && continue

        repo_dir="$REPOS_DIR/$name"

        if [ ! -d "$repo_dir" ]; then
            # Clone if doesn't exist
            echo -e "  ${BLUE}📦 Cloning $name...${NC}"
            if git clone "$ssh_url" "$repo_dir" 2>/dev/null; then
                echo -e "  ${GREEN}✓ $name (cloned)${NC}"
                ((cloned++))
            else
                echo -e "  ${RED}✗ Failed to clone $name${NC}"
                ((failed++))
            fi
        else
            # Pull if exists
            cd "$repo_dir"
            branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

            # Check for uncommitted changes
            if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
                echo -e "  ${YELLOW}⚠️  $name (has uncommitted changes, skipping pull)${NC}"
                ((unchanged++))
            else
                git fetch origin "$branch" 2>/dev/null || true

                local_commit=$(git rev-parse HEAD 2>/dev/null)
                remote_commit=$(git rev-parse "origin/$branch" 2>/dev/null || echo "$local_commit")

                if [ "$local_commit" != "$remote_commit" ]; then
                    if git pull origin "$branch" 2>/dev/null; then
                        echo -e "  ${GREEN}✓ $name (updated)${NC}"
                        ((updated++))
                    else
                        echo -e "  ${RED}✗ $name (pull failed)${NC}"
                        ((failed++))
                    fi
                else
                    echo -e "  ${GREEN}✓ $name${NC}"
                    ((unchanged++))
                fi
            fi
            cd "$REPOS_DIR"
        fi
    done < <(get_all_repos)

    echo ""
    echo "================================"
    echo -e "${GREEN}Cloned: $cloned | Updated: $updated${NC} | Unchanged: $unchanged | ${RED}Failed: $failed${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Repository Status${NC}"
    echo ""

    if [ ! -d "$REPOS_DIR" ]; then
        echo -e "${YELLOW}Repos directory not found: $REPOS_DIR${NC}"
        echo "Run: ./sync-repos.sh --clone-all"
        exit 0
    fi

    local clean=0
    local dirty=0
    local ahead=0
    local behind=0

    printf "%-30s %-10s %-15s %s\n" "REPOSITORY" "BRANCH" "STATUS" "CHANGES"
    printf "%-30s %-10s %-15s %s\n" "----------" "------" "------" "-------"

    for repo_dir in "$REPOS_DIR"/*/; do
        [ -d "$repo_dir/.git" ] || continue

        repo_name=$(basename "$repo_dir")
        cd "$repo_dir"

        branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "???")

        # Check for uncommitted changes
        changes=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

        # Check ahead/behind
        git fetch origin "$branch" 2>/dev/null || true
        ahead_count=$(git rev-list --count "origin/$branch..HEAD" 2>/dev/null || echo "0")
        behind_count=$(git rev-list --count "HEAD..origin/$branch" 2>/dev/null || echo "0")

        if [ "$changes" -gt 0 ]; then
            status="${YELLOW}uncommitted${NC}"
            ((dirty++))
        elif [ "$ahead_count" -gt 0 ]; then
            status="${BLUE}ahead $ahead_count${NC}"
            ((ahead++))
        elif [ "$behind_count" -gt 0 ]; then
            status="${YELLOW}behind $behind_count${NC}"
            ((behind++))
        else
            status="${GREEN}clean${NC}"
            ((clean++))
        fi

        printf "%-30s %-10s " "$repo_name" "$branch"
        echo -e "$status"

        cd "$REPOS_DIR"
    done

    echo ""
    echo "================================"
    echo -e "Total: $((clean + dirty + ahead + behind)) repos"
    echo -e "${GREEN}Clean: $clean${NC} | ${YELLOW}Uncommitted: $dirty${NC} | ${BLUE}Ahead: $ahead${NC} | Behind: $behind"
}

push_all_uncommitted() {
    echo -e "${BLUE}📤 Pushing all uncommitted changes...${NC}"
    echo ""
    echo -e "${YELLOW}Warning: This will commit and push ALL uncommitted changes${NC}"
    read -p "Continue? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi

    for repo_dir in "$REPOS_DIR"/*/; do
        [ -d "$repo_dir/.git" ] || continue

        repo_name=$(basename "$repo_dir")
        cd "$repo_dir"

        if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            echo -e "  ${BLUE}📤 $repo_name${NC}"
            branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
            git add -A
            git commit -m "Sync from $(hostname) - $(date '+%Y-%m-%d %H:%M')"
            git push origin "$branch"
            echo -e "  ${GREEN}✓ $repo_name pushed${NC}"
        fi

        cd "$REPOS_DIR"
    done
}

# ============================================
# Main
# ============================================

case "${1:-}" in
    --clone-all)
        clone_all
        ;;
    --pull-all)
        pull_all
        ;;
    --status)
        show_status
        ;;
    --export)
        export_repos
        ;;
    --push-all)
        push_all_uncommitted
        ;;
    --help|-h)
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  (no option)    Sync all repos (clone missing, pull existing)"
        echo "  --clone-all    Clone all repos from GitHub"
        echo "  --pull-all     Pull latest on all local repos"
        echo "  --status       Show status of all local repos"
        echo "  --push-all     Commit and push all uncommitted changes"
        echo "  --export       Export repo list to ~/dotfiles/repos.txt"
        echo ""
        echo "Environment variables:"
        echo "  GITHUB_USERNAME  Your GitHub username (auto-detected if gh authenticated)"
        echo "  REPOS_DIR        Directory for repos (default: ~/repos)"
        ;;
    *)
        sync_all
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
