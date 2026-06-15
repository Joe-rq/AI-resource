#!/usr/bin/env python3
"""Batch-convert path-prefixed wikilinks to plain-title wikilinks.

Usage: python3 scripts/fix-wikilinks.py [--dry-run]
"""

import os
import re
import sys

WIKI_ROOT = "wiki"

# Special mappings for dangling links (summaries/raw/articles/... targets)
DANGLING_MAP = {
    "summaries/raw/articles/nvidia-agent-toolkit.md": "NVIDIA Agent Toolkit 架构",
    "summaries/raw/articles/2026-05-17-nanoclaws-second-brain.md": "新加坡外长的 AI 第二大脑",
    "summaries/raw/articles/2026-05-02-hermes-agent-nous-research.md": "Hermes Agent：Nous Research 的开源 Agent 框架",
}

# Malformed link fix
MALFORMED_FIXES = {
    "[Dive into Claude Code]([[entities/Dive-into-Claude-Code]])": "[[Dive into Claude Code（论文）]]",
}


def build_title_mapping():
    """Build dict: relative_path_without_ext -> title from frontmatter."""
    mapping = {}
    for dirpath, dirnames, filenames in os.walk(WIKI_ROOT):
        for f in filenames:
            if not f.endswith(".md"):
                continue
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, WIKI_ROOT)

            with open(full_path, "r", encoding="utf-8") as fh:
                content = fh.read()

            if not content.startswith("---"):
                continue
            fm_end = content.index("---", 3)
            fm_text = content[3:fm_end]

            m = re.search(r'^title:\s*"?([^"\n]+?)?"?\s*$', fm_text, re.MULTILINE)
            if not m:
                continue

            title = m.group(1).strip().strip('"')
            key = rel_path[:-3] if rel_path.endswith(".md") else rel_path
            mapping[key] = title

    return mapping


def convert_wikilink(match, title_map):
    """Convert a single [[...]] wikilink from path-prefixed to plain title."""
    full_match = match.group(0)
    inner = match.group(1)

    # Skip anchor links [[#section]]
    if inner.startswith("#"):
        return full_match

    # Check for alias: [[target|alias]]
    if "|" in inner:
        target, alias = inner.rsplit("|", 1)
        target = target.strip()
        alias = alias.strip()
    else:
        target = inner.strip()
        alias = None

    # Check if target is path-prefixed (contains /)
    if "/" not in target:
        # Already a plain title link - leave as-is
        return full_match

    # Handle folder-split index: concepts/Foo/index -> look up concepts/Foo/index
    # Also handle: concepts/Foo/index|Display Name

    # Try direct lookup
    if target in title_map:
        title = title_map[target]
        return f"[[{title}]]"

    # Try with .md stripped (in case target has .md extension)
    clean_target = target.removesuffix(".md")
    if clean_target in title_map:
        title = title_map[clean_target]
        return f"[[{title}]]"

    # Check dangling links
    if target in DANGLING_MAP:
        return f"[[{DANGLING_MAP[target]}]]"
    if clean_target in DANGLING_MAP:
        return f"[[{DANGLING_MAP[clean_target]}]]"

    # Fallback: couldn't resolve, leave as-is and warn
    print(f"  WARNING: Could not resolve wikilink target: {target}", file=sys.stderr)
    return full_match


def process_file(filepath, title_map, dry_run=False):
    """Process a single .md file, converting wikilinks."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix malformed links first
    for bad, good in MALFORMED_FIXES.items():
        content = content.replace(bad, good)

    # Fix escaped pipe in wikilinks: [[foo\|bar]] -> [[foo|bar]]
    # Some files have backslash before pipe as an escape artifact
    content = re.sub(r"\[\[([^\]]*?)\\\|([^\]]*?)\]\]", r"[[\1|\2]]", content)

    # Convert path-prefixed wikilinks
    # Pattern: [[...]] where ... may contain | for alias
    wikilink_pattern = re.compile(r"\[\[([^\]]+)\]\]")
    content = wikilink_pattern.sub(lambda m: convert_wikilink(m, title_map), content)

    if content == original:
        return 0

    changes = sum(1 for a, b in zip(original.split("\n"), content.split("\n")) if a != b)

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changes


def main():
    dry_run = "--dry-run" in sys.argv

    print("Building title mapping...")
    title_map = build_title_mapping()
    print(f"  Found {len(title_map)} pages with titles")

    print(f"\nProcessing wiki files (dry_run={dry_run})...")
    total_changes = 0
    files_changed = 0

    for dirpath, dirnames, filenames in os.walk(WIKI_ROOT):
        for f in filenames:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(dirpath, f)
            changes = process_file(filepath, title_map, dry_run)
            if changes > 0:
                print(f"  {filepath}: {changes} lines changed")
                total_changes += changes
                files_changed += 1

    print(f"\nDone. {files_changed} files changed, {total_changes} total lines modified.")


if __name__ == "__main__":
    main()
