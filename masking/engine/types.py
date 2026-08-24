"""Shared masking data types."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Detection:
    rule: str
    label: str
    start: int
    end: int
    original: str
    masked: str

    @property
    def length(self) -> int:
        return self.end - self.start

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "label": self.label,
            "start": self.start,
            "end": self.end,
            "original": self.original,
            "masked": self.masked,
        }
