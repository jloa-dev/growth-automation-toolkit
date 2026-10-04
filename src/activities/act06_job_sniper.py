"""
Actividad 06: Tech Stack Hiring Signal Detector.
Scrapes and monitors job boards for companies actively hiring specific tech stacks (Next.js, Python, AI, AWS).
Target Pricing: $25 - $50 USD per weekly curated B2B lead feed.
"""

from __future__ import annotations

import csv
import json
import re
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class JobLead:
    company: str
    role_title: str
    detected_stack: List[str]
    location: str
    apply_url: str
    hiring_urgency: str

    def to_dict(self) -> Dict:
        return asdict(self)


class JobSniper:
    TARGET_STACKS = {"python", "react", "next.js", "typescript", "fastapi", "solana", "aws", "docker"}

    @classmethod
    def analyze_listing(cls, company: str, title: str, description: str, apply_url: str, location: str = "Remote") -> JobLead:
        desc_lower = description.lower()
        found_stack = []
        for tech in cls.TARGET_STACKS:
            if re.search(rf"\b{re.escape(tech)}\b", desc_lower):
                found_stack.append(tech.title())

        urgency = "High" if any(w in desc_lower for w in ["immediate", "urgent", "signing bonus", "asap"]) else "Normal"

        return JobLead(
            company=company,
            role_title=title,
            detected_stack=found_stack,
            location=location,
            apply_url=apply_url,
            hiring_urgency=urgency,
        )

    @staticmethod
    def export_csv(jobs: List[JobLead], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["company", "role_title", "detected_stack", "location", "apply_url", "hiring_urgency"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for j in jobs:
                d = j.to_dict()
                d["detected_stack"] = "; ".join(d["detected_stack"])
                writer.writerow(d)
        return str(path.resolve())


if __name__ == "__main__":
    sniper = JobSniper()
    sample_jobs = [
        sniper.analyze_listing(
            "Fintech Dynamics",
            "Senior Backend Engineer",
            "We urgently need an experienced engineer with Python, FastAPI, and Docker for our high-frequency payment rail.",
            "https://jobs.fintechdynamics.com/apply/backend",
        ),
        sniper.analyze_listing(
            "CloudVenture Labs",
            "Full Stack Lead",
            "Building our core dashboard in Next.js, React, and TypeScript on AWS.",
            "https://cloudventure.io/careers/fullstack",
        ),
    ]
    out = sniper.export_csv(sample_jobs, "output_activities/act06_hiring_leads.csv")
    print(f"✅ Actividad 06: Extracted {len(sample_jobs)} tech hiring leads -> {out}")
