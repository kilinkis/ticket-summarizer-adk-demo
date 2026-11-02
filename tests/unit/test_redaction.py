import json
from pathlib import Path

from app.redaction import redact

DATASET = Path(__file__).parents[1] / "eval" / "datasets" / "tickets-dataset.json"


def test_placeholders():
    out = redact(
        "My name is Anna Fakeson. Card 4111 1111 1111 1111, IBAN DE89 3704 0044 0532 0130 00, "
        "mail a.b@example.test, phone +44 20 7946 0958."
    )
    for tag in ("[NAME]", "[CARD]", "[IBAN]", "[EMAIL]", "[PHONE]"):
        assert tag in out
    assert "Fakeson" not in out


def test_amounts_and_dates_survive():
    out = redact("Charged EUR 1,250.00 on 2026-10-30 and 3.5% fee")
    assert "1,250.00" in out and "2026-10-30" in out and "3.5%" in out


def test_no_pii_left_in_any_eval_ticket():
    from re import search

    for case in json.loads(DATASET.read_text())["eval_cases"]:
        out = redact(case["prompt"]["parts"][0]["text"])
        assert not search(r"\d{4} ?\d{4} ?\d{4}", out), case["eval_case_id"]
        assert "@" not in out, case["eval_case_id"]
        assert "DE89" not in out and "GB29" not in out, case["eval_case_id"]
