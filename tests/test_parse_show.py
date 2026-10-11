import statbtrfs
from fakes import (
    SHOW_DEGRADED,
    SHOW_DEGRADED_MARKED,
    SHOW_INCOMPLETE,
    SHOW_MULTI_DEVICE,
    SHOW_SINGLE,
    SHOW_TRICKY_LABEL,
)


def test_parse_show_single_device():
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_SINGLE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "12.34GiB"
    assert device_path == "/dev/sda1"
    assert missing == 0


def test_parse_show_multi_device_paths_joined():
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_MULTI_DEVICE)
    assert uuid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert fs_used == "1.00GiB"
    assert device_path == "/dev/nvme0n1, /dev/nvme1n1"
    assert missing == 0


def test_parse_show_incomplete_returns_nones(capsys):
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_INCOMPLETE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "1.00GiB"
    assert device_path is None
    out = capsys.readouterr().out
    assert "Could not parse btrfs show info" in out


def test_parse_show_ignores_keywords_inside_label():
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_TRICKY_LABEL)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "12.34GiB"
    assert device_path == "/dev/sda1"


def test_parse_show_totals_line_without_bytes_used_does_not_crash(capsys):
    show = [
        "Label: none  uuid: 11111111-2222-3333-4444-555555555555",
        "\tTotal devices 1",
        "\tdevid    1 size 100.00GiB used 50.00GiB path /dev/sda1",
    ]
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(show)
    assert fs_used is None
    assert "Could not parse btrfs show info" in capsys.readouterr().out


def test_parse_show_counts_devices_missing_from_listing():
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_DEGRADED)
    assert device_path == "/dev/nvme0n1"
    assert missing == 1


def test_parse_show_counts_devices_marked_missing():
    uuid, fs_used, device_path, missing = statbtrfs.parse_show_info(SHOW_DEGRADED_MARKED)
    assert device_path == "/dev/nvme0n1"
    assert missing == 1


def test_format_device_path_flags_missing_in_red():
    assert statbtrfs.format_device_path("/dev/sda", 0) == "/dev/sda"
    cell = statbtrfs.format_device_path("/dev/sda", 2)
    assert cell.startswith("/dev/sda, ")
    assert f"{statbtrfs.RED}2 missing{statbtrfs.RESET}" in cell
