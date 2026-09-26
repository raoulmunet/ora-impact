from ora_impact import build_report
from ora_impact.render import render_mermaid, render_text


SQL = """
INSERT INTO dwh.customer_dim (customer_id, customer_name)
SELECT c.customer_id, c.customer_name
FROM crm.customers c
JOIN crm.customer_status s
  ON s.customer_id = c.customer_id
WHERE s.active_flag = 'Y';
"""


def test_build_report():
    report = build_report(SQL)
    assert report.statement_count == 1
    assert report.operations == ["INSERT"]
    assert report.read_objects == ["CRM.CUSTOMERS", "CRM.CUSTOMER_STATUS"]
    assert report.write_objects == ["DWH.CUSTOMER_DIM"]


def test_text_output():
    text = render_text(build_report(SQL))
    assert "CRM.CUSTOMERS" in text
    assert "DWH.CUSTOMER_DIM" in text


def test_mermaid_output():
    graph = render_mermaid(build_report(SQL))
    assert graph.startswith("flowchart LR")
    assert "CRM.CUSTOMERS" in graph
    assert "DWH.CUSTOMER_DIM" in graph
    assert "-->" in graph
