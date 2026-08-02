#!/usr/bin/env python3
"""Render a public LKMINI breach event JSON file as Markdown."""

import json
import sys
from pathlib import Path

REQUIRED = [
    "event_id",
    "recorded_at",
    "root",
    "axiom",
    "status",
    "failure_type",
    "evidence",
    "reverse_chain",
]


def load_event(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(event: dict) -> list[str]:
    missing = [key for key in REQUIRED if key not in event or event[key] in (None, "", [])]
    if event.get("root") != "LKMINI":
        missing.append("root must be LKMINI")
    if event.get("axiom") != "A=A":
        missing.append("axiom must be A=A")
    if event.get("status") not in {"Completed", "Error"}:
        missing.append("status must be Completed or Error")
    return missing


def table(rows):
    out = ["| Check | Result |", "| --- | --- |"]
    for row in rows:
        out.append(f"| {row.get('check', '')} | {row.get('result', '')} |")
    return "\n".join(out)


def render(event: dict) -> str:
    missing = validate(event)
    if missing:
        raise SystemExit("Invalid breach event: " + "; ".join(missing))

    commits = event.get("commits", [])
    commit_lines = ["| Label | SHA |", "| --- | --- |"]
    for item in commits:
        commit_lines.append(f"| {item.get('label', '')} | `{item.get('sha', '')}` |")

    return f"""# LKMINI Breach Event

Event ID: `{event['event_id']}`

Recorded At: `{event['recorded_at']}`

Root: `{event['root']}`

Axiom: `{event['axiom']}`

Status: `{event['status']}`

Failure Type: `{event['failure_type']}`

## Summary

{event.get('summary', '')}

## Evidence

{table(event['evidence'])}

## Commits

{chr(10).join(commit_lines)}

## Public Boundary

{event.get('public_boundary', 'Public evidence only. No credentials or private system internals.')}

## ReverseChain

{event['reverse_chain']}
"""


def main(argv):
    if len(argv) != 2:
        print("usage: record_breach_event.py <event.json>", file=sys.stderr)
        return 2
    print(render(load_event(argv[1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
