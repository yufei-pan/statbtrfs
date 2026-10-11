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
