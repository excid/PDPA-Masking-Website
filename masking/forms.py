"""Masking form."""
from __future__ import annotations

from django import forms
from django.conf import settings

from .engine.registry import rule_catalog


class MaskForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 12, "placeholder": "วาง log หรือข้อความที่นี่..."}),
        required=False,
        max_length=settings.MASKING_MAX_INPUT_CHARS,
        label="ข้อความต้นฉบับ",
    )
    rules = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="กฎที่เปิดใช้",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(r["name"], r["label"]) for r in rule_catalog()]
        self.fields["rules"].choices = choices
        self.fields["rules"].initial = [name for name, _ in choices]

    def enabled_rules(self) -> list[str] | None:
        if "rules" not in self.data:
            return None
        return self.cleaned_data.get("rules") or []
