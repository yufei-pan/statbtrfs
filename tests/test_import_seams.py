def test_embedded_multicmd_is_used_when_the_installed_one_is_older(tmp_path):
    # An installed multiCMD older than 1.61, the gate, is passed over for the embedded copy.
    import os
    import subprocess
    import sys
    from pathlib import Path

    import statbtrfs

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.60'\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c", "import statbtrfs; print(statbtrfs.multiCMD.version)"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "1.61\n"


def test_embedded_multicmd_is_used_when_the_installed_one_fails_to_import(tmp_path):
    # Any failure, not only ImportError: a half-upgraded install must not stop the tool.
    import os
    import subprocess
    import sys
    from pathlib import Path

    import statbtrfs

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("raise RuntimeError('broken install')\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c", "import statbtrfs; print(statbtrfs.multiCMD.version)"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "1.61\n"


def test_a_current_installed_multicmd_is_used(tmp_path):
    import os
    import subprocess
    import sys
    from pathlib import Path

    import statbtrfs

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.61'\nINSTALLED = True\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c", "import statbtrfs; print(statbtrfs.multiCMD.INSTALLED)"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "True\n"


def test_embedded_multicmd_runs_on_a_python_without_lzma(tmp_path):
    # The block unpacks with zlib: a Python built without lzma (no xz-devel) still runs the embedded copy.
    import os
    import subprocess
    import sys
    from pathlib import Path

    import statbtrfs

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.60'\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.modules['lzma'] = None; sys.modules['_lzma'] = None; "
         "import statbtrfs; print(statbtrfs.multiCMD.version)"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "1.61\n"
