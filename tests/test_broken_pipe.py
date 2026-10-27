"""`statbtrfs | head`: a reader that exits early ends the run quietly."""
import os
import subprocess
import sys
from pathlib import Path

import statbtrfs

ROOT = Path(statbtrfs.__file__).resolve().parent

CHILD = """
import sys
sys.path.insert(0, {root!r})
import statbtrfs
statbtrfs.read_proc_mounts = lambda: ["/dev/sdx /mnt/a btrfs rw 0 0"]
statbtrfs.execute_commands = {execute}
statbtrfs._is_root = lambda: True
statbtrfs.btrfs_not_found = lambda: False
sys.argv = ["statbtrfs", "--color=never"]
sys.exit(statbtrfs.main())
"""


def _run_with_gone_reader(execute):
    read_end, write_end = os.pipe()
    os.close(read_end)  # a reader that has already gone, as with `| head -0`
    child = subprocess.Popen([sys.executable, "-c", CHILD.format(root=str(ROOT), execute=execute)],
                             stdout=write_end, stderr=subprocess.PIPE)
    os.close(write_end)
    _, err = child.communicate()
    return child.returncode, err


def test_closed_pipe_exits_quietly_with_141():
    code, err = _run_with_gone_reader("lambda commands: [[] for _ in commands]")
    assert err == b""  # no traceback, and no second error from the exit-time flush
    assert code == statbtrfs.EXIT_PIPE_CLOSED == 141


def test_ctrl_c_with_a_gone_reader_exits_130_quietly():
    # `statbtrfs | grep sda`, discovery hangs, Ctrl-C kills grep too: the 130 path must not print.
    code, err = _run_with_gone_reader("lambda commands: (_ for _ in ()).throw(KeyboardInterrupt())")
    assert err == b""
    assert code == statbtrfs.EXIT_INTERRUPTED == 130


def test_broken_pipe_from_any_print_is_caught(monkeypatch, capsys):
    def run():
        raise BrokenPipeError
    monkeypatch.setattr(statbtrfs, "run", run)
    assert statbtrfs.main() == statbtrfs.EXIT_PIPE_CLOSED
