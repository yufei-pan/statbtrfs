import pytest

import statbtrfs
from conftest import skip_unless_live_btrfs


@pytest.mark.live
def test_live_status_table(monkeypatch, capsys):
    skip_unless_live_btrfs()
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    # Safety: if something patched scrub in, fail hard
    real_exec = statbtrfs.execute_command

    def guard(command, wait=True):
        if list(command)[:3] == ["btrfs", "scrub", "start"] or list(command)[:4] == [
            "sudo",
            "btrfs",
            "scrub",
            "start",
        ]:
            raise AssertionError("live tests must not scrub start")
        return real_exec(command, wait=wait)

    monkeypatch.setattr(statbtrfs, "execute_command", guard)
    # execute_commands used for status; wrap similarly
    real_execs = statbtrfs.execute_commands

    def guard_many(commands, wait=True):
        for command in commands:
            if list(command)[:3] == ["btrfs", "scrub", "start"]:
                raise AssertionError("live tests must not scrub start")
        return real_execs(commands, wait=wait)

    monkeypatch.setattr(statbtrfs, "execute_commands", guard_many)
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "Mount" in out or "scrub_status" in out or "TABLE" in out or "│" in out or "|" in out
    # Header fields appear inside pretty_format_table output; require at least one known column name:
    assert any(h in out for h in ("Mount", "scrub_status", "FS Used", "w_err"))
