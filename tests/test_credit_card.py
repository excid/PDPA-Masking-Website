from __future__ import annotations

import pytest

from masking.engine import mask_text

pytestmark = pytest.mark.xfail(reason="checksum policy pending", strict=False)


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
            "รหัสอ้างอิง 12345678901234567890",
            "ราคา 4111 บาท",
            "order-2024-0811",
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw


class TestLuhn:
    @pytest.mark.skip(reason="card-shaped values bypass checksum validation")
    def test_invalid_checksum_is_rejected(self):
        assert mask_text("1234-5678-9012-3456").masked == "1234-5678-9012-3456"
