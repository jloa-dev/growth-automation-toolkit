"""
Actividad 08: Financial & Invoice Document Table Extractor.
Extracts structured line items, amounts, dates, and vendor details from semi-structured documents.
Target Pricing: $20 - $40 USD per financial batch conversion.
"""

from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class InvoiceLineItem:
    item_id: str
    description: str
    quantity: float
    unit_price: float
    total_amount: float

    def to_dict(self) -> Dict:
        return asdict(self)


class InvoiceTableExtractor:
    @staticmethod
    def parse_plain_text_table(text: str) -> List[InvoiceLineItem]:
        lines = text.strip().split("\n")
        items = []

        # Matches lines with item code/number, description, quantity, price, total
        # e.g.: "ITEM-01  Cloud Database Hosting  2  $45.00  $90.00"
        pattern = re.compile(
            r"^([A-Z0-9_-]+)\s+(.+?)\s+([0-9]+(?:\.[0-9]+)?)\s+\$?([0-9,]+(?:\.[0-9]{2})?)\s+\$?([0-9,]+(?:\.[0-9]{2})?)$"
        )

        for line in lines:
            line_clean = line.strip()
            match = pattern.match(line_clean)
            if match:
                item_id, desc, qty, unit, total = match.groups()
                items.append(InvoiceLineItem(
                    item_id=item_id,
                    description=desc.strip(),
                    quantity=float(qty),
                    unit_price=float(unit.replace(",", "")),
                    total_amount=float(total.replace(",", "")),
                ))

        return items

    @staticmethod
    def export_csv(items: List[InvoiceLineItem], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["item_id", "description", "quantity", "unit_price", "total_amount"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.to_dict())
        return str(path.resolve())


if __name__ == "__main__":
    extractor = InvoiceTableExtractor()
    sample_invoice_text = """
    ITEM-101  API Server Cluster Subscription   1   120.00   120.00
    ITEM-102  SSL Dedicated Wildcard Cert        2    25.00    50.00
    ITEM-103  Managed Backup Storage (TB)        4    15.50    62.00
    """
    parsed_items = extractor.parse_plain_text_table(sample_invoice_text)
    out = extractor.export_csv(parsed_items, "output_activities/act08_invoice_items.csv")
    print(f"✅ Actividad 08: Extracted {len(parsed_items)} line items -> {out}")
