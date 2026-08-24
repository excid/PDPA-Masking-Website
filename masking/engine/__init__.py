"""Public masking engine API."""
from .masker import MaskResult, mask_text
from .registry import RULES, get_rule, rule_names
from .types import Detection

__all__ = ["Detection", "MaskResult", "mask_text", "RULES", "get_rule", "rule_names"]
