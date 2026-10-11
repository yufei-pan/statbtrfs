import pytest

import statbtrfs
from fakes import (
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_RUNNING,
    SHOW_SINGLE,
    STATS_ZERO,
    CommandMap,
    make_show,
    uuid_for,
    install_command_map,
    install_mounts,
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

    # lockout=2 + interval=1 → ≥1 status poll with room under max before lockout elapses
    lockout = 2
    interval = 1
    clock = {"now": 1_000_000.0}
    mount_status = {}  # only started mounts appear; unstarted → Never
    started = []
    start_clocks = []
    sleep_snapshots = []  # (now, len(started)) taken at each sleep entry
    state = {"status_in_round": 0, "round": 0}

    def fake_time():
        return clock["now"]

    def fake_sleep(seconds):
        sleep_snapshots.append((clock["now"], len(started)))
        clock["now"] += seconds

    def lookup(command, wait=True):
        cmd = tuple(command)
        if cmd[:3] == ("btrfs", "scrub", "start"):
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return make_show(uuid_for(sum(map(ord, cmd[3]))))
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        if cmd[:3] == ("btrfs", "scrub", "status"):
            mount = cmd[3]
            # Start of each table round (one status call per mount)
            if state["status_in_round"] == 0:
                state["round"] += 1
                if state["round"] == 1 and started:
                    # Free a slot under -m while one scrub still running (lockout must still block)
                    mount_status[started[0]] = "finished"
                if len(started) == 3:
                    # After wave-2 start, finish everyone so the exit path can fire
                    for m in list(mount_status):
                        mount_status[m] = "finished"
            state["status_in_round"] = (state["status_in_round"] + 1) % len(mounts)

            status = mount_status.get(mount)
            if status == "running":
                return list(SCRUB_RUNNING)
            if status == "finished":
                return list(SCRUB_FINISHED_OK)
            return list(SCRUB_NEVER)
        return []

    def execute_command(command, wait=True):
        if tuple(command)[:3] == ("btrfs", "scrub", "start"):
            mount = command[3]
            started.append(mount)
            start_clocks.append(clock["now"])
            mount_status[mount] = "running"
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
        [
            "statbtrfs",
            "-s",
            "-m",
            "2",
            "--scrub_command_lockout",
            str(lockout),
            "-i",
            str(interval),
        ],
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

    wave_start = start_clocks[0]
    assert start_clocks[0] == start_clocks[1]
    assert started[:2] == sorted(mounts)[:2]
    assert started[2] == sorted(mounts)[2]

    # First sleep is immediately after wave 1 — concurrency cap holds
    assert sleep_snapshots[0] == (wave_start, 2)

    # Mid-loop: room under max (one finished, one running) but lockout not elapsed → still 2 starts
    pre_third_after_poll = [
        (now, n) for now, n in sleep_snapshots[1:] if n == 2
    ]
    assert pre_third_after_poll, "expected ≥1 poll sleep with room under -m before wave 2"
    assert all(n == 2 for _, n in pre_third_after_poll)
    assert all(now - wave_start <= lockout for now, _ in pre_third_after_poll)

    # Third start only after lockout gate (not merely "eventually 3")
    assert len(started) == 3
    assert start_clocks[2] - wave_start > lockout


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
        if cmd[:3] == ("btrfs", "scrub", "status"):
            mount = cmd[3]
            if mount == "/mnt/new":
                return list(SCRUB_FINISHED_OK)
            return list(SCRUB_NEVER)
        if cmd[:3] == ("btrfs", "scrub", "start"):
            started.append(cmd[3])
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return make_show(uuid_for(sum(map(ord, cmd[3]))))
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        return []

    def execute_commands(commands, wait=True):
        return [execute_command(c, wait=wait) for c in commands]

    install_mounts(monkeypatch, statbtrfs, [
        "/dev/sda1 /mnt/old btrfs rw 0 0",
        "/dev/sdb1 /mnt/new btrfs rw 0 0",
    ])
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
