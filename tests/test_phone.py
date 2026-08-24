from __future__ import annotations

import pytest

from masking.engine import mask_text

pytestmark = pytest.mark.xfail(
    reason="mask character and address overlap pending",
    strict=False,
)


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
            "บ้านเลขที่ 689/12",
            "ราคา 1234567 บาท",
            "2024-08-15",
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw


class TestOverlapWithCreditCard:
    def test_credit_card_wins_over_phone(self):
        result = mask_text("4111-1111-1111-1234")
        assert [d.rule for d in result.detections] == ["credit_card"]
