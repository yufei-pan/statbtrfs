import statbtrfs
from fakes import STATS_NONZERO, STATS_ZERO


def test_parse_device_stats_zero():
    d = statbtrfs.parse_device_stats(STATS_ZERO)
    assert d["write_io_errs"] == "0"
    assert d["read_io_errs"] == "0"
    assert d["corruption_errs"] == "0"
    assert d["generation_errs"] == "0"


def test_parse_device_stats_skips_malformed_and_reads_nonzero():
    d = statbtrfs.parse_device_stats(STATS_NONZERO)
    assert d["read_io_errs"] == "3"
    assert d["corruption_errs"] == "12"
    assert d["generation_errs"] == "1"
    assert "not-a-stat-line" not in d


def test_parse_device_stats_empty():
    assert statbtrfs.parse_device_stats([]) == {}
