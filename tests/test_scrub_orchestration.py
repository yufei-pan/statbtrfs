import pytest

import statbtrfs
from fakes import (
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_RUNNING,
    SHOW_SINGLE,
    STATS_ZERO,
    CommandMap,
    install_command_map,
)


def test_issue_scrub_command_yields_cumulative_and_starts(monkeypatch):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    mounts = ["/mnt/a", "/mnt/b"]
    gen = statbtrfs.issue_scrub_command(mounts)
    assert next(gen) == ["/mnt/a"]
    assert next(gen) == ["/mnt/a", "/mnt/b"]
    starts = [c for c in cm.calls if c[0] == "cmd" and c[1][:3] == ["btrfs", "scrub", "start"]]
    assert [c[1][3] for c in starts] == ["/mnt/a", "/mnt/b"]
    assert all(c[2] is False for c in starts)  # wait=False


def test_main_scrub_first_wave_respects_max_count(monkeypatch, capsys):
    mounts = ["/mnt/a", "/mnt/b", "/data"]
    # mount output order is not set order; provide all three lines
    mount_lines = [
        "/dev/sda1 on /mnt/a type btrfs (rw)",
        "/dev/sdb1 on /mnt/b type btrfs (rw)",
        "/dev/sdc1 on /data type btrfs (rw)",
    ]

    state = {"polls": 0}
    clock = {"now": 1_000_000.0}
    started_at_first_sleep = []

    def fake_time():
        return clock["now"]

    def fake_sleep(seconds):
        # First sleep is right after the initial wave (before any later next(scrubber)).
        if not started_at_first_sleep:
            started_at_first_sleep.append(len(started))
        clock["now"] += seconds

    def lookup(command, wait=True):
        cmd = tuple(command)
        if cmd[:3] == ("mount", "-t", "btrfs"):
            return mount_lines
        if cmd[:3] == ("btrfs", "scrub", "start"):
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return list(SHOW_SINGLE)
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        if cmd[:3] == ("btrfs", "scrub", "status"):
            state["polls"] += 1
            # First table poll(s): still running so loop continues; then finished
            if state["polls"] <= len(mounts):
                return list(SCRUB_RUNNING)
            return list(SCRUB_FINISHED_OK)
        return []

    started = []

    def execute_command(command, wait=True):
        if tuple(command)[:3] == ("btrfs", "scrub", "start"):
            started.append(command[3])
        return lookup(command, wait=wait)

    def execute_commands(commands, wait=True):
        return [lookup(c, wait=wait) for c in commands]

    monkeypatch.setattr(statbtrfs, "execute_command", execute_command)
    monkeypatch.setattr(statbtrfs, "execute_commands", execute_commands)
    monkeypatch.setattr(statbtrfs.time, "time", fake_time)
    monkeypatch.setattr(statbtrfs.time, "sleep", fake_sleep)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(
        statbtrfs.sys,
        "argv",
        ["statbtrfs", "-s", "-m", "2", "--scrub_command_lockout", "1", "-i", "1"],
    )

    # Force deterministic iteration order for the set of mounts by patching find_btrfs_mounts
    monkeypatch.setattr(statbtrfs, "find_btrfs_mounts", lambda patterns: set(mounts))
    # And make issue_scrub_command iterate a stable list:
    real_issue = statbtrfs.issue_scrub_command

    def stable_issue(ms):
        return real_issue(sorted(ms))

    monkeypatch.setattr(statbtrfs, "issue_scrub_command", stable_issue)

    statbtrfs.main()
    out = capsys.readouterr().out
    assert "All Scrubs finished." in out
    # Concurrency cap: only 2 starts before first sleep (lockout not yet used for wave 2)
    assert started_at_first_sleep == [2]
    # First wave size 2; later wave should start the remaining mount
    assert len(started) == 3
    assert started[:2] == sorted(mounts)[:2]
    assert started[2] == sorted(mounts)[2]


def test_main_scrub_exclude_recent_never_starts_skipped(monkeypatch, capsys):
    # /mnt/new finished recently -> skipped by -d 7
    # /mnt/old never scrubbed -> kept and started
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    clock = {"now": scrub_epoch + 24 * 3600}

    monkeypatch.setattr(statbtrfs.time, "time", lambda: clock["now"])

    def sleep_and_advance(s):
        clock["now"] += max(s, 1)

    monkeypatch.setattr(statbtrfs.time, "sleep", sleep_and_advance)

    started = []

    def execute_command(command, wait=True):
        cmd = tuple(command)
        if cmd[:3] == ("mount", "-t", "btrfs"):
            return [
                "/dev/sda1 on /mnt/old type btrfs (rw)",
                "/dev/sdb1 on /mnt/new type btrfs (rw)",
            ]
        if cmd[:3] == ("btrfs", "scrub", "status"):
            mount = cmd[3]
            if mount == "/mnt/new":
                return list(SCRUB_FINISHED_OK)
            return list(SCRUB_NEVER)
        if cmd[:3] == ("btrfs", "scrub", "start"):
            started.append(cmd[3])
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return list(SHOW_SINGLE)
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        return []

    def execute_commands(commands, wait=True):
        return [execute_command(c, wait=wait) for c in commands]

    monkeypatch.setattr(statbtrfs, "execute_command", execute_command)
    monkeypatch.setattr(statbtrfs, "execute_commands", execute_commands)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(
        statbtrfs.sys,
        "argv",
        ["statbtrfs", "-s", "-d", "7", "-m", "8", "--scrub_command_lockout", "1", "-i", "1"],
    )

    # Import SCRUB_NEVER at module top with the other fakes.
    statbtrfs.main()
    assert started == ["/mnt/old"]
    assert "/mnt/new" not in started
    assert "Skipping mounts scrubbed within the last 7d" in capsys.readouterr().out
