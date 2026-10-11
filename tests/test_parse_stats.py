import statbtrfs
from fakes import STATS_MULTI_DEVICE, STATS_NONZERO, STATS_ZERO


def test_parse_device_stats_zero():
    d = statbtrfs.parse_device_stats(STATS_ZERO)
    assert d["write_io_errs"] == 0
    assert d["read_io_errs"] == 0
    assert d["flush_io_errs"] == 0
    assert d["corruption_errs"] == 0
    assert d["generation_errs"] == 0


def test_parse_device_stats_skips_malformed_and_reads_nonzero():
    d = statbtrfs.parse_device_stats(STATS_NONZERO)
    assert d["read_io_errs"] == 3
    assert d["corruption_errs"] == 12
    assert d["generation_errs"] == 1
    assert "not-a-stat-line" not in d


def test_parse_device_stats_sums_across_devices():
    d = statbtrfs.parse_device_stats(STATS_MULTI_DEVICE)
    assert d == {
        "write_io_errs": 7,
        "read_io_errs": 1,
        "flush_io_errs": 2,
        "corruption_errs": 42,
        "generation_errs": 0,
    }


def test_parse_device_stats_skips_non_numeric_values():
    d = statbtrfs.parse_device_stats([
        "[/dev/sda1].write_io_errs    n/a",
        "[/dev/sdb1].write_io_errs    5",
    ])
    assert d == {"write_io_errs": 5}


def test_parse_device_stats_empty():
    assert statbtrfs.parse_device_stats([]) == {}
