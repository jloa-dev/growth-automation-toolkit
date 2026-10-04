"""
Actividad 07: Markdown to Polished eBook / Digital Guide Builder.
Transforms raw markdown notes and documentation into publication-ready formatted HTML/PDF guides.
Target Pricing: $10 - $25 USD per formatted digital asset / guide.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


class EbookBuilder:
    @staticmethod
    def markdown_to_html(md: str) -> str:
        # Convert headers
        html = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", md, flags=re.M)
        html = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html, flags=re.M)
        html = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", html, flags=re.M)

        # Bold and italic
        html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

        # Code blocks
        html = re.sub(r"```([a-zA-Z]*)\n(.*?)```", r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.S)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

        # Paragraphs
        paragraphs = html.split("\n\n")
        formatted = []
        for p in paragraphs:
            p_strip = p.strip()
            if not p_strip.startswith(("<h1", "<h2", "<h3", "<pre")):
                formatted.append(f"<p>{p_strip.replace('\n', '<br>')}</p>")
            else:
                formatted.append(p_strip)

        return "\n".join(formatted)

    @classmethod
    def compile_book(cls, title: str, author: str, chapters: List[Dict[str, str]], output_file: str | Path) -> str:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Build TOC
        toc_items = [f'<li><a href="#chap-{i}">{chap["title"]}</a></li>' for i, chap in enumerate(chapters, 1)]
        toc_html = f"<div class='toc'><h2>Table of Contents</h2><ul>{''.join(toc_items)}</ul></div>"

        # Build chapters
        chapter_blocks = []
        for i, chap in enumerate(chapters, 1):
            chap_body = cls.markdown_to_html(chap["content"])
            chapter_blocks.append(f"<section id='chap-{i}' class='chapter'><h2>Chapter {i}: {chap['title']}</h2>{chap_body}</section>")

        document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: 'Georgia', serif; line-height: 1.6; max-width: 800px; margin: 40px auto; color: #222; padding: 0 20px; }}
    h1, h2, h3 {{ font-family: 'Helvetica Neue', sans-serif; color: #111; }}
    .cover {{ text-align: center; padding: 60px 0; border-bottom: 2px solid #eee; margin-bottom: 40px; }}
    .toc {{ background: #f9f9f9; padding: 25px; border-radius: 8px; margin: 30px 0; }}
    pre {{ background: #1e1e1e; color: #dcdcdc; padding: 16px; border-radius: 6px; overflow-x: auto; font-family: monospace; }}
    code {{ background: #f0f0f0; padding: 2px 5px; border-radius: 4px; font-family: monospace; }}
    .chapter {{ margin-top: 50px; page-break-before: always; }}
  </style>
</head>
<body>
  <div class="cover">
    <h1>{title}</h1>
    <p><em>By {author}</em></p>
  </div>
  {toc_html}
  {''.join(chapter_blocks)}
</body>
</html>"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(document)
        return str(path.resolve())


if __name__ == "__main__":
    builder = EbookBuilder()
    chaps = [
        {"title": "The Autonomous Edge", "content": "# Overview\n\nHow AI workflows replace manual data scraping.\n\n```python\nprint('Hello automation')\n```"},
        {"title": "Monetization Architecture", "content": "## Revenue Vectors\n\nFocus on **high-intent buyers** with immediate delivery."},
    ]
    out = builder.compile_book("The Autonomous Growth Playbook", "jloa-dev", chaps, "output_activities/act07_ebook.html")
    print(f"✅ Actividad 07: Generated polished publication -> {out}")
