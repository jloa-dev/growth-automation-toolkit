"""
Actividad 15: Expired & Dropped Domain Opportunity Radar.
Screens domain candidate lists, checks DNS availability, and calculates brandability/SEO scores.
Target Pricing: $15 - $35 USD per curated expired domain shortlist.
"""

from __future__ import annotations

import csv
import socket
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class DomainOpportunity:
    domain: str
    is_resolving: bool
    length: int
    tld: str
    brand_score: int
    status: str

    def to_dict(self) -> Dict:
        return asdict(self)


class DomainRadar:
    HIGH_VALUE_TLDS = {".com": 30, ".io": 25, ".ai": 30, ".dev": 20, ".org": 15}
    VALUABLE_KEYWORDS = {"pay", "app", "cloud", "data", "bot", "ai", "hub", "flow", "fast", "stack"}

    @classmethod
    def evaluate_domain(cls, domain: str) -> DomainOpportunity:
        clean = domain.strip().lower()
        tld = "." + clean.split(".")[-1] if "." in clean else ""
        name_only = clean.replace(tld, "")

        # DNS Check
        resolves = False
        try:
            socket.gethostbyname(clean)
            resolves = True
        except Exception:
            resolves = False

        score = 0
        # Shorter names are more valuable
        length = len(name_only)
        if length <= 5:
            score += 40
        elif length <= 8:
            score += 25
        elif length <= 12:
            score += 15

        # TLD bonus
        score += cls.HIGH_VALUE_TLDS.get(tld, 5)

        # Keyword bonus
        if any(kw in name_only for kw in cls.VALUABLE_KEYWORDS):
            score += 25

        score = min(score, 100)
        status = "TAKEN_ACTIVE" if resolves else ("HIGH_POTENTIAL_DROPPED" if score >= 60 else "AVAILABLE_GENERIC")

        return DomainOpportunity(
            domain=clean,
            is_resolving=resolves,
            length=length,
            tld=tld,
            brand_score=score,
            status=status,
        )

    @classmethod
    def scan_domain_list(cls, domains: List[str]) -> List[DomainOpportunity]:
        return [cls.evaluate_domain(d) for d in domains if d.strip()]

    @staticmethod
    def export_csv(opportunities: List[DomainOpportunity], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["domain", "is_resolving", "length", "tld", "brand_score", "status"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for opp in opportunities:
                writer.writerow(opp.to_dict())
        return str(path.resolve())


if __name__ == "__main__":
    radar = DomainRadar()
    test_domains = ["payai.com", "fastflow.io", "cloudstack.dev", "nonexistentdomain9999123xyz.com"]
    scanned = radar.scan_domain_list(test_domains)
    out = radar.export_csv(scanned, "output_activities/act15_domain_opportunities.csv")
    print(f"✅ Actividad 15: Scanned {len(scanned)} domains -> {out}")
