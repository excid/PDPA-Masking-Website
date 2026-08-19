"""ชนิดข้อมูลกลางที่ทุกกฎต้องใช้ร่วมกัน — ห้ามแก้โดยไม่คุยกับ Lead

`Detection` คือ "สิ่งที่กฎหนึ่งเจอหนึ่งจุด" ตัว orchestrator จะเอา Detection
จากทุกกฎมารวม แล้วค่อยตัดสินว่าจุดไหนทับกันบ้าง ก่อนจะแทนที่จริง
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Detection:
    """ผลการตรวจจับข้อมูลส่วนบุคคล 1 จุดในข้อความ

    Attributes:
        rule:     ชื่อกฎแบบสั้น เช่น ``"email"`` (ใช้เป็น key ใน API/ frontend)
        label:    ชื่อที่แสดงให้ผู้ใช้เห็น เช่น ``"อีเมล"``
        start:    ตำแหน่งเริ่ม (index ใน string ต้นฉบับ, inclusive)
        end:      ตำแหน่งจบ (exclusive) — ใช้คู่กับ start แบบ ``text[start:end]``
        original: ข้อความต้นฉบับช่วงนั้น
        masked:   ข้อความหลัง mask ที่จะเอาไปแทนที่
    """

    rule: str
    label: str
    start: int
    end: int
    original: str
    masked: str

    @property
    def length(self) -> int:
        return self.end - self.start

    def to_dict(self) -> dict:
        """แปลงเป็น dict สำหรับส่งออกทาง JSON API."""
        return {
            "rule": self.rule,
            "label": self.label,
            "start": self.start,
            "end": self.end,
            "original": self.original,
            "masked": self.masked,
        }
