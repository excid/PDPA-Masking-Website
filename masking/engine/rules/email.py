"""กฎที่ 3 — อีเมล   [ผู้รับผิดชอบ: คนที่ 3 / Regex B]

โจทย์: ปิด username เหลือตัวแรก + จำนวน * ตามความยาวที่เหลือ
    somchai@example.com  ->  s*******@example.com
    ab@x.com             ->  a*@x.com
    a@x.com              ->  ต้องตกลงกันว่าจะทำยังไง (username ตัวเดียว)

จุดสำคัญที่อาจารย์น่าจะถาม: ทำไมต้องใช้ re.sub() แบบส่ง callback
-> เพราะจำนวน * ขึ้นกับความยาว username ซึ่งรู้ได้ตอน runtime เท่านั้น
   ในโครงนี้เราแยกออกมาเป็นเมธอด mask() ซึ่งทำหน้าที่เดียวกับ callback

TODO(คนที่ 3):
  [ ] pattern จริง: ใช้ named group (?P<user>...) และ (?P<domain>...)
  [ ] ตัดสินใจเคส username ยาว 1 ตัว แล้วเขียนลง README
  [ ] เคสที่ต้อง "ไม่จับ": ข้อความที่มี @ แต่ไม่ใช่อีเมล เช่น @somchai (mention)
  [ ] เขียนเทสต์ที่ tests/test_email.py
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH


class EmailRule(RegexRule):
    name = "email"
    label = "อีเมล"
    description = "อีเมล เหลือตัวอักษรแรกของ username"
    priority = 30

    pattern = re.compile(
        rf"""
        {NEVER_MATCH}    # TODO: แทนด้วย pattern จริง เช่น (?P<user>...)@(?P<domain>...)
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        return match.group(0)


__all__ = ["EmailRule"]
