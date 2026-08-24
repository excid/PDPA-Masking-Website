"""House-number masking rule."""
from __future__ import annotations

import re

from ..base import RegexRule


class AddressRule(RegexRule):
    name = "address"
    label = "ที่อยู่"
    description = "เลขที่บ้านหลังคำว่า Address, ที่อยู่ หรือ บ้านเลขที่ ปิดเฉพาะตัวเลข"
    priority = 50

    pattern = re.compile(
        r"""
        (?:Address|ที่อยู่|บ้านเลขที่)\s*:?\s*(?P<target>\d+(?:/\d+)?)
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def mask(self, match: re.Match[str]) -> str:
        return re.sub(r"\d", "*", match.group("target"))


__all__ = ["AddressRule"]
