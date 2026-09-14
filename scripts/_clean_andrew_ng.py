#!/usr/bin/env python3
"""Clean and write Andrew Ng's "AI Engineering Skills Map" 5 articles.

Each article has identical chrome (nav, breadcrumb, tags, share buttons,
footer, Elevenlabs player). The body is the letter from "Dear friends"
through "Andrew" + optional P.S.

This script takes the raw markdown fetched earlier and writes cleaned,
frontmatter-prefixed files under raw/articles/andrew-ng-skills-map/.
"""
from pathlib import Path
import re

OUT_DIR = Path("raw/articles/andrew-ng-skills-map")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (part, slug, date, title, raw_md_path)
ARTICLES = [
    (1, "the-ai-engineering-skills-map",
     "2026-08-14",
     "The AI Engineering Skills Map Part 1 — Andrew Ng and DeepLearning.AI Present the Essential Skills Every AI Engineer Needs to Know",
     "Building and deploying AI applications · Software engineering fundamentals · Using coding agents · Shaping the build",
     "/tmp/andrew_part1.md"),
    (2, "he-ai-engineering-skills-map-in-detail-building-and-deploying-ai-applications",
     "2026-08-21",
     "The AI Engineering Skills Map Part 2 — AI Applications: What You Need to Know to Build and Deploy AI Applications In Real Life",
     "LLM foundations · Grounding with data · Agentic systems · Eval-driven development · Production · ML foundations",
     "/tmp/andrew_part2.md"),
    (3, "the-ai-engineering-skills-map-in-detail-software-engineering-fundamentals",
     "2026-08-28",
     "The AI Engineering Skills Map Part 3 — Fundamentals: Why Software Engineering Fundamentals Remain Essential for AI Developers",
     "Full-stack · Data · System architecture · Secure & reliable · Production",
     "/tmp/andrew_part3.md"),
    (4, "the-ai-engineering-skills-map-in-detail-using-coding-agents",
     "2026-09-04",
     "The AI Engineering Skills Map Part 4 — Coding Agents: How to Use Coding Agents Effectively from Planning to Execution and Monitoring",
     "Planning · Execution · Deploy/monitor · Directing workflow · Agent autonomy · Review · Customization · Foundations",
     "/tmp/andrew_part4.md"),
    (5, "the-ai-engineering-skills-map-in-detail-shaping-the-build",
     "2026-09-11",
     "The AI Engineering Skills Map In Detail -- Shaping the Build: AI Engineering Adds New Responsibilities and Opportunities for Product Leadership",
     "Driving build loop · Product decisions · Communicating & leading · High-agency ownership",
     "/tmp/andrew_part5.md"),
]


def extract_body(md: str) -> str:
    """Strip chrome and return just the letter body."""
    # Body starts at "Dear friends," and ends just before the second
    # "Share" line (the first occurrence is inside chrome above the
    # body — but since we slice from "Dear friends," onwards we just
    # need to stop at the next "Share" line after the body ends).
    start = md.find("Dear friends,")
    if start < 0:
        start = md.find("Dear friends")
    if start < 0:
        raise ValueError("could not find body start 'Dear friends'")
    rest = md[start:]

    # Find the body-end anchor: the line that contains the trailing
    # "Andrew" right before the post-body Share/footer block. The
    # pattern is "...\n\nAndrew \n\nShare" or "...\n\nAndrew\n\nShare".
    end_m = re.search(r"\nShare\n", rest)
    if not end_m:
        # Part 1 has a P.S. section after "Andrew" — capture everything
        # up to the next "Share" after that.
        end_m = re.search(r"\nShare", rest[5000:]) if len(rest) > 5000 else None
    if not end_m:
        raise ValueError("could not find body end 'Share' marker")
    body = rest[:end_m.start()]

    # Strip the Elevenlabs loader line if present (lives in the chrome
    # block right above "Dear friends" but doesn't reach body if we
    # slice correctly — defensive).
    body = re.sub(r"^Loading the \[Elevenlabs[^\n]*\n", "", body, flags=re.MULTILINE)
    # Remove the in-body share/social icon lines (they sometimes leak
    # through if the page rendered oddly).
    body = re.sub(r"^-   \[\]\([^\)]*\)\n", "", body, flags=re.MULTILINE)
    return body.strip()


def render_frontmatter(part: int, slug: str, date: str, title: str, subskills: str, body: str) -> str:
    url = f"https://www.deeplearning.ai/the-batch/{slug}"
    out = []
    out.append("---")
    out.append(f'source: "{url}"')
    out.append(f'title: "{title}"')
    out.append(f'date: "{date}"')
    out.append("platform: \"deeplearning-ai-the-batch\"")
    out.append("author: \"Andrew Ng\"")
    out.append("series: \"AI Engineering Skills Map\"")
    out.append(f"part: {part}")
    out.append(f"tags: [ai-engineering, coding-agents, eval-driven-development, agent-skills, software-engineering]")
    out.append(f"sub_skills: \"{subskills}\"")
    out.append("---")
    out.append("")
    out.append(f"# {title}")
    out.append("")
    out.append(f"> Source: [The Batch / Andrew's Letters]({url}) · {date}")
    out.append(f"> Series: AI Engineering Skills Map · Part {part} of 5")
    out.append(f"> Sub-skills in this letter: {subskills}")
    out.append("")
    out.append("---")
    out.append("")
    out.append(body)
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"*Compiled via WebFetch (markdown conversion) on 2026-09-13. Page chrome (nav, breadcrumb, tags, Elevenlabs player, share buttons, footer) stripped; body preserved verbatim including 'Dear friends' / 'Keep building' framing.*")
    out.append("")
    return "\n".join(out)


def main() -> int:
    failures = []
    for part, slug, date, title, subskills, raw_path in ARTICLES:
        raw_p = Path(raw_path)
        if not raw_p.exists():
            failures.append((part, f"missing {raw_path}"))
            continue
        md = raw_p.read_text(encoding="utf-8")
        try:
            body = extract_body(md)
        except ValueError as e:
            failures.append((part, str(e)))
            continue
        rendered = render_frontmatter(part, slug, date, title, subskills, body)
        out_path = OUT_DIR / f"part-{part:02d}-{date}.md"
        out_path.write_text(rendered, encoding="utf-8")
        print(f"part {part}: {len(body)} body chars -> {out_path.name}")
    if failures:
        print("\nFailures:")
        for f in failures:
            print(" ", f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())