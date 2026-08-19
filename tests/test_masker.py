"""เทสต์ตัว orchestrator   [ผู้รับผิดชอบ: คนที่ 1 / Lead]

เทสต์ในไฟล์นี้ต้อง **ผ่านตั้งแต่ยังเป็น stub** เพราะทดสอบกลไกการรวมผล
ไม่ได้ทดสอบ regex ของใคร
"""
from __future__ import annotations

from masking.engine import Detection, mask_text
from masking.engine.masker import apply_detections, resolve_overlaps
from masking.engine.registry import RULES, rule_names


def det(start, end, masked, rule="x", label="X", original="") -> Detection:
    return Detection(rule=rule, label=label, start=start, end=end, original=original, masked=masked)


class TestEmptyAndPlainText:
    def test_empty_string(self):
        assert mask_text("").masked == ""

    def test_plain_text_unchanged(self):
        text = "ระบบเริ่มทำงานเมื่อ 10:22 น. ไม่มีข้อมูลส่วนบุคคล"
        assert mask_text(text).masked == text

    def test_stub_rules_do_not_change_text(self):
        """ตราบใดที่กฎยังเป็น stub ข้อความต้องออกมาเหมือนเดิม"""
        text = "email: somchai@example.com | tel: 081-234-5678"
        assert mask_text(text).masked == text


class TestReplacement:
    def test_replace_from_end_keeps_indexes_valid(self):
        """แทนที่จากท้ายไปหน้า แม้ความยาวใหม่จะไม่เท่าเดิม"""
        text = "AAA BBB CCC"
        result = apply_detections(text, [det(0, 3, "#"), det(8, 11, "######")])
        assert result == "# BBB ######"

    def test_summary_counts_by_rule(self):
        detections = [
            det(0, 1, "*", rule="email"),
            det(2, 3, "*", rule="email"),
            det(4, 5, "*", rule="phone"),
        ]
        from masking.engine.masker import MaskResult

        result = MaskResult(original="abcde", masked="*b*d*", detections=detections)
        assert result.summary == {"email": 2, "phone": 1}
        assert result.total == 3


class TestOverlapResolution:
    def test_longer_match_wins(self):
        long_one = det(0, 16, "LONG", rule="credit_card")
        short_one = det(6, 16, "SHORT", rule="phone")
        assert resolve_overlaps([short_one, long_one]) == [long_one]

    def test_non_overlapping_kept_and_sorted(self):
        a, b = det(10, 12, "a"), det(0, 4, "b")
        assert resolve_overlaps([a, b]) == [b, a]

    def test_touching_spans_are_not_overlapping(self):
        a, b = det(0, 4, "a"), det(4, 8, "b")
        assert len(resolve_overlaps([a, b])) == 2


class TestRuleToggle:
    def test_enabled_none_means_all_rules(self):
        assert len(rule_names()) == len(RULES) == 5

    def test_disable_all_rules(self):
        text = "somchai@example.com"
        assert mask_text(text, enabled=[]).masked == text

    def test_unknown_rule_name_is_ignored(self):
        assert mask_text("hello", enabled=["ไม่มีกฎนี้"]).masked == "hello"


class TestRuleContract:
    """กันไม่ให้ใครเผลอตั้งชื่อกฎซ้ำ หรือลืมใส่ label"""

    def test_names_are_unique(self):
        assert len(set(rule_names())) == len(RULES)

    def test_every_rule_has_label_and_description(self):
        for rule in RULES:
            assert rule.name and rule.label and rule.description
