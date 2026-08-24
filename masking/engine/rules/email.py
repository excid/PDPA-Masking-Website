"""Email-address masking rule."""
from __future__ import annotations

import re

from ..base import RegexRule

_USER_EDGE = r"[A-Za-z0-9]"
_USER_MID = r"[A-Za-z0-9._%+-]"
_DOMAIN_LABEL = rf"{_USER_EDGE}(?:[A-Za-z0-9-]*{_USER_EDGE})?"

MASK_CHAR = "*"


class EmailRule(RegexRule):
    name = "email"
    label = "อีเมล"
    description = "อีเมล ปิดอักขระกลางของชื่อผู้ใช้และคงโดเมนเดิม"
    priority = 30

    pattern = re.compile(
        rf"""
        (?<![\w.+-])
        (?P<target>
            {_USER_EDGE}
            (?:{_USER_MID}*{_USER_EDGE})?
        )
        @
        (?P<domain>
            {_DOMAIN_LABEL}
            (?:\.{_DOMAIN_LABEL})+
        )
        (?![\w.-])
        """,
        re.VERBOSE,
    )

    def mask(self, match: re.Match[str]) -> str:
        username = match.group("target")
        length = len(username)
        if length <= 2:
            return username
        return username[0] + MASK_CHAR * (length - 2) + username[-1]


__all__ = ["EmailRule"]
