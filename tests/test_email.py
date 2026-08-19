"""เทสต์กฎ: อีเมล   [ผู้รับผิดชอบ: คนที่ 3 / Regex B]

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
            ("somchai@example.com", "s*******@example.com"),
            ("ab@x.com", "a*@x.com"),
            ("john.doe@mail.co.th", "j*******@mail.co.th"),
        ],
    )
    def test_username_masked_domain_kept(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_star_count_equals_username_length_minus_one(self):
        out = mask_text("abcdefgh@x.com").masked
        assert out.count("*") == len("abcdefgh") - 1

    def test_multiple_emails_in_one_line(self):
        result = mask_text("ติดต่อ a.one@x.com หรือ b.two@y.com")
        assert result.summary == {"email": 2}


class TestEdgeCases:
    def test_single_char_username(self):
        """TODO(คนที่ 3): ตกลงกันว่าจะได้ 'a@x.com' หรือ '*@x.com' แล้วแก้เทสต์นี้"""
        assert mask_text("a@x.com").masked == "a@x.com"


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "@somchai กล่าวว่า",     # mention ไม่ใช่อีเมล
            "ราคา 100@ชิ้น",          # @ ที่ไม่ใช่อีเมล
            "user@",                  # ไม่มีโดเมน
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw
