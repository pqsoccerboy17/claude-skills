"""Tests for PDF processing scripts - syntax validation."""

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_SCRIPTS_DIR = REPO_ROOT / "document-processing" / "pdf" / "scripts"

# Collect all PDF Python scripts
PDF_SCRIPTS = sorted(PDF_SCRIPTS_DIR.glob("*.py")) if PDF_SCRIPTS_DIR.exists() else []


@pytest.mark.parametrize(
    "script_path",
    PDF_SCRIPTS,
    ids=lambda p: p.name,
)
def test_pdf_script_parses(script_path):
    """Each PDF script should be valid Python syntax."""
    source = script_path.read_text()
    ast.parse(source, filename=str(script_path))


class TestPdfScriptsExist:
    """Verify the PDF scripts directory has expected files."""

    def test_scripts_directory_exists(self):
        assert PDF_SCRIPTS_DIR.exists(), "PDF scripts directory should exist"

    def test_has_at_least_one_script(self):
        assert len(PDF_SCRIPTS) > 0, "Should have at least one PDF script"

    def test_check_fillable_fields_exists(self):
        assert (PDF_SCRIPTS_DIR / "check_fillable_fields.py").exists()

    def test_convert_pdf_to_images_exists(self):
        assert (PDF_SCRIPTS_DIR / "convert_pdf_to_images.py").exists()

    def test_fill_pdf_form_exists(self):
        assert (PDF_SCRIPTS_DIR / "fill_pdf_form_with_annotations.py").exists()
