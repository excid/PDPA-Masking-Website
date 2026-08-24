"""กฎที่ 2 — เบอร์โทรศัพท์   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

รูปแบบที่รองรับ (เก็บ 4 ตัวท้าย ที่เหลือแทนด้วย X โดยคงเครื่องหมาย - / เว้นวรรค เดิมไว้):
    081-234-5678     -> XXX-XXX-5678      # มือถือ มีขีด (08x/09x)
    0812345678       -> XXXXXX5678        # มือถือ ไม่มีขีด
    02-345-6789      -> XX-XXX-6789       # เบอร์บ้าน กทม.
    +66 81 234 5678  -> +XX XX XXX 5678   # รูปแบบสากล
"""
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
        (?<!\d)                              # ไม่ใช่ส่วนกลางของเลขอื่น (กันชนบัตรเครดิต)
        (?:
            \+66[\s-]?\d{1,2}[\s-]?\d{3}[\s-]?\d{4}   # +66 81 234 5678
            |
            0\d{2}-\d{3}-\d{4}                        # 081-234-5678 (มือถือ 3-3-4)
            |
            0\d{1}-\d{3}-\d{4}                         # 02-345-6789 (บ้าน 2-3-4)
            |
            0\d{9}                                     # 0812345678 (ไม่มีขีด)
        )
        (?!\d)                               # ไม่ตามด้วยตัวเลขอีก (กันชน เลขบัตร/เลขอ้างอิงยาวกว่า)
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        text = match.group(0)
        digits = sum(c.isdigit() for c in text)
        keep_from = digits - 4  # index (0-based, among digits) where "keep" zone starts
        out = []
        seen = 0
        for c in text:
            if c.isdigit():
                out.append(c if seen >= keep_from else "X")
                seen += 1
            else:
                out.append(c)  # เก็บ -, +, เว้นวรรค ไว้ตามเดิม
        return "".join(out)


__all__ = ["PhoneRule"]