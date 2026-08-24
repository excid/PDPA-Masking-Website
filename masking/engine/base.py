"""Base class for regex masking rules."""
from __future__ import annotations

import re
from typing import ClassVar

from .types import Detection

# Mask only this named group when a pattern defines it.
TARGET_GROUP = "target"


class RegexRule:
    name: ClassVar[str] = ""
    label: ClassVar[str] = ""
    priority: ClassVar[int] = 100
    description: ClassVar[str] = ""
    pattern: ClassVar[re.Pattern[str]]

    def mask(self, match: re.Match[str]) -> str:
        """Return the replacement text for a match."""
        raise NotImplementedError

    def is_valid(self, match: re.Match[str]) -> bool:
        """Return whether a regex match passes extra validation."""
        return True

    def span_of(self, match: re.Match[str]) -> tuple[int, int]:
        if TARGET_GROUP in self.pattern.groupindex:
            return match.span(TARGET_GROUP)
        return match.span()

    def find(self, text: str) -> list[Detection]:
        """Return valid detections without modifying the input."""
        found: list[Detection] = []
        for match in self.pattern.finditer(text):
            if not self.is_valid(match):
                continue
            start, end = self.span_of(match)
            if start < 0 or end <= start:
                continue
            found.append(
                Detection(
                    rule=self.name,
                    label=self.label,
                    start=start,
                    end=end,
                    original=text[start:end],
                    masked=self.mask(match),
                )
            )
        return found

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{type(self).__name__} name={self.name!r}>"
