"""
Enrichment and validation module for LeadPulse.
Performs email validation, segmentation, and deduplication.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple
from .core import LeadRecord

DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "10minutemail.com", "guerrillamail.com",
    "sharklasers.com", "throwawaymail.com", "yopmail.com", "trashmail.com",
    "example.com", "example.org", "example.net", "test.com"
}

ROLE_BASED_PREFIXES = {
    "admin", "info", "contact", "support", "sales", "billing", "help", "hello",
    "team", "office", "marketing", "press", "inquiries"
}


class LeadEnricher:
    @staticmethod
    def classify_email(email: str) -> Dict[str, bool]:
        email_clean = email.lower().strip()
        parts = email_clean.split("@")
        if len(parts) != 2:
            return {"valid_syntax": False, "is_disposable": False, "is_role_based": False}

        user, domain = parts
        is_disposable = domain in DISPOSABLE_DOMAINS
        is_role_based = user in ROLE_BASED_PREFIXES
        valid_syntax = bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_clean))

        return {
            "valid_syntax": valid_syntax,
            "is_disposable": is_disposable,
            "is_role_based": is_role_based,
        }

    @classmethod
    def enrich_record(cls, record: LeadRecord) -> LeadRecord:
        validated_emails = []
        for em in record.emails:
            info = cls.classify_email(em)
            if info["valid_syntax"] and not info["is_disposable"]:
                validated_emails.append(em)

        record.emails = validated_emails

        if record.lead_score >= 70 and record.emails and "linkedin" in record.social_links:
            record.notes = "Tier-1 Lead (Email + LinkedIn Profile Found)"
        elif record.emails:
            record.notes = "Tier-2 Lead (Email Verified)"
        elif record.phones:
            record.notes = "Tier-3 Lead (Phone Verified Only)"
        else:
            record.notes = "Unverified (Metadata Only)"

        return record

    @classmethod
    def deduplicate(cls, records: List[LeadRecord]) -> List[LeadRecord]:
        seen_domains = set()
        unique_records = []
        for r in records:
            if r.domain and r.domain not in seen_domains:
                seen_domains.add(r.domain)
                unique_records.append(cls.enrich_record(r))
        return unique_records
