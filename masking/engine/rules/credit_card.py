"""กฎที่ 1 — เลขบัตรเครดิต   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

โจทย์: ปิดเลขบัตร 16 หลัก เหลือเห็นแค่ 4 ตัวท้าย
    4111-1111-1111-1234  ->  ****-****-****-1234
    4111 1111 1111 1234  ->  **** **** **** 1234
    4111111111111234     ->  ************1234
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH, keep_last


def luhn_check(number: str) -> bool:
    # ดึงเฉพาะตัวเลขออกมา
    digits = [int(c) for c in number if c.isdigit()]
    
    if not digits:
        return False

    checksum = 0
    is_second_digit = False
    
    # วนลูปจากหลังมาหน้าตามสูตร Luhn Algorithm
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
    description = "เลขบัตรเครดิต 16 หลัก เหลือ 4 ตัวท้าย"
    priority = 10

    pattern = re.compile(
        r"""
        (?<!\d)                              # กันชนหน้า: ไม่ต่อจากตัวเลขอื่น (กันเคส 20 หลัก)
        (?P<cc_number>
            \d{4}                            # 4 หลักแรก
            [\s-]?                           # คั่นด้วยช่องว่างหรือขีด (มีหรือไม่มีก็ได้)
            \d{4}
            [\s-]?
            \d{4}
            [\s-]?
            \d{4}                            # 4 หลักสุดท้าย
        )
        (?!\d)                               # กันชนหลัง: ไม่ตามด้วยตัวเลขอื่น
        """,
        re.VERBOSE,
    )



    def mask(self, match: re.Match[str]) -> str:
        text = match.group("cc_number")
        return keep_last(text, 4, "*")


__all__ = ["CreditCardRule", "keep_last", "luhn_check"]
