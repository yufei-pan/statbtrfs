import pytest

import statbtrfs
from fakes import (
    MOUNT_LINES_MULTI,
    MOUNT_LINES_SINGLE,
    SCRUB_FINISHED_OK,
    SHOW_SINGLE,
    STATS_ZERO,
    CommandMap,
    install_command_map,
)


def _status_map_for_mounts(mount_lines, mounts_show_stats_scrub):
    """Build CommandMap for mount + per-mount show/stats/scrub triples."""
    mapping = {("mount", "-t", "btrfs"): mount_lines}
    # execute_commands looks up each subcommand individually via _lookup
    for mount, (show, stats, scrub) in mounts_show_stats_scrub.items():
        mapping[("btrfs", "filesystem", "show", mount)] = show
        mapping[("btrfs", "device", "stats", mount)] = stats
        mapping[("btrfs", "scrub", "status", mount)] = scrub
    return CommandMap(mapping=mapping)


def test_main_no_mounts_message(monkeypatch, capsys):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    assert "No Btrfs mounts found." in capsys.readouterr().out


def test_main_status_prints_table_once(monkeypatch, capsys):
    cm = _status_map_for_mounts(
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


def test_main_version(monkeypatch):
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-V"])
    with pytest.raises(SystemExit) as ei:
        statbtrfs.main()
    assert ei.value.code == 0


def test_main_exclude_recent_prints_skip(monkeypatch, capsys):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 24 * 3600)

    mapping = {
        ("mount", "-t", "btrfs"): MOUNT_LINES_SINGLE,
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
