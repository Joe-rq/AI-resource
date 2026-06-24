#!/usr/bin/env python3
"""Ashby coverage check — every failure mode needs >=1 implemented control.

Reads docs/governance-matrix.json and reports failure modes with no
'implemented' control. Conceptual basis: [[Harness Cybernetics]] Ashby's Law —
a failure mode with no control will escape. This script is the meta-layer that
keeps the coverage matrix itself from rotting (the same way lint_consistency
keeps CLAUDE.md from rotting, and the matrix's own 'coverage-meta' row covers
*this* tool — self-referential by design).

Inspection tool, NOT a commit gate: uncovered items are TODOs, not breakage.
Exits 1 when uncovered modes exist (for visibility), 0 when fully covered.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "docs" / "governance-matrix.json"


def main() -> int:
    if not MATRIX.exists():
        print(f"[coverage] matrix not found: {MATRIX}")
        return 1
    data = json.loads(MATRIX.read_text(encoding="utf-8"))

    uncovered = []
    total = 0
    for fm in data.get("failure_modes", []):
        total += 1
        controls = fm.get("controls", [])
        if not any(c.get("status") == "implemented" for c in controls):
            described = [f"{c.get('name','?')}({c.get('status','?')})" for c in controls]
            uncovered.append((fm.get("id", "?"), fm.get("desc", ""), described))

    if uncovered:
        print(f"[coverage] {len(uncovered)}/{total} failure mode(s) have NO implemented control (Ashby gap):")
        for fid, desc, controls in uncovered:
            print(f"  - {fid}: {desc}")
            print(f"      controls: {controls or '(none)'}")
        return 1
    print(f"[coverage] OK — all {total} failure mode(s) have >=1 implemented control")
    return 0


if __name__ == "__main__":
    sys.exit(main())
