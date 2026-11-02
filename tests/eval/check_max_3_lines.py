"""Deterministic: the summary must be 1 to 3 non-empty lines."""


def evaluate(instance):
    r = instance.get("response", "")
    text = r if isinstance(r, str) else str(r)
    lines = [l for l in text.splitlines() if l.strip()]
    return {"score": 1 if 0 < len(lines) <= 3 else 0, "explanation": f"{len(lines)} non-empty lines"}
