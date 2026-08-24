"""Thai phone-number masking rule."""
from __future__ import annotations

import re

from ..base import RegexRule


class PhoneRule(RegexRule):
    name = "phone"
    label = "เบอร์โทรศัพท์"
    description = "เบอร์โทรไทย (มือถือ/บ้าน/สากล) เหลือ 4 ตัวท้าย"
    priority = 20

    pattern = re.compile(
        r"""
        (?<!\d)
        (?:
            \+66[\s-]?\d{1,2}[\s-]?\d{3}[\s-]?\d{4}
            |
            0\d{2}-\d{3}-\d{4}
            |
            0\d{1}-\d{3}-\d{4}
            |
            0\d{9}
        )
        (?!\d)
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        text = match.group(0)
        digits = sum(c.isdigit() for c in text)
        keep_from = digits - 4
        out = []
        seen = 0
        for c in text:
            if c.isdigit():
                out.append(c if seen >= keep_from else "X")
                seen += 1
            else:
                out.append(c)
        return "".join(out)


__all__ = ["PhoneRule"]
