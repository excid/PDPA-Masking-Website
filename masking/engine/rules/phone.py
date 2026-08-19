"""กฎที่ 2 — เบอร์โทรศัพท์   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

โจทย์: ปิดเบอร์มือถือไทย เหลือเห็นแค่ 4 ตัวท้าย (หรือตามที่ทีมตกลง)
    081-234-5678   ->  ***-***-5678
    0812345678     ->  ******5678
    +66 81 234 5678 -> ...

TODO(คนที่ 2):
  [ ] รองรับ 08x/09x/06x, เบอร์บ้าน 02-xxx-xxxx, +66
  [ ] ระวังชนกับเลขบัตรเครดิต (priority ของกฎบัตร = 10 มาก่อนแล้ว)
  [ ] เคสที่ต้อง "ไม่จับ": เลขที่บ้าน 689/12, เลข 10 หลักที่เป็นรหัสอ้างอิง
  [ ] เขียนเทสต์ที่ tests/test_phone.py
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH


class PhoneRule(RegexRule):
    name = "phone"
    label = "เบอร์โทรศัพท์"
    description = "เบอร์โทรไทย เหลือ 4 ตัวท้าย"
    priority = 20

    pattern = re.compile(
        rf"""
        {NEVER_MATCH}    # TODO: แทนด้วย pattern จริง
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        return match.group(0)


__all__ = ["PhoneRule"]
