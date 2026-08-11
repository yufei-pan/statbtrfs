import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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
    import statbtrfs

    mounts = statbtrfs.find_btrfs_mounts([])
    if not mounts:
        pytest.skip("no btrfs mounts")
