"""ตัวช่วยเล็ก ๆ ที่ใช้ร่วมกันหลายกฎ (Lead ดูแล)"""
from __future__ import annotations

#: pattern ที่ไม่ match อะไรเลย — ใช้เป็น placeholder ของ stub
#: พอเขียนกฎจริงเสร็จให้ลบทิ้ง
NEVER_MATCH = r"(?!x)x"


def keep_last(digits: str, keep: int = 4, mask_char: str = "*") -> str:
    """mask ตัวเลขทั้งหมดยกเว้น ``keep`` ตัวท้าย โดยคงตัวคั่นเดิมไว้

    >>> keep_last("4111-1111-1111-1234")
    '****-****-****-1234'
    """
    out: list[str] = []
    total_digits = sum(ch.isdigit() for ch in digits)
    seen = 0
    for ch in digits:
        if ch.isdigit():
            seen += 1
            out.append(ch if seen > total_digits - keep else mask_char)
        else:
            out.append(ch)
    return "".join(out)
