from datetime import datetime

import statbtrfs
from fakes import (
    SCRUB_FINISHED_ERRORS,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_RUNNING,
    SCRUB_TIME_BASIC,
    SCRUB_TIME_ISO,
)


def test_parse_scrub_never_defaults():
    data = statbtrfs.parse_scrub_status(SCRUB_NEVER)
    assert data["scrub_status"] == "Never"
    assert data["scrub_time"] == "N/A"
    assert data["scrub_rate"] == "N/A"
    assert data["scrubbed_data"] == "N/A"
    assert data["error_summary"] == "N/A"


def test_parse_scrub_empty_defaults():
    data = statbtrfs.parse_scrub_status([])
    assert data["scrub_status"] == "Never"


def test_parse_scrub_finished_ok_uses_total_to_scrub():
    data = statbtrfs.parse_scrub_status(SCRUB_FINISHED_OK)
    assert data["scrub_status"] == "finished"
    assert data["scrub_time"] == "Thu May  2 09:56:55 2024"
    assert data["scrub_rate"] == "17.00MiB/s"
    assert data["scrubbed_data"] == "10.00GiB"
    assert "OK" in data["error_summary"]
    assert statbtrfs.GREEN in data["error_summary"]


def test_parse_scrub_running_uses_bytes_scrubbed():
    data = statbtrfs.parse_scrub_status(SCRUB_RUNNING)
    assert data["scrub_status"] == "running"
    assert data["scrubbed_data"] == "40.00GiB"


def test_parse_scrub_finished_with_errors_is_red():
    data = statbtrfs.parse_scrub_status(SCRUB_FINISHED_ERRORS)
    assert "csum=3" in data["error_summary"]
    assert statbtrfs.RED in data["error_summary"]


def test_parse_scrub_time_formats():
    epoch = statbtrfs.parse_scrub_time_to_epoch(SCRUB_TIME_BASIC)
    assert epoch == datetime.strptime(SCRUB_TIME_BASIC, "%a %b %d %H:%M:%S %Y").timestamp()
    epoch_iso = statbtrfs.parse_scrub_time_to_epoch(SCRUB_TIME_ISO)
    assert epoch_iso == datetime.strptime(SCRUB_TIME_ISO, "%Y-%m-%d %H:%M:%S").timestamp()
    assert statbtrfs.parse_scrub_time_to_epoch("N/A") is None
    assert statbtrfs.parse_scrub_time_to_epoch("not a time") is None


def test_parse_scrub_error_summary_is_one_line_with_nonzero_counts():
    data = statbtrfs.parse_scrub_status(SCRUB_FINISHED_ERRORS)
    assert data["error_summary"] == f"{statbtrfs.RED}csum=3 uncorrectable=3{statbtrfs.RESET}"


def test_parse_scrub_error_summary_multiple_types_and_counts():
    data = statbtrfs.parse_scrub_status([
        "Status:           finished",
        "Error summary:    read=1 csum=2",
        "  Corrected:      3",
        "  Uncorrectable:  0",
        "  Unverified:     0",
    ])
    assert data["error_summary"] == f"{statbtrfs.RED}read=1 csum=2 corrected=3{statbtrfs.RESET}"


def test_parse_scrub_error_summary_stops_at_first_non_count_line():
    data = statbtrfs.parse_scrub_status([
        "Error summary:    csum=1",
        "  Uncorrectable:  1",
        "Something else:   7",
        "  Corrected:      9",
    ])
    assert data["error_summary"] == f"{statbtrfs.RED}csum=1 uncorrectable=1{statbtrfs.RESET}"


def test_parse_scrub_has_errors_flag():
    assert statbtrfs.parse_scrub_status(SCRUB_FINISHED_ERRORS)["has_errors"] is True
    assert statbtrfs.parse_scrub_status(SCRUB_FINISHED_OK)["has_errors"] is False
    assert statbtrfs.parse_scrub_status(SCRUB_NEVER)["has_errors"] is False
