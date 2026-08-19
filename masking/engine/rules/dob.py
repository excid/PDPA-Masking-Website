"""กฎที่ 4 — วันเดือนปีเกิด   [ผู้รับผิดชอบ: คนที่ 4 / Regex C]

โจทย์: ปิดวันเกิดที่นำหน้าด้วย ``DOB:`` (หรือ "วันเกิด:") แต่คง prefix ไว้
    DOB: 15/08/2540   ->  DOB: **/**/****
    วันเกิด: 1990-08-15 -> ...

เทคนิคที่ต้องใช้:
  * ``re`` ไม่รองรับ lookbehind ความยาวไม่คงที่ → ให้ครอบส่วนที่จะ mask
    ด้วย named group ชื่อ ``target`` แทน เอนจินจะ mask เฉพาะกลุ่มนั้น
    ตัวอย่างโครง:  ``(?:DOB|วันเกิด)\s*:\s*(?P<target>...)``
  * validate วัน 1–31 / เดือน 1–12 ใน is_valid()

TODO(คนที่ 4):
  [ ] pattern จริง + named group target
  [ ] รองรับทั้ง พ.ศ. (2540) และ ค.ศ. (1997), ตัวคั่น / - .
  [ ] เคสที่ต้อง "ไม่จับ": วันที่ทั่วไปใน log ที่ไม่มี prefix เช่น 2024-08-15 10:22:01
  [ ] เขียนเทสต์ที่ tests/test_dob.py
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH


class DobRule(RegexRule):
    name = "dob"
    label = "วันเดือนปีเกิด"
    description = "วันเกิดที่มี prefix DOB: / วันเกิด: (คง prefix ไว้)"
    priority = 40

    pattern = re.compile(
        rf"""
        {NEVER_MATCH}    # TODO: (?:DOB|วันเกิด)\s*:\s*(?P<target>วันที่จริง)
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def mask(self, match: re.Match[str]) -> str:
        return match.group(0)

    def is_valid(self, match: re.Match[str]) -> bool:
        # TODO(คนที่ 4): เช็ควัน 1–31 เดือน 1–12 (และปีที่สมเหตุสมผล)
        return True


__all__ = ["DobRule"]
