"""
Actividad 11: Competitor Ad Copy & Landing Page Swipe File Extractor.
Extracts marketing headlines, subheadlines, call-to-action hooks, and value propositions for ad agencies.
Target Pricing: $20 - $40 USD per competitive ad swipe file report.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class AdCreativeAnalysis:
    url: str
    primary_headline: str
    subheadline: str
    call_to_actions: List[str] = field(default_factory=list)
    key_value_props: List[str] = field(default_factory=list)
    social_proof_claims: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


class AdCreativeSpy:
    @staticmethod
    def extract_from_html(html: str, url: str) -> AdCreativeAnalysis:
        # Extract H1
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        h1 = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip() if h1_match else "No Headline Detected"

        # Extract H2 subheadline
        h2_match = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.I | re.S)
        h2 = re.sub(r"<[^>]+>", "", h2_match.group(1)).strip() if h2_match else ""

        # Extract CTA buttons
        ctas = set()
        btn_matches = re.findall(r"<(?:button|a)[^>]+(?:class|id)=[\"'][^\"']*(?:cta|btn|button)[^\"']*[\"'][^>]*>(.*?)</(?:button|a)>", html, re.I | re.S)
        for b in btn_matches:
            text = re.sub(r"<[^>]+>", "", b).strip()
            if 2 <= len(text) <= 40 and not text.isdigit():
                ctas.add(text)

        # Value props from list items
        props = []
        li_matches = re.findall(r"<li[^>]*>(.*?)</li>", html, re.I | re.S)
        for li in li_matches[:6]:
            clean_li = re.sub(r"<[^>]+>", "", li).strip()
            if 10 <= len(clean_li) <= 120:
                props.append(clean_li)

        # Social proof numbers like "10,000+ customers", "5 stars"
        proofs = re.findall(r"\b[0-9]+(?:,[0-9]+)?\+?\s+(?:customers|users|teams|companies|stars|reviews|downloads)\b", html, re.I)

        return AdCreativeAnalysis(
            url=url,
            primary_headline=h1,
            subheadline=h2,
            call_to_actions=list(ctas),
            key_value_props=props,
            social_proof_claims=list(set(proofs)),
        )

    @staticmethod
    def export_swipe_file_markdown(analysis: AdCreativeAnalysis, output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# 🎯 Competitor Ad & Messaging Swipe File: {analysis.url}",
            f"\n### Primary Headline (Hook)",
            f"> \"{analysis.primary_headline}\"",
            f"\n### Subheadline (Value Explanation)",
            f"> \"{analysis.subheadline or '*None*'}\"",
            f"\n### Calls-to-Action (Buttons)",
        ]
        for cta in analysis.call_to_actions or ["Get Started"]:
            lines.append(f"- `[{cta}]`")
        lines.append(f"\n### Key Value Propositions ({len(analysis.key_value_props)})")
        for vp in analysis.key_value_props:
            lines.append(f"- {vp}")
        lines.append(f"\n### Social Proof Angles Detected")
        for sp in analysis.social_proof_claims or ["None explicitly stated"]:
            lines.append(f"- ⭐ {sp}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return str(path.resolve())


if __name__ == "__main__":
    spy = AdCreativeSpy()
    sample_html = """
    <html><body>
    <h1>Scale Your Cold Outbound with Zero Manual Work</h1>
    <h2>AI-driven SDR agents that book 30+ qualified sales calls every month.</h2>
    <a href="/trial" class="btn btn-primary cta-button">Start Free 14-Day Trial</a>
    <button class="cta-book">Book a 15-Min Demo</button>
    <ul>
      <li>100% verified work emails with zero bounce guarantee</li>
      <li>Automatic personalized icebreakers written from LinkedIn activity</li>
      <li>Instant sync with HubSpot, Salesforce and Apollo</li>
    </ul>
    <p>Trusted by over 5,000+ teams and 500+ companies worldwide.</p>
    </body></html>
    """
    res = spy.extract_from_html(sample_html, "https://outboundsdr.ai")
    out = spy.export_swipe_file_markdown(res, "output_activities/act11_swipe_file.md")
    print(f"✅ Actividad 11: Created competitor swipe file -> {out}")
