"""Deterministic PII redaction. Runs before any text reaches the model."""

import re

_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{1,4}){4,8}\b")
_CARD = re.compile(r"(?<![\w-])(?:\d[ -]?){12,18}\d(?![\w-])")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PHONE = re.compile(r"(?<![\w.])\+?\(?\d[\d\s().-]{6,}\d(?!\w)")
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

_NAME = r"[A-Z][a-z]+(?:[ ][A-Z][a-z]+){0,2}"
_NAME_PATTERNS = [
    re.compile(rf"\b(?:Mr|Mrs|Ms|Miss|Dr|Prof)\.?\s+({_NAME})"),
    re.compile(rf"(?i:\b(?:my name is|name:|this is|i am|i'm|customer:|contact:))[ ]+({_NAME})"),
    re.compile(rf"(?i:\b(?:regards|thanks|thank you|best|cheers|sincerely|kind regards)),?\s*\n\s*({_NAME})"),
    re.compile(rf"(?i:\b(?:regards|thanks|best|cheers|sincerely)),[ ]+({_NAME})\s*$", re.M),
]


def _phone_sub(m: re.Match) -> str:
    text = m.group(0)
    digits = sum(c.isdigit() for c in text)
    if _ISO_DATE.fullmatch(text.strip()) or digits < 8:
        return text
    return "[PHONE]"


def _name_sub(pattern: re.Pattern, text: str) -> str:
    def sub(m: re.Match) -> str:
        s, e = m.span(1)
        start = m.start()
        return m.group(0)[: s - start] + "[NAME]" + m.group(0)[e - start :]

    return pattern.sub(sub, text)


def redact(text: str) -> str:
    """Replace card numbers, IBANs, emails, phones and obvious names with placeholders."""
    text = _IBAN.sub("[IBAN]", text)
    text = _EMAIL.sub("[EMAIL]", text)
    text = _CARD.sub("[CARD]", text)
    text = _PHONE.sub(_phone_sub, text)
    for p in _NAME_PATTERNS:
        text = _name_sub(p, text)
    return text
