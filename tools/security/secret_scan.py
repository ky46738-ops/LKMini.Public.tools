#!/usr/bin/env python3
"""Scan current source files for credentials that must never be committed."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "Telegram Bot token",
        re.compile(r"(?<![A-Za-z0-9_])\d{8,12}:[A-Za-z0-9_-]{30,}(?![A-Za-z0-9_])"),
    ),
    ("Telegram Bot API URL", re.compile(r"https://api[.]telegram[.]org/bot", re.I)),
    ("OpenAI API key", re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}")),
    ("GitHub token", re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{20,}")),
    (
        "Private key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
)

TEXT_SUFFIXES = {
    ".css",
    ".env",
    ".html",
    ".htm",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        root / Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    ]


def candidate_files(root: Path, explicit_paths: list[str]) -> list[Path]:
    if explicit_paths:
        return [(root / path).resolve() for path in explicit_paths]
    return tracked_files(root)


def scan_file(path: Path) -> list[tuple[int, str]]:
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((line_number, label))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Scan one path relative to --root; repeat for more paths.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures: list[tuple[Path, int, str]] = []
    for path in candidate_files(root, args.path):
        for line_number, label in scan_file(path):
            failures.append((path, line_number, label))

    if failures:
        for path, line_number, label in failures:
            try:
                display = path.relative_to(root)
            except ValueError:
                display = path
            print(f"ERROR {display}:{line_number}: {label}")
        print(f"Secret scan failed with {len(failures)} finding(s).")
        return 1

    print("Secret scan passed: no credential patterns found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
