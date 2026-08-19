"""เทสต์กฎ: วันเดือนปีเกิด   [ผู้รับผิดชอบ: คนที่ 4 / Regex C]

วิธีใช้ไฟล์นี้
  1. ตอนนี้กฎยังเป็น stub เทสต์จึงถูกทำเครื่องหมาย xfail ไว้ (ไม่ทำให้ CI แดง)
  2. พอเขียน regex เสร็จ ให้ **ลบบรรทัด pytestmark ทิ้ง** แล้วเทสต์จะเริ่มบังคับใช้จริง
  3. เกณฑ์ให้คะแนนดู "ความหลากหลายของกรณีทดสอบ" → ต้องมีทั้งเคสที่ต้องจับ
     และเคสที่ต้อง **ไม่** จับ (คลาส TestMustNotMatch)
"""
from __future__ import annotations

import pytest

from masking.engine import mask_text

pytestmark = pytest.mark.xfail(reason="กฎยังเป็น stub — ลบบรรทัดนี้เมื่อเขียนเสร็จ", strict=False)


class TestMustMatch:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("DOB: 15/08/2540", "DOB: **/**/****"),
            ("DOB: 1997-08-15", "DOB: ****-**-**"),
            ("วันเกิด: 15/08/2540", "วันเกิด: **/**/****"),
        ],
    )
    def test_prefix_is_kept(self, raw, expected):
        """prefix ต้องอยู่ครบ mask เฉพาะตัววันที่"""
        assert mask_text(raw).masked == expected

    def test_case_insensitive_prefix(self):
        assert mask_text("dob: 15/08/2540").masked.startswith("dob:")


class TestValidation:
    @pytest.mark.parametrize("raw", ["DOB: 32/08/2540", "DOB: 15/13/2540"])
    def test_invalid_day_or_month_not_masked(self, raw):
        assert mask_text(raw).masked == raw


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "2024-08-15 10:22:01 INFO ระบบเริ่มทำงาน",   # timestamp ใน log ไม่มี prefix
            "หมดอายุ 15/08/2570",                        # วันที่ทั่วไป ไม่มี prefix
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw
