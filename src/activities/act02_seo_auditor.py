"""
Actividad 02: Automated Technical SEO Auditor.
Analyzes websites for meta tags, heading hierarchy, alt attributes, mobile friendliness, and page speed signals.
Target Pricing: $15 - $25 USD per audit report.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class SEOAuditResult:
    url: str
    status_code: int = 0
    title: str = ""
    title_length: int = 0
    description: str = ""
    description_length: int = 0
    canonical: str = ""
    h1_count: int = 0
    h1_tags: List[str] = field(default_factory=list)
    images_count: int = 0
    images_missing_alt: int = 0
    has_viewport: bool = False
    has_favicon: bool = False
    has_schema_org: bool = False
    seo_score: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


class SEOAuditor:
    def __init__(self, user_agent: Optional[str] = None):
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def audit_html(self, html: str, url: str) -> SEOAuditResult:
        res = SEOAuditResult(url=url, status_code=200)

        # Title
        t_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        if t_match:
            res.title = re.sub(r"\s+", " ", t_match.group(1)).strip()
            res.title_length = len(res.title)

        # Meta description
        d_match = re.search(r'<meta[^>]+(?:name=["\']description["\'])[^>]+content=["\'](.*?)["\']', html, re.I)
        if d_match:
            res.description = d_match.group(1).strip()
            res.description_length = len(res.description)

        # Canonical
        c_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html, re.I)
        if c_match:
            res.canonical = c_match.group(1).strip()

        # Headings
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        res.h1_tags = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
        res.h1_count = len(res.h1_tags)

        # Images
        img_tags = re.findall(r"<img\s+[^>]*>", html, re.I)
        res.images_count = len(img_tags)
        missing_alt = [img for img in img_tags if 'alt=' not in img.lower() or 'alt=""' in img.lower()]
        res.images_missing_alt = len(missing_alt)

        # Mobile viewport
        res.has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.I))

        # Schema JSON-LD
        res.has_schema_org = bool(re.search(r'<script[^>]+type=["\']application/ld\+json["\']', html, re.I))

        # Scoring & Recommendations
        score = 100
        recs = []

        if not res.title:
            score -= 20
            recs.append("CRITICAL: Missing <title> tag.")
        elif res.title_length < 30 or res.title_length > 65:
            score -= 10
            recs.append(f"WARNING: Title length ({res.title_length} chars) is outside optimal 30-65 range.")

        if not res.description:
            score -= 20
            recs.append("CRITICAL: Missing meta description.")
        elif res.description_length < 70 or res.description_length > 160:
            score -= 10
            recs.append(f"WARNING: Meta description length ({res.description_length} chars) should be between 70-160.")

        if res.h1_count == 0:
            score -= 15
            recs.append("CRITICAL: Missing <h1> heading on page.")
        elif res.h1_count > 1:
            score -= 5
            recs.append(f"NOTICE: Found multiple <h1> tags ({res.h1_count}). Best practice is 1 main <h1>.")

        if res.images_missing_alt > 0:
            penalty = min(res.images_missing_alt * 2, 15)
            score -= penalty
            recs.append(f"WARNING: {res.images_missing_alt} image(s) missing alt descriptive tags.")

        if not res.has_viewport:
            score -= 15
            recs.append("CRITICAL: Missing mobile viewport meta tag.")

        if not res.has_schema_org:
            score -= 5
            recs.append("RECOMMENDATION: Add Schema.org JSON-LD structured data for rich snippets.")

        res.seo_score = max(score, 0)
        res.recommendations = recs
        return res

    def export_report_markdown(self, audit: SEOAuditResult, output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = [
            f"# Technical SEO Audit Report: {audit.url}",
            f"\n**Overall SEO Health Score:** **{audit.seo_score}/100**",
            f"\n## Core Metadata Summary",
            f"- **Page Title:** {audit.title or '*Missing*'} ({audit.title_length} chars)",
            f"- **Meta Description:** {audit.description or '*Missing*'} ({audit.description_length} chars)",
            f"- **Canonical URL:** {audit.canonical or '*Not specified*'}",
            f"- **H1 Tags Found:** {audit.h1_count}",
            f"- **Total Images:** {audit.images_count} ({audit.images_missing_alt} missing ALT)",
            f"- **Mobile Viewport Tag:** {'✅ Configured' if audit.has_viewport else '❌ Missing'}",
            f"- **Structured Data (Schema.org):** {'✅ Present' if audit.has_schema_org else '❌ None'}",
            f"\n## Actionable Recommendations ({len(audit.recommendations)})",
        ]
        for rec in audit.recommendations:
            content.append(f"- {rec}")
        report_text = "\n".join(content) + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(report_text)
        return str(path.resolve())


if __name__ == "__main__":
    auditor = SEOAuditor()
    sample_html = """
    <html><head><title>Best Miami Plumbers - 24/7 Emergency Service</title>
    <meta name="description" content="Affordable 24/7 plumbing repair and emergency drainage in Miami FL. Call now!">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head><body><h1>Emergency Plumbing in Miami</h1><img src="pipe.jpg"><img src="truck.jpg" alt="Service truck"></body></html>
    """
    res = auditor.audit_html(sample_html, "https://miamiplumbingpro.com")
    out = auditor.export_report_markdown(res, "output_activities/act02_seo_report.md")
    print(f"✅ Actividad 02: Audited {res.url} -> Score: {res.seo_score}/100 -> {out}")
