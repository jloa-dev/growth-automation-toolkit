"""
Exporter module for LeadPulse.
Supports CSV, JSON, and Executive Markdown report generation.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List
from .core import LeadRecord


class LeadExporter:
    @staticmethod
    def to_csv(records: List[LeadRecord], output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "domain",
            "url",
            "title",
            "description",
            "primary_email",
            "all_emails",
            "primary_phone",
            "all_phones",
            "linkedin",
            "twitter",
            "lead_score",
            "status",
            "tier_notes",
        ]

        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow({
                    "domain": r.domain,
                    "url": r.url,
                    "title": r.title,
                    "description": r.description,
                    "primary_email": r.emails[0] if r.emails else "",
                    "all_emails": "; ".join(r.emails),
                    "primary_phone": r.phones[0] if r.phones else "",
                    "all_phones": "; ".join(r.phones),
                    "linkedin": r.social_links.get("linkedin", ""),
                    "twitter": r.social_links.get("twitter", ""),
                    "lead_score": r.lead_score,
                    "status": r.status,
                    "tier_notes": r.notes,
                })
        return str(path.resolve())

    @staticmethod
    def to_json(records: List[LeadRecord], output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [r.to_dict() for r in records]
        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(path.resolve())

    @staticmethod
    def to_executive_report(records: List[LeadRecord], output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        total = len(records)
        with_emails = sum(1 for r in records if r.emails)
        with_phones = sum(1 for r in records if r.phones)
        with_linkedin = sum(1 for r in records if "linkedin" in r.social_links)
        high_score = sum(1 for r in records if r.lead_score >= 70)

        lines = [
            "# LeadPulse Executive Dataset Summary",
            f"\n**Total Domains Analyzed:** {total}",
            f"- **Verified Email Contacts:** {with_emails} ({with_emails/max(total, 1)*100:.1f}%)",
            f"- **Verified Phone Contacts:** {with_phones} ({with_phones/max(total, 1)*100:.1f}%)",
            f"- **LinkedIn Company/Founder Profiles:** {with_linkedin} ({with_linkedin/max(total, 1)*100:.1f}%)",
            f"- **High-Quality Qualified Leads (Score >= 70):** {high_score} ({high_score/max(total, 1)*100:.1f}%)",
            "\n## Top Verified Leads\n",
            "| Domain | Lead Score | Primary Email | LinkedIn | Notes |",
            "| :--- | :---: | :--- | :--- | :--- |",
        ]

        top_records = sorted(records, key=lambda x: x.lead_score, reverse=True)[:15]
        for r in top_records:
            em = r.emails[0] if r.emails else "*None*"
            li = f"[Profile]({r.social_links['linkedin']})" if "linkedin" in r.social_links else "*None*"
            lines.append(f"| `{r.domain}` | **{r.lead_score}/100** | {em} | {li} | {r.notes} |")

        report_content = "\n".join(lines) + "\n"
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(report_content)
        return str(path.resolve())
