"""ตัวช่วยกลางของเทสต์ทั้งชุด (Lead ดูแล)"""
from __future__ import annotations

import pytest

from masking.engine import mask_text
from masking.engine.registry import get_rule


@pytest.fixture
def mask():
    """เรียกเอนจินเต็มระบบ: ``mask("...").masked``"""
    return mask_text


@pytest.fixture
def rule_of():
    """ดึงกฎเดี่ยวมาทดสอบแยก: ``rule_of("email").find(text)``"""
    return get_rule


def assert_unchanged(text: str) -> None:
    """ช่วยเขียนเคส 'ต้องไม่จับ' ให้สั้นลง"""
    assert mask_text(text).masked == text
    assert mask_text(text).detections == []
