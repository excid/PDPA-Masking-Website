"""เทสต์กฎ: เลขบัตรเครดิต   [ผู้รับผิดชอบ: คนที่ 2 / Regex A]

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
            ("4111-1111-1111-1234", "****-****-****-1234"),
            ("4111 1111 1111 1234", "**** **** **** 1234"),
            ("4111111111111234", "************1234"),
        ],
    )
    def test_mask_keeps_last_four(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_inside_a_sentence(self):
        out = mask_text("ชำระด้วยบัตร 4111-1111-1111-1234 เมื่อเวลา 10:22").masked
        assert "1234" in out and "4111-1111" not in out

    def test_detection_metadata(self):
        result = mask_text("4111-1111-1111-1234")
        assert result.total == 1
        assert result.detections[0].rule == "credit_card"


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "รหัสอ้างอิง 12345678901234567890",   # เลข 20 หลัก ไม่ใช่บัตร
            "ราคา 4111 บาท",                      # เลข 4 หลักเฉย ๆ
            "order-2024-0811",                    # เลขปนขีด แต่ไม่ครบ 16 หลัก
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw


class TestLuhn:
    @pytest.mark.skip(reason="TODO(คนที่ 2): เปิดเมื่อทำ luhn_check เสร็จ")
    def test_invalid_checksum_is_rejected(self):
        assert mask_text("1234-5678-9012-3456").masked == "1234-5678-9012-3456"
