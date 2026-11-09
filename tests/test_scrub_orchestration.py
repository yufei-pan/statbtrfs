"""-s orchestration (#7): starting scrubs, -m / lockout, failures, summary and Ctrl-C."""
import os
import signal
import sys
import time

import pytest

import statbtrfs
from fakes import (
    SCRUB_ABORTED,
    SCRUB_FAILED_LOCKED,
    SCRUB_FAILED_LOCKED_WARNING,
    SCRUB_FAILED_READ,
    SCRUB_FAILED_READ_MODERN,
    SCRUB_NEVER,
    SCRUB_OLD_ABORTED,
    SCRUB_OLD_INTERRUPTED,
    SCRUB_OLD_RUNNING,
    SCRUB_RUNNING,
    SCRUB_FINISHED_OK,
    STATS_ZERO,
    FakeBtrfs,
    install_status,
    make_show,
    uuid_for,
)

# The unguarded function (conftest wraps statbtrfs.run_detached to block real btrfs commands).
run_detached = statbtrfs.run_detached


def _run(monkeypatch, argv):
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"] + argv)
    return statbtrfs.main()


# --- run_detached / start_scrub -------------------------------------------------

def test_run_detached_does_not_wait_for_background_children(monkeypatch):
    # Like `btrfs scrub start`: the command exits, a forked child keeps its stdout open.
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    script = (
        "import subprocess, sys\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])\n"
        "print('child', child.pid)\n"
        "sys.exit(3)\n"
    )
    t0 = time.monotonic()
    code, output = run_detached([sys.executable, "-c", script])
    elapsed = time.monotonic() - t0
    os.kill(int(output.split()[1]), signal.SIGKILL)
    assert code == 3
    assert output.startswith("child ")
    assert elapsed < 10


def test_run_detached_uses_a_new_session(monkeypatch):
    # Keeps the terminal's Ctrl-C (SIGINT cancels a btrfs scrub) and hangup away from it.
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    code, output = run_detached([sys.executable, "-c", "import os; print(os.getsid(0))"])
    assert code == 0
    assert int(output) != os.getsid(0)


def test_run_detached_missing_command(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    code, output = run_detached(["/nonexistent/btrfs"])
    assert code == 127
    assert output


def test_exec_failure_is_a_failed_start_not_a_crash(monkeypatch):
    # fork EAGAIN / ENOMEM, or btrfs removed during a long -s: start_scrub reports a failed start, so the
    # orchestration records it and goes on to the queued scrubs.
    def fail(command, **kw):
        raise OSError(11, "Resource temporarily unavailable")
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    monkeypatch.setattr(statbtrfs, "run_detached", run_detached)
    monkeypatch.setattr(statbtrfs.subprocess, "call", fail)
    state, message = statbtrfs.start_scrub("/mnt/a")
    assert state == "failed"
    assert "Resource temporarily unavailable" in message


def test_run_detached_prefixes_sudo_in_per_command_mode(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = []
    monkeypatch.setattr(statbtrfs.subprocess, "call", lambda cmd, **kw: seen.append((cmd, kw)) or 0)
    run_detached(["btrfs", "scrub", "start", "/mnt/a"])
    assert seen[0][0] == ["sudo", "btrfs", "scrub", "start", "/mnt/a"]
    assert seen[0][1]["start_new_session"] is True


def _mounted(monkeypatch, read_only):
    """statvfs() of /mnt/... answers as a mount read-only or not; other paths are asked for real."""
    import types
    real = statbtrfs.os.statvfs

    def statvfs(path):
        if str(path).startswith("/mnt/"):
            return types.SimpleNamespace(f_flag=statbtrfs.os.ST_RDONLY if path in read_only else 0)
        return real(path)

    monkeypatch.setattr(statbtrfs.os, "statvfs", statvfs)


def test_start_scrub_is_read_only_on_a_read_only_mount(monkeypatch):
    # A read-write scrub there is aborted at once (4.9.1: "aborted after 00:00:00", 0 bytes); `-r` scrubs it.
    _mounted(monkeypatch, read_only={"/mnt/ro"})
    seen = []
    monkeypatch.setattr(statbtrfs, "run_detached", lambda cmd: seen.append(cmd) or (0, "scrub started"))
    assert statbtrfs.start_scrub("/mnt/ro")[0] == "started"
    assert statbtrfs.start_scrub("/mnt/rw")[0] == "started"
    assert seen == [["btrfs", "scrub", "start", "-r", "/mnt/ro"], ["btrfs", "scrub", "start", "/mnt/rw"]]


def _scrub_one_filesystem(monkeypatch, capsys, read_only):
    """-s on one filesystem mounted at /mnt/a and /mnt/b; the commands `btrfs scrub start` was given."""
    _mounted(monkeypatch, read_only=read_only)
    show = make_show(uuid_for(1))
    install_status(monkeypatch, statbtrfs, {m: (show, STATS_ZERO, SCRUB_FINISHED_OK) for m in ("/mnt/a", "/mnt/b")})
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: None)
    seen = []
    monkeypatch.setattr(statbtrfs, "run_detached", lambda cmd: seen.append(cmd) or (0, "scrub started"))
    _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    return seen, capsys.readouterr().out


def test_scrub_goes_through_the_first_mount_that_is_not_read_only(monkeypatch, capsys):
    # A read-only scrub repairs nothing: with a read-write mount of the filesystem, use that one.
    seen, out = _scrub_one_filesystem(monkeypatch, capsys, read_only={"/mnt/a"})
    assert seen == [["btrfs", "scrub", "start", "/mnt/b"]]
    assert "Started scrub on /mnt/a (through /mnt/b)" in out and "read-only" not in out


def test_scrub_is_read_only_only_when_every_mount_is(monkeypatch, capsys):
    seen, out = _scrub_one_filesystem(monkeypatch, capsys, read_only={"/mnt/a", "/mnt/b"})
    assert seen == [["btrfs", "scrub", "start", "-r", "/mnt/a"]]
    assert "Started read-only scrub (repairs nothing) on /mnt/a\n" in out


def test_the_resume_note_goes_through_the_mount_that_is_not_read_only(monkeypatch, capsys):
    _mounted(monkeypatch, read_only={"/mnt/a"})
    aborted = (make_show(uuid_for(1)), STATS_ZERO, SCRUB_OLD_ABORTED)
    install_status(monkeypatch, statbtrfs, {"/mnt/a": aborted, "/mnt/b": aborted})
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE
    assert "continue it with `btrfs scrub resume /mnt/b`." in capsys.readouterr().out


def test_start_scrub_leaves_a_mount_it_cannot_ask_to_btrfs(monkeypatch):
    def statvfs(path):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(statbtrfs.os, "statvfs", statvfs)
    seen = []
    monkeypatch.setattr(statbtrfs, "run_detached", lambda cmd: seen.append(cmd) or (0, "scrub started"))
    statbtrfs.start_scrub("/mnt/a")
    assert seen == [["btrfs", "scrub", "start", "/mnt/a"]]


def test_the_note_on_a_read_only_mount_resumes_read_only(monkeypatch, capsys):
    # A plain `btrfs scrub resume` aborts there too: the status file keeps no -r for it.
    _mounted(monkeypatch, read_only={"/mnt/a"})
    FakeBtrfs(["/mnt/a", "/mnt/b"], replies={"/mnt/a": [SCRUB_OLD_ABORTED], "/mnt/b": [SCRUB_OLD_ABORTED]}).install(
        monkeypatch, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    assert statbtrfs.main() == statbtrfs.EXIT_FAILURE
    out = capsys.readouterr().out
    assert "The last scrub of /mnt/a did not complete: continue it with `btrfs scrub resume -r /mnt/a`." in out
    assert "The last scrub of /mnt/b did not complete: continue it with `btrfs scrub resume /mnt/b`." in out


@pytest.mark.parametrize(
    "code,output,expected",
    [
        (0, "scrub started on /mnt/a, fsid x (pid=1)", ("started", "scrub started on /mnt/a, fsid x (pid=1)")),
        (1, "ERROR: Scrub is already running.\nTo cancel use 'btrfs scrub cancel /mnt/a'.", "running"),
        (1, "ERROR: scrub already running", "running"),
        (1, "ERROR: cannot access '/mnt/a': Read-only file system\nmore", ("failed", "ERROR: cannot access '/mnt/a': Read-only file system")),
        (1, "", ("failed", "exit code 1")),
    ],
)
def test_start_scrub_classifies_results(monkeypatch, code, output, expected):
    monkeypatch.setattr(statbtrfs, "run_detached", lambda cmd: (code, output))
    state, message = statbtrfs.start_scrub("/mnt/a")
    if isinstance(expected, tuple):
        assert (state, message) == expected
    else:
        assert state == expected


# --- orchestration ---------------------------------------------------------------

def test_first_wave_respects_max_and_refill_waits_for_lockout(monkeypatch, capsys):
    fake = FakeBtrfs(["/mnt/a", "/mnt/b", "/mnt/c"], polls={"/mnt/a": 1, "/mnt/b": 6, "/mnt/c": 2}).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    code = _run(monkeypatch, ["-s", "-m", "2", "--scrub_command_lockout", "2", "-i", "1"])
    assert [m for m, _ in fake.started] == ["/mnt/a", "/mnt/b", "/mnt/c"]
    assert fake.started[0][1] == fake.started[1][1] == t0  # first wave at once, capped at -m
    # /mnt/a finished on the first poll (t0+1), freeing a slot, but the lockout holds /mnt/c back.
    assert fake.started[2][1] - t0 > 2
    assert code == statbtrfs.EXIT_OK
    assert "All scrubs finished." in capsys.readouterr().out


def test_old_progs_scrub_is_followed_until_it_finishes(monkeypatch, capsys):
    # btrfs-progs 4.9.1: "no stats available" for the first seconds, then "running for"; well past the lockout.
    fake = FakeBtrfs(["/mnt/a"], polls=20, stats_delay=3, old_progs=True).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "2"])
    out = capsys.readouterr().out
    assert fake.state["/mnt/a"] == "finished"
    assert "/mnt/a: finished, " in out
    assert code == statbtrfs.EXIT_OK


def test_old_progs_first_seconds_do_not_read_as_finished_with_a_short_lockout(monkeypatch, capsys):
    # "no stats available" for about 5 s of a real scrub, and no lockout to wait it out.
    fake = FakeBtrfs(["/mnt/a"], polls=20, stats_delay=3, old_progs=True).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "2"])
    assert fake.state["/mnt/a"] == "finished"
    assert "/mnt/a: finished, " in capsys.readouterr().out


def test_a_scrub_that_never_reports_does_not_hold_the_run_for_ever(monkeypatch, capsys):
    fake = FakeBtrfs(["/mnt/a"], old_progs=True, start_results={"/mnt/a": ("started", "")}).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "2"])
    assert statbtrfs.SCRUB_HOLD_SECONDS <= fake.clock - t0 <= statbtrfs.SCRUB_HOLD_SECONDS + 4
    assert "/mnt/a: Never" in capsys.readouterr().out
    assert code == statbtrfs.EXIT_OK


FAILED_READS = [SCRUB_FAILED_LOCKED, SCRUB_FAILED_LOCKED_WARNING, SCRUB_FAILED_READ]


@pytest.mark.parametrize("failed", FAILED_READS)
def test_a_failed_status_read_does_not_end_the_run(monkeypatch, capsys, failed):
    # Past the lockout, a second reader has the status file's lock for a poll or two.
    fake = FakeBtrfs(
        ["/mnt/a"], polls=20, old_progs=True,
        replies={"/mnt/a": [None] * 12 + [failed, failed]},
    ).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "1"])
    assert fake.state["/mnt/a"] == "finished"
    assert "/mnt/a: finished, " in capsys.readouterr().out
    assert code == statbtrfs.EXIT_OK


@pytest.mark.parametrize("failed", [SCRUB_FAILED_LOCKED, SCRUB_FAILED_LOCKED_WARNING])
def test_a_failed_status_read_does_not_end_the_run_on_modern_progs(monkeypatch, failed):
    fake = FakeBtrfs(["/mnt/a"], polls=20, replies={"/mnt/a": [None] * 12 + [failed]}).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-i", "1"])
    assert fake.state["/mnt/a"] == "finished"


def test_a_failed_status_read_does_not_free_a_max_slot(monkeypatch):
    fake = FakeBtrfs(
        ["/mnt/a", "/mnt/b"], polls={"/mnt/a": 20, "/mnt/b": 1}, old_progs=True,
        replies={"/mnt/a": [None] * 12 + [SCRUB_FAILED_LOCKED]},
    ).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "0", "-i", "1"])
    assert fake.started[1][1] - t0 >= 19


def test_the_hold_outlasts_a_long_interval(monkeypatch):
    # A reading must hold for the whole hold: the last running reading may be long past.
    fake = FakeBtrfs(
        ["/mnt/a"], polls=6, old_progs=True, replies={"/mnt/a": [None, SCRUB_FAILED_LOCKED]},
    ).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-i", "60"])
    assert fake.state["/mnt/a"] == "finished"


def test_the_hold_does_not_pace_starts(monkeypatch):
    # Filesystems reading Never in the queue hold nothing back: only -m and the lockout pace starts.
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=1, old_progs=True).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "0", "-i", "1"])
    assert fake.started[1][1] - t0 <= 2


@pytest.mark.parametrize("running", [SCRUB_OLD_RUNNING, SCRUB_RUNNING], ids=["old", "modern"])
def test_interrupted_at_the_very_end_of_a_scrub_is_read_past(monkeypatch, capsys, running):
    # For a moment as a scrub ends, btrfs sees it gone from the kernel with no finished record yet.
    fake = FakeBtrfs(
        ["/mnt/a"], polls=14, replies={"/mnt/a": [running] * 12 + [SCRUB_OLD_INTERRUPTED]},
    ).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-i", "1"])
    assert "/mnt/a: finished, " in capsys.readouterr().out


def test_a_really_interrupted_scrub_ends_the_run_after_the_hold(monkeypatch, capsys):
    fake = FakeBtrfs(
        ["/mnt/a"], polls=99, old_progs=True, replies={"/mnt/a": [None] * 12 + [SCRUB_OLD_INTERRUPTED] * 50},
    ).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    _run(monkeypatch, ["-s", "-i", "1"])
    assert 12 + statbtrfs.SCRUB_HOLD_SECONDS <= fake.clock - t0 <= 12 + statbtrfs.SCRUB_HOLD_SECONDS + 3
    assert "/mnt/a: interrupted, " in capsys.readouterr().out


# --- a scrub that did not complete, a status that could not be read ---------------

@pytest.mark.parametrize("old", [False, True], ids=["modern", "old"])
def test_a_cancelled_scrub_is_not_ok_and_does_not_exit_0(monkeypatch, capsys, old):
    # `btrfs scrub cancel` elsewhere, or a read-only mount: aborted.
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=3, old_progs=old).install(monkeypatch, statbtrfs)
    fake.replies["/mnt/a"] = [None] + [SCRUB_OLD_ABORTED if old else SCRUB_ABORTED] * 20
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert "All scrubs finished." not in out
    assert "Scrubs ended; 1 did not complete or could not be read." in out
    assert "/mnt/a: aborted, incomplete" in out
    assert "/mnt/a: finished, OK" not in out and "/mnt/b: finished, OK" in out
    assert "The last scrub of /mnt/a did not complete: continue it with `btrfs scrub resume /mnt/a`." in out
    assert code == statbtrfs.EXIT_FAILURE


def test_a_killed_scrub_is_not_ok_and_does_not_exit_0(monkeypatch, capsys):
    FakeBtrfs(
        ["/mnt/a"], polls=99, old_progs=True, replies={"/mnt/a": [None] * 12 + [SCRUB_OLD_INTERRUPTED] * 50},
    ).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "1"])
    out = capsys.readouterr().out
    assert "/mnt/a: interrupted, incomplete" in out
    assert "All scrubs finished." not in out
    assert code == statbtrfs.EXIT_FAILURE


def test_an_incomplete_scrub_with_errors_exits_1(monkeypatch, capsys):
    from fakes import SCRUB_FINISHED_ERRORS
    aborted = [line.replace("finished", "aborted") for line in SCRUB_FINISHED_ERRORS]
    FakeBtrfs(["/mnt/a"], polls=2, replies={"/mnt/a": [None, aborted]}).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    assert "/mnt/a: aborted, csum=3 uncorrectable=3" in capsys.readouterr().out
    assert code == statbtrfs.EXIT_PROBLEMS


def test_a_run_that_ends_on_a_failed_status_read_exits_2(monkeypatch, capsys):
    # The status file stays locked by another reader past the hold: the run ends, but it can't say the scrub was OK.
    FakeBtrfs(
        ["/mnt/a"], polls=99, replies={"/mnt/a": [None] * 12 + [SCRUB_FAILED_LOCKED] * 50},
    ).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "1"])
    out = capsys.readouterr().out
    assert "/mnt/a: unknown" in out
    assert "Could not read the scrub status of /mnt/a." in out
    assert "All scrubs finished." not in out
    assert code == statbtrfs.EXIT_FAILURE


def test_a_part_way_read_at_the_end_of_a_scrub_does_not_hide_its_errors(monkeypatch, capsys):
    # A `-B` scrub started elsewhere ends while a poll reads its progress: rc 0, a reply like a never-scrubbed one,
    # and the warning on stderr. The run must read on to the finished record, and its errors.
    fake = FakeBtrfs(
        ["/mnt/a"], polls=13, running=["/mnt/a"], errors=["/mnt/a"],
        replies={"/mnt/a": [SCRUB_RUNNING] * 12 + [SCRUB_FAILED_READ_MODERN]},
    ).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "1"])
    assert fake.status_polls == 14
    assert "/mnt/a: was already running; finished, csum=3 uncorrectable=3" in capsys.readouterr().out
    assert code == statbtrfs.EXIT_PROBLEMS


@pytest.mark.parametrize("old", [False, True], ids=["modern", "old"])
def test_ctrl_c_in_a_scrubs_first_seconds_still_names_it(monkeypatch, capsys, old):
    # One poll done, the scrub still without a record: Ctrl-C must not lose it.
    FakeBtrfs(["/mnt/a"], polls=20, stats_delay=5, old_progs=old, interrupt_on_sleep=2).install(monkeypatch, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: False, raising=False)
    assert _run(monkeypatch, ["-s", "-i", "2"]) == statbtrfs.EXIT_INTERRUPTED
    assert "Still running (started by this run): /mnt/a" in capsys.readouterr().out


def test_old_progs_scrub_errors_reach_the_summary_and_exit_code(monkeypatch, capsys):
    FakeBtrfs(["/mnt/a"], polls=8, errors=["/mnt/a"], old_progs=True).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-i", "2"])
    assert "csum=2 uncorrectable=2" in capsys.readouterr().out
    assert code == statbtrfs.EXIT_PROBLEMS


def test_old_progs_max_holds_the_next_scrub_back(monkeypatch):
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls={"/mnt/a": 20, "/mnt/b": 1}, old_progs=True).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "2", "-i", "1"])
    assert fake.started[1][1] - t0 >= 19


def test_max_zero_means_cpu_count(monkeypatch):
    monkeypatch.setattr(statbtrfs.os, "cpu_count", lambda: 1)
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=1).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-m", "0", "--scrub_command_lockout", "0", "-i", "1"])
    assert fake.started[1][1] > fake.started[0][1]


def test_failed_start_is_reported_and_the_rest_continue(monkeypatch, capsys):
    fake = FakeBtrfs(
        ["/mnt/a", "/mnt/b"], polls=1,
        start_results={"/mnt/a": ("failed", "ERROR: Read-only file system")},
    ).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert [m for m, _ in fake.started] == ["/mnt/a", "/mnt/b"]
    assert fake.started[0][1] == fake.started[1][1]  # a failure doesn't use up the slot
    assert "Could not start scrub on /mnt/a: ERROR: Read-only file system" in out
    assert "All scrubs finished." not in out
    assert "/mnt/a: failed to start: ERROR: Read-only file system" in out
    assert code == statbtrfs.EXIT_FAILURE


def test_nothing_started_does_not_claim_success(monkeypatch, capsys):
    FakeBtrfs(["/mnt/a"], start_results={"/mnt/a": ("failed", "boom")}).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "10", "-i", "1"])
    out = capsys.readouterr().out
    assert "All scrubs finished." not in out
    assert code == statbtrfs.EXIT_FAILURE


def test_already_running_scrub_is_adopted_and_counts_toward_max(monkeypatch, capsys):
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=3, running=["/mnt/a"]).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert "already running on /mnt/a" in out
    # /mnt/b waits until the adopted scrub on /mnt/a is no longer running.
    assert fake.started[1][1] > fake.started[0][1] + 1
    assert "/mnt/a: was already running; finished, OK" in out
    assert code == statbtrfs.EXIT_OK


def test_summary_reports_scrub_errors(monkeypatch, capsys):
    FakeBtrfs(["/mnt/a", "/mnt/b"], polls=1, errors=["/mnt/b"]).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert "/mnt/a: finished, OK" in out
    assert "/mnt/b: finished, csum=3 uncorrectable=3" in out
    assert code == statbtrfs.EXIT_PROBLEMS


def test_exclude_recent_never_starts_skipped(monkeypatch, capsys):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    fake = FakeBtrfs(["/mnt/new", "/mnt/old"], polls=1, finished=["/mnt/new"], clock=scrub_epoch + 24 * 3600)
    fake.install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-d", "7", "--scrub_command_lockout", "1", "-i", "1"])
    assert [m for m, _ in fake.started] == ["/mnt/old"]
    assert "Skipping mounts scrubbed within the last 7d: /mnt/new" in capsys.readouterr().out


# --- Ctrl-C -------------------------------------------------------------------------

def _interactive(monkeypatch, answer):
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: True, raising=False)
    monkeypatch.setattr(statbtrfs.sys.stdout, "isatty", lambda: True, raising=False)
    prompts = []
    monkeypatch.setattr("builtins.input", lambda prompt="": prompts.append(prompt) or answer)
    return prompts


def _interrupted_run(monkeypatch):
    # /mnt/c runs elsewhere; /mnt/a and /mnt/b are started by us; /mnt/d is still queued at ^C.
    fake = FakeBtrfs(["/mnt/a", "/mnt/b", "/mnt/c", "/mnt/d"], polls=50, running=["/mnt/c"], interrupt_on_sleep=3)
    fake.install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-m", "3", "--scrub_command_lockout", "0", "-i", "1"])
    return fake, code


def test_ctrl_c_without_terminal_leaves_scrubs_running(monkeypatch, capsys):
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: False, raising=False)
    monkeypatch.setattr("builtins.input", lambda prompt="": pytest.fail("must not prompt without a terminal"))
    fake, code = _interrupted_run(monkeypatch)
    out = capsys.readouterr().out
    assert code == statbtrfs.EXIT_INTERRUPTED == 130
    assert fake.cancelled == []
    assert "Still running (started by this run): /mnt/a, /mnt/b" in out
    assert "Still running (started elsewhere): /mnt/c" in out
    assert "Never started: /mnt/d" in out
    assert "btrfs scrub cancel" in out and "btrfs scrub resume" in out


def test_ctrl_c_on_terminal_asks_and_cancels_only_our_scrubs(monkeypatch, capsys):
    prompts = _interactive(monkeypatch, "y")
    fake, code = _interrupted_run(monkeypatch)
    assert prompts == ["Cancel 2 running scrubs started by this run? [y/N] "]
    assert fake.cancelled == ["/mnt/a", "/mnt/b"]
    assert "Cancelled scrub on /mnt/a" in capsys.readouterr().out
    assert code == statbtrfs.EXIT_INTERRUPTED


def test_ctrl_c_cancel_names_each_resume_read_only_where_mounted_read_only(monkeypatch, capsys):
    _mounted(monkeypatch, read_only={"/mnt/b"})
    _interactive(monkeypatch, "y")
    _interrupted_run(monkeypatch)
    out = capsys.readouterr().out
    assert "Cancelled scrub on /mnt/a: it keeps its progress, continue it with `btrfs scrub resume /mnt/a`." in out
    assert "Cancelled scrub on /mnt/b: it keeps its progress, continue it with `btrfs scrub resume -r /mnt/b`." in out


def test_ctrl_c_cancel_names_the_resume_through_the_mount_that_is_not_read_only(monkeypatch, capsys):
    # One filesystem at /mnt/a (read-only, sorts first) and /mnt/b: the scrub went through /mnt/b, so does the advice.
    _mounted(monkeypatch, read_only={"/mnt/a"})
    _interactive(monkeypatch, "y")
    show = make_show(uuid_for(1))
    install_status(monkeypatch, statbtrfs, {m: (show, STATS_ZERO, SCRUB_RUNNING) for m in ("/mnt/a", "/mnt/b")})
    monkeypatch.setattr(statbtrfs, "run_detached", lambda cmd: (0, "scrub started"))
    sleeps = []

    def sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(statbtrfs.time, "sleep", sleep)
    assert _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"]) == statbtrfs.EXIT_INTERRUPTED
    out = capsys.readouterr().out
    assert "Cancelled scrub on /mnt/a: it keeps its progress, continue it with `btrfs scrub resume /mnt/b`." in out


@pytest.mark.parametrize("answer", ["", "n", "no", "anything"])
def test_ctrl_c_on_terminal_defaults_to_keep_running(monkeypatch, capsys, answer):
    _interactive(monkeypatch, answer)
    fake, code = _interrupted_run(monkeypatch)
    assert fake.cancelled == []
    assert "btrfs scrub cancel" in capsys.readouterr().out


def test_ctrl_c_at_the_prompt_keeps_scrubs_running(monkeypatch):
    _interactive(monkeypatch, None)

    def raise_interrupt(prompt=""):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_interrupt)
    fake, code = _interrupted_run(monkeypatch)
    assert fake.cancelled == []
    assert code == statbtrfs.EXIT_INTERRUPTED


def test_describe_scrub():
    assert statbtrfs.describe_scrub(None) == "status unknown"
    assert statbtrfs.describe_scrub(statbtrfs.parse_scrub_status(SCRUB_NEVER)) == "Never"


def test_scrub_without_stats_yet_still_counts_as_running(monkeypatch, capsys):
    # Real btrfs prints "no stats available" (no Status: line) until the scrub's first progress record.
    fake = FakeBtrfs(["/mnt/a"], polls=4, stats_delay=3).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert fake.status_polls == 5  # 3 without stats + 1 running + 1 finished
    assert "/mnt/a: finished, OK" in out
    assert code == statbtrfs.EXIT_OK


def test_max_respected_while_scrubs_have_no_stats_yet(monkeypatch):
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=4, stats_delay=3).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-s", "-m", "1", "--scrub_command_lockout", "0", "-i", "1"])
    # /mnt/b must wait for /mnt/a to finish, not start while /mnt/a shows "no stats available".
    assert fake.started[1][1] - fake.started[0][1] >= 5
