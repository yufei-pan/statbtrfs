import os
import sys
import types

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


def _fake_run_command(seen, returncode=0, stdout=(), stderr=()):
    """multiCMD.run_command as statbtrfs calls it: records each command, and answers in the shape its flags ask for, as
    the real one does (with return_object the task, else the stdout lines, then the stderr's with with_stdErr)."""
    def run_command(command, with_stdErr=False, return_object=False, **kw):
        seen.append(command)
        if return_object:
            return types.SimpleNamespace(returncode=returncode, stdout=list(stdout), stderr=list(stderr))
        return list(stdout) + (list(stderr) if with_stdErr else [])
    return run_command


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
    assert ei.value.code == statbtrfs.EXIT_FAILURE == 2
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
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", _fake_run_command(seen, stdout=["out"], stderr=["err"]))
    assert statbtrfs.execute_command(["btrfs", "scrub", "status", "/mnt/a"]) == ["out", "err"]
    # -n: a sudo that wants a password fails at once; in multiCMD's process group it would stop at its prompt
    assert seen == [["sudo", "-n", "btrfs", "scrub", "status", "/mnt/a"]]


def test_scrub_cancel_goes_through_per_command_sudo(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = []
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", _fake_run_command(seen))
    assert statbtrfs.cancel_scrub("/mnt/a") is None
    assert seen == [["sudo", "-n", "btrfs", "scrub", "cancel", "/mnt/a"]]


def test_execute_commands_prefixes_sudo_and_caps_parallelism(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = {}

    def fake_run_commands(cmds, **kw):
        seen["cmds"], seen["kw"] = cmds, kw
        return [[] for _ in cmds]

    monkeypatch.setattr(statbtrfs.multiCMD, "run_commands", fake_run_commands)
    statbtrfs.execute_commands([["btrfs", "device", "stats", "/mnt/a"]])
    assert seen["cmds"] == [["sudo", "-n", "btrfs", "device", "stats", "/mnt/a"]]
    assert seen["kw"]["max_threads"] == statbtrfs.MAX_PARALLEL_COMMANDS


def test_btrfs_replies_carry_stderr_after_stdout(monkeypatch):
    # `btrfs scrub status` that fails to read part way exits 0 and says so only on stderr.
    from fakes import SCRUB_FAILED_READ_MODERN, SHOW_SINGLE, STATS_ZERO
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    stdout = {"show": SHOW_SINGLE, "stats": STATS_ZERO, "status": SCRUB_FAILED_READ_MODERN[:-1]}
    stderr = {"status": SCRUB_FAILED_READ_MODERN[-1:]}

    def run_commands(cmds, with_stdErr=False, return_object=False, **kw):
        if return_object:
            return [types.SimpleNamespace(returncode=0, stdout=stdout[c[2]], stderr=stderr.get(c[2], [])) for c in cmds]
        return [stdout[c[2]] + (stderr.get(c[2], []) if with_stdErr else []) for c in cmds]

    def run_command(cmd, **kw):
        return run_commands([cmd], **kw)[0]

    monkeypatch.setattr(statbtrfs.multiCMD, "run_commands", run_commands)
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", run_command)
    fs = {"uuid": None, "mounts": ["/mnt/a"]}
    status = statbtrfs.build_status(statbtrfs.poll_filesystems([fs]))
    assert status.scrubs["/mnt/a"]["scrub_status"] == "unknown"
    assert status.failures is True
    assert statbtrfs.execute_command(["btrfs", "scrub", "status", "/mnt/a"]) == SCRUB_FAILED_READ_MODERN
