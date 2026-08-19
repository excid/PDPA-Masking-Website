"""ฟอร์มรับข้อความจากหน้าเว็บ   [ผู้รับผิดชอบ: คนที่ 7 / Backend]"""
from __future__ import annotations

from django import forms
from django.conf import settings

from .engine.registry import rule_catalog


class MaskForm(forms.Form):
    """textarea + checkbox เปิด/ปิดแต่ละกฎ"""

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
        """คืน ``None`` เมื่อไม่ได้ส่ง field มาเลย = เปิดทุกกฎ"""
        if "rules" not in self.data:
            return None
        return self.cleaned_data.get("rules") or []
