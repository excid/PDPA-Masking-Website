"""คลาสฐานของกฎทุกข้อ

คน 2–5 แค่สืบทอด :class:`RegexRule` แล้วกำหนด 4 อย่าง:

1. ``name``    — ชื่อสั้น ๆ ใช้เป็น key (ห้ามซ้ำกับคนอื่น)
2. ``label``   — ชื่อภาษาไทยที่โชว์บนหน้าเว็บ
3. ``pattern`` — ``re.compile(..., re.VERBOSE)``
4. ``mask()``  — รับ ``re.Match`` คืน string ที่ mask แล้ว

**เทคนิคสำคัญ**: ถ้า pattern มี named group ชื่อ ``target``
เอนจินจะ mask เฉพาะช่วงของ group นั้น ส่วนที่เหลือ (เช่น prefix ``DOB:``)
จะถูกเก็บไว้ตามเดิม — ใช้แทน lookbehind แบบความยาวไม่คงที่ซึ่ง ``re`` ไม่รองรับ
"""
from __future__ import annotations

import re
from typing import ClassVar

from .types import Detection

#: ชื่อ named group พิเศษ — ถ้ามี จะ mask เฉพาะกลุ่มนี้
TARGET_GROUP = "target"


class RegexRule:
    """กฎที่ทำงานด้วย regex หนึ่งชุด"""

    name: ClassVar[str] = ""
    label: ClassVar[str] = ""
    #: เลขน้อย = ได้สิทธิ์ก่อนเวลาช่วงทับกัน (ดู masker.resolve_overlaps)
    priority: ClassVar[int] = 100
    #: คำอธิบายสั้น ๆ ใช้โชว์ใน UI และใน README
    description: ClassVar[str] = ""
    pattern: ClassVar[re.Pattern[str]]

    # ---- ส่วนที่แต่ละคนต้องเขียนเอง ----
    def mask(self, match: re.Match[str]) -> str:
        """คืนข้อความที่ mask แล้ว สำหรับ match นี้

        ถ้า pattern มี group ``target`` ให้คืนค่าเฉพาะส่วนของ ``target``
        """
        raise NotImplementedError

    def is_valid(self, match: re.Match[str]) -> bool:
        """ตัวกรองเพิ่มเติมหลัง regex ผ่านแล้ว

        ใช้กับเงื่อนไขที่ regex เขียนแล้วอ่านไม่รู้เรื่อง เช่น เช็ควันที่ 31/02
        หรือ Luhn checksum ของบัตรเครดิต — คืน ``False`` เพื่อทิ้ง match นี้
        """
        return True

    # ---- ส่วนที่เอนจินจัดการให้ ไม่ต้องแก้ ----
    def span_of(self, match: re.Match[str]) -> tuple[int, int]:
        if TARGET_GROUP in self.pattern.groupindex:
            return match.span(TARGET_GROUP)
        return match.span()

    def find(self, text: str) -> list[Detection]:
        """หา match ทั้งหมดในข้อความ แล้วคืนเป็น Detection (ยังไม่แทนที่)"""
        found: list[Detection] = []
        for match in self.pattern.finditer(text):
            if not self.is_valid(match):
                continue
            start, end = self.span_of(match)
            if start < 0 or end <= start:
                continue
            found.append(
                Detection(
                    rule=self.name,
                    label=self.label,
                    start=start,
                    end=end,
                    original=text[start:end],
                    masked=self.mask(match),
                )
            )
        return found

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{type(self).__name__} name={self.name!r}>"
