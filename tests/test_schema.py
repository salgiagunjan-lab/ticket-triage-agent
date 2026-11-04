"""Tests for the output schema validator."""
import pytest

from triage.schema import validate

VALID = {
    "category": "card_auth_decline",
    "priority": "P3",
    "confidence": 0.9,
    "reasoning": "one sentence",
    "extracted": {
        "http_status": None,
        "endpoint": None,
        "error_code": None,
        "request_id": None,
        "event_ids": [],
    },
    "first_step": "check the card limits",
}


def test_valid_answer_has_no_problems():
    assert validate(VALID) == []


def test_not_a_dict_is_reported():
    assert validate([1]) == ["answer is not a JSON object"]


def test_missing_key_is_reported():
    bad = dict(VALID)
    del bad["reasoning"]
    assert "missing key: reasoning" in validate(bad)


def test_missing_extracted_keys_are_reported():
    problems = validate({**VALID, "extracted": {}})
    for key in ["http_status", "endpoint", "error_code", "request_id", "event_ids"]:
        assert f"missing key in extracted: {key}" in problems


CASES = [
    ({**VALID, "category": "nope"}, "unknown category: 'nope'"),
    ({**VALID, "category": ["x"]}, "category is not a string"),
    ({**VALID, "priority": "x"}, "unknown priority: 'x'"),
    ({**VALID, "priority": 1}, "priority is not a string"),
    ({**VALID, "confidence": "x"}, "confidence is not a number: 'x'"),
    ({**VALID, "confidence": 1.1}, "confidence is not between 0 and 1: 1.1"),
    ({**VALID, "confidence": -0.1}, "confidence is not between 0 and 1: -0.1"),
    ({**VALID, "extracted": "x"}, "extracted is not a JSON object: 'x'"),
    (
        {**VALID, "extracted": {**VALID["extracted"], "event_ids": "evt_1"}},
        "event_ids is not a list: 'evt_1'",
    ),
]


@pytest.mark.parametrize("bad, expected", CASES)
def test_bad_answer_reports_problem(bad, expected):
    assert expected in validate(bad)


def test_non_string_category_and_priority_do_not_crash():
    problems = validate({**VALID, "category": ["x"], "priority": ["P1"]})
    assert "category is not a string" in problems
    assert "priority is not a string" in problems


def test_multiple_problems_are_all_reported():
    bad = {
        **VALID,
        "confidence": 1.5,
        "extracted": {"endpoint": "/foo", "error_code": "E1", "request_id": "r", "event_ids": "1"},
    }
    problems = validate(bad)
    assert "confidence is not between 0 and 1: 1.5" in problems
    assert "missing key in extracted: http_status" in problems
    assert "event_ids is not a list: '1'" in problems