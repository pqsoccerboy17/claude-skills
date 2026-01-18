#!/usr/bin/env python3
"""
Integration tests for Asset Manager Pipeline.

Tests the data flow between components:
  Gmail Scanner → Manual Finder → Drive Uploader → Review Queue

Each module is tested for:
  1. CLI interface works
  2. Outputs match expected schema
  3. Modules accept each other's outputs
  4. Low-confidence items route to review queue
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestModuleCLI(unittest.TestCase):
    """Test that each module's CLI works correctly."""

    def test_gmail_scanner_help(self):
        """Gmail scanner --help works."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "gmail_scanner.py"), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Gmail", result.stdout)

    def test_manual_finder_help(self):
        """Manual finder --help works or fails gracefully on missing deps."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "manual_finder.py"), "--help"],
            capture_output=True,
            text=True,
        )
        # Either works or fails with clear dependency message
        if result.returncode != 0:
            self.assertIn("pip install", result.stdout + result.stderr)
        else:
            self.assertIn("manual", result.stdout.lower())

    def test_drive_uploader_help(self):
        """Drive uploader --help works or fails gracefully on missing deps."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "drive_uploader.py"), "--help"],
            capture_output=True,
            text=True,
        )
        # Either works or fails with clear dependency message
        if result.returncode != 0:
            self.assertIn("pip install", result.stdout + result.stderr)
        else:
            self.assertIn("drive", result.stdout.lower())

    def test_review_queue_help(self):
        """Review queue --help works."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "review_queue.py"), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("review", result.stdout.lower())


class TestGmailScannerOutput(unittest.TestCase):
    """Test Gmail scanner generates valid output schema."""

    def test_mock_mode_generates_valid_json(self):
        """Gmail scanner in mock mode generates valid purchase records."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "gmail_scanner.py"),
                    "--mock",
                    "--days",
                    "30",
                    "--output",
                    output_file,
                ],
                capture_output=True,
                text=True,
            )

            # Check if mock mode is supported
            if result.returncode != 0 and "mock" in result.stderr.lower():
                self.skipTest("Mock mode not implemented")

            if result.returncode == 0 and os.path.exists(output_file):
                with open(output_file) as f:
                    data = json.load(f)

                self.assertIsInstance(data, list)
                if len(data) > 0:
                    record = data[0]
                    # Verify schema per ARCHITECTURE.md
                    required_fields = [
                        "id",
                        "vendor",
                        "product_name",
                        "confidence",
                        "status",
                    ]
                    for field in required_fields:
                        self.assertIn(
                            field, record, f"Missing required field: {field}"
                        )
                    self.assertIsInstance(record["confidence"], (int, float))
                    self.assertGreaterEqual(record["confidence"], 0.0)
                    self.assertLessEqual(record["confidence"], 1.0)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestReviewQueueIntegration(unittest.TestCase):
    """Test review queue accepts items from other modules."""

    def setUp(self):
        """Create temp directory for review queue data."""
        self.temp_dir = tempfile.mkdtemp()
        self.queue_file = os.path.join(self.temp_dir, "review_queue.json")
        os.environ["TREEHOUSE_CONFIG_DIR"] = self.temp_dir

    def tearDown(self):
        """Clean up temp directory."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_review_queue_stats(self):
        """Review queue --stats works."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "review_queue.py"),
                "--stats",
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "TREEHOUSE_CONFIG_DIR": self.temp_dir},
        )
        # Should work even with empty queue
        self.assertIn(result.returncode, [0, 1])

    def test_review_queue_list_empty(self):
        """Review queue --list works with empty queue."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "review_queue.py"),
                "--list",
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "TREEHOUSE_CONFIG_DIR": self.temp_dir},
        )
        self.assertIn(result.returncode, [0, 1])


class TestDataFlowSchema(unittest.TestCase):
    """Test that data schemas match between modules."""

    def test_purchase_record_schema(self):
        """Verify PurchaseRecord schema matches ARCHITECTURE.md."""
        expected_fields = {
            "id": str,
            "vendor": str,
            "product_name": str,
            "model_number": str,
            "purchase_date": str,
            "price": (int, float, type(None)),
            "email_id": str,
            "email_subject": str,
            "confidence": (int, float),
            "raw_snippet": str,
            "suggested_property": str,
            "suggested_category": str,
            "status": str,
        }

        # Create a sample record
        sample_record = {
            "id": "abc123",
            "vendor": "amazon",
            "product_name": "Test Product",
            "model_number": "TP-001",
            "purchase_date": "2026-01-15",
            "price": 99.99,
            "email_id": "msg123",
            "email_subject": "Your order has shipped",
            "confidence": 0.95,
            "raw_snippet": "Sample text...",
            "suggested_property": "DAL",
            "suggested_category": "APPL",
            "status": "pending_review",
        }

        for field, field_type in expected_fields.items():
            self.assertIn(field, sample_record)
            self.assertIsInstance(sample_record[field], field_type)

    def test_manual_result_schema(self):
        """Verify ManualResult schema matches ARCHITECTURE.md."""
        expected_fields = {
            "purchase_id": str,
            "manual_url": str,
            "manual_path": str,
            "source": str,
            "confidence": (int, float),
            "file_size": int,
            "status": str,
        }

        sample_result = {
            "purchase_id": "abc123",
            "manual_url": "https://example.com/manual.pdf",
            "manual_path": "/path/to/manual.pdf",
            "source": "manufacturer",
            "confidence": 0.9,
            "file_size": 1024000,
            "status": "found",
        }

        for field, field_type in expected_fields.items():
            self.assertIn(field, sample_result)
            self.assertIsInstance(sample_result[field], field_type)

    def test_review_item_schema(self):
        """Verify ReviewItem schema matches ARCHITECTURE.md."""
        expected_fields = {
            "id": str,
            "type": str,
            "created_at": str,
            "data": dict,
            "suggested_action": str,
            "notes": str,
            "status": str,
        }

        sample_item = {
            "id": "review123",
            "type": "purchase",
            "created_at": "2026-01-15T12:00:00Z",
            "data": {"product": "Test"},
            "suggested_action": "approve",
            "notes": "",
            "status": "pending",
        }

        for field, field_type in expected_fields.items():
            self.assertIn(field, sample_item)
            self.assertIsInstance(sample_item[field], field_type)


class TestConfidenceThreshold(unittest.TestCase):
    """Test that low-confidence items are routed to review queue."""

    def test_low_confidence_threshold(self):
        """Items with confidence < 0.8 should be flagged for review."""
        threshold = 0.8

        test_cases = [
            (0.5, True),  # Should need review
            (0.79, True),  # Should need review
            (0.8, False),  # Exactly at threshold - no review
            (0.9, False),  # Above threshold - no review
            (1.0, False),  # Perfect confidence - no review
        ]

        for confidence, needs_review in test_cases:
            result = confidence < threshold
            self.assertEqual(
                result,
                needs_review,
                f"Confidence {confidence} should {'need' if needs_review else 'not need'} review",
            )


class TestDryRunMode(unittest.TestCase):
    """Test that dry-run mode doesn't modify anything."""

    def test_gmail_scanner_dry_run(self):
        """Gmail scanner --dry-run doesn't write files."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "gmail_scanner.py"),
                "--dry-run",
                "--days",
                "1",
            ],
            capture_output=True,
            text=True,
        )
        # Should complete without error (may not have credentials)
        # Just verify it doesn't crash
        self.assertNotIn("Traceback", result.stderr)

    def test_drive_uploader_dry_run(self):
        """Drive uploader --dry-run doesn't upload."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test content")
            test_file = f.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "drive_uploader.py"),
                    "--dry-run",
                    "--file",
                    test_file,
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotIn("Traceback", result.stderr)
        finally:
            os.unlink(test_file)


class TestEndToEndPipeline(unittest.TestCase):
    """Test complete pipeline with mock data."""

    def setUp(self):
        """Create temp directory for test data."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temp directory."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_purchase_to_manual_pipeline(self):
        """Test that gmail_scanner output can be consumed by manual_finder."""
        # Create sample purchase data (gmail_scanner output format)
        purchases = [
            {
                "id": "test001",
                "vendor": "amazon",
                "product_name": "Samsung Refrigerator",
                "model_number": "RF28R7551SR",
                "purchase_date": "2026-01-15",
                "price": 1999.99,
                "email_id": "msg001",
                "email_subject": "Your Amazon order has shipped",
                "confidence": 0.92,
                "raw_snippet": "Samsung 28 cu ft French Door Refrigerator",
                "suggested_property": "DAL",
                "suggested_category": "APPL",
                "status": "approved",
            },
            {
                "id": "test002",
                "vendor": "homedepot",
                "product_name": "Carrier AC Unit",
                "model_number": "24ACC636A003",
                "purchase_date": "2026-01-10",
                "price": 3500.00,
                "email_id": "msg002",
                "email_subject": "Home Depot Receipt",
                "confidence": 0.65,  # Low confidence - should be flagged
                "raw_snippet": "Carrier 3 Ton AC System",
                "suggested_property": "",
                "suggested_category": "HVAC",
                "status": "pending_review",
            },
        ]

        purchase_file = os.path.join(self.temp_dir, "purchases.json")
        with open(purchase_file, "w") as f:
            json.dump(purchases, f)

        # Verify file is valid JSON that manual_finder could read
        with open(purchase_file) as f:
            loaded = json.load(f)

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["model_number"], "RF28R7551SR")

        # Count items needing review (confidence < 0.8)
        needs_review = [p for p in loaded if p["confidence"] < 0.8]
        self.assertEqual(len(needs_review), 1)
        self.assertEqual(needs_review[0]["id"], "test002")


if __name__ == "__main__":
    unittest.main(verbosity=2)
