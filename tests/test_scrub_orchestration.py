"""-s orchestration (#7): starting scrubs, -m / lockout, failures, summary and Ctrl-C."""
import os
import signal
import sys
import time

import pytest

import statbtrfs
from fakes import FakeBtrfs

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


def test_run_detached_prefixes_sudo_in_per_command_mode(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = []
    monkeypatch.setattr(statbtrfs.subprocess, "call", lambda cmd, **kw: seen.append((cmd, kw)) or 0)
    run_detached(["btrfs", "scrub", "start", "/mnt/a"])
    assert seen[0][0] == ["sudo", "btrfs", "scrub", "start", "/mnt/a"]
    assert seen[0][1]["start_new_session"] is True


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
    assert statbtrfs.describe_scrub(statbtrfs.parse_scrub_status([])) == "Never"


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
