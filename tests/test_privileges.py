import os
import sys

import pytest

import statbtrfs


class Execv(Exception):
    """Raised by the fake os.execv so the test sees what would have been exec'd."""


@pytest.fixture
def non_root(monkeypatch):
    monkeypatch.setattr(statbtrfs, "_is_root", lambda: False)
    monkeypatch.setattr(statbtrfs.shutil, "which", lambda name: "/usr/bin/sudo" if name == "sudo" else None)
    execs = []

    def fake_execv(path, args):
        execs.append((path, args))
        raise Execv()

    monkeypatch.setattr(statbtrfs.os, "execv", fake_execv)
    return execs


def _sudo_list_returns(monkeypatch, code, tty=True):
    checks = []
    monkeypatch.setattr(statbtrfs.subprocess, "call", lambda cmd, **kw: checks.append(cmd) or code)
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: tty, raising=False)
    return checks


def test_acquire_root_as_root_runs_nothing(monkeypatch):
    monkeypatch.setattr(statbtrfs, "_is_root", lambda: True)
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    monkeypatch.setattr(statbtrfs.subprocess, "call", lambda *a, **k: pytest.fail("no sudo check as root"))
    statbtrfs.acquire_root(["-s"])
    assert statbtrfs.USE_SUDO is False


def test_acquire_root_without_sudo_exits(monkeypatch, capsys):
    monkeypatch.setattr(statbtrfs, "_is_root", lambda: False)
    monkeypatch.setattr(statbtrfs.shutil, "which", lambda name: None)
    with pytest.raises(SystemExit) as ei:
        statbtrfs.acquire_root([])
    assert ei.value.code == 1
    assert "needs root" in capsys.readouterr().out


def test_acquire_root_reexecs_when_sudo_allows_it(monkeypatch, non_root):
    checks = _sudo_list_returns(monkeypatch, 0, tty=True)
    with pytest.raises(Execv):
        statbtrfs.acquire_root(["-s", "pool"])
    script = os.path.abspath(statbtrfs.__file__)
    assert checks == [["/usr/bin/sudo", "-l", "--", sys.executable, script, "-s", "pool"]]
    assert non_root == [("/usr/bin/sudo", ["/usr/bin/sudo", "--", sys.executable, script, "-s", "pool"])]


def test_acquire_root_never_prompts_without_a_tty(monkeypatch, non_root):
    checks = _sudo_list_returns(monkeypatch, 0, tty=False)
    with pytest.raises(Execv):
        statbtrfs.acquire_root([])
    assert checks[0][:3] == ["/usr/bin/sudo", "-n", "-l"]


def test_acquire_root_falls_back_to_per_command_sudo(monkeypatch, non_root):
    # e.g. sudoers allows only /usr/bin/btrfs: re-running the script is refused
    _sudo_list_returns(monkeypatch, 1)
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    statbtrfs.acquire_root([])
    assert non_root == []
    assert statbtrfs.USE_SUDO is True
    seen = []
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", lambda cmd, **kw: seen.append(cmd) or [])
    statbtrfs.execute_command(["btrfs", "scrub", "status", "/mnt/a"])
    assert seen == [["sudo", "btrfs", "scrub", "status", "/mnt/a"]]
