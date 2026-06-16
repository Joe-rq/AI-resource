#!/usr/bin/env python3
"""
check_consistency.py — 检查 CLAUDE.md ↔ index.md ↔ wiki/磁盘 的三方一致性。

用法:
    uv run python scripts/check_consistency.py [--root .]

退出码: 0 = 一致, 1 = 不一致
"""

import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    result = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def get_disk_pages(wiki_dir: Path) -> dict[str, str]:
    """Return {stem: title} for all top-level wiki pages (skip folder-split children)."""
    pages = {}
    for p in sorted(wiki_dir.rglob("*.md")):
        rel = str(p.relative_to(wiki_dir))
        # Skip folder-split sub-pages (parent != null)
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm and fm.get("parent"):
            continue
        title = fm.get("title", p.stem) if fm else p.stem
        pages[rel] = title
    return pages


def get_claude_md_slugs(root_dir: Path) -> set[str]:
    """Extract page references from CLAUDE.md (all sections)."""
    claude_path = root_dir / "CLAUDE.md"
    if not claude_path.exists():
        return set()
    text = claude_path.read_text(encoding="utf-8")
    slugs = set()
    in_articles = False
    for line in text.split("\n"):
        ls = line.strip()
        if ls == "## Current articles":
            in_articles = True
            continue
        if in_articles and ls.startswith("## "):
            break
        if not in_articles:
            continue
        # Wikilink entries: "- [[Page Title]] — desc"
        for m in WIKILINK_RE.finditer(line):
            slugs.add(m.group(1).strip())
        # Slug entries in Summaries: "- slug — desc"
        if ls.startswith("- ") and not ls.startswith("- [["):
            slug = ls[2:].split(" — ")[0].strip()
            if slug:
                slugs.add(slug)
    return slugs


def get_index_titles(wiki_dir: Path) -> set[str]:
    """Extract all wikilink targets from index.md."""
    index_path = wiki_dir / "index.md"
    if not index_path.exists():
        return set()
    text = index_path.read_text(encoding="utf-8")
    return {m.group(1).strip() for m in WIKILINK_RE.finditer(text)}


def slug_matches(slug: str, rel_path: str, title: str) -> bool:
    """Check if a CLAUDE.md reference matches a disk page."""
    stem = Path(rel_path).stem
    # Direct stem match (for summary slugs like "01-minimax-...")
    if slug == stem:
        return True
    # Title match (for wikilink refs like "Agent Runtime")
    if slug == title:
        return True
    # Space-normalized stem match
    if slug == stem.replace("-", " "):
        return True
    # Folder-split: "Agent Memory" matches concepts/Agent-Memory/index.md
    if rel_path.endswith("/index.md"):
        parent_dir = Path(rel_path).parent.stem  # "Agent-Memory"
        if slug == parent_dir or slug == parent_dir.replace("-", " "):
            return True
        # Also match "Claude-Code-Subagent/index" format
        idx_slug = f"{parent_dir}/index"
        if slug == idx_slug:
            return True
    return False


def main():
    args = [a for a in sys.argv[1:] if a != "--root"]
    root = Path(args[0]) if args else Path(".")
    root = root.resolve()
    wiki_dir = root / "wiki"

    if not wiki_dir.exists():
        print(f"ERROR: wiki/ directory not found at {wiki_dir}")
        return 1

    issues = 0
    disk = get_disk_pages(wiki_dir)
    claude_slugs = get_claude_md_slugs(root)
    index_titles = get_index_titles(wiki_dir)

    # Known exclusions
    TOMBSTONE_SLUGS = {"hermes-agent-harness-engineering"}

    # ── Check: disk → CLAUDE.md ──
    for rel, title in sorted(disk.items()):
        if rel == "index.md":
            continue
        matched = any(slug_matches(s, rel, title) for s in claude_slugs)
        if not matched:
            print(f"🟡 Disk page not in CLAUDE.md: {rel} (\"{title}\")")
            issues += 1

    # ── Check: CLAUDE.md → disk ──
    for slug in sorted(claude_slugs):
        if slug in TOMBSTONE_SLUGS:
            continue
        matched = any(slug_matches(slug, rel, title) for rel, title in disk.items())
        if not matched:
            print(f"🔴 CLAUDE.md entry not on disk: {slug}")
            issues += 1

    # ── Check: disk → index.md ──
    for rel, title in sorted(disk.items()):
        if rel == "index.md":
            continue
        if title in index_titles:
            continue
        # Space-normalized stem
        if Path(rel).stem.replace("-", " ") in index_titles:
            continue
        # Folder-split: parent dir name
        if rel.endswith("/index.md"):
            parent_name = Path(rel).parent.stem.replace("-", " ")
            if parent_name in index_titles:
                continue
        print(f"🟡 Disk page not in index.md: {rel} (\"{title}\")")
        issues += 1

    # ── Summary ──
    print(f"\n{'─'*40}")
    if issues == 0:
        print("✅ CLAUDE.md ↔ index.md ↔ wiki/disk 三方一致")
    else:
        print(f"⚠️  {issues} consistency issue(s) found")

    return 0 if issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
