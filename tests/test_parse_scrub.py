from datetime import datetime

import pytest

import statbtrfs
from fakes import (
    SCRUB_FAILED_LOCKED,
    SCRUB_FAILED_LOCKED_WARNING,
    SCRUB_FAILED_READ,
    SCRUB_FINISHED_ERRORS,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_OLD_ABORTED,
    SCRUB_OLD_FINISHED_ERRORS,
    SCRUB_OLD_FINISHED_OK,
    SCRUB_OLD_INTERRUPTED,
    SCRUB_OLD_NEVER,
    SCRUB_OLD_RESUMED,
    SCRUB_OLD_RUNNING,
    SCRUB_RESUMED,
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


@pytest.mark.parametrize("reply", [SCRUB_FAILED_LOCKED, SCRUB_FAILED_LOCKED_WARNING])
def test_parse_scrub_failed_read_is_unknown_not_never(reply):
    data = statbtrfs.parse_scrub_status(reply)
    assert data["scrub_status"] == "unknown"
    assert data["no_record"] is True


def test_parse_scrub_failed_part_way_reads_as_no_record():
    assert statbtrfs.parse_scrub_status(SCRUB_FAILED_READ)["no_record"] is True


def test_parse_scrub_no_record_only_where_the_reply_says_nothing():
    assert statbtrfs.parse_scrub_status(SCRUB_OLD_NEVER)["no_record"] is True
    # Modern btrfs-progs show a scrub's first seconds ("Time left:"), so their Never is the plain truth.
    assert statbtrfs.parse_scrub_status(SCRUB_NEVER)["no_record"] is False
    assert statbtrfs.parse_scrub_status(SCRUB_FINISHED_OK)["no_record"] is False
    assert statbtrfs.parse_scrub_status(SCRUB_OLD_FINISHED_OK)["no_record"] is False


def test_parse_scrub_resumed_time_is_read():
    data = statbtrfs.parse_scrub_status(SCRUB_RESUMED)
    assert data["scrub_time"] == "Thu May  2 09:56:55 2024"


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


def test_parse_scrub_running_before_first_progress_record():
    from fakes import SCRUB_JUST_STARTED

    data = statbtrfs.parse_scrub_status(SCRUB_JUST_STARTED)
    assert data["scrub_status"] == "running"
    assert data["scrubbed_data"] == "0.00B  (0.00%)"


def test_parse_scrub_never_real_output():
    from fakes import SCRUB_NEVER_REAL

    data = statbtrfs.parse_scrub_status(SCRUB_NEVER_REAL)
    assert data["scrub_status"] == "Never"
    assert data["has_errors"] is False


# --- btrfs-progs 4.9.1 (EL7): real output ---------------------------------------

@pytest.mark.parametrize("lines, status, time, scrubbed", [
    (SCRUB_OLD_RUNNING, "running", "Sat Nov  7 02:56:56 2026", "1.20GiB"),
    (SCRUB_OLD_FINISHED_OK, "finished", "Sat Nov  7 02:55:51 2026", "5.87GiB"),
    (SCRUB_OLD_ABORTED, "aborted", "Sat Nov  7 02:56:56 2026", "2.95GiB"),
    (SCRUB_OLD_RESUMED, "finished", "Sat Nov  7 02:57:08 2026", "6.37GiB"),
    (SCRUB_OLD_INTERRUPTED, "interrupted", "Sat Nov  7 02:58:27 2026", "1.18GiB"),
])
def test_parse_scrub_old_progs(lines, status, time, scrubbed):
    data = statbtrfs.parse_scrub_status(lines)
    assert data["scrub_status"] == status
    assert data["scrub_time"] == time
    assert data["scrubbed_data"] == scrubbed
    assert data["scrub_rate"] == "N/A"  # 4.9.1 prints no rate
    assert data["error_summary"] == f"{statbtrfs.GREEN}OK{statbtrfs.RESET}"
    assert data["has_errors"] is False


def test_parse_scrub_old_progs_never_keeps_the_defaults():
    data = statbtrfs.parse_scrub_status(SCRUB_OLD_NEVER)
    assert data["scrub_status"] == "Never"
    assert data["scrub_time"] == "N/A"
    assert data["scrubbed_data"] == "N/A"
    assert data["error_summary"] == "N/A"
    assert data["has_errors"] is False


def test_parse_scrub_old_progs_time_is_one_the_day_filter_reads():
    data = statbtrfs.parse_scrub_status(SCRUB_OLD_FINISHED_OK)
    assert statbtrfs.parse_scrub_time_to_epoch(data["scrub_time"]) is not None


def test_parse_scrub_old_progs_errors_read_like_the_modern_ones():
    data = statbtrfs.parse_scrub_status(SCRUB_OLD_FINISHED_ERRORS)
    assert data["scrub_status"] == "finished"
    assert data["scrubbed_data"] == "1.25MiB"
    assert data["error_summary"] == f"{statbtrfs.RED}csum=2 uncorrectable=2{statbtrfs.RESET}"
    assert data["has_errors"] is True
