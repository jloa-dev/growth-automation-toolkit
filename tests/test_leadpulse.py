"""
Unit tests for LeadPulse core, enricher, and exporter.
"""

import unittest
from pathlib import Path
from src.leadpulse.core import LeadExtractor, LeadRecord
from src.leadpulse.enricher import LeadEnricher
from src.leadpulse.exporter import LeadExporter


class TestLeadPulse(unittest.TestCase):
    def setUp(self):
        self.extractor = LeadExtractor()
        self.html = """
        <html>
            <head>
                <title>Test Software Labs</title>
                <meta name="description" content="AI Software and Data Engineering">
            </head>
            <body>
                <p>Reach us at support@testlabs.com or hello@testlabs.com</p>
                <p>Fake email image.png@example.com should be ignored</p>
                <p>Call: +1-800-555-0199</p>
                <a href="https://linkedin.com/company/testlabs-ai">LinkedIn</a>
            </body>
        </html>
        """

    def test_extract_from_html(self):
        rec = self.extractor.extract_from_html(self.html, "https://testlabs.com")
        self.assertEqual(rec.domain, "testlabs.com")
        self.assertEqual(rec.title, "Test Software Labs")
        self.assertIn("support@testlabs.com", rec.emails)
        self.assertIn("hello@testlabs.com", rec.emails)
        self.assertIn("linkedin", rec.social_links)
        self.assertGreaterEqual(rec.lead_score, 70)

    def test_email_enrichment(self):
        rec = LeadRecord(
            url="https://temp.org",
            domain="temp.org",
            emails=["user@mailinator.com", "valid@company.com"],
        )
        enriched = LeadEnricher.enrich_record(rec)
        self.assertNotIn("user@mailinator.com", enriched.emails)
        self.assertIn("valid@company.com", enriched.emails)

    def test_deduplication(self):
        recs = [
            LeadRecord(url="https://a.com", domain="a.com", emails=["a@a.com"]),
            LeadRecord(url="https://a.com/about", domain="a.com", emails=["a2@a.com"]),
            LeadRecord(url="https://b.com", domain="b.com", emails=["b@b.com"]),
        ]
        deduped = LeadEnricher.deduplicate(recs)
        self.assertEqual(len(deduped), 2)
        self.assertEqual({r.domain for r in deduped}, {"a.com", "b.com"})

    def test_export_pipeline(self):
        rec = self.extractor.extract_from_html(self.html, "https://testlabs.com")
        test_dir = Path("output_test")
        csv_file = LeadExporter.to_csv([rec], test_dir / "test.csv")
        json_file = LeadExporter.to_json([rec], test_dir / "test.json")
        rep_file = LeadExporter.to_executive_report([rec], test_dir / "test.md")

        self.assertTrue(Path(csv_file).exists())
        self.assertTrue(Path(json_file).exists())
        self.assertTrue(Path(rep_file).exists())


if __name__ == "__main__":
    unittest.main()
