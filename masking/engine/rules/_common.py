"""Shared masking helpers."""
from __future__ import annotations

NEVER_MATCH = r"(?!x)x"


def keep_last(digits: str, keep: int = 4, mask_char: str = "*") -> str:
    """Mask digits except the final ``keep`` digits, preserving separators."""
    out: list[str] = []
    total_digits = sum(ch.isdigit() for ch in digits)
    seen = 0
    for ch in digits:
        if ch.isdigit():
            seen += 1
            out.append(ch if seen > total_digits - keep else mask_char)
        else:
            out.append(ch)
    return "".join(out)
