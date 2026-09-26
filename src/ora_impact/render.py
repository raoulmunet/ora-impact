from __future__ import annotations

import json
import re
from .report import ImpactReport


def render_text(report: ImpactReport) -> str:
    ops = ", ".join(report.operations) if report.operations else "-"
    reads = ", ".join(report.read_objects) if report.read_objects else "-"
    writes = ", ".join(report.write_objects) if report.write_objects else "-"
    return "\n".join([
        f"Statements : {report.statement_count}",
        f"Operations : {ops}",
        f"Reads      : {reads}",
        f"Writes     : {writes}",
    ])


def render_json(report: ImpactReport) -> str:
    return json.dumps(report.to_dict(), indent=2)


def _safe_id(prefix: str, value: str, index: int) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]", "_", value)
    return f"{prefix}{index}_{slug}"


def render_mermaid(report: ImpactReport) -> str:
    lines = ["flowchart LR"]
    if not report.read_objects and not report.write_objects:
        lines.append('    N0["No object dependencies detected"]')
        return "\n".join(lines)

    read_ids: list[str] = []
    write_ids: list[str] = []

    for i, obj in enumerate(report.read_objects):
        node_id = _safe_id("R", obj, i)
        read_ids.append(node_id)
        lines.append(f'    {node_id}["{obj}"]')

    for i, obj in enumerate(report.write_objects):
        node_id = _safe_id("W", obj, i)
        write_ids.append(node_id)
        lines.append(f'    {node_id}["{obj}"]')

    if read_ids and write_ids:
        for r in read_ids:
            for w in write_ids:
                lines.append(f"    {r} --> {w}")

    return "\n".join(lines)
