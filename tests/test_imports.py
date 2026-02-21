"""Smoke tests: verify all Python scripts parse without syntax errors."""

import ast
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# All Python scripts in the repo
PYTHON_SCRIPTS = sorted(REPO_ROOT.rglob("*.py"))

# Exclude test files and __pycache__
PYTHON_SCRIPTS = [
    p for p in PYTHON_SCRIPTS
    if "tests/" not in str(p.relative_to(REPO_ROOT))
    and "__pycache__" not in str(p)
]


@pytest.mark.parametrize(
    "script_path",
    PYTHON_SCRIPTS,
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_script_parses(script_path: Path):
    """Each Python script should parse as valid Python (no syntax errors)."""
    source = script_path.read_text()
    ast.parse(source, filename=str(script_path))
