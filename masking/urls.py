from django.urls import path

from . import api, views

app_name = "masking"

urlpatterns = [
    # ---- หน้าเว็บ (คนที่ 6) ----
    path("", views.index, name="index"),
    path("mask/", views.mask_partial, name="mask_partial"),  # HTMX โยนมาที่นี่
    path("sample/", views.load_sample, name="load_sample"),  # ปุ่ม "โหลดตัวอย่าง log"
    # ---- JSON API (คนที่ 7) ----
    path("api/mask/", api.mask_api, name="api_mask"),
    path("api/rules/", api.rules_api, name="api_rules"),
    path("api/health/", api.health, name="api_health"),
]
