"""เทสต์กฎ: อีเมล   [ผู้รับผิดชอบ: คนที่ 3 / Regex B]

หมายเหตุ (แก้ไขจากไฟล์ต้นฉบับ): เอกสารโจทย์ ToC Assignment ระบุให้เก็บทั้ง
"ตัวแรก" และ "ตัวสุดท้าย" ของ username ไว้ (ไม่ใช่เก็บแค่ตัวแรกตัวเดียว
ตามที่ร่างเทสต์เดิมเขียนไว้) ตัวอย่างจากเอกสารโจทย์โดยตรง:

    somchai.d@company.com  ->  s*******d@company.com

ไฟล์นี้แก้ค่าคาดหวัง (expected) ให้ตรงกับสเปกจริงจากเอกสารโจทย์ และลบ
``pytestmark = xfail`` ออกแล้ว เพราะกฎ email เขียนเสร็จแล้ว
"""
from __future__ import annotations

import pytest

from masking.engine import mask_text


class TestMustMatch:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            # ตัวอย่างตรงจากเอกสารโจทย์ ToC Assignment
            ("somchai.d@company.com", "s*******d@company.com"),
            # username ไม่มีจุดก็ต้องทำงานเหมือนกัน (เก็บตัวแรก-ตัวท้าย)
            ("somchai@example.com", "s*****i@example.com"),
            ("john.doe@mail.co.th", "j******e@mail.co.th"),
        ],
    )
    def test_username_masked_domain_kept(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_star_count_equals_username_length_minus_two(self):
        # เก็บตัวแรก + ตัวสุดท้ายไว้ 2 ตัว ที่เหลือปิดเป็น * ทั้งหมด
        out = mask_text("abcdefgh@x.com").masked
        assert out.count("*") == len("abcdefgh") - 2

    def test_multiple_emails_in_one_line(self):
        result = mask_text("ติดต่อ a.one@x.com หรือ b.two@y.com")
        assert result.summary == {"email": 2}


class TestEdgeCases:
    def test_single_char_username_unchanged(self):
        # username ยาว 1 ตัว: ตัวแรก/ตัวสุดท้ายคือตัวเดียวกัน ไม่มีตรงกลางให้ปิด
        assert mask_text("a@x.com").masked == "a@x.com"

    def test_two_char_username_unchanged(self):
        # username ยาว 2 ตัว: ตัวแรกกับตัวสุดท้ายชนกันพอดี ไม่มีตรงกลางให้ปิด
        assert mask_text("ab@x.com").masked == "ab@x.com"

    def test_multi_level_domain_kept_intact(self):
        # โดเมนหลายระดับ (เช่น .co.th) ต้องเปิดเผยทั้งหมด ไม่โดนตัดกลางคัน
        assert mask_text("prasit_k@dept.uni.ac.th").masked == "p******k@dept.uni.ac.th"


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "@somchai กล่าวว่า",     # mention ไม่ใช่อีเมล (ไม่มี username นำหน้า @)
            "ราคา 100@ชิ้น",          # @ ที่ไม่ใช่อีเมล (โดเมนไม่ใช่รูปแบบโดเมนจริง)
            "user@",                  # ไม่มีโดเมน
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw
