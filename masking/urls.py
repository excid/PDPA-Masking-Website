from django.urls import path

from . import api, views

app_name = "masking"

urlpatterns = [
    path("", views.index, name="index"),
    path("mask/", views.mask_partial, name="mask_partial"),
    path("sample/", views.load_sample, name="load_sample"),
    path("api/mask/", api.mask_api, name="api_mask"),
    path("api/rules/", api.rules_api, name="api_rules"),
    path("api/health/", api.health, name="api_health"),
]
