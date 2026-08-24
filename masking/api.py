"""JSON endpoints for the masking service."""
from __future__ import annotations

import json

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .engine import mask_text
from .engine.registry import rule_catalog, rule_names


@csrf_exempt  # This endpoint does not use session authentication.
@require_POST
def mask_api(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "payload ต้องเป็น object"}, status=400)

    text = payload.get("text", "")
    if not isinstance(text, str):
        return JsonResponse({"error": "field 'text' ต้องเป็น string"}, status=400)
    if len(text) > settings.MASKING_MAX_INPUT_CHARS:
        return JsonResponse(
            {"error": f"ข้อความยาวเกิน {settings.MASKING_MAX_INPUT_CHARS} ตัวอักษร"}, status=413
        )

    rules = payload.get("rules")
    if rules is not None:
        if not isinstance(rules, list) or not all(isinstance(r, str) for r in rules):
            return JsonResponse({"error": "field 'rules' ต้องเป็น list ของ string"}, status=400)
        unknown = sorted(set(rules) - set(rule_names()))
        if unknown:
            return JsonResponse({"error": f"ไม่รู้จักกฎ: {', '.join(unknown)}"}, status=400)

    return JsonResponse(mask_text(text, rules).to_dict())


@require_GET
def rules_api(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"rules": rule_catalog()})


@require_GET
def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})
