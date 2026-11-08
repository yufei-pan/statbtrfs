"""-w / --watch (#9): follow scrubs started elsewhere until none is running."""
import pytest

import statbtrfs
from fakes import SCRUB_FAILED_LOCKED, SCRUB_FAILED_READ_MODERN, SCRUB_OLD_INTERRUPTED, FakeBtrfs


def _run(monkeypatch, argv):
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"] + argv)
    return statbtrfs.main()


def test_watch_follows_running_scrubs_until_idle(monkeypatch):
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls={"/mnt/a": 3}, running=["/mnt/a"]).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-w", "-i", "5"])
    assert fake.started == []          # never starts a scrub
    assert fake.status_polls == 4      # running, running, running, finished
    assert fake.sleeps == 3
    assert fake.clock == 1_000_000.0 + 3 * 5
    assert code == statbtrfs.EXIT_OK


def test_watch_follows_an_old_progs_scrub(monkeypatch):
    fake = FakeBtrfs(["/mnt/a"], polls=3, running=["/mnt/a"], old_progs=True).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_OK
    assert fake.status_polls == 4


def test_watch_right_after_a_start_on_old_progs_follows_the_scrub(monkeypatch):
    # `btrfs scrub start /mnt; statbtrfs -w`: 4.9.1 says "no stats available" for about 5 s.
    fake = FakeBtrfs(["/mnt/a"], polls=9, running=["/mnt/a"], stats_delay=0, old_progs=True)
    fake.no_stats_yet["/mnt/a"] = 3
    fake.install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w", "-i", "2"]) == statbtrfs.EXIT_OK
    assert fake.state["/mnt/a"] == "finished"
    assert fake.status_polls == 10


def test_watch_on_an_idle_old_progs_filesystem_ends_after_the_hold(monkeypatch):
    fake = FakeBtrfs(["/mnt/a"], old_progs=True).install(monkeypatch, statbtrfs)
    t0 = fake.clock
    assert _run(monkeypatch, ["-w", "-i", "2"]) == statbtrfs.EXIT_OK
    assert statbtrfs.SCRUB_HOLD_SECONDS <= fake.clock - t0 <= statbtrfs.SCRUB_HOLD_SECONDS + 2


def test_watch_survives_a_failed_status_read(monkeypatch):
    fake = FakeBtrfs(
        ["/mnt/a"], polls=9, running=["/mnt/a"], replies={"/mnt/a": [None, None, SCRUB_FAILED_LOCKED]},
    ).install(monkeypatch, statbtrfs)
    _run(monkeypatch, ["-w"])
    assert fake.state["/mnt/a"] == "finished"


def test_watch_does_not_hold_for_an_interrupted_scrub_of_long_ago(monkeypatch):
    fake = FakeBtrfs(["/mnt/a"], replies={"/mnt/a": [SCRUB_OLD_INTERRUPTED]}).install(monkeypatch, statbtrfs)
    # It does not wait for it, but the last scrub did not complete: not healthy.
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_FAILURE
    assert fake.status_polls == 1


def test_watch_ending_on_a_failed_status_read_exits_2(monkeypatch):
    fake = FakeBtrfs(
        ["/mnt/a"], polls=99, running=["/mnt/a"], replies={"/mnt/a": [None] * 3 + [SCRUB_FAILED_LOCKED] * 50},
    ).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_FAILURE
    assert fake.status_polls > 3


def test_watch_reads_past_a_part_way_read_at_the_end_of_a_scrub(monkeypatch):
    fake = FakeBtrfs(
        ["/mnt/a"], polls=4, running=["/mnt/a"], errors=["/mnt/a"],
        replies={"/mnt/a": [None] * 3 + [SCRUB_FAILED_READ_MODERN]},
    ).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_PROBLEMS
    assert fake.status_polls == 5


def test_watch_prints_once_when_nothing_is_running(monkeypatch, capsys):
    fake = FakeBtrfs(["/mnt/a"]).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["--watch"]) == statbtrfs.EXIT_OK
    assert fake.status_polls == 1
    assert "TABLE" in capsys.readouterr().out


def test_watch_exit_code_reflects_final_status(monkeypatch):
    FakeBtrfs(["/mnt/a"], polls=2, running=["/mnt/a"], errors=["/mnt/a"]).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_PROBLEMS


def test_watch_ctrl_c_exits_quietly(monkeypatch, capsys):
    FakeBtrfs(["/mnt/a"], polls=50, running=["/mnt/a"], interrupt_on_sleep=2).install(monkeypatch, statbtrfs)
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_INTERRUPTED
    assert "Traceback" not in capsys.readouterr().out


def test_watch_redraws_on_a_terminal(monkeypatch, capsys):
    FakeBtrfs(["/mnt/a"], polls=1, running=["/mnt/a"]).install(monkeypatch, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys.stdout, "isatty", lambda: True, raising=False)
    _run(monkeypatch, ["-w"])
    assert statbtrfs.CLEAR_SCREEN in capsys.readouterr().out


def test_watch_and_scrub_are_mutually_exclusive(monkeypatch, capsys):
    with pytest.raises(SystemExit) as ei:
        _run(monkeypatch, ["-w", "-s"])
    assert ei.value.code == 2
    assert "not allowed with" in capsys.readouterr().err
