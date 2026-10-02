#!/usr/bin/env python3
"""Render the research corpus into COMPARISON.md and comparison.json.

Output is deterministic: entries sort by descending year then id, JSON keys
are sorted, and nothing depends on filesystem ordering or wall-clock time.

    python research/scripts/render.py            # write both files
    python research/scripts/render.py --check    # exit 1 if either is stale
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    sys.exit(
        f"missing dependency: {exc.name}\n"
        "install with: pip install -r research/requirements.txt"
    )

RESEARCH = Path(__file__).resolve().parent.parent
PAPERS_DIR = RESEARCH / "papers"
MD_PATH = RESEARCH / "COMPARISON.md"
JSON_PATH = RESEARCH / "comparison.json"

SCHEMA_VERSION = 1

# Derived, never authored. See validate.py for the forward-only rule.
INVERSE = {
    "supersedes": "superseded-by",
    "extends": "extends-by",
    "contradicts": "contradicts",
    "same-authors": "same-authors",
}

CELL_WIDTH = 48


# --------------------------------------------------------------------------
# loading


def load_entries(directory: Path) -> list[dict]:
    entries = []
    for path in sorted(directory.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("id"):
            entries.append(data)
    return sorted(entries, key=sort_key)


def sort_key(entry: dict):
    return (-int(entry.get("year") or 0), entry["id"])


def display_name(entry: dict) -> str:
    return entry.get("short_name") or entry["title"]


# --------------------------------------------------------------------------
# markdown helpers


def _cell(value, max_len: int | None = None) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        if not value:
            return "—"
        value = ", ".join(str(v) for v in value)
    text = " ".join(str(value).split())
    if not text:
        return "—"
    if max_len and len(text) > max_len:
        text = text[: max_len - 1].rstrip() + "…"
    return text.replace("|", "\\|")


def _code(value) -> str:
    text = " ".join(str(value).split())
    return f"`{text}`" if "`" not in text else "`` " + text + " ``"


def _label(entry: dict) -> str:
    name = display_name(entry)
    url = (entry.get("links") or {}).get("paper")
    return f"[{name}]({url})" if url else name


def _table(rows: list[list[str]]) -> str:
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def _paper_table(entries: list[dict]) -> str:
    header = ["Paper", "Year", "Paradigm", "Memory", "Tools", "Eval datasets", "Repro"]
    rows = [header, ["---"] * len(header)]
    for entry in entries:
        arch = entry.get("architecture") or {}
        evaluation = entry.get("evaluation") or {}
        memory = arch.get("memory") or {}
        rows.append([
            _cell(_label(entry)),
            _cell(entry.get("year")),
            _cell(arch.get("paradigm")),
            _cell(memory.get("type")),
            _cell(arch.get("tools"), CELL_WIDTH),
            _cell(evaluation.get("datasets"), CELL_WIDTH),
            _cell(evaluation.get("reproducible")),
        ])
    return _table(rows)


def _partial_table(entries: list[dict]) -> str:
    header = ["Paper", "Year", "Basis", "Paradigm", "Problem"]
    rows = [header, ["---"] * len(header)]
    for entry in entries:
        arch = entry.get("architecture") or {}
        rows.append([
            _cell(_label(entry)),
            _cell(entry.get("year")),
            _cell(entry.get("extraction_basis")),
            _cell(arch.get("paradigm")),
            _cell(entry.get("problem")),
        ])
    return _table(rows)


# --------------------------------------------------------------------------
# derived data


def _collect(entries: list[dict], path: tuple[str, ...]) -> dict[str, list[str]]:
    """Map each value at `path` to the ids of entries that declare it."""
    out: dict[str, list[str]] = {}
    for entry in entries:
        node = entry
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if not isinstance(node, list):
            continue
        for value in node:
            out.setdefault(str(value), []).append(entry["id"])
    return out


def _collect_models(entries: list[dict]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for entry in entries:
        models = (entry.get("architecture") or {}).get("models") or []
        for model in models:
            if isinstance(model, dict) and model.get("name"):
                out.setdefault(str(model["name"]), []).append(entry["id"])
    return out


def _shared(mapping: dict[str, list[str]]) -> dict[str, list[str]]:
    """Keep only values referenced by more than one entry, sorted throughout."""
    return {
        value: sorted(set(ids))
        for value, ids in sorted(mapping.items())
        if len(set(ids)) > 1
    }


def overlap(entries: list[dict]) -> dict[str, dict[str, list[str]]]:
    return {
        "datasets": _shared(_collect(entries, ("evaluation", "datasets"))),
        "tools": _shared(_collect(entries, ("architecture", "tools"))),
        "models": _shared(_collect_models(entries)),
    }


def relations(entries: list[dict]) -> list[dict]:
    known = {entry["id"] for entry in entries}
    edges = []
    for entry in entries:
        for rel in entry.get("related") or []:
            target = rel.get("id")
            relation = rel.get("relation")
            if target not in known or relation not in INVERSE:
                continue
            edges.append({"from": entry["id"], "relation": relation, "to": target,
                          "derived": False})
            edges.append({"from": target, "relation": INVERSE[relation],
                          "to": entry["id"], "derived": True})
    return sorted(edges, key=lambda e: (e["from"], e["relation"], e["to"]))


# --------------------------------------------------------------------------
# builders


def _overlap_section(groups: dict[str, dict[str, list[str]]]) -> list[str]:
    lines = ["## Overlap", ""]
    if not any(groups.values()):
        lines += ["*No dataset, tool, or model is shared by more than one entry.*", ""]
        return lines

    lines += [
        "Values referenced by more than one paper. Identifiers match "
        "`papers/<id>.yaml`.",
        "",
    ]
    for label, mapping in groups.items():
        if not mapping:
            continue
        lines += [f"### {label.capitalize()}", ""]
        for value, ids in mapping.items():
            lines.append(f"- {_code(value)} — {', '.join(ids)}")
        lines.append("")
    return lines


def _relations_section(edges: list[dict]) -> list[str]:
    declared = [e for e in edges if not e["derived"]]
    lines = ["## Declared relations", ""]
    if not declared:
        lines += ["*No relations declared.*", ""]
        return lines

    header = ["From", "Relation", "To"]
    rows = [header, ["---"] * len(header)]
    for edge in declared:
        rows.append([
            _cell(edge["from"]),
            _cell(edge["relation"]),
            _cell(edge["to"]),
        ])
    lines += [
        _table(rows),
        "",
        "*Inverses (`superseded-by`, `extends-by`) are derived, not authored. "
        "The full edge set including inverses is in `comparison.json`.*",
        "",
    ]
    return lines


def build_markdown(entries: list[dict]) -> str:
    full = [e for e in entries if e.get("extraction_basis") == "full-text"]
    partial = [e for e in entries if e.get("extraction_basis") != "full-text"]

    lines = [
        "# Comparison of LLM threat-hunting papers",
        "",
        "<!-- GENERATED BY research/scripts/render.py — DO NOT EDIT BY HAND -->",
        "",
        f"*{len(entries)} entries in the corpus, {len(full)} with full-text extraction.*",
        "",
        "## Full-text extractions",
        "",
    ]
    lines += [_paper_table(full) if full else "*No full-text entries yet.*", ""]

    if partial:
        lines += [
            "## Abstract-only and secondhand entries",
            "",
            "*Not read in full. Treated as leads, not findings.*",
            "",
            _partial_table(partial),
            "",
        ]

    lines += _relations_section(relations(entries))
    lines += _overlap_section(overlap(entries))

    return "\n".join(lines).rstrip() + "\n"


def build_payload(entries: list[dict]) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "research/scripts/render.py",
        "papers": entries,
        "relations": relations(entries),
        "overlap": overlap(entries),
    }


def render() -> tuple[str, str]:
    entries = load_entries(PAPERS_DIR)
    markdown = build_markdown(entries)
    payload = json.dumps(
        build_payload(entries), indent=2, sort_keys=True, ensure_ascii=False
    )
    return markdown, payload + "\n"


# --------------------------------------------------------------------------
# entrypoint


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the generated files differ from what is on disk",
    )
    args = parser.parse_args(argv)

    if not PAPERS_DIR.exists():
        print(f"missing directory: {PAPERS_DIR}", file=sys.stderr)
        return 1

    markdown, payload = render()
    targets = [(MD_PATH, markdown), (JSON_PATH, payload)]

    if args.check:
        stale = []
        for path, content in targets:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path)
        if stale:
            for path in stale:
                print(f"stale: {path.name}", file=sys.stderr)
            print("run: python research/scripts/render.py", file=sys.stderr)
            return 1
        print("generated files are up to date")
        return 0

    for path, content in targets:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        print(f"wrote {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
