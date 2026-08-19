"""View ฝั่งหน้าเว็บ (HTMX)   [ผู้รับผิดชอบ: คนที่ 6 Frontend + คนที่ 7 Backend]

รูปแบบการทำงานของ HTMX ในโปรเจกต์นี้:
    textarea -> POST /mask/ -> คืน **HTML บางส่วน** (partials/_result.html)
    -> HTMX เอาไปยัดใน <div id="result"> โดยไม่ต้องรีเฟรชหน้า
"""
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
    """หน้าแรก — textarea + ปุ่ม + กล่องผลลัพธ์"""
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
    """รับข้อความจาก HTMX แล้วคืน HTML บางส่วนของผลลัพธ์"""
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
    """ปุ่ม 'โหลดตัวอย่าง log' — คืน <textarea> ที่มีข้อความตัวอย่างอยู่แล้ว"""
    sample = SAMPLE_LOG_PATH.read_text(encoding="utf-8") if SAMPLE_LOG_PATH.exists() else ""
    form = MaskForm(initial={"text": sample})
    return render(request, "masking/partials/_input.html", {"form": form})


def build_segments(result) -> list[dict]:
    """แตกข้อความหลัง mask เป็นชิ้น ๆ เพื่อให้ template ใส่สีไฮไลต์ได้

    คืน list ของ ``{"text": ..., "rule": ... | None, "label": ...}``
    ชิ้นที่ ``rule`` เป็น ``None`` คือข้อความธรรมดา

    TODO(คนที่ 6): ตอนนี้คำนวณจาก detection บนข้อความ **ต้นฉบับ**
    ต้อง map ตำแหน่งใหม่หลังแทนที่ด้วย (ความยาว masked ไม่เท่าต้นฉบับเสมอไป)
    """
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
