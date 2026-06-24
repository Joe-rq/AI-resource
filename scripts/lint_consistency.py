#!/usr/bin/env python3
"""Consistency check: verify scripts/ paths referenced in docs/configs exist.

Catches the 'phantom script' failure mode — CLAUDE.md or .claude/settings.json
referencing a script that was never created or got renamed (e.g. the historical
`lint_wilinks.py` that didn't exist, or hook commands pointing nowhere).

Conceptual basis: [[Stateless Reducer]]'s checkable state (declared state must
match real state) + [[Agent-Harness-治理协议]] dual-layer verification.

Scans CLAUDE.md + .claude/settings.json by default; extra file paths can be
passed as args (useful for fixture-based testing). Exits 1 if any referenced
script is missing, 0 otherwise.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_REF_RE = re.compile(r"scripts/[A-Za-z0-9_-]+\.py")
DEFAULT_SCAN = ["CLAUDE.md", ".claude/settings.json"]


def referenced_scripts(files: list[str]) -> dict[str, set[str]]:
    """Return {script_path: {source files referencing it}}."""
    refs: dict[str, set[str]] = {}
    for rel in files:
        p = Path(rel) if Path(rel).is_absolute() else ROOT / rel
        if not p.exists():
            continue
        for m in SCRIPT_REF_RE.finditer(p.read_text(encoding="utf-8")):
            refs.setdefault(m.group(0), set()).add(rel)
    return refs


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify scripts/ references in docs/configs exist.")
    ap.add_argument("extra_files", nargs="*", help="additional files to scan (default: CLAUDE.md + settings.json)")
    args = ap.parse_args()

    files = DEFAULT_SCAN + list(args.extra_files)
    refs = referenced_scripts(files)

    missing = [(s, sorted(src)) for s, src in refs.items() if not (ROOT / s).exists()]
    if missing:
        print(f"[consistency] {len(missing)} referenced script(s) MISSING:")
        for script, sources in sorted(missing):
            print(f"  - {script}  (referenced in: {', '.join(sources)})")
        return 1
    print(f"[consistency] OK — {len(refs)} referenced script(s) all exist (scanned {len(files)} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
