import os
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _assume_root(monkeypatch):
    """main() would otherwise re-exec the test run under sudo on a non-root machine."""
    import statbtrfs

    monkeypatch.setattr(statbtrfs, "_is_root", lambda: True, raising=False)


@pytest.fixture(autouse=True)
def _never_start_real_scrubs(monkeypatch):
    """-s tests must fake start_scrub(); never let one reach a real `btrfs scrub start`."""
    import statbtrfs

    real = getattr(statbtrfs, "run_detached", None)
    if real is None:
        return

    def guarded(command):
        if "btrfs" in command:
            pytest.fail(f"test tried to run {command}: fake statbtrfs.start_scrub")
        return real(command)

    monkeypatch.setattr(statbtrfs, "run_detached", guarded)


@pytest.fixture(autouse=True)
def _restore_colors():
    """main() switches colours off when stdout is not a terminal (as under pytest)."""
    import statbtrfs

    saved = (statbtrfs.RED, statbtrfs.GREEN, statbtrfs.YELLOW, statbtrfs.RESET)
    yield
    statbtrfs.RED, statbtrfs.GREEN, statbtrfs.YELLOW, statbtrfs.RESET = saved


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: soft smoke against real host btrfs (status only)",
    )


def skip_unless_live_btrfs():
    if sys.platform != "linux":
        pytest.skip("Linux only")
    if not shutil.which("btrfs"):
        pytest.skip("btrfs binary required")
    if os.geteuid() != 0:
        pytest.skip("live btrfs queries need root (run pytest -m live as root)")
    import statbtrfs

    if not statbtrfs.find_btrfs_mounts([]):
        pytest.skip("no btrfs mounts")
