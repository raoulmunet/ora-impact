from __future__ import annotations

from dataclasses import dataclass, asdict
from ora_core import analyze_sql


@dataclass(frozen=True)
class ImpactReport:
    statement_count: int
    operations: list[str]
    read_objects: list[str]
    write_objects: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def build_report(sql: str) -> ImpactReport:
    analysis = analyze_sql(sql)
    return ImpactReport(
        statement_count=analysis.statement_count,
        operations=analysis.operations,
        read_objects=analysis.read_objects,
        write_objects=analysis.write_objects,
    )
