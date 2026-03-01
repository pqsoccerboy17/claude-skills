"""Tests for the file organizer module."""

import sys
import tempfile
from pathlib import Path

import pytest

# Add the file-organizer script to the path
ORGANIZER_DIR = Path(__file__).resolve().parent.parent / "productivity" / "file-organizer" / "scripts"
sys.path.insert(0, str(ORGANIZER_DIR))

import organize


class TestCategorizeFile:
    """Tests for categorize_file function."""

    def test_keyword_invoice(self):
        assert organize.categorize_file("invoice-2024-001.pdf") == "Invoices"

    def test_keyword_tax(self):
        assert organize.categorize_file("tax-return-2024.pdf") == "Tax"

    def test_keyword_receipt(self):
        assert organize.categorize_file("receipt-amazon-march.pdf") == "Receipts"

    def test_keyword_contract(self):
        assert organize.categorize_file("contract-client-abc.docx") == "Contracts"

    def test_keyword_statement(self):
        assert organize.categorize_file("bank-statement-jan.pdf") == "Statements"

    def test_extension_pdf(self):
        assert organize.categorize_file("random-document.pdf") == "Financial"

    def test_extension_jpg(self):
        assert organize.categorize_file("photo.jpg") == "Images"

    def test_extension_png(self):
        assert organize.categorize_file("screenshot.png") == "Images"

    def test_extension_docx(self):
        assert organize.categorize_file("notes.docx") == "Documents"

    def test_extension_zip(self):
        assert organize.categorize_file("backup.zip") == "Archives"

    def test_extension_pptx(self):
        assert organize.categorize_file("slides.pptx") == "Presentations"

    def test_unknown_extension(self):
        assert organize.categorize_file("data.xyz") == "Other"

    def test_no_extension(self):
        assert organize.categorize_file("README") == "Other"

    def test_keyword_priority_over_extension(self):
        # Keywords are checked first, so "invoice.jpg" should be Invoices not Images
        assert organize.categorize_file("invoice-photo.jpg") == "Invoices"

    def test_case_insensitive_keyword(self):
        assert organize.categorize_file("INVOICE-2024.PDF") == "Invoices"


class TestOrganizeByType:
    """Tests for organize_by_type with dry_run."""

    def test_dry_run_categorizes_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            dest = Path(tmpdir) / "dest"
            source.mkdir()
            dest.mkdir()

            # Create test files
            (source / "invoice-001.pdf").write_text("test")
            (source / "photo.jpg").write_text("test")
            (source / "notes.txt").write_text("test")

            results = organize.organize_by_type(source, dest, dry_run=True)

            assert len(results["moved"]) == 3
            assert len(results["errors"]) == 0

    def test_dry_run_skips_hidden_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            dest = Path(tmpdir) / "dest"
            source.mkdir()
            dest.mkdir()

            (source / ".hidden").write_text("hidden")
            (source / "visible.txt").write_text("visible")

            results = organize.organize_by_type(source, dest, dry_run=True)

            assert len(results["moved"]) == 1

    def test_dry_run_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            dest = Path(tmpdir) / "dest"
            source.mkdir()
            dest.mkdir()

            (source / "test.pdf").write_text("test")

            organize.organize_by_type(source, dest, dry_run=True)

            # File should still be in source
            assert (source / "test.pdf").exists()
            # No subdirectories created in dest
            assert len(list(dest.iterdir())) == 0
