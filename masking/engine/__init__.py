"""Masking engine — ส่วนนี้เป็น Python ล้วน ไม่ผูกกับ Django

ให้ import ผ่าน package นี้เท่านั้น เช่น::

    from masking.engine import mask_text
"""
from .masker import MaskResult, mask_text
from .registry import RULES, get_rule, rule_names
from .types import Detection

__all__ = ["Detection", "MaskResult", "mask_text", "RULES", "get_rule", "rule_names"]
