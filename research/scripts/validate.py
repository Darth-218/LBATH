#!/usr/bin/env python3
"""Validate the research corpus under research/.

Checks, in order:
  1. Every file parses as YAML and is a mapping.
  2. Every entry conforms to schema.json.
  3. The filename stem matches the entry's `id` (DOI `/` escaped as `_`;
     see expected_stem).
  4. No duplicate ids across papers/.
  5. Every notes/<id>.yaml has a matching papers/<id>.yaml.
  6. Every `related[].id` resolves to a known paper.
  7. Relations are authored in the forward direction only, with no
     self-references, duplicate edges, or contradictory back-edges.

Exit status is 0 when the corpus is clean, 1 otherwise.

    python research/scripts/validate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry
    from referencing.jsonschema import DRAFT202012
except ImportError as exc:  # pragma: no cover
    sys.exit(
        f"missing dependency: {exc.name}\n"
        "install with: pip install -r research/requirements.txt"
    )

RESEARCH = Path(__file__).resolve().parent.parent
PAPERS_DIR = RESEARCH / "papers"
NOTES_DIR = RESEARCH / "notes"
SCHEMA_PATH = RESEARCH / "schema.json"

# Base URI under which schema.json is mounted for reference resolution.
# Entries are validated against `schema.json` as a whole via a `$ref`
# wrapper: a `$defs` sub-document passed on its own cannot resolve its own
# `#/$defs/…` references.
ROOT_URI = "urn:lbath:schema"

# Relations an author may declare. The inverse of each is derived by
# render.py and must never be written by hand: declaring one direction is
# the convention, not a preference.
FORWARD_RELATIONS = {"supersedes", "extends", "contradicts", "same-authors"}

# Relations where a back-edge is a genuine contradiction rather than
# redundant symmetry.
ASYMMETRIC_RELATIONS = {"supersedes", "extends"}


def expected_stem(entry_id: str) -> str:
    """Filesystem-safe stem for an id.

    Only DOI ids contain `/`, which cannot appear in a filename; it is
    escaped as `_`. arXiv ids pass through unchanged. The `id` field always
    keeps the true identifier.
    """
    return entry_id.replace("/", "_")


class Report:
    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, where, message: str) -> None:
        self.errors.append((_display(where), message))

    def warn(self, where, message: str) -> None:
        self.warnings.append((_display(where), message))


def _display(path) -> str:
    path = Path(path)
    try:
        return str(path.relative_to(RESEARCH.parent))
    except ValueError:
        return str(path)


def load(path: Path, report: Report):
    """Parse one YAML file, reporting rather than raising on failure."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(path, f"cannot read: {exc}")
        return None

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        report.error(path, f"invalid YAML: {exc}")
        return None

    if data is None:
        report.error(path, "file is empty")
        return None
    if not isinstance(data, dict):
        report.error(path, f"expected a mapping at the top level, got {type(data).__name__}")
        return None
    return data


def explain(error) -> str:
    """Collapse jsonschema's nested anyOf/oneOf errors into one sentence."""
    err = error
    while err.validator in ("anyOf", "oneOf") and err.context:
        # Prefer the sub-error that got furthest into the document; that is
        # almost always the one describing what the author actually got wrong.
        err = max(err.context, key=lambda e: (len(e.absolute_path), -len(e.message)))
    return err.message


def make_validator(definition_id: str, schema: dict):
    """Validate an entry against one `$defs` section of the root schema.

    A bare `$defs` sub-schema is not a self-contained document: its
    `$ref: "#/$defs/…"` pointers resolve against the root. We therefore
    register the root under ROOT_URI and validate through a wrapper that
    points into it.
    """
    registry = Registry().with_resource(ROOT_URI, DRAFT202012.create_resource(schema))
    return Draft202012Validator(
        {"$ref": f"{ROOT_URI}#/$defs/{definition_id}"},
        registry=registry,
        format_checker=FormatChecker(),
    )


def check_schema(data, validator, path: Path, report: Report) -> bool:
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    for err in errors:
        loc = "$" + "".join(
            f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.absolute_path
        )
        report.error(path, f"{loc}: {explain(err)}")
    return not errors


def load_entries(directory: Path, definition_id: str, schema, report: Report) -> tuple[dict, dict]:
    """Return ({id: data}, {id: path}) for every valid entry in `directory`."""
    entries: dict = {}
    paths: dict = {}
    validator = make_validator(definition_id, schema)

    for path in sorted(directory.glob("*.yaml")):
        data = load(path, report)
        if data is None:
            continue
        if not check_schema(data, validator, path, report):
            continue

        entry_id = data["id"]
        if expected_stem(entry_id) != path.stem:
            report.error(
                path, f"id {entry_id!r} does not match filename stem {path.stem!r}"
            )
        if entry_id in entries:
            report.error(
                path,
                f"duplicate id {entry_id!r}, already defined in {_display(paths[entry_id])}",
            )
            continue

        entries[entry_id] = data
        paths[entry_id] = path

    return entries, paths


def check_relations(papers: dict, paper_paths: dict, report: Report) -> None:
    for paper_id, entry in papers.items():
        path = paper_paths[paper_id]
        seen: set[tuple[str, str]] = set()

        for rel in entry.get("related") or []:
            target = rel["id"]
            relation = rel["relation"]

            if (target, relation) in seen:
                report.error(path, f"duplicate relation {relation} -> {target}")
                continue
            seen.add((target, relation))

            if target == paper_id:
                report.error(path, f"relation points at itself ({paper_id})")
                continue

            if target not in papers:
                report.error(
                    path, f"related id {target!r} does not match any file in papers/"
                )
                continue

            back = [
                r["relation"]
                for r in (papers[target].get("related") or [])
                if r.get("id") == paper_id
            ]
            if not back:
                continue

            if relation in ASYMMETRIC_RELATIONS and back[0] in ASYMMETRIC_RELATIONS:
                report.error(
                    path,
                    f"{relation} -> {target} conflicts with {back[0]} declared "
                    f"from {target}; one of these is wrong",
                )
            else:
                report.warn(
                    path,
                    f"{relation} -> {target} is already declared from the other "
                    f"side ({back[0]}); drop one direction",
                )


def check_notes(notes: dict, note_paths: dict, papers: dict, report: Report) -> None:
    for note_id, _ in notes.items():
        if note_id not in papers:
            report.error(
                note_paths[note_id],
                f"no matching file in papers/ for id {note_id!r}",
            )


def emit(report: Report) -> None:
    for label, items in (("error", report.errors), ("warning", report.warnings)):
        grouped: dict[str, list[str]] = {}
        for path, message in items:
            grouped.setdefault(path, []).append(message)
        for path in sorted(grouped):
            print(f"{path}:", file=sys.stderr)
            for message in grouped[path]:
                print(f"  {label}: {message}", file=sys.stderr)


def main() -> int:
    report = Report()

    if not SCHEMA_PATH.exists():
        print(f"missing schema: {_display(SCHEMA_PATH)}", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    for directory in (PAPERS_DIR, NOTES_DIR):
        if not directory.exists():
            print(f"missing directory: {_display(directory)}", file=sys.stderr)
            return 1

    papers, paper_paths = load_entries(PAPERS_DIR, "paper", schema, report)
    notes, note_paths = load_entries(NOTES_DIR, "note", schema, report)

    check_relations(papers, paper_paths, report)
    check_notes(notes, note_paths, papers, report)

    emit(report)

    n_err, n_warn = len(report.errors), len(report.warnings)
    if n_err:
        print(
            f"\n{n_err} error{'s' if n_err != 1 else ''}, "
            f"{n_warn} warning{'s' if n_warn != 1 else ''}",
            file=sys.stderr,
        )
        return 1

    suffix = f" ({n_warn} warning{'s' if n_warn != 1 else ''})" if n_warn else ""
    print(f"ok: {len(papers)} papers, {len(notes)} notes{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
