"""เทสต์กฎ: เบอร์โทรศัพท์   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

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
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("081-234-5678", "***-***-5678"),
            ("0812345678", "******5678"),
            ("02-123-4567", "**-***-4567"),
        ],
    )
    def test_mask_keeps_last_four(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_international_format(self):
        out = mask_text("+66 81 234 5678").masked
        assert "5678" in out and "81 234" not in out


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "บ้านเลขที่ 689/12",       # เลขที่บ้าน ไม่ใช่เบอร์
            "ราคา 1234567 บาท",         # เลขไม่ขึ้นต้นด้วย 0
            "2024-08-15",               # วันที่
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw


class TestOverlapWithCreditCard:
    def test_credit_card_wins_over_phone(self):
        """10 หลักท้ายของเลขบัตรต้องไม่ถูกจับเป็นเบอร์โทร"""
        result = mask_text("4111-1111-1111-1234")
        assert [d.rule for d in result.detections] == ["credit_card"]
