#!/usr/bin/env python3
"""Batch-fetch Madhu Guru's "How to build great evals" tweets.

For each tweet id: curl the X status page HTML, extract the full text
from <h1 class="sr-only">, date / view / engagement counts from meta tags,
and write a clean Markdown file under raw/notes/madhuguru-evals/.
"""
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

OUT_DIR = Path("raw/notes/madhuguru-evals")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TWEETS = [
    # (part, tweet_id, iso_date, view_hint)
    (1,  "2089480958571331623", "2026-08-17", None),  # prologue / "This could be a series"
    (2,  "2089918106814603728", "2026-08-19", None),
    (3,  "2090242427944833047", "2026-08-20", None),
    (4,  "2090595384905113939", "2026-08-21", None),
    (5,  "2090930137885774324", "2026-08-21", None),
    (6,  "2091278653435072523", "2026-08-22", None),
    (7,  "2091684812012875981", "2026-08-24", None),
    (8,  "2092058332735693264", "2026-08-25", None),
    (9,  "2092426017118028266", "2026-08-26", None),
    (10, "2098064969464217720", "2026-09-10", None),
]


def curl_html(tweet_id: str) -> str:
    url = f"https://x.com/realmadhuguru/status/{tweet_id}"
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "30", "-A",
         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
         url],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def extract_sr_only(html: str) -> str | None:
    """The accessibility <h1 class="sr-only"> holds the full tweet text."""
    m = re.search(r'<h1 class="sr-only">(.*?)</h1>', html, re.DOTALL)
    if not m:
        return None
    return unescape(m.group(1)).strip()


def extract_meta(html: str, prop: str) -> str | None:
    m = re.search(rf'<meta property="{re.escape(prop)}" content="([^"]+)"', html)
    if not m:
        return None
    return unescape(m.group(1)).strip()


def extract_display_time(html: str) -> str | None:
    """The formatted display time e.g. '3:04 PM · Sep 10, 2026'."""
    m = re.search(r'(\d{1,2}:\d{2}\s*[AP]M\s*·\s*[A-Z][a-z]{2}\s*\d{1,2},\s*\d{4})', html)
    if not m:
        return None
    return m.group(1)


def extract_engagement(html: str, tweet_id: str) -> dict:
    """Sidebar counters for the *primary* tweet.

    X renders ``aria-label="Reply" / "Repost" / "Like" / "Bookmark" /
    "View count"`` buttons; the visible count is the first ``>N<`` (or
    ``>N.NK<``) inside the button. The Reply button for the primary
    tweet has ``href="/i/status/<tweet_id>"`` — we anchor there and walk
    forward through the next ~5KB to capture the other four buttons.
    """
    out = {"views": None, "replies": None, "reposts": None,
           "likes": None, "bookmarks": None}
    anchor_pat = rf'href="/i/status/{re.escape(tweet_id)}"[^>]*aria-label="Reply"'
    anchor_m = re.search(anchor_pat, html)
    if not anchor_m:
        # Fallback: just take first "Reply" anchor
        anchor_m = re.search(r'aria-label="Reply"', html)
        if not anchor_m:
            return out
    slice_ = html[anchor_m.start():anchor_m.start() + 5000]
    for key, aria in [("replies", "Reply"),
                      ("reposts", "Repost"),
                      ("likes", "Like"),
                      ("bookmarks", "Bookmark"),
                      ("views", "View count")]:
        m = re.search(rf'aria-label="{aria}"', slice_)
        if not m:
            continue
        # The button is a complex element; the visible count is the
        # first bare number wrapped in a span/div after the aria-label
        # for "Reply/Repost/Like/Bookmark"; for View count it's just
        # the first number in the button. Search a small window.
        window = slice_[m.start():m.start() + 3000]
        nums = re.findall(r'>(\d+(?:\.\d+)?[KM]?)<', window)
        # Skip "0" because that means the counter hasn't loaded; keep
        # the first meaningful one.
        for n in nums:
            if n == "0":
                continue
            out[key] = n
            break
    return out


def strip_x_prefix(full_text: str) -> str:
    """The accessibility h1 often reads ``Madhu Guru on X: "..."``."""
    return re.sub(r'^Madhu Guru on X:\s*["“]?', '', full_text).rstrip('"” ').strip()


def split_title_and_body(full_text: str) -> tuple[str, str]:
    """If text starts with 'How to build great evals — Part N' treat as title.

    The sr-only h1 begins with ``Madhu Guru on X: "`` — strip that first.
    """
    text = strip_x_prefix(full_text)
    m = re.match(r'^(How to build great evals\s*[—–-]\s*[Pp]art\s*\d+\b)', text)
    if m:
        return m.group(1).rstrip('—–- ').strip(), text[m.end():].lstrip('\n').strip()
    return "", text


def render_markdown(part: int, tweet_id: str, iso_date: str, full_text: str,
                    og_desc: str | None, display_time: str | None,
                    engagement: dict) -> str:
    title, body = split_title_and_body(full_text)
    header = title if title else f"How to build great evals — Part {part} (prologue)"
    url = f"https://x.com/realmadhuguru/status/{tweet_id}"

    lines = []
    lines.append("---")
    lines.append(f'title: "{header}"')
    lines.append(f"type: source")
    lines.append("source_type: tweet")
    lines.append(f"source_url: {url}")
    lines.append(f"tweet_id: \"{tweet_id}\"")
    lines.append(f"author: realmadhuguru")
    lines.append(f"date: {iso_date}")
    if display_time:
        lines.append(f"display_time: \"{display_time}\"")
    for key in ("replies", "reposts", "likes", "bookmarks", "views"):
        if engagement.get(key):
            lines.append(f"{key}: \"{engagement[key]}\"")
    lines.append("tags: [agent-evals, eval-methodology, agent-evaluation]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {header}")
    lines.append("")
    lines.append(f"**Source**: [Madhu Guru (@realmadhuguru) on X]({url}) · {iso_date}")
    lines.append("")
    lines.append("## Full text")
    lines.append("")
    lines.append(body)
    lines.append("")
    if og_desc and og_desc != full_text[:280]:
        lines.append("## OpenGraph description (preview)")
        lines.append("")
        lines.append(f"> {og_desc}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- Tweet ID: `{tweet_id}`")
    lines.append(f"- Author: [@realmadhuguru](https://x.com/realmadhuguru) (Madhu Guru)")
    lines.append(f"- URL: {url}")
    lines.append("- Extraction: full text from accessibility `<h1 class=\"sr-only\">` (no login)")
    lines.append(f"- Date source: meta `article:published_time` and rendered display time")
    lines.append("")
    return "\n".join(l for l in lines if l is not None)


def main() -> int:
    failures = []
    for part, tid, iso_date, _ in TWEETS:
        out_path = OUT_DIR / f"part-{part:02d}-{iso_date}.md"
        if out_path.exists() and out_path.stat().st_size > 200:
            print(f"skip {out_path.name} (already present)")
            continue
        print(f"fetch part {part:02d} ({tid}) …", end=" ", flush=True)
        try:
            html = curl_html(tid)
        except Exception as e:
            print(f"FAIL curl: {e}")
            failures.append((part, tid, str(e)))
            continue
        full_text = extract_sr_only(html)
        if not full_text:
            print("FAIL no <h1 class=sr-only>")
            failures.append((part, tid, "no sr-only h1"))
            continue
        og_desc = extract_meta(html, "og:description")
        display_time = extract_display_time(html)
        engagement = extract_engagement(html, tid)
        md = render_markdown(part, tid, iso_date, full_text, og_desc, display_time, engagement)
        out_path.write_text(md, encoding="utf-8")
        print(f"ok ({len(full_text)} chars)")
    if failures:
        print("\nFailures:", json.dumps(failures, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())