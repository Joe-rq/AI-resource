#!/usr/bin/env python3
"""ingest checkpoint — reducer-style snapshot/rollback for wiki ingest.

The ingest process lives in llm-wiki SKILL.md (an LLM-run flow, not a script),
so it is currently an irreversible side-effect: a bad ingest means hand-rolling
back many edits. This wraps it with a transaction layer backed by git tags +
an append-only event log. Conceptual basis: [[Stateless Reducer]] + [[ESAA]]
— ingest becomes a replayable/rollback-able event.

Usage (LLM calls these around the ingest):
  ingest_checkpoint.py begin <slug>        # tag pre-ingest/<slug> at HEAD + log
  ingest_checkpoint.py end <slug>          # log completion + show diff since tag
  ingest_checkpoint.py rollback <slug>     # DRY-RUN restore wiki/log/docs
  ingest_checkpoint.py rollback <slug> --force   # actually restore

Safety: rollback restores only wiki/ log/ docs/ via `git checkout` (NOT global
`git reset --hard`), so unrelated uncommitted changes survive. Untracked new
files are reported for manual deletion, never auto-deleted.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENT_LOG = ROOT / "log" / "ingest-events.jsonl"
# ingest only writes under these paths — rollback scope stays here
INGEST_PATHS = ["wiki/", "log/", "docs/"]


def git(*args, check=True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"git {' '.join(args)} failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return r


def tag_for(slug: str) -> str:
    return f"pre-ingest/{slug}"


def log_event(event: dict) -> None:
    EVENT_LOG.parent.mkdir(exist_ok=True)
    event["ts"] = datetime.now().isoformat(timespec="seconds")
    with open(EVENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def cmd_begin(slug: str) -> int:
    head = git("rev-parse", "HEAD").stdout.strip()
    git("tag", "-f", tag_for(slug))  # point tag at current HEAD (overwrite if same slug reused)
    log_event({"event": "begin", "slug": slug, "tag": tag_for(slug), "head": head})
    print(f"[checkpoint] began '{slug}' at {head[:8]} (tag {tag_for(slug)})")
    dirty = git("status", "--porcelain").stdout.strip()
    if dirty:
        print("[checkpoint] WARNING: working tree not clean. Uncommitted changes are NOT in the snapshot:")
        print(dirty)
    return 0


def cmd_end(slug: str) -> int:
    tag = tag_for(slug)
    diff = git("diff", "--stat", tag, "--", *INGEST_PATHS, check=False)
    log_event({"event": "end", "slug": slug})
    print(f"[checkpoint] ended '{slug}'. Changes under {INGEST_PATHS} since {tag}:")
    print(diff.stdout.strip() or "(none)")
    return 0


def cmd_rollback(slug: str, force: bool) -> int:
    tag = tag_for(slug)
    if git("rev-parse", "--verify", tag, check=False).returncode != 0:
        print(f"[checkpoint] no checkpoint tag '{tag}' for slug '{slug}'", file=sys.stderr)
        return 1

    changed = git("diff", "--name-only", tag, "--", *INGEST_PATHS, check=False).stdout.strip()
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *INGEST_PATHS).stdout.strip()

    if not force:
        print(f"[checkpoint] DRY RUN — rollback to {tag} would:")
        print("  restore tracked files under " + ",".join(INGEST_PATHS) + ":")
        print("    " + (changed.replace("\n", "\n    ") if changed else "(none)"))
        print("  these untracked files are present (rollback will NOT touch them — review manually):")
        print("    " + (untracked.replace("\n", "\n    ") if untracked else "(none)"))
        print("  re-run with --force to apply the restore.")
        return 0

    git("checkout", tag, "--", *INGEST_PATHS)
    log_event({"event": "rollback", "slug": slug, "tag": tag})
    print(f"[checkpoint] rolled back '{slug}' — restored tracked files under {INGEST_PATHS} to {tag}")
    if untracked:
        print("[checkpoint] untracked files present under these paths (NOT auto-deleted — review & rm manually):")
        print("    " + untracked.replace("\n", "\n    "))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("begin", "end"):
        s = sub.add_parser(c, help=f"{c} checkpoint")
        s.add_argument("slug", help="short id for this ingest (e.g. article slug)")
    rb = sub.add_parser("rollback", help="restore to checkpoint (dry-run by default)")
    rb.add_argument("slug")
    rb.add_argument("--force", action="store_true", help="actually restore (default is dry-run)")
    args = ap.parse_args()

    if args.cmd == "begin":
        return cmd_begin(args.slug)
    if args.cmd == "end":
        return cmd_end(args.slug)
    if args.cmd == "rollback":
        return cmd_rollback(args.slug, args.force)
    return 1


if __name__ == "__main__":
    sys.exit(main())
