"""`statbtrfs | head`: a reader that exits early ends the run quietly."""
import os
import subprocess
import sys
from pathlib import Path

import statbtrfs

ROOT = Path(statbtrfs.__file__).resolve().parent

CHILD = """
import sys, time
sys.path.insert(0, {root!r})
import statbtrfs
statbtrfs.read_proc_mounts = lambda: ["/dev/sdx /mnt/a btrfs rw 0 0"]
statbtrfs.execute_commands = lambda commands: [[] for _ in commands]
statbtrfs._is_root = lambda: True
statbtrfs.btrfs_not_found = lambda: False
sys.argv = ["statbtrfs", "--color=never"]
time.sleep(0.5)  # the reader has closed the pipe by now
sys.exit(statbtrfs.main())
"""


def test_closed_pipe_exits_quietly_with_141():
    read_end, write_end = os.pipe()
    os.close(read_end)  # a reader that has already gone, as with `| head -0`
    child = subprocess.Popen([sys.executable, "-c", CHILD.format(root=str(ROOT))],
                             stdout=write_end, stderr=subprocess.PIPE)
    os.close(write_end)
    _, err = child.communicate()
    assert err == b""  # no traceback, and no second error from the exit-time flush
    assert child.returncode == statbtrfs.EXIT_PIPE_CLOSED == 141


def test_broken_pipe_from_any_print_is_caught(monkeypatch, capsys):
    def run():
        raise BrokenPipeError
    monkeypatch.setattr(statbtrfs, "run", run)
    assert statbtrfs.main() == statbtrfs.EXIT_PIPE_CLOSED
