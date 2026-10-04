"""
Actividad 13: Video Transcript Extractor & Multi-Platform Content Repurposer.
Transforms video transcripts into executive summaries, Twitter threads, and LinkedIn posts.
Target Pricing: $15 - $30 USD per video content repurposing package.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class RepurposedContent:
    title: str
    executive_summary: str
    key_takeaways: List[str]
    twitter_thread: List[str]
    linkedin_post: str

    def to_dict(self) -> Dict:
        return asdict(self)


class TranscriptRepurposer:
    @classmethod
    def process_transcript(cls, title: str, transcript: str) -> RepurposedContent:
        clean_text = re.sub(r"\s+", " ", transcript).strip()
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text) if len(s.strip()) > 15]

        # Extract 4 key takeaways
        takeaways = []
        for s in sentences:
            if any(k in s.lower() for k in ["important", "key", "remember", "strategy", "result", "first", "must"]):
                takeaways.append(s)
            if len(takeaways) >= 4:
                break
        if not takeaways:
            takeaways = sentences[:4]

        # Twitter Thread (3 tweets)
        t1 = f"🧵 1/3 Break down: {title}\n\nHere are the core insights and actionable takeaways you can apply today 👇"
        t2 = f"2/3 The core bottleneck:\n\n• {takeaways[0] if len(takeaways) > 0 else 'Focus on high-leverage execution'}\n• {takeaways[1] if len(takeaways) > 1 else 'Automate deterministic workflows'}"
        t3 = f"3/3 Summary:\n\nDon't waste time on manual repetitive work. Build systems that compound.\n\nRetweet if you found this valuable!"
        thread = [t1, t2, t3]

        # LinkedIn Post
        li = (
            f"🚀 Key lessons from '{title}':\n\n"
            + "\n".join([f"🔹 {t}" for t in takeaways])
            + "\n\n💡 What is your perspective on this? Let's discuss in the comments below.\n\n#Automation #Engineering #Productivity"
        )

        exec_summary = " ".join(sentences[:3])

        return RepurposedContent(
            title=title,
            executive_summary=exec_summary,
            key_takeaways=takeaways,
            twitter_thread=thread,
            linkedin_post=li,
        )

    @staticmethod
    def export_markdown(content: RepurposedContent, output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# 🎬 Repurposed Content Kit: {content.title}",
            f"\n## 📌 Executive Summary",
            f"{content.executive_summary}",
            f"\n## 🎯 Key Takeaways",
        ]
        for tk in content.key_takeaways:
            lines.append(f"- {tk}")
        lines.append("\n## 🐦 Twitter / X Thread")
        for tw in content.twitter_thread:
            lines.append(f"\n```text\n{tw}\n```")
        lines.append("\n## 💼 LinkedIn Post Draft")
        lines.append(f"\n```text\n{content.linkedin_post}\n```")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return str(path.resolve())


if __name__ == "__main__":
    repurposer = TranscriptRepurposer()
    sample_text = (
        "In this talk we break down how modern engineering teams move 10x faster with autonomous workflows. "
        "The first important strategy is to remove all human friction from continuous delivery. "
        "A key finding from our benchmarks showed that 80 percent of errors come from manual configuration drift. "
        "You must eliminate manual data entry with programmatic validation before shipping. "
        "This completely transforms developer velocity."
    )
    res = repurposer.process_transcript("10x Engineering Velocity", sample_text)
    out = repurposer.export_markdown(res, "output_activities/act13_repurposed_content.md")
    print(f"✅ Actividad 13: Repurposed video transcript -> {out}")
