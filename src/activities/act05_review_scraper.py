"""
Actividad 05: Customer Review & Sentiment Analyzer.
Extracts product/service customer reviews and computes sentiment scores for market research.
Target Pricing: $20 - $35 USD per competitive review analysis.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


POSITIVE_WORDS = {"excellent", "great", "awesome", "fantastic", "love", "good", "fast", "helpful", "easy", "perfect"}
NEGATIVE_WORDS = {"terrible", "bad", "slow", "awful", "horrible", "broken", "scam", "waste", "buggy", "frustrating"}


@dataclass
class CustomerReview:
    author: str
    rating: int
    title: str
    body: str
    sentiment: str
    sentiment_score: float

    def to_dict(self) -> Dict:
        return asdict(self)


class ReviewSentimentAnalyzer:
    @staticmethod
    def calculate_sentiment(text: str) -> tuple[str, float]:
        tokens = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
        pos_hits = len(tokens & POSITIVE_WORDS)
        neg_hits = len(tokens & NEGATIVE_WORDS)

        if pos_hits > neg_hits:
            score = round((pos_hits) / max(pos_hits + neg_hits, 1), 2)
            return "POSITIVE", score
        elif neg_hits > pos_hits:
            score = round(-(neg_hits) / max(pos_hits + neg_hits, 1), 2)
            return "NEGATIVE", score
        else:
            return "NEUTRAL", 0.0

    @classmethod
    def parse_reviews_from_text(cls, reviews_data: List[Dict]) -> List[CustomerReview]:
        results = []
        for r in reviews_data:
            body = r.get("body", "")
            sent, score = cls.calculate_sentiment(body)
            results.append(CustomerReview(
                author=r.get("author", "Anonymous"),
                rating=int(r.get("rating", 5)),
                title=r.get("title", ""),
                body=body,
                sentiment=sent,
                sentiment_score=score,
            ))
        return results

    @staticmethod
    def export_csv(reviews: List[CustomerReview], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["author", "rating", "title", "body", "sentiment", "sentiment_score"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rev in reviews:
                writer.writerow(rev.to_dict())
        return str(path.resolve())


if __name__ == "__main__":
    analyzer = ReviewSentimentAnalyzer()
    sample_data = [
        {"author": "Alex M.", "rating": 5, "title": "Incredible experience", "body": "Great support, fast delivery and love the dashboard."},
        {"author": "Sarah K.", "rating": 1, "title": "Disappointed", "body": "Terrible checkout flow, bad customer service and broken links."},
        {"author": "David R.", "rating": 3, "title": "Average", "body": "Standard software, does what it says."}
    ]
    parsed = analyzer.parse_reviews_from_text(sample_data)
    out = analyzer.export_csv(parsed, "output_activities/act05_reviews.csv")
    print(f"✅ Actividad 05: Analyzed {len(parsed)} reviews -> {out}")
