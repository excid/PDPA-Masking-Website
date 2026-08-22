"""กฎที่ 3 — อีเมล   [ผู้รับผิดชอบ: คนที่ 3 / Regex B]

โจทย์ (ตามเอกสาร ToC Assignment): ซ่อนชื่อผู้ใช้ (username/local-part) ทั้งหมด
ยกเว้นตัวอักษร "ตัวแรก" และ "ตัวสุดท้าย" ส่วนโดเมนให้เปิดเผยตามเดิม

    somchai.d@company.com  ->  s*******d@company.com
    (username "somchai.d" ยาว 9 ตัว: เก็บ s กับ d ไว้ ปิดตรงกลาง 7 ตัวเป็น *)

หมายเหตุ: docstring ฉบับร่างเดิมของกฎนี้ชวนให้ปิดทุกตัวยกเว้นตัวแรกตัวเดียว
(ไม่เก็บตัวสุดท้าย) ซึ่งไม่ตรงกับตัวอย่างในเอกสารโจทย์จริงที่ให้เก็บทั้งตัวแรก
และตัวสุดท้าย จึงยึดตามเอกสารโจทย์เป็นหลัก (ดู docs/regex.md หัวข้อที่ 3
สำหรับคำอธิบายเพิ่มเติม)

กรณี username สั้นมาก (เอกสารไม่ได้ระบุ จึงตัดสินใจเอง):
  * ยาว 1 ตัว (เช่น a@x.com)  -> ตัวเดียวกันเป็นทั้งตัวแรกและตัวสุดท้าย
    ไม่มีอะไรให้ปิดตรงกลาง จึงคงค่าเดิมไว้ทั้งหมด
  * ยาว 2 ตัว (เช่น ab@x.com) -> ตัวแรกกับตัวสุดท้ายชนกันพอดี (a และ b)
    ไม่มีตัวกลางให้ปิดเช่นกัน จึงคงค่าเดิมไว้ทั้งหมด

ทำไมต้องใช้เมธอด mask() แบบ callback (แทนการแทนที่ตรง ๆ)
-> เพราะจำนวน * ต้องเท่ากับ (ความยาว username - 2) ซึ่งรู้ได้ตอน runtime
   เท่านั้น (username แต่ละอันยาวไม่เท่ากัน)
"""
from __future__ import annotations

import re

from ..base import RegexRule

# ตัวอักษรตัวแรก/ตัวสุดท้ายของ username ต้องเป็นตัวอักษรหรือตัวเลข
# (กันไม่ให้ username เริ่ม/จบด้วยจุดหรือขีด ซึ่งไม่ใช่อีเมลที่ถูกต้อง)
_USER_EDGE = r"[A-Za-z0-9]"
# ตัวกลางของ username อนุญาตอักขระที่พบได้ทั่วไปในอีเมลจริง
_USER_MID = r"[A-Za-z0-9._%+-]"
# หนึ่ง label ของโดเมน (เช่น "company", "co") ต้องเริ่ม/จบด้วยตัวอักษรหรือตัวเลข
_DOMAIN_LABEL = rf"{_USER_EDGE}(?:[A-Za-z0-9-]*{_USER_EDGE})?"

MASK_CHAR = "*"


class EmailRule(RegexRule):
    name = "email"
    label = "อีเมล"
    description = "อีเมล เก็บตัวอักษรตัวแรก-ตัวสุดท้ายของ username เปิดเผยโดเมน"
    priority = 30

    pattern = re.compile(
        rf"""
        (?<![\w.+-])                         # ไม่ให้ username ต่อจากตัวอักษร/สัญลักษณ์อื่น
                                              # (กันเคส mention "@somchai" ที่ไม่มี user
                                              #  อยู่ข้างหน้า @ จริง ๆ)
        (?P<target>
            {_USER_EDGE}                      # ตัวแรกของ username
            (?:{_USER_MID}*{_USER_EDGE})?      # ตัวกลาง (ถ้ามี) ต้องจบด้วยตัวอักษร/ตัวเลข
        )
        @
        (?P<domain>
            {_DOMAIN_LABEL}                    # โดเมนหลัก เช่น "company"
            (?:\.{_DOMAIN_LABEL})+             # ต้องมีอย่างน้อย 1 จุด เช่น ".com" / ".co.th"
        )
        (?![\w.-])                            # กันไม่ให้โดเมนโดนตัดกลางคัน
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        username = match.group("target")
        length = len(username)
        # ยาว <= 2 ตัว: ตัวแรกกับตัวสุดท้ายชนกัน/ติดกัน ไม่มีตรงกลางให้ปิด
        if length <= 2:
            return username
        return username[0] + MASK_CHAR * (length - 2) + username[-1]


__all__ = ["EmailRule"]
