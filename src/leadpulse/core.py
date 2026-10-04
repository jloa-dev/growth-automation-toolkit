"""
Core extraction module for LeadPulse.
Extracts contact information, metadata, and social profiles from target domains.
"""

from __future__ import annotations

import re
import urllib.parse
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set
import requests


EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,12}",
    re.IGNORECASE,
)

PHONE_REGEX = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}",
)

SOCIAL_PATTERNS = {
    "linkedin": re.compile(r"https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+", re.IGNORECASE),
    "twitter": re.compile(r"https?://(?:www\.)?(?:twitter\.com|x\.com)/[a-zA-Z0-9_]+", re.IGNORECASE),
    "instagram": re.compile(r"https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.]+", re.IGNORECASE),
    "facebook": re.compile(r"https?://(?:www\.)?facebook\.com/[a-zA-Z0-9_.]+", re.IGNORECASE),
    "github": re.compile(r"https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE),
}

DISCARD_EMAIL_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".css", ".js", ".woff", ".woff2"
}

DISCARD_EMAIL_PREFIXES = {
    "noreply", "no-reply", "mailer-daemon", "postmaster", "root", "example", "sentry"
}

DISCARD_EMAIL_DOMAINS = {
    "example.com", "example.org", "example.net", "test.com", "sample.com"
}


@dataclass
class LeadRecord:
    url: str
    domain: str
    title: str = ""
    description: str = ""
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    social_links: Dict[str, str] = field(default_factory=dict)
    lead_score: int = 0
    status: str = "pending"
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class LeadExtractor:
    def __init__(self, timeout: int = 10, user_agent: Optional[str] = None):
        self.timeout = timeout
        self.headers = {
            "User-Agent": user_agent or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    def clean_domain(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc.lower().replace("www.", "")

    def normalize_url(self, raw: str) -> str:
        raw = raw.strip()
        if not raw.startswith(("http://", "https://")):
            return f"https://{raw}"
        return raw

    def extract_from_html(self, html: str, base_url: str) -> LeadRecord:
        domain = self.clean_domain(base_url)
        record = LeadRecord(url=base_url, domain=domain)

        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if title_match:
            record.title = re.sub(r"\s+", " ", title_match.group(1)).strip()

        desc_match = re.search(
            r'<meta[^>]+(?:name=["\']description["\']|property=["\']og:description["\'])[^>]+content=["\'](.*?)["\']',
            html,
            re.IGNORECASE,
        )
        if desc_match:
            record.description = desc_match.group(1).strip()

        raw_emails = set(EMAIL_REGEX.findall(html))
        filtered_emails: Set[str] = set()
        for email in raw_emails:
            email_lower = email.lower().strip()
            if any(email_lower.endswith(ext) for ext in DISCARD_EMAIL_EXTENSIONS):
                continue
            parts = email_lower.split("@")
            if len(parts) != 2:
                continue
            prefix, domain_part = parts
            if prefix in DISCARD_EMAIL_PREFIXES or domain_part in DISCARD_EMAIL_DOMAINS:
                continue
            if len(prefix) < 2 or len(email_lower) > 60:
                continue
            filtered_emails.add(email_lower)
        record.emails = sorted(list(filtered_emails))

        raw_phones = set(PHONE_REGEX.findall(html))
        clean_phones: Set[str] = set()
        for phone in raw_phones:
            p_strip = phone.strip()
            digits = re.sub(r"\D", "", p_strip)
            if 8 <= len(digits) <= 15:
                clean_phones.add(p_strip)
        record.phones = sorted(list(clean_phones))[:5]

        for platform, pattern in SOCIAL_PATTERNS.items():
            match = pattern.search(html)
            if match:
                record.social_links[platform] = match.group(0)

        score = 0
        if record.emails:
            score += 40 + (min(len(record.emails), 3) * 10)
        if record.phones:
            score += 20
        if "linkedin" in record.social_links:
            score += 20
        if record.social_links:
            score += 10
        if record.title and record.description:
            score += 10
        record.lead_score = min(score, 100)
        record.status = "enriched" if record.lead_score >= 50 else "partial"

        return record

    def fetch_and_extract(self, url: str) -> LeadRecord:
        norm_url = self.normalize_url(url)
        domain = self.clean_domain(norm_url)
        try:
            response = requests.get(norm_url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return self.extract_from_html(response.text, norm_url)
            else:
                return LeadRecord(
                    url=norm_url,
                    domain=domain,
                    status="failed",
                    notes=f"HTTP {response.status_code}",
                )
        except Exception as exc:
            return LeadRecord(
                url=norm_url,
                domain=domain,
                status="error",
                notes=str(exc)[:120],
            )
