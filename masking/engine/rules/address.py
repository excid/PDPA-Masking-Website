"""กฎที่ 5 — ที่อยู่ (ยากที่สุด)   [ผู้รับผิดชอบ: คนที่ 5 / Regex D]

โจทย์: ปิด "เลขที่บ้าน" แต่ต้องไม่ไปปิด "เลขซอย"
    Address: 689/12 ซอยสุขุมวิท 71  ->  Address: ***/** ซอยสุขุมวิท 71
                                        (เลข 71 ของซอยต้องอยู่ครบ)

ทำไมถึงยาก: ทั้งสองอย่างคือ "ตัวเลขในที่อยู่" เหมือนกัน ต้องแยกด้วย "บริบท"
  * เลขที่บ้านมักอยู่ต้นที่อยู่ / ตามหลัง ``บ้านเลขที่`` / มีรูปแบบ 689/12
  * เลขซอยตามหลังคำว่า ซอย / ซ. / Soi
แนวทาง: ใช้ named group ``target`` ครอบเฉพาะเลขที่บ้าน + non-capturing group
``(?:...)`` สำหรับส่วนที่เป็น optional (ซอย/หมู่/ถนน)

TODO(คนที่ 5):
  [ ] pattern จริง + named group target ครอบเฉพาะเลขที่บ้าน
  [ ] เคสที่ต้อง "ไม่จับ": ``ซอยสุขุมวิท 71``, ``หมู่ 5``, ``ชั้น 12``
  [ ] ตัดสินใจว่าจะ mask ถนน/ตำบล/อำเภอด้วยไหม แล้วเขียนลง README
  [ ] เขียนเทสต์ที่ tests/test_address.py
"""
from __future__ import annotations

import re

from ..base import RegexRule
from ._common import NEVER_MATCH


class AddressRule(RegexRule):
    name = "address"
    label = "ที่อยู่"
    description = "เลขที่บ้านในที่อยู่ (ไม่แตะเลขซอย)"
    priority = 50

    pattern = re.compile(
        rf"""
        {NEVER_MATCH}    # TODO: (?:Address|ที่อยู่|บ้านเลขที่)\s*:?\s*(?P<target>\d+(?:/\d+)?)
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def mask(self, match: re.Match[str]) -> str:
        return match.group(0)


__all__ = ["AddressRule"]
