import statbtrfs


def test_module_imports_without_exiting():
    assert hasattr(statbtrfs, "version")
    assert callable(statbtrfs.main)


def test_embedded_multicmd_is_used_when_the_installed_one_is_older_and_lines_up_cjk(tmp_path):
    # An installed multiCMD older than 1.55 is passed over for the embedded copy,
    # whose tables size columns in terminal columns: a CJK character takes two.
    import os
    import subprocess
    import sys
    from pathlib import Path

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.54'\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c",
         "import statbtrfs; m = statbtrfs.multiCMD; "
         "print(m.version); print(m.pretty_format_table([['name', 'v'], ['中文', '1']], full=True), end='')"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "1.55\nname | v\n-----+--\n中文 | 1\n"


def test_embedded_multicmd_reads_terminal_columns_when_stdout_is_piped(tmp_path):
    # `statbtrfs | less` on a 200x40 terminal: the size comes from stdin's TIOCGWINSZ,
    # whose winsize struct holds the rows before the columns.
    import os
    import subprocess
    import sys
    from pathlib import Path

    import pytest
    pty = pytest.importorskip("pty")
    import fcntl
    import struct
    import termios

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.0'\n")  # too old: the embedded copy is used
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    master, slave = pty.openpty()
    try:
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 200, 0, 0))
        out = subprocess.run(
            [sys.executable, "-c", "import statbtrfs; print(*statbtrfs.multiCMD.get_terminal_size()[:2])"],
            stdin=slave, stdout=subprocess.PIPE, cwd=str(tmp_path), env=env, universal_newlines=True, check=True,
        ).stdout
    finally:
        os.close(slave)
        os.close(master)
    assert out.split() == ["200", "40"]
