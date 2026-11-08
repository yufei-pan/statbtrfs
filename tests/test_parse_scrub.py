from datetime import datetime

import pytest

import statbtrfs
from fakes import (
    SCRUB_ABORTED,
    SCRUB_FAILED_LOCKED,
    SCRUB_FAILED_LOCKED_WARNING,
    SCRUB_FAILED_READ,
    SCRUB_FAILED_READ_MODERN,
    SCRUB_FINISHED_ERRORS,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_NEVER_REAL,
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


@pytest.mark.parametrize("reply", [SCRUB_FAILED_READ, SCRUB_FAILED_READ_MODERN], ids=["old", "modern"])
def test_parse_scrub_failed_part_way_is_unknown_not_never(reply):
    # rc 0 and a reply that reads like a filesystem never scrubbed: only the warning on stderr tells.
    data = statbtrfs.parse_scrub_status(reply)
    assert data["scrub_status"] == "unknown"
    assert data["no_record"] is True
    assert data["error_summary"] == "N/A"
    assert data["scrub_rate"] == "N/A"


def test_parse_scrub_no_record_only_where_the_reply_says_nothing():
    assert statbtrfs.parse_scrub_status(SCRUB_OLD_NEVER)["no_record"] is True
    # Modern btrfs-progs show a scrub's first seconds ("Time left:"), so their Never is the plain truth.
    assert statbtrfs.parse_scrub_status(SCRUB_NEVER)["no_record"] is False
    assert statbtrfs.parse_scrub_status(SCRUB_NEVER_REAL)["no_record"] is False
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
        "UUID:             76f821a1-8129-4147-b0f1-436771be839f",
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

OK = "OK"
INCOMPLETE = "incomplete"


# 4.9.1 prints no rate: it is the bytes over the duration, as current btrfs-progs compute it.
@pytest.mark.parametrize("lines, status, time, scrubbed, rate, summary", [
    (SCRUB_OLD_RUNNING, "running", "Sat Nov  7 02:56:56 2026", "1.20GiB", "245.76MiB/s", OK),         # / 5 s
    (SCRUB_OLD_FINISHED_OK, "finished", "Sat Nov  7 02:55:51 2026", "5.87GiB", "2.94GiB/s", OK),      # / 2 s
    (SCRUB_OLD_ABORTED, "aborted", "Sat Nov  7 02:56:56 2026", "2.95GiB", "251.73MiB/s", INCOMPLETE),  # / 12 s
    (SCRUB_OLD_RESUMED, "finished", "Sat Nov  7 02:57:08 2026", "6.37GiB", "250.88MiB/s", OK),        # / 26 s
    (SCRUB_OLD_INTERRUPTED, "interrupted", "Sat Nov  7 02:58:27 2026", "1.18GiB", "241.66MiB/s", INCOMPLETE),
])
def test_parse_scrub_old_progs(lines, status, time, scrubbed, rate, summary):
    data = statbtrfs.parse_scrub_status(lines)
    assert data["scrub_status"] == status
    assert data["scrub_time"] == time
    assert data["scrubbed_data"] == scrubbed
    assert data["scrub_rate"] == rate
    color = statbtrfs.GREEN if summary == OK else statbtrfs.YELLOW
    assert data["error_summary"] == f"{color}{summary}{statbtrfs.RESET}"
    assert data["has_errors"] is False
    assert data["incomplete"] is (summary == INCOMPLETE)


def test_parse_scrub_old_progs_rate_under_a_second_is_not_a_number():
    # "finished after 00:00:00": no rate to tell.
    assert statbtrfs.parse_scrub_status(SCRUB_OLD_FINISHED_ERRORS)["scrub_rate"] == "N/A"


def test_parse_scrub_old_progs_rate_over_a_day():
    data = statbtrfs.parse_scrub_status([
        "scrub status for 7ce03782-1b05-405a-bdf3-01d1cc986790",
        "\tscrub started at Sat Nov  7 02:55:51 2026 and finished after 100:00:00",
        "\ttotal bytes scrubbed: 351.57TiB with 0 errors",
    ])
    assert data["scrub_status"] == "finished"
    assert data["scrub_rate"] == "1.00GiB/s"


@pytest.mark.parametrize("text, expected", [
    ("0.00B", 0), ("512.00B", 512), ("1.00KiB", 1024), ("1.25MiB", 1.25 * 2 ** 20), ("5.87GiB", 5.87 * 2 ** 30),
    ("2.00TiB", 2 * 2 ** 40), ("1.00PiB", 2 ** 50), ("1.00EiB", 2 ** 60), (" 3.50GiB ", 3.5 * 2 ** 30),
])
def test_parse_size(text, expected):
    assert statbtrfs.parse_size(text) == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "N/A", "1.00", "GiB", "1.00 GiB", "1.00GB", "1.00gib", "-1.00GiB", "1.00GiBx"])
def test_parse_size_refuses_what_btrfs_does_not_print(text):
    assert statbtrfs.parse_size(text) is None


@pytest.mark.parametrize("num_bytes, expected", [
    (0, "0.00B"), (1023, "1023.00B"), (1024, "1.00KiB"), (17.0 * 2 ** 20, "17.00MiB"), (2 ** 70, "1024.00EiB"),
])
def test_format_size_as_btrfs_prints_it(num_bytes, expected):
    assert statbtrfs.format_size(num_bytes) == expected


def test_parse_scrub_modern_aborted_is_incomplete_not_ok():
    data = statbtrfs.parse_scrub_status(SCRUB_ABORTED)
    assert data["scrub_status"] == "aborted"
    assert data["incomplete"] is True
    assert data["has_errors"] is False
    assert data["error_summary"] == f"{statbtrfs.YELLOW}incomplete{statbtrfs.RESET}"


def test_parse_scrub_incomplete_with_errors_still_shows_the_errors():
    data = statbtrfs.parse_scrub_status([line.replace("finished", "aborted") for line in SCRUB_FINISHED_ERRORS])
    assert data["incomplete"] is True
    assert data["has_errors"] is True
    assert data["error_summary"] == f"{statbtrfs.RED}csum=3 uncorrectable=3{statbtrfs.RESET}"


def test_parse_scrub_complete_readings_are_not_incomplete():
    for reply in (SCRUB_FINISHED_OK, SCRUB_RUNNING, SCRUB_NEVER_REAL, SCRUB_OLD_NEVER, SCRUB_FAILED_LOCKED):
        assert statbtrfs.parse_scrub_status(reply)["incomplete"] is False


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
