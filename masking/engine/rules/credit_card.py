"""Credit-card masking rule."""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import keep_last


def luhn_check(number: str) -> bool:
    digits = [int(c) for c in number if c.isdigit()]

    if not digits:
        return False

    checksum = 0
    is_second_digit = False

    for digit in reversed(digits):
        if is_second_digit:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        is_second_digit = not is_second_digit

    return checksum % 10 == 0


class CreditCardRule(RegexRule):
    name = "credit_card"
    label = "บัตรเครดิต"
    description = "เลขบัตร 16 หลัก ปิด 12 หลักแรกและคงตัวคั่นเดิม"
    priority = 10

    pattern = re.compile(
        r"""
        (?<!\d)
        (?P<cc_number>
            \d{4}
            [\s-]?
            \d{4}
            [\s-]?
            \d{4}
            [\s-]?
            \d{4}
        )
        (?!\d)
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        text = match.group("cc_number")
        return keep_last(text, 4, "*")


__all__ = ["CreditCardRule", "keep_last", "luhn_check"]
