"""กฎที่ 1 — เลขบัตรเครดิต   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

โจทย์: ปิดเลขบัตร 16 หลัก เหลือเห็นแค่ 4 ตัวท้าย
    4111-1111-1111-1234  ->  ****-****-****-1234
    4111 1111 1111 1234  ->  **** **** **** 1234
    4111111111111234     ->  ************1234

TODO(คนที่ 2):
  [ ] เขียน pattern จริงแทน NEVER_MATCH (รองรับตัวคั่น -, เว้นวรรค, ไม่มีตัวคั่น)
  [ ] กันไม่ให้ไปจับเลขยาว ๆ ที่ไม่ใช่บัตร เช่น transaction id 20 หลัก
      (ใช้ \b หรือ lookaround กันเลขติดกันเกิน)
  [ ] (โบนัส) ตรวจ Luhn checksum ใน is_valid() -> คะแนน "ความครอบคลุม"
  [ ] เขียนเทสต์ที่ tests/test_credit_card.py
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH, keep_last


class CreditCardRule(RegexRule):
    name = "credit_card"
    label = "บัตรเครดิต"
    description = "เลขบัตรเครดิต 16 หลัก เหลือ 4 ตัวท้าย"
    # กฎนี้ได้สิทธิ์ก่อนเบอร์โทร เพราะเลขบัตรยาวกว่าและมีโอกาสถูกกฎอื่นกินซ้ำ
    priority = 10

    pattern = re.compile(
        rf"""
        {NEVER_MATCH}    # TODO: แทนด้วย pattern จริง
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        # stub: ยังไม่ mask อะไร คืนของเดิมไปก่อนเพื่อให้ทีมอื่นทำงานต่อได้
        return match.group(0)

    def is_valid(self, match: re.Match[str]) -> bool:
        return True


def luhn_check(number: str) -> bool:
    """ตรวจ checksum แบบ Luhn — TODO(คนที่ 2) เขียนจริงถ้าจะเก็บคะแนนโบนัส"""
    raise NotImplementedError


__all__ = ["CreditCardRule", "keep_last", "luhn_check"]
