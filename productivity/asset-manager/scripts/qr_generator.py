#!/usr/bin/env python3
"""
QR Code Generator for Asset Management

Generate QR codes that link to Notion asset pages for easy scanning and access.

Usage:
    # Generate QR code for a single asset
    python3 qr_generator.py --asset-id "TH-HVAC-01" --notion-url "https://notion.so/page-id"

    # Generate QR code with custom output path
    python3 qr_generator.py --asset-id "TH-HVAC-01" --notion-url "https://notion.so/page-id" \
        --output ~/Desktop/qr-codes/

    # Generate QR codes for multiple assets from a file
    python3 qr_generator.py --batch assets.csv

    # Generate with custom size
    python3 qr_generator.py --asset-id "TH-HVAC-01" --notion-url "https://notion.so/page-id" \
        --size 300

Requirements:
    pip install qrcode pillow

CSV Format for batch mode:
    asset_id,notion_url
    TH-HVAC-01,https://notion.so/page-id-1
    TH-APPL-01,https://notion.so/page-id-2
"""

import argparse
import csv
import os
import sys
from pathlib import Path

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Required libraries not found.")
    print("Install with: pip install qrcode pillow")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Desktop/qr-codes")
DEFAULT_QR_SIZE = 200  # pixels
DEFAULT_BORDER = 4  # QR code border (modules)
LABEL_HEIGHT = 40  # pixels for asset ID label


# =============================================================================
# QR Code Generation
# =============================================================================

def generate_qr_code(
    asset_id: str,
    notion_url: str,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    size: int = DEFAULT_QR_SIZE,
    include_label: bool = True
) -> str:
    """
    Generate a QR code image for an asset.

    Args:
        asset_id: The asset identifier (e.g., TH-HVAC-01)
        notion_url: The Notion page URL to encode
        output_dir: Directory to save the QR code image
        size: Size of the QR code in pixels
        include_label: Whether to include asset ID label below QR

    Returns:
        Path to the generated QR code image
    """
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=DEFAULT_BORDER,
    )
    qr.add_data(notion_url)
    qr.make(fit=True)

    # Create QR image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Resize to desired size
    qr_image = qr_image.resize((size, size), Image.Resampling.LANCZOS)

    if include_label:
        # Create new image with space for label
        total_height = size + LABEL_HEIGHT
        final_image = Image.new("RGB", (size, total_height), "white")

        # Paste QR code
        final_image.paste(qr_image, (0, 0))

        # Add label
        draw = ImageDraw.Draw(final_image)

        # Try to use a nice font, fall back to default
        try:
            # Try common system fonts
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
                "/System/Library/Fonts/Menlo.ttc",
                "/System/Library/Fonts/Monaco.dfont",
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 16)
                    break
            if font is None:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        # Calculate text position (centered)
        text_bbox = draw.textbbox((0, 0), asset_id, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (size - text_width) // 2
        text_y = size + (LABEL_HEIGHT - 20) // 2

        draw.text((text_x, text_y), asset_id, fill="black", font=font)

        output_image = final_image
    else:
        output_image = qr_image

    # Save image
    filename = f"{asset_id.lower()}_qr.png"
    filepath = output_path / filename
    output_image.save(filepath)

    print(f"Generated: {filepath}")
    return str(filepath)


def generate_batch(
    csv_file: str,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    size: int = DEFAULT_QR_SIZE
) -> list:
    """
    Generate QR codes for multiple assets from a CSV file.

    CSV format:
        asset_id,notion_url
        TH-HVAC-01,https://notion.so/page-id-1
        TH-APPL-01,https://notion.so/page-id-2

    Args:
        csv_file: Path to CSV file
        output_dir: Directory to save QR code images
        size: Size of QR codes in pixels

    Returns:
        List of generated file paths
    """
    generated = []

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_id = row.get("asset_id", "").strip()
            notion_url = row.get("notion_url", "").strip()

            if not asset_id or not notion_url:
                print(f"Skipping invalid row: {row}")
                continue

            filepath = generate_qr_code(
                asset_id=asset_id,
                notion_url=notion_url,
                output_dir=output_dir,
                size=size
            )
            generated.append(filepath)

    print(f"\nGenerated {len(generated)} QR codes in {output_dir}")
    return generated


def create_print_sheet(
    qr_files: list,
    output_path: str = None,
    codes_per_row: int = 4
) -> str:
    """
    Create a printable sheet with multiple QR codes.

    Args:
        qr_files: List of QR code image file paths
        output_path: Path for the output sheet (default: qr_print_sheet.png)
        codes_per_row: Number of QR codes per row

    Returns:
        Path to the print sheet image
    """
    if not qr_files:
        print("No QR codes to create sheet from")
        return None

    # Load first image to get dimensions
    sample = Image.open(qr_files[0])
    code_width, code_height = sample.size

    # Calculate sheet dimensions
    num_codes = len(qr_files)
    num_rows = (num_codes + codes_per_row - 1) // codes_per_row

    padding = 20
    sheet_width = codes_per_row * code_width + (codes_per_row + 1) * padding
    sheet_height = num_rows * code_height + (num_rows + 1) * padding

    # Create sheet
    sheet = Image.new("RGB", (sheet_width, sheet_height), "white")

    # Paste QR codes
    for i, qr_file in enumerate(qr_files):
        row = i // codes_per_row
        col = i % codes_per_row

        x = padding + col * (code_width + padding)
        y = padding + row * (code_height + padding)

        qr_img = Image.open(qr_file)
        sheet.paste(qr_img, (x, y))

    # Save sheet
    if output_path is None:
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, "qr_print_sheet.png")

    sheet.save(output_path)
    print(f"\nCreated print sheet: {output_path}")
    return output_path


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate QR codes for asset management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Single QR code
    python3 qr_generator.py --asset-id "TH-HVAC-01" --notion-url "https://notion.so/page-id"

    # Batch from CSV
    python3 qr_generator.py --batch assets.csv

    # Create print sheet from existing QR codes
    python3 qr_generator.py --print-sheet ~/Desktop/qr-codes/
        """
    )

    parser.add_argument("--asset-id", help="Asset ID (e.g., TH-HVAC-01)")
    parser.add_argument("--notion-url", help="Notion page URL")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--size", type=int, default=DEFAULT_QR_SIZE, help="QR code size in pixels")
    parser.add_argument("--no-label", action="store_true", help="Don't include asset ID label")
    parser.add_argument("--batch", help="CSV file for batch generation")
    parser.add_argument("--print-sheet", help="Create print sheet from QR codes in directory")

    args = parser.parse_args()

    if args.batch:
        # Batch mode
        qr_files = generate_batch(
            csv_file=args.batch,
            output_dir=args.output,
            size=args.size
        )
        # Optionally create print sheet
        if qr_files:
            create_print_sheet(qr_files)

    elif args.print_sheet:
        # Create print sheet from existing QR codes
        qr_dir = Path(args.print_sheet)
        qr_files = sorted(qr_dir.glob("*_qr.png"))
        if qr_files:
            create_print_sheet([str(f) for f in qr_files])
        else:
            print(f"No QR codes found in {args.print_sheet}")

    elif args.asset_id and args.notion_url:
        # Single QR code
        generate_qr_code(
            asset_id=args.asset_id,
            notion_url=args.notion_url,
            output_dir=args.output,
            size=args.size,
            include_label=not args.no_label
        )

    else:
        parser.print_help()
        print("\nError: Provide --asset-id and --notion-url, or --batch, or --print-sheet")
        sys.exit(1)


if __name__ == "__main__":
    main()
