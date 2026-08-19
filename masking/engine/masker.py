"""Orchestrator — รวมผลจากทุกกฎแล้วแทนที่ครั้งเดียว   [ผู้รับผิดชอบ: คนที่ 1 / Lead]

หัวใจของไฟล์นี้คือ "ห้าม mask ทีละกฎแบบไล่เรียงกัน" เพราะข้อความที่ถูก mask แล้ว
(เช่น ``****-****-****-1234``) อาจโดนกฎถัดไปจับซ้ำ วิธีที่ใช้คือ

    1. ให้ทุกกฎ scan ข้อความ **ต้นฉบับ** แล้วคืน span (start, end) มา
    2. ตัดช่วงที่ทับกันออกตาม priority  (resolve_overlaps)
    3. แทนที่จาก **ท้ายไปหน้า** เพื่อไม่ให้ index ที่คำนวณไว้เพี้ยน
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .registry import select_rules
from .types import Detection


@dataclass(slots=True)
class MaskResult:
    """ผลลัพธ์ที่ส่งกลับให้ API / template"""

    original: str
    masked: str
    detections: list[Detection] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        """นับจำนวนที่เจอแยกตามกฎ เช่น ``{"email": 3, "credit_card": 2}``"""
        return dict(Counter(d.rule for d in self.detections))

    @property
    def total(self) -> int:
        return len(self.detections)

    def to_dict(self) -> dict:
        return {
            "masked": self.masked,
            "detections": [d.to_dict() for d in self.detections],
            "summary": self.summary,
            "total": self.total,
        }


def collect_detections(text: str, enabled: list[str] | None = None) -> list[Detection]:
    """ขั้นที่ 1 — ให้ทุกกฎที่เปิดอยู่ scan ข้อความต้นฉบับ"""
    found: list[Detection] = []
    for rule in select_rules(enabled):
        found.extend(rule.find(text))
    return found


def resolve_overlaps(detections: list[Detection]) -> list[Detection]:
    """ขั้นที่ 2 — ถ้าสองกฎจับช่วงที่ทับกัน ให้เก็บอันเดียว

    เกณฑ์ตัดสิน (เรียงตามลำดับ):
        1. ช่วงที่ยาวกว่าชนะ  — จับได้ครอบคลุมกว่า
        2. ถ้ายาวเท่ากัน ให้ตัวที่ start มาก่อนชนะ
    ตัวอย่าง: เลขบัตร 16 หลัก กับ เบอร์โทรที่ไปจับ 10 หลักท้ายของบัตร
    → เลขบัตรยาวกว่า จึงชนะ
    """
    ordered = sorted(detections, key=lambda d: (-d.length, d.start, d.rule))
    kept: list[Detection] = []
    for candidate in ordered:
        if any(candidate.start < k.end and k.start < candidate.end for k in kept):
            continue
        kept.append(candidate)
    return sorted(kept, key=lambda d: d.start)


def apply_detections(text: str, detections: list[Detection]) -> str:
    """ขั้นที่ 3 — แทนที่จากท้ายไปหน้า

    ต้องเรียงจากท้ายมาหน้า เพราะถ้าแทนจากหน้าไปท้าย ความยาวข้อความจะเปลี่ยน
    ทำให้ start/end ของ detection ตัวถัด ๆ ไปชี้ผิดตำแหน่ง
    """
    out = text
    for det in sorted(detections, key=lambda d: d.start, reverse=True):
        out = out[: det.start] + det.masked + out[det.end :]
    return out


def mask_text(text: str, enabled: list[str] | None = None) -> MaskResult:
    """API หลักของเอนจิน — ใช้ที่เดียวทั้งโปรเจกต์

    Args:
        text:    ข้อความ/log ที่ผู้ใช้วางเข้ามา
        enabled: รายชื่อกฎที่เปิดใช้ (``None`` = ทุกกฎ) มาจาก checkbox บนหน้าเว็บ

    Returns:
        :class:`MaskResult` ที่มีทั้งข้อความหลัง mask, รายการ detection และสรุปจำนวน

    >>> result = mask_text("hello")
    >>> result.masked
    'hello'
    """
    if not text:
        return MaskResult(original="", masked="", detections=[])

    detections = resolve_overlaps(collect_detections(text, enabled))
    return MaskResult(
        original=text,
        masked=apply_detections(text, detections),
        detections=detections,
    )
