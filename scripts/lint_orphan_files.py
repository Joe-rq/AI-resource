#!/usr/bin/env python3
"""Detect orphan .md files dropped at the project root.

Catches the 'phantom file' failure mode: stray empty/duplicate files left at
the project root (e.g. the 2026-06-24 `Stateless Reducer.md` and
`AI Resource 项目介绍.md` — both 0-byte duplicates of real wiki pages).
Conceptual basis: [[Heartbeat Watchdog]] — an independent guard surfacing
silent environmental drift.

Scope is deliberately narrow: only top-level *.md (not recursive). The real
threat is clutter at the root; .md files inside subdirectories are assumed
organized. This avoids an ever-growing allowlist of legitimate subdirs
(references/, outputs/, etc.) — zero maintenance, high precision on the
actual failure mode.

Exits 1 if orphan root-level .md found (beyond CLAUDE.md / README.md), else 0.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_ROOT_FILES = {"CLAUDE.md", "README.md", "purpose.md"}


def find_orphans(root: Path = ROOT) -> list[str]:
    """Root-level .md files that aren't in the allowed set."""
    return sorted(p.name for p in root.glob("*.md") if p.name not in ALLOWED_ROOT_FILES)


def main() -> int:
    orphans = find_orphans()
    if orphans:
        print(f"[orphan-files] {len(orphans)} stray .md at project root:")
        for name in orphans:
            print(f"  - {name}")
        print(f"  (only {sorted(ALLOWED_ROOT_FILES)} are expected at root)")
        return 1
    print("[orphan-files] OK — no stray .md at project root")
    return 0


if __name__ == "__main__":
    sys.exit(main())
