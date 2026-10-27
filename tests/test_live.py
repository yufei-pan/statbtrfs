import pytest

import statbtrfs
from conftest import skip_unless_live_btrfs


@pytest.mark.live
def test_live_status_table(monkeypatch, capsys):
    skip_unless_live_btrfs()
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    # Safety: conftest's autouse fixture already fails any test that reaches run_detached with btrfs.
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "Mount" in out or "scrub_status" in out or "TABLE" in out or "│" in out or "|" in out
    # Header fields appear inside pretty_format_table output; require at least one known column name:
    assert any(h in out for h in ("Mount", "scrub_status", "FS Used", "w_err"))
