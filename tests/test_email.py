from __future__ import annotations

import pytest

from masking.engine import mask_text


class TestMustMatch:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("somchai.d@company.com", "s*******d@company.com"),
            ("somchai@example.com", "s*****i@example.com"),
            ("john.doe@mail.co.th", "j******e@mail.co.th"),
        ],
    )
    def test_username_masked_domain_kept(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_star_count_equals_username_length_minus_two(self):
        out = mask_text("abcdefgh@x.com").masked
        assert out.count("*") == len("abcdefgh") - 2

    def test_multiple_emails_in_one_line(self):
        result = mask_text("ติดต่อ a.one@x.com หรือ b.two@y.com")
        assert result.summary == {"email": 2}


class TestEdgeCases:
    def test_single_char_username_unchanged(self):
        assert mask_text("a@x.com").masked == "a@x.com"

    def test_two_char_username_unchanged(self):
        assert mask_text("ab@x.com").masked == "ab@x.com"

    def test_multi_level_domain_kept_intact(self):
        assert mask_text("prasit_k@dept.uni.ac.th").masked == "p******k@dept.uni.ac.th"


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "@somchai กล่าวว่า",
            "ราคา 100@ชิ้น",
            "user@",
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw
