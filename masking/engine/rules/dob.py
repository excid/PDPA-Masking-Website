
from __future__ import annotations

import calendar
import re

from ..base import RegexRule

_DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class DobRule(RegexRule):
    name = "dob"
    label = "วันเดือนปีเกิด"
    description = "วันเกิดรูปแบบ DOB: DD/MM/พ.ศ. ปิดวัน เดือน และ 2 หลักท้ายของปี"
    priority = 40

    pattern = re.compile(
        r"""
        \bDOB\s*:\s*
        (?P<target>
            (?P<day>0[1-9]|[12][0-9]|3[01])   
            /
            (?P<month>0[1-9]|1[0-2])          
            /
            (?P<year>\d{4})                   
        )
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def mask(self, match: re.Match[str]) -> str:
        year = match.group("year")
        return f"XX/XX/{year[:2]}XX"

    def is_valid(self, match: re.Match[str]) -> bool:
        day = int(match.group("day"))
        month = int(match.group("month"))
        year_be = int(match.group("year"))

        days_in_month = _DAYS_IN_MONTH[month - 1]
        if month == 2 and calendar.isleap(year_be - 543):
            days_in_month = 29
        return day <= days_in_month


__all__ = ["DobRule"]
