#!/usr/bin/env python3
"""Lint & fix: same-target wikilink linked more than N times per page.

CLAUDE.md naming rule: "Link the first mention of every entity or concept.
Do not link the same page more than twice per article."

This catches a blind spot of lint_redundant_aliases.py (which only flags
[[X|X]] where target==alias): the same page linked 3+ times, possibly under
different aliases (e.g. [[Nous Research]] and [[Nous Research|Hermes]]).

Modes:
  default        scan git-diff-changed wiki files (hook-friendly), report only
  --all          scan the entire wiki/
  --fix          deduplicate — keep the first N links per target, strip [[]]
                 from the rest ([[A|B]] -> B, [[A]] -> A). Combine with --all
                 to fix the whole wiki at once.
  --threshold N  max links allowed per target per page (default 2, per rule)
  --root PATH    wiki root (default: auto-detect next to this file's parent)

Target = text before '|' (and before '#' heading anchors) inside [[...]].
Wikilinks inside fenced code blocks are ignored. Exits 1 on violations
(lint mode), 0 otherwise.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

# [[target]], [[target|alias]], [[target#anchor]], [[target#anchor|alias]]
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")


def _fence_line_numbers(text: str) -> set[int]:
    """Return 1-based line numbers that are fenced code block delimiters or contents."""
    inside: set[int] = set()
    in_fence = False
    for i, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            inside.add(i)
            continue
        if in_fence:
            inside.add(i)
    return inside


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_violations(path: Path, threshold: int) -> list[tuple[str, int, int]]:
    """Return [(target, count, first_line)] for targets linked more than threshold times."""
    text = path.read_text(encoding="utf-8")
    fence_lines = _fence_line_numbers(text)
    counts: dict[str, list[int]] = {}
    for m in WIKILINK_RE.finditer(text):
        if _line_of(text, m.start()) in fence_lines:
            continue
        target = m.group(1).strip()
        counts.setdefault(target, []).append(_line_of(text, m.start()))
    return [(t, len(lines), lines[0]) for t, lines in counts.items() if len(lines) > threshold]


def fix_page(path: Path, threshold: int) -> int:
    """Keep the first `threshold` links per target, strip [[]] from the rest. Returns edits made."""
    text = path.read_text(encoding="utf-8")
    fence_lines = _fence_line_numbers(text)

    seen: dict[str, int] = {}
    to_strip: list[tuple[int, int, str]] = []  # (start, end, replacement)
    for m in WIKILINK_RE.finditer(text):
        if _line_of(text, m.start()) in fence_lines:
            continue
        target = m.group(1).strip()
        seen[target] = seen.get(target, 0) + 1
        if seen[target] <= threshold:
            continue
        alias = m.group(2)
        repl = alias.strip() if alias is not None else target
        to_strip.append((m.start(), m.end(), repl))

    for start, end, repl in sorted(to_strip, key=lambda x: -x[0]):
        text = text[:start] + repl + text[end:]

    if to_strip:
        path.write_text(text, encoding="utf-8")
    return len(to_strip)


def get_changed_wiki_files(root: Path) -> list[Path]:
    """Get changed .md files under root/ from git diff (staged + unstaged)."""
    changed: set[Path] = set()
    for args in (["git", "diff", "--cached", "--name-only"],
                 ["git", "diff", "--name-only"]):
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=root.parent)
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    p = root.parent / line
                    if p.exists() and p.suffix == ".md" and root in p.resolve().parents:
                        changed.add(p.resolve())
        except Exception:
            pass
    return sorted(changed)


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint/fix same-target wikilinks linked >N times per page.")
    ap.add_argument("--all", action="store_true", help="scan the entire wiki/")
    ap.add_argument("--fix", action="store_true", help="deduplicate (keep first N per target)")
    ap.add_argument("--threshold", type=int, default=2, help="max links per target per page (default 2)")
    ap.add_argument("--root", type=Path, default=WIKI_DIR, help="wiki root")
    args = ap.parse_args()

    root: Path = args.root
    files = sorted(root.rglob("*.md")) if args.all else get_changed_wiki_files(root)
    if not files:
        print("No wiki files to check.")
        return 0

    base = root.parent
    if args.fix:
        total = 0
        for f in files:
            n = fix_page(f, args.threshold)
            if n:
                print(f"  fixed {n} overlink(s) in {f.relative_to(base)}")
            total += n
        print(f"[overlinks] fixed {total} link(s) across {len(files)} file(s) (threshold={args.threshold})")
        return 0

    total_viol = 0
    for f in files:
        for target, count, line in find_violations(f, args.threshold):
            print(f"  {f.relative_to(base)}:{line}  «{target}» x{count}")
            total_viol += 1
    if total_viol:
        print(f"[overlinks] {total_viol} violation(s) across {len(files)} file(s) (threshold={args.threshold})")
        return 1
    print(f"[overlinks] OK ({len(files)} file(s) checked, threshold={args.threshold})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
