
from __future__ import annotations

import pytest

from masking.engine import mask_text


class TestMustMatch:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("DOB:25/12/2549", "DOB:XX/XX/25XX"),
            ("DOB:01/01/2540", "DOB:XX/XX/25XX"),
            ("DOB:31/12/2568", "DOB:XX/XX/25XX"),
        ],
    )
    def test_prefix_is_kept_year_prefix_revealed(self, raw, expected):
        assert mask_text(raw).masked == expected

    def test_case_insensitive_prefix(self):
        assert mask_text("dob:25/12/2549").masked == "dob:XX/XX/25XX"

    def test_optional_space_after_colon(self):
        assert mask_text("DOB: 25/12/2549").masked == "DOB: XX/XX/25XX"

    def test_embedded_in_log_line(self):
        raw = "user_id=42 DOB:25/12/2549 status=active"
        assert mask_text(raw).masked == "user_id=42 DOB:XX/XX/25XX status=active"


class TestValidation:
    @pytest.mark.parametrize(
        "raw",
        [
            "DOB:30/02/2549",  
            "DOB:31/04/2549",  
            "DOB:29/02/2550",  
        ],
    )
    def test_invalid_day_for_month_not_masked(self, raw):
        assert mask_text(raw).masked == raw

    def test_leap_year_feb_29_is_valid(self):
        assert mask_text("DOB:29/02/2551").masked == "DOB:XX/XX/25XX"


class TestMustNotMatch:
    @pytest.mark.parametrize(
        "raw",
        [
            "25/12/2549",                                 
            "2024-08-15 10:22:01 INFO ระบบเริ่มทำงาน",    
            "หมดอายุ 25/12/2570",                          
            "DOB:2549-12-25",                              
            "DOB:5/8/2549",                              
        ],
    )
    def test_not_masked(self, raw):
        assert mask_text(raw).masked == raw
