from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .report import build_report
from .render import render_json, render_mermaid, render_text


def _read_sql(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ora-impact",
        description="Static Oracle SQL impact analysis.",
    )
    parser.add_argument("source", help="SQL file path, or '-' to read from stdin")
    parser.add_argument(
        "--format",
        choices=("text", "json", "mermaid"),
        default="text",
        help="Output format (default: text)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        sql = _read_sql(args.source)
    except OSError as exc:
        print(f"ora-impact: {exc}", file=sys.stderr)
        return 2

    report = build_report(sql)
    renderer = {
        "text": render_text,
        "json": render_json,
        "mermaid": render_mermaid,
    }[args.format]
    print(renderer(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
