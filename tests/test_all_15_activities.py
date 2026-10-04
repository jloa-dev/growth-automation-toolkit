"""
Comprehensive Unit Test Suite for All 15 Monetization Activities.
"""

import unittest
from pathlib import Path

from src.activities.act01_gmaps_harvester import LocalBusinessHarvester
from src.activities.act02_seo_auditor import SEOAuditor
from src.activities.act03_price_tracker import EcomPriceTracker
from src.activities.act04_email_verifier import BulkEmailVerifier
from src.activities.act05_review_scraper import ReviewSentimentAnalyzer
from src.activities.act06_job_sniper import JobSniper
from src.activities.act07_ebook_builder import EbookBuilder
from src.activities.act08_pdf_table_extractor import InvoiceTableExtractor
from src.activities.act09_github_lead_finder import GitHubLeadFinder
from src.activities.act10_newsletter_curator import NewsletterCurator
from src.activities.act11_ad_creative_spy import AdCreativeSpy
from src.activities.act12_sitemap_checker import SitemapAuditor, UrlHealthStatus
from src.activities.act13_transcript_summarizer import TranscriptRepurposer
from src.activities.act14_csv_deduper import CSVDeduplicator
from src.activities.act15_domain_radar import DomainRadar


class TestAll15Activities(unittest.TestCase):
    def test_act01_gmaps_harvester(self):
        harvester = LocalBusinessHarvester()
        results = harvester.parse_osm_places("Doctor", "Orlando", limit=2)
        self.assertGreater(len(results), 0)
        out = harvester.export_csv(results, "output_activities/test_act01.csv")
        self.assertTrue(Path(out).exists())

    def test_act02_seo_auditor(self):
        auditor = SEOAuditor()
        html = "<html><head><title>Test Title That Is Good Length 12345</title><meta name='description' content='Valid description with sufficient length for test purposes.'><meta name='viewport' content='width=device-width'></head><body><h1>Main Heading</h1><img src='a.jpg' alt='Test'></body></html>"
        res = auditor.audit_html(html, "https://test.com")
        self.assertGreaterEqual(res.seo_score, 80)
        out = auditor.export_report_markdown(res, "output_activities/test_act02.md")
        self.assertTrue(Path(out).exists())

    def test_act03_price_tracker(self):
        tracker = EcomPriceTracker()
        html = "<html><head><title>Super Widget</title></head><body><span class='price'>$49.99</span></body></html>"
        res = tracker.extract_from_html(html, "https://store.com/widget")
        self.assertEqual(res.current_price, 49.99)
        out = tracker.export_price_comparison([res], "output_activities/test_act03.csv")
        self.assertTrue(Path(out).exists())

    def test_act04_email_verifier(self):
        verifier = BulkEmailVerifier()
        clean = verifier.verify_single("test@gmail.com")
        self.assertTrue(clean.is_valid_syntax)
        disp = verifier.verify_single("bot@mailinator.com")
        self.assertTrue(disp.is_disposable)

    def test_act05_review_scraper(self):
        analyzer = ReviewSentimentAnalyzer()
        data = [{"author": "Bob", "rating": 5, "title": "Great", "body": "Excellent and awesome product love it"}]
        res = analyzer.parse_reviews_from_text(data)
        self.assertEqual(res[0].sentiment, "POSITIVE")

    def test_act06_job_sniper(self):
        sniper = JobSniper()
        lead = sniper.analyze_listing("AI Labs", "Python Dev", "We need Python and FastAPI urgently.", "https://apply.com")
        self.assertIn("Python", lead.detected_stack)
        self.assertEqual(lead.hiring_urgency, "High")

    def test_act07_ebook_builder(self):
        builder = EbookBuilder()
        out = builder.compile_book("Test Guide", "Author", [{"title": "Intro", "content": "# Hello\n\nWorld"}], "output_activities/test_act07.html")
        self.assertTrue(Path(out).exists())

    def test_act08_pdf_table_extractor(self):
        extractor = InvoiceTableExtractor()
        text = "ITEM-01 Hosting 1 50.00 50.00\nITEM-02 Domain 1 15.00 15.00"
        items = extractor.parse_plain_text_table(text)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].total_amount, 50.0)

    def test_act09_github_lead_finder(self):
        finder = GitHubLeadFinder()
        from src.activities.act09_github_lead_finder import DeveloperLead
        leads = [DeveloperLead("dev1", "Dev One", "Acme", "SF", "dev@acme.com", "Bio", "https://github.com/dev1")]
        out = finder.export_csv(leads, "output_activities/test_act09.csv")
        self.assertTrue(Path(out).exists())

    def test_act10_newsletter_curator(self):
        curator = NewsletterCurator()
        xml = "<rss><channel><item><title>News 1</title><link>https://a.com</link><description>Desc</description></item></channel></rss>"
        articles = curator.parse_rss_xml(xml)
        self.assertEqual(len(articles), 1)

    def test_act11_ad_creative_spy(self):
        spy = AdCreativeSpy()
        html = "<html><body><h1>Scale Your Business</h1><h2>Automate today</h2><a class='btn-cta'>Get Started</a></body></html>"
        res = spy.extract_from_html(html, "https://saas.com")
        self.assertEqual(res.primary_headline, "Scale Your Business")

    def test_act12_sitemap_checker(self):
        auditor = SitemapAuditor()
        xml = "<urlset><url><loc>https://example.com/p1</loc></url></urlset>"
        urls = auditor.parse_sitemap_xml(xml)
        self.assertEqual(urls, ["https://example.com/p1"])

    def test_act13_transcript_summarizer(self):
        repurposer = TranscriptRepurposer()
        res = repurposer.process_transcript("Title", "This is an important concept. You must remember to execute daily. Systems compound.")
        self.assertEqual(len(res.twitter_thread), 3)

    def test_act14_csv_deduper(self):
        deduper = CSVDeduplicator()
        data = [
            {"email": "USER@test.com", "phone": "1234567890"},
            {"email": "user@test.com", "phone": "123-456-7890"}
        ]
        clean, dups = deduper.clean_and_dedupe(data, dedupe_key="email")
        self.assertEqual(len(clean), 1)
        self.assertEqual(dups, 1)

    def test_act15_domain_radar(self):
        radar = DomainRadar()
        opp = radar.evaluate_domain("fastflow.ai")
        self.assertEqual(opp.tld, ".ai")
        self.assertGreaterEqual(opp.brand_score, 50)


if __name__ == "__main__":
    unittest.main()
