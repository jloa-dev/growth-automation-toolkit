# Growth Automation Toolkit 🚀

[![CI Tests](https://github.com/jloa-dev/growth-automation-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/jloa-dev/growth-automation-toolkit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)

A production-grade collection of **16 high-performance automation engines** for B2B lead generation, SEO auditing, e-commerce price monitoring, and data extraction.

Developed and maintained by **[jloa-dev](https://github.com/jloa-dev)** (`jloa.dev@gmail.com`).

---

## 💼 On-Demand Data & Automation Services ($10 – $50 USD)

Need custom datasets, scraper setups, or ongoing data pipelines for your company? We deliver turnkey solutions in under 12 hours:

| Service / Tool | Description | Turnaround | Price |
| :--- | :--- | :---: | :---: |
| **B2B Lead Generation** | 1,000 verified company contacts (Emails, Phones, LinkedIn, Metadata) | < 12h | **$50 USD** |
| **Local Business Directory** | 500 local businesses (Dentists, Contractors, Clinics) in any city | < 4h | **$15 USD** |
| **Technical SEO Audit** | Full health check (Meta, H1-H6, Alt, Schema.org, Viewport) + PDF Report | < 2h | **$15 USD** |
| **Bulk Email Cleaning** | 5,000 emails cleaned (Syntax, MX DNS check, Disposable domain filter) | < 1h | **$15 USD** |
| **Competitor Price Monitor** | Automated tracking script for competitor catalog prices & stock status | < 24h | **$25 USD** |
| **Custom Web Scraping Script** | Tailored Python scraper for any directory, store, or portal | < 24h | **$50 USD** |

👉 **Inquiries & Custom Requests:** Reach out directly via GitHub Issues, email `jloa.dev@gmail.com`, or hire via [commercial_catalog.md](templates/activities/commercial_catalog.md).

---

## 🛠️ The 16 Engines Overview

### Core Engine: LeadPulse
Extracts corporate contacts, verified emails, phone numbers, and LinkedIn/Twitter links directly from company domains with automated lead scoring (0–100).
```bash
# Scan a single domain
python -m src.leadpulse.cli scan stripe.com

# Batch scan target list
python -m src.leadpulse.cli batch sample_targets.txt --output leads_output/
```

### Specialized Micro-Engines (`src/activities/`)

1. **`act01_gmaps_harvester.py`**: Local business listings by city & category.
2. **`act02_seo_auditor.py`**: Automated technical SEO auditor with Markdown report.
3. **`act03_price_tracker.py`**: E-commerce price and inventory monitor with discount alerts.
4. **`act04_email_verifier.py`**: Bulk email deliverability verifier and spam trap cleaner.
5. **`act05_review_scraper.py`**: Customer reviews extractor with sentiment polarity analysis.
6. **`act06_job_sniper.py`**: Hiring signals detector for specific tech stacks (Next.js, Python, AWS).
7. **`act07_ebook_builder.py`**: Compiles raw Markdown notes into styled HTML/PDF digital guides.
8. **`act08_pdf_table_extractor.py`**: Extracts tables from invoices and financial statements into clean CSV.
9. **`act09_github_lead_finder.py`**: Discovers developer leads from open-source GitHub repositories.
10. **`act10_newsletter_curator.py`**: Aggregates RSS feeds and formats weekly Substack/Beehiiv drafts.
11. **`act11_ad_creative_spy.py`**: Extracts competitor advertising copy, hooks, and CTAs (Swipe File).
12. **`act12_sitemap_checker.py`**: XML sitemap crawler for dead links and 404 status detection.
13. **`act13_transcript_summarizer.py`**: Video transcript repurposer for viral Twitter threads & LinkedIn.
14. **`act14_csv_deduper.py`**: High-volume CRM CSV normalizer and deduplicator.
15. **`act15_domain_radar.py`**: Expired domain monitor with brandability and DNS scoring.

---

## 🧪 Testing & Verification

Run the entire 19-test suite locally:
```bash
python -m unittest discover -s tests
```
*Current status:* **19/19 tests passing in < 1.0s.**

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
