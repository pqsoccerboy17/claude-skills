"""Tests for the CSV data summarizer module."""

import sys
import json
from pathlib import Path

import pytest

# Add the summarizer script to the path
SUMMARIZER_DIR = Path(__file__).resolve().parent.parent / "data-analysis" / "csv-data-summarizer" / "scripts"
sys.path.insert(0, str(SUMMARIZER_DIR))

import summarize

# pandas is required by summarize module
import pandas as pd


class TestDetectColumnTypes:
    """Tests for detect_column_types function."""

    def test_detects_date_columns(self):
        df = pd.DataFrame({"created_date": ["2024-01-01"], "name": ["test"]})
        types = summarize.detect_column_types(df)
        assert "created_date" in types["date_cols"]
        assert "name" not in types["date_cols"]

    def test_detects_amount_columns(self):
        df = pd.DataFrame({"total_amount": [100.0], "name": ["test"]})
        types = summarize.detect_column_types(df)
        assert "total_amount" in types["amount_cols"]

    def test_detects_category_columns(self):
        df = pd.DataFrame({"category": ["A"], "status": ["active"]})
        types = summarize.detect_column_types(df)
        assert "category" in types["category_cols"]
        assert "status" in types["category_cols"]

    def test_detects_id_columns(self):
        df = pd.DataFrame({"id": [1], "ref_number": [100]})
        types = summarize.detect_column_types(df)
        assert "id" in types["id_cols"]
        assert "ref_number" in types["id_cols"]

    def test_unrecognized_columns_not_categorized(self):
        df = pd.DataFrame({"foo": [1], "bar": [2]})
        types = summarize.detect_column_types(df)
        for key in types:
            assert "foo" not in types[key]
            assert "bar" not in types[key]


class TestBasicSummary:
    """Tests for basic_summary function."""

    def test_row_and_column_counts(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = summarize.basic_summary(df)
        assert result["row_count"] == 3
        assert result["column_count"] == 2

    def test_columns_list(self):
        df = pd.DataFrame({"name": ["a"], "value": [1]})
        result = summarize.basic_summary(df)
        assert result["columns"] == ["name", "value"]

    def test_missing_values(self):
        df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, 6]})
        result = summarize.basic_summary(df)
        assert result["missing_values"]["a"] == 1
        assert result["missing_values"]["b"] == 2

    def test_memory_usage_positive(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = summarize.basic_summary(df)
        assert result["memory_usage_mb"] > 0


class TestNumericSummary:
    """Tests for numeric_summary function."""

    def test_stats_for_numeric_column(self):
        df = pd.DataFrame({"amount": [10, 20, 30, 40, 50]})
        result = summarize.numeric_summary(df)
        assert "amount" in result
        assert result["amount"]["count"] == 5
        assert result["amount"]["mean"] == 30.0
        assert result["amount"]["min"] == 10.0
        assert result["amount"]["max"] == 50.0
        assert result["amount"]["sum"] == 150.0

    def test_empty_when_no_numeric(self):
        df = pd.DataFrame({"name": ["a", "b", "c"]})
        result = summarize.numeric_summary(df)
        assert result == {}

    def test_ignores_non_numeric_columns(self):
        df = pd.DataFrame({"name": ["a", "b"], "value": [10, 20]})
        result = summarize.numeric_summary(df)
        assert "name" not in result
        assert "value" in result


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_text_format(self):
        analysis = {
            "basic": {
                "row_count": 100,
                "column_count": 5,
                "memory_usage_mb": 0.01,
            }
        }
        report = summarize.generate_report(analysis, format="text")
        assert "DATA SUMMARY REPORT" in report
        assert "100" in report
        assert "BASIC INFO" in report

    def test_json_format(self):
        analysis = {"basic": {"row_count": 10, "column_count": 2, "memory_usage_mb": 0.01}}
        report = summarize.generate_report(analysis, format="json")
        parsed = json.loads(report)
        assert parsed["basic"]["row_count"] == 10

    def test_financial_section_in_report(self):
        analysis = {
            "financial": {
                "date_range": {
                    "start": "2024-01-01",
                    "end": "2024-12-31",
                    "span_days": 365,
                },
                "amounts": {
                    "total": 5000.00,
                    "income": 8000.00,
                    "expenses": 3000.00,
                    "net": 5000.00,
                    "average": 500.00,
                    "transaction_count": 10,
                },
            }
        }
        report = summarize.generate_report(analysis, format="text")
        assert "FINANCIAL SUMMARY" in report
        assert "DATE RANGE" in report
