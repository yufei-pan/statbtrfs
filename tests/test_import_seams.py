def test_embedded_multicmd_is_used_when_the_installed_one_is_older(tmp_path):
    # An installed multiCMD older than 1.56 is passed over for the embedded copy.
    import os
    import subprocess
    import sys
    from pathlib import Path

    import statbtrfs

    root = Path(statbtrfs.__file__).resolve().parent
    (tmp_path / "multiCMD.py").write_text("version = '1.55'\n")
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tmp_path), str(root)]))
    out = subprocess.run(
        [sys.executable, "-c", "import statbtrfs; print(statbtrfs.multiCMD.version)"],
        cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, check=True,
    ).stdout.decode("utf-8")
    assert out == "1.56\n"
