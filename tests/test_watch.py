"""-w / --watch (#9): follow scrubs started elsewhere until none is running."""
import pytest

import statbtrfs
from fakes import FakeBtrfs


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
