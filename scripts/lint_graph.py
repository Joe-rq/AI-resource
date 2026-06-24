#!/usr/bin/env python3
"""Graph-level wiki health — connected components, orphans, bridge nodes, hubs.

Complements lint_orphan_files.py (file-level strays at project root) with
graph-level analysis over the wikilink graph. Conceptual basis: nashsu/llm_wiki's
knowledge-graph insights (isolated pages, bridge nodes, sparse communities),
applied to our own wikilinks — pure stdlib.

Scope note (honest): this does connected-components analysis, NOT Louvain
community detection. Connected components find DISCONNECTED knowledge islands
(concepts cut off from the main graph); Louvain finds DENSE sub-clusters. The
former is stdlib-trivial and catches the "stranded concept" failure mode; the
latter needs networkx. If dense-cluster discovery is ever wanted, add networkx.

Metrics:
  - connected components (BFS) — islands disconnected from the main graph
  - orphan nodes (degree <= 1) — graph-level strays (vs lint_orphan's file-level)
  - articulation points (Tarjan) — bridge nodes whose removal splits the graph
  - hubs (top degree) — most-connected concepts

Inspection tool, NOT a commit gate. Exits 1 if orphans or small components
found (for review), 0 if the graph is one healthy component with no strays.
"""

import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
import lint_wiki  # noqa: E402

WIKI_DIR = SCRIPTS_DIR.parent / "wiki"
ROOT_INDEX = WIKI_DIR / "index.md"


def build_graph() -> tuple[dict[str, set[str]], set[str], set[str]]:
    """Undirected graph: node = page title, edge = wikilink (either direction).
    Returns (adjacency, titles, has_parent) — has_parent marks folder-split
    sub-pages (legal degree-1 leaves reached via their index, not real orphans)."""
    pages = lint_wiki.load_pages(WIKI_DIR)  # title/stem/rel/normalized -> Path
    adj: dict[str, set[str]] = defaultdict(set)
    titles: set[str] = set()
    has_parent: set[str] = set()
    for p in WIKI_DIR.rglob("*.md"):
        if p == ROOT_INDEX:
            continue  # root index is navigation, not a knowledge node
        fm = lint_wiki.parse_frontmatter(p.read_text(encoding="utf-8"))
        if not fm or "title" not in fm:
            continue
        src = fm["title"]
        titles.add(src)
        if "parent" in fm:
            has_parent.add(src)
        for target in lint_wiki.extract_wikilinks(p.read_text(encoding="utf-8")):
            tgt_path = pages.get(target.strip()) or pages.get(Path(target.strip()).stem)
            if not tgt_path:
                continue
            dst_fm = lint_wiki.parse_frontmatter(tgt_path.read_text(encoding="utf-8"))
            dst = dst_fm.get("title") if dst_fm else None
            if dst and dst != src:
                adj[src].add(dst)
                adj[dst].add(src)
    for t in titles:
        adj.setdefault(t, set())
    return adj, titles, has_parent


def connected_components(adj: dict[str, set[str]]) -> list[list[str]]:
    seen: set[str] = set()
    comps: list[list[str]] = []
    for start in adj:
        if start in seen:
            continue
        stack, comp = [start], []
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            stack.extend(adj[u] - seen)
        comps.append(sorted(comp))
    return sorted(comps, key=len, reverse=True)


def articulation_points(adj: dict[str, set[str]]) -> set[str]:
    """Tarjan's algorithm — nodes whose removal increases component count."""
    sys.setrecursionlimit(10000)
    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    visited: set[str] = set()
    parent: dict[str, str | None] = {}
    ap: set[str] = set()
    timer = [0]

    def dfs(u: str) -> None:
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in adj[u]:
            if v not in visited:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent.get(u) is None and children > 1:
                    ap.add(u)
                if parent.get(u) is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])

    for n in adj:
        if n not in visited:
            parent[n] = None
            dfs(n)
    return ap


def main() -> int:
    adj, titles, has_parent = build_graph()
    if not titles:
        print("[graph] no pages found")
        return 1

    comps = connected_components(adj)
    deg = {n: len(adj[n]) for n in adj}
    # folder-split sub-pages (has_parent) are legal degree-1 leaves — not orphans
    orphans = sorted(n for n in adj if deg[n] <= 1 and n not in has_parent)
    aps = articulation_points(adj)
    hubs = sorted(adj, key=lambda n: -deg[n])[:8]

    edge_count = sum(len(s) for s in adj.values()) // 2
    print(f"[graph] {len(titles)} nodes, {edge_count} edges, {len(comps)} connected component(s)")

    small = [c for c in comps if len(c) <= 2]
    if len(comps) > 1:
        print(f"  ⚠️ graph is FRAGMENTED — {len(comps)} components (knowledge islands):")
        for c in comps:
            tag = "ISLAND" if len(c) <= 2 else "main"
            print(f"     [{tag}] {len(c)} node(s): {c[:8]}{'...' if len(c)>8 else ''}")
    else:
        print("  ✅ single connected component — no disconnected islands")

    if orphans:
        print(f"  🟡 {len(orphans)} orphan node(s) (degree≤1) — graph-level strays:")
        for n in orphans:
            print(f"     {n} (deg {deg[n]})")
    else:
        print("  ✅ no orphan nodes (all degree≥2)")

    if aps:
        print(f"  bridge nodes (articulation points, {len(aps)}) — removal would fragment:")
        for n in sorted(aps, key=lambda x: -deg[x]):
            print(f"     {n} (deg {deg[n]})")

    print(f"  top hubs: {', '.join(f'{n}({deg[n]})' for n in hubs[:5])}")

    return 1 if (orphans or len(comps) > 1) else 0


if __name__ == "__main__":
    sys.exit(main())
