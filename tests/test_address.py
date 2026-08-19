"""เทสต์กฎ: ที่อยู่   [ผู้รับผิดชอบ: คนที่ 5 / Regex D]

วิธีใช้ไฟล์นี้
  1. ตอนนี้กฎยังเป็น stub เทสต์จึงถูกทำเครื่องหมาย xfail ไว้ (ไม่ทำให้ CI แดง)
  2. พอเขียน regex เสร็จ ให้ **ลบบรรทัด pytestmark ทิ้ง** แล้วเทสต์จะเริ่มบังคับใช้จริง
  3. เกณฑ์ให้คะแนนดู "ความหลากหลายของกรณีทดสอบ" → ต้องมีทั้งเคสที่ต้องจับ
     และเคสที่ต้อง **ไม่** จับ (คลาส TestMustNotMatch)
"""
from __future__ import annotations

import pytest

from masking.engine import mask_text

pytestmark = pytest.mark.xfail(reason="กฎยังเป็น stub — ลบบรรทัดนี้เมื่อเขียนเสร็จ", strict=False)


class TestMustMatch:
    def test_house_number_masked(self):
        assert mask_text("Address: 689/12 ถนนสุขุมวิท").masked == "Address: ***/** ถนนสุขุมวิท"

    def test_thai_prefix(self):
        out = mask_text("ที่อยู่: 42 หมู่บ้านสุขใจ").masked
        assert "42" not in out

    def test_prefix_is_kept(self):
        assert mask_text("Address: 689/12").masked.startswith("Address:")


class TestSoiNumberMustSurvive:
    """หัวใจของกฎนี้ — เลขซอยต้องไม่ถูก mask"""

    def test_soi_number_kept(self):
        out = mask_text("Address: 689/12 ซอยสุขุมวิท 71").masked
        assert out.endswith("ซอยสุขุมวิท 71")
        assert "689" not in out

    @pytest.mark.parametrize("raw", ["ซอยลาดพร้าว 101", "ซ. 15", "Soi 71", "หมู่ 5", "ชั้น 12"])
    def test_context_numbers_not_masked(self, raw):
        assert mask_text(raw).masked == raw
