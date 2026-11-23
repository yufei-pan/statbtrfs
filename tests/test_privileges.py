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


@pytest.fixture(params=[True, False], ids=["terminal", "no-terminal"])
def terminal(request, monkeypatch):
    """Both outcomes of the check for a controlling terminal, forced."""
    monkeypatch.setattr(statbtrfs, "_has_terminal", lambda: request.param)
    return request.param


def _sudo(terminal):
    """The per-command sudo of a command multiCMD runs: `sudo -n` while statbtrfs has a terminal, where sudo could stop
    at a prompt (in multiCMD's process group it can't read the terminal); plain sudo without one, where it can't."""
    return ["sudo", "-n"] if terminal else ["sudo"]


def _fake_run_command(seen, returncode=0, stdout=(), stderr=()):
    """multiCMD.run_command as statbtrfs calls it: records each command, and answers in the shape its flags ask for, as
    the real one does (with return_object the task, else the stdout lines, then the stderr's with with_stdErr)."""
    def run_command(command, with_stdErr=False, return_object=False, **kw):
        seen.append(command)
        if return_object:
            return types.SimpleNamespace(returncode=returncode, stdout=list(stdout), stderr=list(stderr))
        return list(stdout) + (list(stderr) if with_stdErr else [])
    return run_command


def _sudo_list_returns(monkeypatch, code, tty=True, foreground=False):
    """sudo -l answers `code`; stdin is a terminal or not, and statbtrfs holds its controlling terminal's foreground or
    not (both forced: never what the machine that runs the tests has)."""
    checks = []
    monkeypatch.setattr(statbtrfs.subprocess, "call", lambda cmd, **kw: checks.append(cmd) or code)
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: tty, raising=False)
    monkeypatch.setattr(statbtrfs, "_in_foreground", lambda: foreground)
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


@pytest.mark.parametrize("tty,foreground,asks", [
    (True, True, True),     # statbtrfs in a terminal
    (True, False, True),    # `statbtrfs &` from an interactive shell: stdin is the terminal, sudo stops at its prompt, and
                            # `fg` goes on; `-n -l` would refuse a sudo that authenticates with no question
    (False, True, True),    # `statbtrfs </dev/null`, a pipe, nohup in the foreground: sudo asks on the terminal, not on stdin
    (False, False, False),  # cron, `ssh host statbtrfs`, `statbtrfs </dev/null &` in an interactive shell: nobody to ask
], ids=["terminal", "background-with-stdin-terminal", "foreground-stdin-elsewhere", "no-one-to-ask"])
def test_acquire_root_asks_for_a_password_only_where_someone_can_answer(monkeypatch, non_root, tty, foreground, asks):
    checks = _sudo_list_returns(monkeypatch, 0, tty=tty, foreground=foreground)
    with pytest.raises(Execv):
        statbtrfs.acquire_root([])
    assert checks[0][:3] == (["/usr/bin/sudo", "-l", "--"] if asks else ["/usr/bin/sudo", "-n", "-l"])


@pytest.mark.parametrize("foreground,asks", [(True, True), (False, False)], ids=["foreground", "background"])
def test_acquire_root_with_no_stdin_is_not_a_terminal_input(monkeypatch, non_root, foreground, asks):
    # `statbtrfs 0<&-`: fd 0 is closed, so Python's sys.stdin is None; it is not a terminal, and the foreground decides
    checks = _sudo_list_returns(monkeypatch, 0, foreground=foreground)
    monkeypatch.setattr(statbtrfs.sys, "stdin", None)
    with pytest.raises(Execv):
        statbtrfs.acquire_root([])
    assert checks[0][:3] == (["/usr/bin/sudo", "-l", "--"] if asks else ["/usr/bin/sudo", "-n", "-l"])


def test_acquire_root_falls_back_to_per_command_sudo(monkeypatch, non_root, terminal):
    # e.g. sudoers allows only /usr/bin/btrfs: re-running the script is refused
    _sudo_list_returns(monkeypatch, 1)
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    statbtrfs.acquire_root([])
    assert non_root == []
    assert statbtrfs.USE_SUDO is True
    seen = []
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", _fake_run_command(seen, stdout=["out"], stderr=["err"]))
    assert statbtrfs.execute_command(["btrfs", "scrub", "status", "/mnt/a"]) == ["out", "err"]
    assert seen == [_sudo(terminal) + ["btrfs", "scrub", "status", "/mnt/a"]]


def test_scrub_cancel_goes_through_per_command_sudo(monkeypatch, terminal):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = []
    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", _fake_run_command(seen))
    assert statbtrfs.cancel_scrub("/mnt/a") is None
    assert seen == [_sudo(terminal) + ["btrfs", "scrub", "cancel", "/mnt/a"]]


def test_execute_commands_prefixes_sudo_and_caps_parallelism(monkeypatch, terminal):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    seen = {}

    def fake_run_commands(cmds, **kw):
        seen["cmds"], seen["kw"] = cmds, kw
        return [[] for _ in cmds]

    monkeypatch.setattr(statbtrfs.multiCMD, "run_commands", fake_run_commands)
    statbtrfs.execute_commands([["btrfs", "device", "stats", "/mnt/a"]])
    assert seen["cmds"] == [_sudo(terminal) + ["btrfs", "device", "stats", "/mnt/a"]]
    assert seen["kw"]["max_threads"] == statbtrfs.MAX_PARALLEL_COMMANDS


def test_has_terminal_is_whether_dev_tty_opens_not_whether_stdin_is_one(monkeypatch):
    real_open, opened, closed = os.open, [], []

    def fake_open(path, flags, *a, **k):
        if path != "/dev/tty":
            return real_open(path, flags, *a, **k)
        opened.append(flags)
        if outcome == "none":
            raise OSError(6, "No such device or address")
        return 99

    monkeypatch.setattr(statbtrfs.os, "open", fake_open)
    monkeypatch.setattr(statbtrfs.os, "close", lambda fd: closed.append(fd))
    # stdin is not a terminal, but /dev/tty opens: `statbtrfs </dev/null` in a terminal
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: False, raising=False)
    outcome = "tty"
    assert statbtrfs._has_terminal() is True
    assert opened == [os.O_RDWR | os.O_NOCTTY] and closed == [99]  # opened as not to make it ours, and closed
    # stdin is a terminal as far as it can tell, but there is no controlling terminal to open
    monkeypatch.setattr(statbtrfs.sys.stdin, "isatty", lambda: True, raising=False)
    outcome = "none"
    assert statbtrfs._has_terminal() is False


@pytest.mark.parametrize("outcome", ["ours", "another-group", "no-terminal", "unreadable"])
def test_in_foreground_is_whether_our_group_is_the_terminals(monkeypatch, outcome):
    real_open, opened, closed = os.open, [], []

    def fake_open(path, flags, *a, **k):
        if path != "/dev/tty":
            return real_open(path, flags, *a, **k)
        opened.append(flags)
        if outcome == "no-terminal":
            raise OSError(6, "No such device or address")
        return 99

    def tcgetpgrp(fd):
        assert fd == 99
        if outcome == "unreadable":
            raise OSError(25, "Inappropriate ioctl for device")
        return 4000 if outcome == "ours" else 4001

    monkeypatch.setattr(statbtrfs.os, "open", fake_open)
    monkeypatch.setattr(statbtrfs.os, "close", lambda fd: closed.append(fd))
    monkeypatch.setattr(statbtrfs.os, "tcgetpgrp", tcgetpgrp)
    monkeypatch.setattr(statbtrfs.os, "getpgrp", lambda: 4000)
    monkeypatch.setattr(statbtrfs.os, "getpid", lambda: 4001)  # the group is asked for, not the process
    assert statbtrfs._in_foreground() is (outcome == "ours")
    assert opened == [os.O_RDWR | os.O_NOCTTY]  # not to make it ours
    assert closed == ([] if outcome == "no-terminal" else [99])


_REAL_TERMINAL_CHILD = """
import fcntl, os, sys, termios
sys.path.insert(0, sys.argv[1])
import statbtrfs
fcntl.ioctl(os.open(sys.argv[2], os.O_RDWR | os.O_NOCTTY), termios.TIOCSCTTY, 0)  # a session leader: now our terminal
reader, writer = os.pipe()
if os.fork() == 0:
    os.setpgid(0, 0)  # a group of its own, which is not the terminal's foreground
    os.write(writer, b"background=%d" % statbtrfs._in_foreground())
    os._exit(0)
os.wait()
print("foreground=%d" % statbtrfs._in_foreground(), os.read(reader, 64).decode())
"""


def test_in_foreground_on_a_real_terminal():
    import pty
    import subprocess
    try:
        master, slave = pty.openpty()
    except OSError as e:
        pytest.skip(f"no pseudo-terminal here: {e}")
    try:
        done = subprocess.run([sys.executable, "-c", _REAL_TERMINAL_CHILD, os.path.dirname(statbtrfs.__file__),
                               os.ttyname(slave)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, start_new_session=True, timeout=60)
    finally:
        os.close(master)
        os.close(slave)
    assert done.stdout.split() == ["foreground=1", "background=0"], done.stderr


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
