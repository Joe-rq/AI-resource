#!/usr/bin/env python3
"""Aggregate post-edit wiki quality check for git-diff-changed files.

Runs four checks against changed wiki/*.md in a single process, keeping the
PostToolUse hook under the <500ms budget (one `uv run`, not four):

  1. frontmatter compliance          -> lint_frontmatter.validate_frontmatter
  2. redundant aliases / path links  -> lint_redundant_aliases.check_file
  3. dead wikilinks                  -> lint_wiki.load_pages + extract_wikilinks
  4. same-target wikilinks > N       -> lint_overlinks.find_violations (N=2)

Intended to be invoked from a PostToolUse hook on Edit|Write, behind a
`git diff --name-only | grep -q wiki/` guard. Exits 1 if any issue is found
(warn-only under PostToolUse — it cannot block), 0 otherwise. Silent when no
wiki files changed.
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))  # import sibling lint modules

import lint_frontmatter          # noqa: E402
import lint_overlinks            # noqa: E402
import lint_redundant_aliases    # noqa: E402
import lint_wiki                 # noqa: E402

WIKI_DIR = SCRIPTS_DIR.parent / "wiki"
OVERLINK_THRESHOLD = 2  # CLAUDE.md: "not more than twice per article"


def get_changed_wiki_files() -> list[Path]:
    """Changed wiki/*.md — tracked diffs (staged + unstaged) AND untracked new files.

    `git diff` omits untracked files, so newly created pages (the main ingest
    case) would slip past the hook. `git ls-files --others` closes that gap.
    """
    changed: set[Path] = set()
    for args in (["git", "diff", "--cached", "--name-only"],
                 ["git", "diff", "--name-only"]):
        try:
            r = subprocess.run(args, capture_output=True, text=True, cwd=SCRIPTS_DIR.parent)
            if r.returncode != 0:
                continue
            for line in r.stdout.strip().split("\n"):
                line = line.strip()
                if line.startswith("wiki/") and line.endswith(".md"):
                    p = (SCRIPTS_DIR.parent / line).resolve()
                    if p.exists():
                        changed.add(p)
        except Exception:
            pass
    try:
        r = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "--", "wiki/"],
            capture_output=True, text=True, cwd=SCRIPTS_DIR.parent)
        if r.returncode == 0:
            for line in r.stdout.strip().split("\n"):
                line = line.strip()
                if line.endswith(".md"):
                    p = (SCRIPTS_DIR.parent / line).resolve()
                    if p.exists():
                        changed.add(p)
    except Exception:
        pass
    return sorted(changed)


def check_dead_links(files: list[Path], pages: dict) -> list[str]:
    """Flag wikilink targets in changed files that resolve to no page.

    `pages` is lint_wiki.load_pages()'s title->path index. Mirrors lint_wiki.py
    Pass 1 but scoped to changed files only.
    """
    issues: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for target in lint_wiki.extract_wikilinks(text):
            t = target.strip()
            if t in pages or Path(t).stem in pages:
                continue
            issues.append(f"{f.name}: dead wikilink [[{t}]]")
    return issues


def main() -> int:
    files = get_changed_wiki_files()
    if not files:
        return 0  # silent — nothing wiki-related changed

    issues: list[str] = []

    for f in files:
        issues += lint_frontmatter.validate_frontmatter(f)
        issues += lint_redundant_aliases.check_file(f)

    issues += check_dead_links(files, lint_wiki.load_pages(WIKI_DIR))

    for f in files:
        for target, count, line in lint_overlinks.find_violations(f, OVERLINK_THRESHOLD):
            issues.append(f"{f.name}:{line} «{target}» linked x{count} (>2)")

    if issues:
        print(f"[wiki-lint] {len(issues)} issue(s) across {len(files)} changed file(s):")
        for i in issues:
            print(f"  - {i}")
        return 1
    print(f"[wiki-lint] OK — {len(files)} changed file(s), 4 checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
