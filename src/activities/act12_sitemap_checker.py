"""
Actividad 12: XML Sitemap Health & Broken Link Auditor.
Crawls sitemap URLs, detects 404 errors, redirect loops, and generates site repair reports.
Target Pricing: $15 - $30 USD per site broken link audit.
"""

from __future__ import annotations

import csv
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class UrlHealthStatus:
    url: str
    status_code: int
    is_broken: bool
    redirect_url: str = ""
    error_message: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class SitemapAuditor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SitemapChecker/1.0"}

    def parse_sitemap_xml(self, xml_content: str) -> List[str]:
        urls = []
        try:
            root = ET.fromstring(xml_content)
            # Find all <loc> tags regardless of namespace
            for elem in root.iter():
                if elem.tag.endswith("loc") and elem.text:
                    urls.append(elem.text.strip())
        except Exception:
            urls = re.findall(r"<loc>(.*?)</loc>", xml_content, re.I)
        return urls

    def check_url(self, url: str) -> UrlHealthStatus:
        req = urllib.request.Request(url, headers=self.headers, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                final_url = resp.geturl()
                is_redirect = (final_url != url)
                return UrlHealthStatus(
                    url=url,
                    status_code=resp.status,
                    is_broken=False,
                    redirect_url=final_url if is_redirect else "",
                )
        except urllib.error.HTTPError as he:
            return UrlHealthStatus(url=url, status_code=he.code, is_broken=True, error_message=str(he))
        except Exception as e:
            return UrlHealthStatus(url=url, status_code=0, is_broken=True, error_message=str(e)[:80])

    def audit_urls(self, urls: List[str]) -> List[UrlHealthStatus]:
        return [self.check_url(u) for u in urls if u.startswith(("http://", "https://"))]

    @staticmethod
    def export_csv(results: List[UrlHealthStatus], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["url", "status_code", "is_broken", "redirect_url", "error_message"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r.to_dict())
        return str(path.resolve())


if __name__ == "__main__":
    auditor = SitemapAuditor()
    sample_xml = """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://example.com/about</loc></url>
      <url><loc>https://example.com/pricing</loc></url>
      <url><loc>https://example.com/dead-link-404-test</loc></url>
    </urlset>
    """
    urls = auditor.parse_sitemap_xml(sample_xml)
    # Check against mock statuses for dry-run
    checks = [
        UrlHealthStatus("https://example.com/about", 200, False),
        UrlHealthStatus("https://example.com/pricing", 200, False),
        UrlHealthStatus("https://example.com/dead-link-404-test", 404, True, error_message="HTTP Error 404: Not Found"),
    ]
    out = auditor.export_csv(checks, "output_activities/act12_sitemap_audit.csv")
    print(f"✅ Actividad 12: Audited sitemap URLs -> {out}")
