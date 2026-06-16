#!/usr/bin/env python3
"""Validate YAML frontmatter of changed wiki pages.

Checks:
- Frontmatter exists and is valid YAML
- Required fields: title, type, created, updated, sources, tags
- type is one of: concept, entity, summary, index
- created/updated are valid YYYY-MM-DD dates
- sources is a non-empty list (except type=index which may have empty sources)
- tags is a non-empty list
"""

import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
REQUIRED_FIELDS = {"title", "type", "created", "updated", "sources", "tags"}
VALID_TYPES = {"concept", "entity", "summary", "index"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_simple_yaml(text: str) -> dict | None:
    """Parse a minimal subset of YAML used in wiki frontmatter (no external deps).

    Handles: string values (bare/quoted), list values [a, b, c], inline lists [a,b,c],
    and multi-level key: value lines (e.g., sources:, tags:, parent:).
    """
    data = {}
    current_key = None
    current_list = None
    list_indent = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check if we're inside a list continuation
        if current_key is not None and current_list is not None:
            # Detect indentation level of first list item
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                item = item.strip("\"'")
                current_list.append(item)
                continue
            elif stripped.startswith("-"):
                # Compact form: -item
                item = stripped[1:].strip()
                item = item.strip("\"'")
                current_list.append(item)
                continue
            else:
                # End of list, commit it
                data[current_key] = current_list
                current_key = None
                current_list = None
                list_indent = None
                # Fall through to parse as new key: value

        # Try inline list: key: [val1, val2, val3]
        inline_list_match = re.match(r'^(\w[\w_-]*)\s*:\s*\[(.*)\]$', stripped)
        if inline_list_match:
            key = inline_list_match.group(1)
            items_str = inline_list_match.group(2)
            items = []
            for item in items_str.split(","):
                item = item.strip().strip("\"'")
                if item:
                    items.append(item)
            data[key] = items
            continue

        # Try key: value
        kv_match = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)$', stripped)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip()

            # Check if value starts a list
            if value == "" or value == "[]":
                # Multi-line list or empty list
                current_key = key
                current_list = []
                list_indent = None
                continue

            # String value - strip quotes
            value = value.strip("\"'")
            data[key] = value
            continue

    # Commit any pending list
    if current_key is not None and current_list is not None:
        data[current_key] = current_list

    return data if data else None


def extract_frontmatter(path: Path) -> tuple[dict | None, int]:
    """Extract YAML frontmatter between --- markers. Returns (data, end_line)."""
    with open(path) as f:
        content = f.read()

    if not content.startswith("---"):
        return None, 0

    # Find closing ---
    end = content.find("---", 3)
    if end == -1:
        return None, 0

    fm_text = content[3:end].strip()
    if not fm_text:
        return None, 0

    data = parse_simple_yaml(fm_text)
    if data is None:
        return None, 0

    return data, content[:end].count("\n") + 1


def validate_date(value: str, field: str, path: Path) -> list[str]:
    errors = []
    if not isinstance(value, str) or not DATE_RE.match(value):
        errors.append(f"{path.name}: '{field}' must be YYYY-MM-DD, got: {value}")
        return errors
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        errors.append(f"{path.name}: '{field}' is not a valid date: {value}")
    return errors


def validate_frontmatter(path: Path) -> list[str]:
    errors = []
    data, _ = extract_frontmatter(path)

    if data is None:
        errors.append(f"{path.name}: missing or invalid YAML frontmatter")
        return errors

    if not isinstance(data, dict):
        errors.append(f"{path.name}: frontmatter must be a YAML mapping, got {type(data).__name__}")
        return errors

    page_type = data.get("type", "")

    # Check required fields
    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        errors.append(f"{path.name}: missing required field(s): {', '.join(sorted(missing))}")

    # Validate type
    if "type" in data and data["type"] not in VALID_TYPES:
        errors.append(f"{path.name}: invalid type '{data['type']}', must be one of: {', '.join(sorted(VALID_TYPES))}")

    # Validate dates
    for field in ("created", "updated"):
        if field in data:
            errors.extend(validate_date(data[field], field, path))

    # Validate sources (allow empty only for index type)
    if "sources" in data:
        if not isinstance(data["sources"], list):
            errors.append(f"{path.name}: 'sources' must be a list, got {type(data['sources']).__name__}")
        elif page_type != "index" and len(data["sources"]) == 0:
            errors.append(f"{path.name}: 'sources' is empty (only index pages may have empty sources)")

    # Validate tags
    if "tags" in data:
        if not isinstance(data["tags"], list):
            errors.append(f"{path.name}: 'tags' must be a list, got {type(data['tags']).__name__}")
        elif len(data["tags"]) == 0:
            errors.append(f"{path.name}: 'tags' is empty")

    # Check for legacy fields that should have been removed
    legacy_fields = {"source_url", "source_type", "date", "ingested", "entity_type"}
    found_legacy = legacy_fields & set(data.keys())
    if found_legacy:
        errors.append(f"{path.name}: legacy field(s) should be removed: {', '.join(sorted(found_legacy))}")

    return errors


def get_changed_wiki_files() -> list[Path]:
    """Get list of changed .md files in wiki/ from git diff --cached and unstaged."""
    import subprocess
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


def main():
    files = get_changed_wiki_files()
    if not files:
        print("No changed wiki files to check.")
        return 0

    all_errors = []
    for f in files:
        if not f.exists():
            continue  # deleted file
        errors = validate_frontmatter(f)
        all_errors.extend(errors)

    if all_errors:
        print(f"[frontmatter] {len(all_errors)} error(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    else:
        print(f"[frontmatter] OK ({len(files)} file(s) checked)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
