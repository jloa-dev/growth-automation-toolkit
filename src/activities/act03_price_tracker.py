"""
Actividad 03: E-commerce Competitor Price & Inventory Tracker.
Extracts pricing, currency, stock status, and discount rates across e-commerce product pages.
Target Pricing: $20 - $35 USD per catalog monitoring setup.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ProductPricePoint:
    url: str
    product_name: str
    current_price: float
    original_price: float
    currency: str
    discount_pct: float
    in_stock: bool
    sku: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class EcomPriceTracker:
    @staticmethod
    def extract_from_html(html: str, url: str) -> ProductPricePoint:
        # Check OpenGraph / Schema JSON-LD price first
        price = 0.0
        orig_price = 0.0
        currency = "USD"
        name = ""
        in_stock = True
        sku = ""

        # Schema JSON-LD
        schema_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S)
        for s in schema_matches:
            try:
                data = json.loads(s.strip())
                if isinstance(data, dict):
                    if data.get("@type") == "Product":
                        name = data.get("name", "")
                        offers = data.get("offers", {})
                        if isinstance(offers, dict):
                            price = float(offers.get("price", 0))
                            currency = offers.get("priceCurrency", "USD")
                            in_stock = "InStock" in offers.get("availability", "InStock")
                        sku = str(data.get("sku", ""))
            except Exception:
                pass

        if not name:
            t = re.search(r"<title[^>]*>(.*?)</title>", html, re.I)
            name = t.group(1).split("-")[0].strip() if t else "Unknown Product"

        if price == 0.0:
            price_match = re.search(r'(?:\$|€|£|USD\s*)\s*([0-9]+(?:\.[0-9]{2})?)', html)
            if price_match:
                price = float(price_match.group(1))

        if orig_price == 0.0:
            orig_price = price

        discount = 0.0
        if orig_price > price and orig_price > 0:
            discount = round(((orig_price - price) / orig_price) * 100, 1)

        return ProductPricePoint(
            url=url,
            product_name=name,
            current_price=price,
            original_price=orig_price,
            currency=currency,
            discount_pct=discount,
            in_stock=in_stock,
            sku=sku,
        )

    @staticmethod
    def export_price_comparison(products: List[ProductPricePoint], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["product_name", "current_price", "original_price", "currency", "discount_pct", "in_stock", "sku", "url"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in products:
                writer.writerow(p.to_dict())
        return str(path.resolve())


if __name__ == "__main__":
    sample_html = """
    <html><head><title>Wireless Noise Cancelling Headphones - AudioStore</title>
    <script type="application/ld+json">
    {"@type": "Product", "name": "AcousticPro Wireless Headphones", "sku": "AP-700", "offers": {"price": 149.99, "priceCurrency": "USD", "availability": "https://schema.org/InStock"}}
    </script>
    </head><body><h1>AcousticPro Headphones</h1><span class="price">$149.99</span></body></html>
    """
    tracker = EcomPriceTracker()
    prod = tracker.extract_from_html(sample_html, "https://audiostore.com/p/ap-700")
    out = tracker.export_price_comparison([prod], "output_activities/act03_prices.csv")
    print(f"✅ Actividad 03: Tracked {prod.product_name} at ${prod.current_price} -> {out}")
