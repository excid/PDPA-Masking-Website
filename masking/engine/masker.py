"""Collect, resolve, and apply masking detections."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .registry import select_rules
from .types import Detection


@dataclass(slots=True)
class MaskResult:
    original: str
    masked: str
    detections: list[Detection] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        return dict(Counter(d.rule for d in self.detections))

    @property
    def total(self) -> int:
        return len(self.detections)

    def to_dict(self) -> dict:
        return {
            "masked": self.masked,
            "detections": [d.to_dict() for d in self.detections],
            "summary": self.summary,
            "total": self.total,
        }


def collect_detections(text: str, enabled: list[str] | None = None) -> list[Detection]:
    found: list[Detection] = []
    for rule in select_rules(enabled):
        found.extend(rule.find(text))
    return found


def resolve_overlaps(detections: list[Detection]) -> list[Detection]:
    """Prefer longer overlaps, then the detection with the earlier start."""
    ordered = sorted(detections, key=lambda d: (-d.length, d.start, d.rule))
    kept: list[Detection] = []
    for candidate in ordered:
        if any(candidate.start < k.end and k.start < candidate.end for k in kept):
            continue
        kept.append(candidate)
    return sorted(kept, key=lambda d: d.start)


def apply_detections(text: str, detections: list[Detection]) -> str:
    """Apply replacements right to left so offsets remain valid."""
    out = text
    for det in sorted(detections, key=lambda d: d.start, reverse=True):
        out = out[: det.start] + det.masked + out[det.end :]
    return out


def mask_text(text: str, enabled: list[str] | None = None) -> MaskResult:
    if not text:
        return MaskResult(original="", masked="", detections=[])

    detections = resolve_overlaps(collect_detections(text, enabled))
    return MaskResult(
        original=text,
        masked=apply_detections(text, detections),
        detections=detections,
    )
