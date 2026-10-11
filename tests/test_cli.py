import pytest

import statbtrfs
from fakes import (
    MOUNT_LINES_MULTI,
    MOUNT_LINES_SINGLE,
    SCRUB_FINISHED_OK,
    SHOW_DEGRADED,
    SHOW_MULTI_DEVICE,
    SHOW_SINGLE,
    STATS_MULTI_DEVICE,
    STATS_ZERO,
    SUBVOL_MOUNT_LINES,
    SUBVOL_SHOWS,
    CommandMap,
    install_command_map,
    install_mounts,
)


def _status_map_for_mounts(monkeypatch, mount_lines, mounts_show_stats_scrub):
    """Install mount lines and build a CommandMap of per-mount show/stats/scrub triples."""
    install_mounts(monkeypatch, statbtrfs, mount_lines)
    mapping = {}
    # execute_commands looks up each subcommand individually via _lookup
    for mount, (show, stats, scrub) in mounts_show_stats_scrub.items():
        mapping[("btrfs", "filesystem", "show", mount)] = show
        mapping[("btrfs", "device", "stats", mount)] = stats
        mapping[("btrfs", "scrub", "status", mount)] = scrub
    return CommandMap(mapping=mapping)


def test_main_no_mounts_message(monkeypatch, capsys):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    install_mounts(monkeypatch, statbtrfs, [])
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    assert "No Btrfs mounts found." in capsys.readouterr().out


def test_main_status_prints_table_once(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        monkeypatch,
        MOUNT_LINES_SINGLE,
        {"/mnt/a": (SHOW_SINGLE, STATS_ZERO, SCRUB_FINISHED_OK)},
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    sleeps = []
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: sleeps.append(s))
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "TABLE" in out
    assert sleeps == []  # no -s => single pass, no sleep


def test_main_pattern_filters_mounts(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        monkeypatch,
        MOUNT_LINES_MULTI,
        {
            "/data": (SHOW_SINGLE, STATS_ZERO, SCRUB_FINISHED_OK),
        },
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: f"ROWS={len(rows)}")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "data"])
    statbtrfs.main()
    assert "ROWS=1" in capsys.readouterr().out


def test_main_table_shows_errors_from_every_device(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        monkeypatch,
        MOUNT_LINES_SINGLE,
        {"/mnt/a": (SHOW_MULTI_DEVICE, STATS_MULTI_DEVICE, SCRUB_FINISHED_OK)},
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    captured = {}

    def fake_table(rows, header=None):
        captured["rows"], captured["header"] = rows, header
        return "TABLE"

    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", fake_table)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    (row,) = captured["rows"]
    cells = dict(zip(captured["header"], row))
    assert cells["w_err"] == statbtrfs.color_error_count(7)
    assert cells["r_err"] == statbtrfs.color_error_count(1)
    assert cells["f_err"] == statbtrfs.color_error_count(2)
    assert cells["bit_rot"] == statbtrfs.color_error_count(42)
    assert cells["gen_err"] == statbtrfs.color_error_count(0)


def test_main_table_flags_degraded_filesystem(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        monkeypatch,
        MOUNT_LINES_SINGLE,
        {"/mnt/a": (SHOW_DEGRADED, STATS_ZERO, SCRUB_FINISHED_OK)},
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    captured = {}

    def fake_table(rows, header=None):
        captured["rows"], captured["header"] = rows, header
        return "TABLE"

    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", fake_table)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    (row,) = captured["rows"]
    cells = dict(zip(captured["header"], row))
    assert cells["Path"] == statbtrfs.format_device_path("/dev/nvme0n1", 1)


def _subvol_status_map(monkeypatch):
    return _status_map_for_mounts(
        monkeypatch,
        SUBVOL_MOUNT_LINES,
        {m: (show, STATS_ZERO, SCRUB_FINISHED_OK) for m, show in SUBVOL_SHOWS.items()},
    )


def test_main_lists_each_filesystem_once(monkeypatch):
    install_command_map(monkeypatch, _subvol_status_map(monkeypatch), statbtrfs)
    captured = {}

    def fake_table(rows, header=None):
        captured["rows"], captured["header"] = rows, header
        return "TABLE"

    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", fake_table)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    mounts = [dict(zip(captured["header"], row))["Mount"] for row in captured["rows"]]
    assert mounts == ["/, /home, /var/log", "/mnt/pool"]


def test_main_scrub_starts_once_per_filesystem(monkeypatch):
    cm = install_command_map(monkeypatch, _subvol_status_map(monkeypatch), statbtrfs)
    clock = {"now": 1_000_000.0}
    monkeypatch.setattr(statbtrfs.time, "time", lambda: clock["now"])
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: clock.__setitem__("now", clock["now"] + s))
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-s", "--scrub_command_lockout", "0", "-i", "1"])
    statbtrfs.main()
    starts = [c[1][3] for c in cm.calls if c[0] == "cmd" and c[1][:3] == ["btrfs", "scrub", "start"]]
    assert starts == ["/", "/mnt/pool"]


def test_main_version(monkeypatch):
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-V"])
    with pytest.raises(SystemExit) as ei:
        statbtrfs.main()
    assert ei.value.code == 0


def test_main_exclude_recent_prints_skip(monkeypatch, capsys):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 24 * 3600)

    install_mounts(monkeypatch, statbtrfs, MOUNT_LINES_SINGLE)
    mapping = {
        ("btrfs", "scrub", "status", "/mnt/a"): list(SCRUB_FINISHED_OK),
    }
    cm = CommandMap(mapping=mapping, default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-d", "7"])
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "Skipping mounts scrubbed within the last 7d" in out
    assert "/mnt/a" in out
    assert "No Btrfs mounts found." in out
