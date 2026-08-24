from __future__ import annotations

import pytest

from masking.engine import mask_text
from masking.engine.registry import get_rule


@pytest.fixture
def mask():
    return mask_text


@pytest.fixture
def rule_of():
    return get_rule


def assert_unchanged(text: str) -> None:
    assert mask_text(text).masked == text
    assert mask_text(text).detections == []
