"""Deterministic: each expected key fact (from the case's reference) appears in the summary.

Reference format: ';' separates required facts, '|' separates synonyms for one fact.
"""


def evaluate(instance):
    r = instance.get("response", "")
    text = (r if isinstance(r, str) else str(r)).lower()
    ref = instance.get("reference", "")
    keys = (ref if isinstance(ref, str) else str(ref)).lower()
    groups = [g for g in keys.split(";") if g.strip()]
    missing = [g for g in groups if not any(a.strip() in text for a in g.split("|"))]
    return {"score": 1 if not missing else 0, "explanation": f"missing facts: {missing}" if missing else "all present"}
