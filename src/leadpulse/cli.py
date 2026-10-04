"""
Command Line Interface for LeadPulse.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from .core import LeadExtractor, LeadRecord
from .enricher import LeadEnricher
from .exporter import LeadExporter


def run_batch(urls: List[str], output_dir: str = "output") -> None:
    print(f"\n🚀 [LeadPulse Engine] Starting extraction for {len(urls)} targets...")
    extractor = LeadExtractor(timeout=8)
    records: List[LeadRecord] = []

    for idx, url in enumerate(urls, 1):
        clean_url = url.strip()
        if not clean_url:
            continue
        print(f"  [{idx}/{len(urls)}] Processing: {clean_url}...", end=" ", flush=True)
        rec = extractor.fetch_and_extract(clean_url)
        print(f"Status: {rec.status.upper()} | Score: {rec.lead_score}/100 | Emails: {len(rec.emails)}")
        records.append(rec)

    enriched = LeadEnricher.deduplicate(records)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = LeadExporter.to_csv(enriched, out_dir / "leads.csv")
    json_path = LeadExporter.to_json(enriched, out_dir / "leads.json")
    rep_path = LeadExporter.to_executive_report(enriched, out_dir / "summary_report.md")

    print("\n✅ Extraction and Enrichment Complete!")
    print(f"  📁 CSV Export:  {csv_path}")
    print(f"  📁 JSON Export: {json_path}")
    print(f"  📁 Report:      {rep_path}\n")


def run_demo() -> None:
    print("\n⚡ [LeadPulse Demo] Executing local extraction pipeline test...")
    sample_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Apex Digital Agency | Scalable B2B Growth</title>
        <meta name="description" content="We build high-converting growth systems for tech startups and B2B SaaS.">
      </head>
      <body>
        <h1>Scale Your Pipeline</h1>
        <p>Inquiries: contact@apexdigital.io or sales@apexdigital.io</p>
        <p>Phone: +1 (555) 234-5678</p>
        <a href="https://linkedin.com/company/apex-digital-growth">LinkedIn</a>
        <a href="https://twitter.com/apexdigital">Twitter</a>
      </body>
    </html>
    """
    extractor = LeadExtractor()
    record = extractor.extract_from_html(sample_html, "https://apexdigital.io")
    record = LeadEnricher.enrich_record(record)

    out_dir = Path("output_demo")
    csv_path = LeadExporter.to_csv([record], out_dir / "demo_leads.csv")
    rep_path = LeadExporter.to_executive_report([record], out_dir / "demo_report.md")

    print(f"  Domain:       {record.domain}")
    print(f"  Title:        {record.title}")
    print(f"  Lead Score:   {record.lead_score}/100")
    print(f"  Emails:       {record.emails}")
    print(f"  Phones:       {record.phones}")
    print(f"  Social Links: {record.social_links}")
    print(f"  Notes:        {record.notes}")
    print(f"  Exported to:  {csv_path}")
    print(f"  Report to:    {rep_path}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LeadPulse - Professional B2B Lead Harvester & Contact Enrichment Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_parser = subparsers.add_parser("scan", help="Scan a single domain or URL")
    scan_parser.add_argument("url", help="Target URL or domain (e.g. stripe.com)")

    batch_parser = subparsers.add_parser("batch", help="Scan a list of domains from file")
    batch_parser.add_argument("file", help="Path to text file containing domains/URLs (one per line)")
    batch_parser.add_argument("--output", default="output", help="Directory for output files")

    subparsers.add_parser("demo", help="Run a verification demo with sample data")

    args = parser.parse_args()

    if args.command == "demo":
        run_demo()
    elif args.command == "scan":
        run_batch([args.url], "output_single")
    elif args.command == "batch":
        with open(args.file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        run_batch(lines, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
