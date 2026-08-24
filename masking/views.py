"""HTML views for the masking interface."""
from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .engine import mask_text
from .engine.registry import rule_catalog
from .forms import MaskForm

SAMPLE_LOG_PATH = Path(settings.BASE_DIR) / "samples" / "sample_log.txt"


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "masking/index.html",
        {
            "form": MaskForm(),
            "rules": rule_catalog(),
            "github_url": settings.GITHUB_REPO_URL,
        },
    )


@require_POST
def mask_partial(request: HttpRequest) -> HttpResponse:
    form = MaskForm(request.POST)
    if not form.is_valid():
        return render(request, "masking/partials/_error.html", {"form": form}, status=400)

    result = mask_text(form.cleaned_data["text"], form.enabled_rules())
    return render(
        request,
        "masking/partials/_result.html",
        {"result": result, "segments": build_segments(result)},
    )


@require_GET
def load_sample(request: HttpRequest) -> HttpResponse:
    sample = SAMPLE_LOG_PATH.read_text(encoding="utf-8") if SAMPLE_LOG_PATH.exists() else ""
    form = MaskForm(initial={"text": sample})
    return render(request, "masking/partials/_input.html", {"form": form})


def build_segments(result) -> list[dict]:
    """Split masked text into highlighted and plain segments."""
    segments: list[dict] = []
    cursor = 0
    offset = 0
    for det in result.detections:
        start = det.start + offset
        if start > cursor:
            segments.append({"text": result.masked[cursor:start], "rule": None, "label": ""})
        end = start + len(det.masked)
        segments.append({"text": result.masked[start:end], "rule": det.rule, "label": det.label})
        offset += len(det.masked) - (det.end - det.start)
        cursor = end
    if cursor < len(result.masked):
        segments.append({"text": result.masked[cursor:], "rule": None, "label": ""})
    return segments
