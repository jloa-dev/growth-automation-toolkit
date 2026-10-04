"""
Actividad 14: High-Performance CSV Deduplicator & Normalizer.
Standardizes messy CSVs, normalizes phone numbers & emails, and deduplicates records by arbitrary keys.
Target Pricing: $10 - $20 USD per CRM data cleanup job.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, List, Set


class CSVDeduplicator:
    @staticmethod
    def normalize_phone(phone: str) -> str:
        digits = re.sub(r"\D", "", phone)
        if len(digits) == 10:
            return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith("1"):
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return phone.strip()

    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().lower()

    @classmethod
    def clean_and_dedupe(cls, rows: List[Dict[str, str]], dedupe_key: str = "email") -> tuple[List[Dict[str, str]], int]:
        seen: Set[str] = set()
        clean_rows: List[Dict[str, str]] = []
        duplicates_removed = 0

        for r in rows:
            # Normalize fields if present
            if "email" in r:
                r["email"] = cls.normalize_email(r["email"])
            if "phone" in r:
                r["phone"] = cls.normalize_phone(r["phone"])

            key_val = r.get(dedupe_key, "").strip().lower()
            if not key_val:
                clean_rows.append(r)
                continue

            if key_val in seen:
                duplicates_removed += 1
                continue

            seen.add(key_val)
            clean_rows.append(r)

        return clean_rows, duplicates_removed

    @staticmethod
    def export_csv(rows: List[Dict[str, str]], output_file: str | Path) -> str:
        if not rows:
            return ""
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return str(path.resolve())


if __name__ == "__main__":
    deduper = CSVDeduplicator()
    sample_data = [
        {"name": "Alice Smith", "email": "ALICE@acme.com", "phone": "1234567890", "company": "Acme Inc"},
        {"name": "Alice S.", "email": "alice@acme.com", "phone": "123-456-7890", "company": "Acme"},
        {"name": "Bob Jones", "email": "bob@globex.corp", "phone": "5551234567", "company": "Globex"},
    ]
    cleaned, dups = deduper.clean_and_dedupe(sample_data, dedupe_key="email")
    out = deduper.export_csv(cleaned, "output_activities/act14_cleaned_data.csv")
    print(f"✅ Actividad 14: Deduplicated data (removed {dups} duplicates) -> {out}")
