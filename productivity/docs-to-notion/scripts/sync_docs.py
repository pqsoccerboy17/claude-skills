#!/usr/bin/env python3
"""
Sync MkDocs documentation to Notion for mobile access.

Mirrors the docs/ directory structure to Notion pages, converting
markdown content to Notion blocks.

Requirements:
    pip install notion-client markdown

Environment:
    NOTION_TOKEN - Notion integration token
    NOTION_DOCS_PARENT_PAGE_ID - Parent page ID for docs mirror

Usage:
    python sync_docs.py [--dry-run]
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    from notion_client import Client
except ImportError:
    print("Error: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)


class NotionDocsSyncer:
    """Syncs markdown docs to Notion pages."""

    def __init__(self, token: str, parent_page_id: str, dry_run: bool = False):
        self.client = Client(auth=token)
        self.parent_page_id = parent_page_id
        self.dry_run = dry_run
        self.created_pages = {}

    def sync_directory(self, docs_path: Path) -> dict:
        """
        Sync entire docs directory to Notion.

        Returns dict mapping file paths to Notion page IDs.
        """
        print(f"Syncing docs from: {docs_path}")

        if not docs_path.exists():
            print(f"Error: Docs path does not exist: {docs_path}")
            return {}

        # Create root page
        root_page_id = self._create_or_update_page(
            parent_id=self.parent_page_id,
            title="📚 Documentation",
            content="Auto-synced from MkDocs documentation.",
            is_database=False
        )

        if not root_page_id:
            return {}

        # Process index.md first if it exists
        index_path = docs_path / "index.md"
        if index_path.exists():
            self._sync_file(index_path, root_page_id, "🏠 Home")

        # Process subdirectories
        for subdir in sorted(docs_path.iterdir()):
            if subdir.is_dir() and not subdir.name.startswith('.'):
                self._sync_subdirectory(subdir, root_page_id)

        return self.created_pages

    def _sync_subdirectory(self, subdir: Path, parent_page_id: str):
        """Sync a subdirectory as a Notion page with children."""
        dir_name = subdir.name.replace('-', ' ').title()
        icons = {
            'skills': '⚡',
            'guides': '📖',
            'architecture': '🏗️',
        }
        icon = icons.get(subdir.name, '📁')

        # Create section page
        section_title = f"{icon} {dir_name}"
        section_id = self._create_or_update_page(
            parent_id=parent_page_id,
            title=section_title,
            content=f"Documentation for {dir_name.lower()}.",
            is_database=False
        )

        if not section_id:
            return

        # Process markdown files in this directory
        for md_file in sorted(subdir.glob("*.md")):
            file_title = md_file.stem.replace('-', ' ').title()
            if file_title.lower() == 'index':
                file_title = f"{dir_name} Overview"
            self._sync_file(md_file, section_id, file_title)

    def _sync_file(self, file_path: Path, parent_id: str, title: str):
        """Sync a single markdown file to Notion."""
        print(f"  Syncing: {file_path.name} -> {title}")

        content = file_path.read_text()
        blocks = self._markdown_to_blocks(content)

        page_id = self._create_or_update_page(
            parent_id=parent_id,
            title=title,
            blocks=blocks,
            is_database=False
        )

        if page_id:
            self.created_pages[str(file_path)] = page_id

    def _create_or_update_page(
        self,
        parent_id: str,
        title: str,
        content: str = None,
        blocks: list = None,
        is_database: bool = False
    ) -> Optional[str]:
        """Create a Notion page under the given parent."""
        if self.dry_run:
            print(f"    [DRY RUN] Would create page: {title}")
            return f"dry-run-{title}"

        try:
            children = blocks if blocks else []
            if content and not blocks:
                children = [{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }]

            page = self.client.pages.create(
                parent={"page_id": parent_id},
                properties={
                    "title": {
                        "title": [{"type": "text", "text": {"content": title}}]
                    }
                },
                children=children[:100]  # Notion limit
            )

            print(f"    Created: {title}")
            return page["id"]

        except Exception as e:
            print(f"    Error creating page '{title}': {e}")
            return None

    def _markdown_to_blocks(self, markdown: str) -> list:
        """Convert markdown to Notion blocks."""
        blocks = []
        lines = markdown.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Skip YAML frontmatter
            if i == 0 and line.strip() == '---':
                i += 1
                while i < len(lines) and lines[i].strip() != '---':
                    i += 1
                i += 1
                continue

            # Headers
            if line.startswith('#'):
                match = re.match(r'^(#+)\s*(.+)$', line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2)
                    block_type = {
                        1: "heading_1",
                        2: "heading_2",
                        3: "heading_3"
                    }.get(level, "heading_3")

                    blocks.append({
                        "object": "block",
                        "type": block_type,
                        block_type: {
                            "rich_text": [{"type": "text", "text": {"content": text}}]
                        }
                    })
                    i += 1
                    continue

            # Code blocks
            if line.startswith('```'):
                language = line[3:].strip() or "plain text"
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1

                code_content = '\n'.join(code_lines)[:2000]  # Notion limit
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_content}}],
                        "language": language if language in NOTION_LANGUAGES else "plain text"
                    }
                })
                i += 1
                continue

            # Bullet lists
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                text = re.sub(r'^[\s]*[-*]\s*', '', line)
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": self._parse_inline_formatting(text)
                    }
                })
                i += 1
                continue

            # Numbered lists
            if re.match(r'^\s*\d+\.\s', line):
                text = re.sub(r'^\s*\d+\.\s*', '', line)
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": self._parse_inline_formatting(text)
                    }
                })
                i += 1
                continue

            # Blockquotes / admonitions
            if line.strip().startswith('>') or line.strip().startswith('!!! '):
                text = re.sub(r'^[\s]*[>!]+\s*', '', line)
                blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": text}}],
                        "icon": {"emoji": "💡"}
                    }
                })
                i += 1
                continue

            # Regular paragraph
            if line.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": self._parse_inline_formatting(line)
                    }
                })

            i += 1

        return blocks

    def _parse_inline_formatting(self, text: str) -> list:
        """Parse inline markdown formatting to Notion rich text."""
        # Simple implementation - just return plain text
        # Full implementation would handle **bold**, *italic*, `code`, [links]()

        rich_text = []

        # Handle inline code
        parts = re.split(r'(`[^`]+`)', text)
        for part in parts:
            if part.startswith('`') and part.endswith('`'):
                rich_text.append({
                    "type": "text",
                    "text": {"content": part[1:-1]},
                    "annotations": {"code": True}
                })
            elif part:
                # Handle bold
                bold_parts = re.split(r'(\*\*[^*]+\*\*)', part)
                for bp in bold_parts:
                    if bp.startswith('**') and bp.endswith('**'):
                        rich_text.append({
                            "type": "text",
                            "text": {"content": bp[2:-2]},
                            "annotations": {"bold": True}
                        })
                    elif bp:
                        rich_text.append({
                            "type": "text",
                            "text": {"content": bp}
                        })

        return rich_text if rich_text else [{"type": "text", "text": {"content": text}}]


# Notion supported languages for code blocks
NOTION_LANGUAGES = {
    "abap", "arduino", "bash", "basic", "c", "clojure", "coffeescript", "cpp",
    "csharp", "css", "dart", "diff", "docker", "elixir", "elm", "erlang",
    "flow", "fortran", "fsharp", "gherkin", "glsl", "go", "graphql", "groovy",
    "haskell", "html", "java", "javascript", "json", "julia", "kotlin", "latex",
    "less", "lisp", "livescript", "lua", "makefile", "markdown", "markup",
    "matlab", "mermaid", "nix", "objective-c", "ocaml", "pascal", "perl", "php",
    "plain text", "powershell", "prolog", "protobuf", "python", "r", "reason",
    "ruby", "rust", "sass", "scala", "scheme", "scss", "shell", "sql", "swift",
    "typescript", "vb.net", "verilog", "vhdl", "visual basic", "webassembly",
    "xml", "yaml", "java/c/c++/c#"
}


def main():
    parser = argparse.ArgumentParser(description="Sync MkDocs docs to Notion")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating pages")
    parser.add_argument("--docs-path", default="docs", help="Path to docs directory")
    args = parser.parse_args()

    # Get configuration from environment
    token = os.environ.get("NOTION_TOKEN")
    parent_page_id = os.environ.get("NOTION_DOCS_PARENT_PAGE_ID")

    if not token:
        print("Error: NOTION_TOKEN environment variable not set")
        print("Get your token from: https://www.notion.so/my-integrations")
        sys.exit(1)

    if not parent_page_id:
        print("Error: NOTION_DOCS_PARENT_PAGE_ID environment variable not set")
        print("This should be the ID of the Notion page where docs will be created")
        print("Find it in the page URL: notion.so/Page-Name-<PAGE_ID>")
        sys.exit(1)

    # Find docs directory
    docs_path = Path(args.docs_path)
    if not docs_path.is_absolute():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent.parent.parent
        docs_path = script_dir / args.docs_path

    syncer = NotionDocsSyncer(token, parent_page_id, dry_run=args.dry_run)
    results = syncer.sync_directory(docs_path)

    print(f"\nSync complete. Created {len(results)} pages.")

    if args.dry_run:
        print("\n[DRY RUN] No pages were actually created.")


if __name__ == "__main__":
    main()
