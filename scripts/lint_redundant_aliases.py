#!/usr/bin/env python3
"""Detect redundant wikilink pipe aliases: [[X|X]] where display text equals target.

Also detects path-based wikilinks: [[concepts/.../file|Display]] which should
use [[Page Title]] format per CLAUDE.md convention.
"""

import re
import sys
import subprocess
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

# Match [[target|display]] wikilinks
PIPE_LINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")
# Match path-based links: [[concepts/... or [[entities/... or [[summaries/...
PATH_LINK_RE = re.compile(r"\[\[(concepts|entities|summaries)/[^\]]+\]\]")


def get_changed_wiki_files() -> list[Path]:
    changed = set()
    for args in (["git", "diff", "--cached", "--name-only"],
                 ["git", "diff", "--name-only"]):
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=WIKI_DIR.parent)
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    line = line.strip()
                    if line.startswith("wiki/") and line.endswith(".md"):
                        changed.add(Path(line))
        except Exception:
            pass
    return sorted(changed)


def check_file(path: Path) -> list[str]:
    errors = []
    with open(path) as f:
        content = f.read()

    for lineno, line in enumerate(content.split("\n"), 1):
        # Check redundant pipe aliases
        for m in PIPE_LINK_RE.finditer(line):
            target = m.group(1)
            display = m.group(2)
            if target == display:
                errors.append(f"{path.name}:{lineno}: redundant alias [[{target}|{target}]] → use [[{target}]]")

        # Check path-based wikilinks
        for m in PATH_LINK_RE.finditer(line):
            full_match = m.group(0)
            errors.append(f"{path.name}:{lineno}: path-based wikilink {full_match} → use [[Page Title]] format instead")

    return errors


def main():
    files = get_changed_wiki_files()
    if not files:
        print("No changed wiki files to check.")
        return 0

    all_errors = []
    for f in files:
        if not f.exists():
            continue
        errors = check_file(f)
        all_errors.extend(errors)

    if all_errors:
        print(f"[redundant-aliases] {len(all_errors)} issue(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    else:
        print(f"[redundant-aliases] OK ({len(files)} file(s) checked)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
