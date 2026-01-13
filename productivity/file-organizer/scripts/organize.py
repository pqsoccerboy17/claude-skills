#!/usr/bin/env python3
"""
File Organizer - Business document organization utility
Supports organization by date, type, or custom rules
"""

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CATEGORY_RULES = {
    'Financial': ['.pdf', '.csv', '.xlsx', '.xls'],
    'Images': ['.jpg', '.jpeg', '.png', '.heic', '.gif', '.webp'],
    'Documents': ['.doc', '.docx', '.txt', '.rtf', '.md'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Presentations': ['.ppt', '.pptx', '.key'],
    'Spreadsheets': ['.xlsx', '.xls', '.csv', '.numbers'],
}

KEYWORD_RULES = {
    'Invoices': ['invoice', 'inv-', 'inv_', 'bill'],
    'Statements': ['statement', 'stmt', 'bank'],
    'Receipts': ['receipt', 'rcpt', 'purchase'],
    'Contracts': ['contract', 'agreement', 'lease', 'msa'],
    'Tax': ['tax', '1099', 'w2', 'w-2', '1040'],
}


def categorize_file(filename: str) -> str:
    """Determine category based on extension and keywords"""
    name_lower = filename.lower()
    ext = Path(filename).suffix.lower()

    # Check keywords first (more specific)
    for category, keywords in KEYWORD_RULES.items():
        if any(kw in name_lower for kw in keywords):
            return category

    # Fall back to extension-based categorization
    for category, extensions in CATEGORY_RULES.items():
        if ext in extensions:
            return category

    return 'Other'


def organize_by_type(source_dir: Path, dest_dir: Path, dry_run: bool = False) -> dict:
    """Organize files by type/category"""
    results = {'moved': [], 'skipped': [], 'errors': []}

    for file in source_dir.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            category = categorize_file(file.name)
            target_dir = dest_dir / category
            target_path = target_dir / file.name

            if dry_run:
                logger.info(f"[DRY RUN] Would move {file.name} -> {category}/")
                results['moved'].append({'file': str(file), 'destination': str(target_path)})
            else:
                try:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), target_path)
                    logger.info(f"Moved {file.name} -> {category}/")
                    results['moved'].append({'file': str(file), 'destination': str(target_path)})
                except Exception as e:
                    logger.error(f"Error moving {file.name}: {e}")
                    results['errors'].append({'file': str(file), 'error': str(e)})

    return results


def organize_by_date(source_dir: Path, dest_dir: Path, dry_run: bool = False) -> dict:
    """Organize files into YYYY/MM folders by modification date"""
    results = {'moved': [], 'skipped': [], 'errors': []}

    for file in source_dir.rglob('*'):
        if file.is_file() and not file.name.startswith('.'):
            try:
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                target_dir = dest_dir / str(mtime.year) / f"{mtime.month:02d}"
                target_path = target_dir / file.name

                if dry_run:
                    logger.info(f"[DRY RUN] Would move {file.name} -> {mtime.year}/{mtime.month:02d}/")
                    results['moved'].append({'file': str(file), 'destination': str(target_path)})
                else:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), target_path)
                    logger.info(f"Moved {file.name} -> {mtime.year}/{mtime.month:02d}/")
                    results['moved'].append({'file': str(file), 'destination': str(target_path)})
            except Exception as e:
                logger.error(f"Error processing {file.name}: {e}")
                results['errors'].append({'file': str(file), 'error': str(e)})

    return results


def organize_hybrid(source_dir: Path, dest_dir: Path, dry_run: bool = False) -> dict:
    """Organize by category, then by date within each category"""
    results = {'moved': [], 'skipped': [], 'errors': []}

    for file in source_dir.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            try:
                category = categorize_file(file.name)
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                target_dir = dest_dir / category / str(mtime.year) / f"{mtime.month:02d}"
                target_path = target_dir / file.name

                if dry_run:
                    logger.info(f"[DRY RUN] Would move {file.name} -> {category}/{mtime.year}/{mtime.month:02d}/")
                    results['moved'].append({'file': str(file), 'destination': str(target_path)})
                else:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), target_path)
                    logger.info(f"Moved {file.name} -> {category}/{mtime.year}/{mtime.month:02d}/")
                    results['moved'].append({'file': str(file), 'destination': str(target_path)})
            except Exception as e:
                logger.error(f"Error processing {file.name}: {e}")
                results['errors'].append({'file': str(file), 'error': str(e)})

    return results


def main():
    parser = argparse.ArgumentParser(description='Organize files by type or date')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    parser.add_argument('--by-type', action='store_true', help='Organize by file type')
    parser.add_argument('--by-date', action='store_true', help='Organize by date')
    parser.add_argument('--hybrid', action='store_true', help='Organize by type, then date')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without moving')
    parser.add_argument('--output-json', help='Output results to JSON file')

    args = parser.parse_args()

    source = Path(args.source).expanduser()
    dest = Path(args.destination).expanduser()

    if not source.exists():
        logger.error(f"Source directory does not exist: {source}")
        return 1

    dest.mkdir(parents=True, exist_ok=True)

    if args.by_date:
        results = organize_by_date(source, dest, args.dry_run)
    elif args.hybrid:
        results = organize_hybrid(source, dest, args.dry_run)
    else:  # Default to by-type
        results = organize_by_type(source, dest, args.dry_run)

    # Summary
    print(f"\nSummary:")
    print(f"  Moved: {len(results['moved'])} files")
    print(f"  Errors: {len(results['errors'])} files")

    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(results, f, indent=2)

    return 0 if not results['errors'] else 1


if __name__ == '__main__':
    exit(main())
