"""Tests for umpyre.storage.query_utils against a temp history folder."""

from datetime import datetime

import pytest

from umpyre.storage import query_utils as q

NAMES = [
    "2025_11_14_22_45_00__700e012__0.1.0.json",
    "2025_11_14_22_50_00__abc1234__0.1.0.json",
    "2025_11_15_08_00_00__def5678__0.2.0.json",
    "2025_11_16_09_30_00__0a1b2c3__none.json",
    "notes.json",  # not a metrics file: must be ignored
]


@pytest.fixture
def history(tmp_path):
    for n in NAMES:
        (tmp_path / n).write_text("{}")
    return tmp_path


def test_parse_metric_filename():
    info = q.parse_metric_filename(NAMES[0])
    assert info["commit_sha"] == "700e012" and info["pypi_version"] == "0.1.0"
    assert info["has_version"] is True
    assert info["timestamp"] == datetime(2025, 11, 14, 22, 45, 0)
    assert info["timestamp_str"] == "2025-11-14T22:45:00"
    none = q.parse_metric_filename(NAMES[3])
    assert none["pypi_version"] is None and none["has_version"] is False


def test_parse_metric_filename_rejects_garbage():
    for bad in ["notes.json", "2025_11_14_22_45_00__700e012.json", "x__y__z.json"]:
        with pytest.raises(ValueError, match="Invalid filename format"):
            q.parse_metric_filename(bad)


def test_find_by_commit_short_and_full_sha(history):
    assert q.find_metrics_by_commit(history, "700e012").name == NAMES[0]
    assert q.find_metrics_by_commit(history, "700e0123456789abcdef").name == NAMES[0]
    assert q.find_metrics_by_commit(history, "ffffff0") is None


def test_find_by_version_latest_first(history):
    found = q.find_metrics_by_version(history, "0.1.0")
    assert [p.name for p in found] == [NAMES[1], NAMES[0]]
    assert q.find_metrics_by_version(history, "9.9.9") == []
    assert q.get_latest_metric_for_version(history, "0.1.0").name == NAMES[1]
    assert q.get_latest_metric_for_version(history, "9.9.9") is None


def test_get_all_versions_skips_none_and_garbage(history):
    assert q.get_all_versions(history) == ["0.1.0", "0.2.0"]


def test_filter_by_date_range(history):
    names = lambda ps: [p.name for p in ps]
    assert names(q.filter_by_date_range(history)) == sorted(NAMES[:4])
    since = q.filter_by_date_range(history, start_date=datetime(2025, 11, 15))
    assert names(since) == [NAMES[2], NAMES[3]]
    until = q.filter_by_date_range(history, end_date=datetime(2025, 11, 14, 22, 45, 0))
    assert names(until) == [NAMES[0]]  # inclusive upper bound
    window = q.filter_by_date_range(
        history, datetime(2025, 11, 14, 22, 50, 0), datetime(2025, 11, 15, 8, 0, 0)
    )
    assert names(window) == [NAMES[1], NAMES[2]]
