#!/usr/bin/env python3
"""Detect concept-page drift — deletions & additions under wiki/concepts/.

[[Agent-Harness-治理协议]] warns that concepts can OSCILLATE (renamed back
and forth, each renamer unaware of prior decisions) or accumulate dead nodes.

This is a deliberately WEAK Computational check: it detects that a
deletion/addition (≈ rename) HAPPENED in recent history and surfaces it for
human novelty review. It does NOT judge whether the change brought new info —
that is a semantic call left to a human (human-on-the-loop, per
[[Agentic-Code-Review]]). Auto-judging novelty would require an LLM, violating
the deterministic-first principle ([[Harness Cybernetics]]).

Lists recent wiki/concepts/ deletions & additions. Exits 1 if drift found
(review needed), 0 if stable.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_COUNT = 50  # recent commits to scan


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def changed_files(filter_letter: str) -> list[str]:
    """wiki/concepts/ files with the given change type (D=deleted, A=added)."""
    r = git("log", "--max-count", str(MAX_COUNT), f"--diff-filter={filter_letter}",
            "--name-only", "--pretty=format:", "--", "wiki/concepts/")
    return sorted({line.strip() for line in r.stdout.splitlines() if line.strip()})


def main() -> int:
    deletions = changed_files("D")
    if not deletions:
        print(f"[concept-drift] OK — no concept-page deletions in last {MAX_COUNT} commits")
        return 0
    print(f"[concept-drift] {len(deletions)} concept-page deletion(s) in last {MAX_COUNT} commits — confirm each is legit evolution (rename/folder-split/merge), NOT oscillation:")
    for f in deletions:
        print(f"  - {f}")
    print("  → 振荡 = 同一概念反复删/加。确认每次删除带了「为何删 / 合并去向」说明（[[Agent-Harness-治理协议]] 新颖性检查）")
    return 1


if __name__ == "__main__":
    sys.exit(main())
