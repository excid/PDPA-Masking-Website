"""Masking rule registry."""
from __future__ import annotations

from .base import RegexRule
from .rules.address import AddressRule
from .rules.credit_card import CreditCardRule
from .rules.dob import DobRule
from .rules.email import EmailRule
from .rules.phone import PhoneRule

RULES: tuple[RegexRule, ...] = (
    CreditCardRule(),
    PhoneRule(),
    EmailRule(),
    DobRule(),
    AddressRule(),
)

_BY_NAME = {rule.name: rule for rule in RULES}


def rule_names() -> list[str]:
    return [rule.name for rule in RULES]


def get_rule(name: str) -> RegexRule:
    return _BY_NAME[name]


def select_rules(enabled: list[str] | tuple[str, ...] | set[str] | None) -> list[RegexRule]:
    if enabled is None:
        return list(RULES)
    wanted = set(enabled)
    return [rule for rule in RULES if rule.name in wanted]


def rule_catalog() -> list[dict]:
    return [
        {"name": r.name, "label": r.label, "description": r.description}
        for r in RULES
    ]
