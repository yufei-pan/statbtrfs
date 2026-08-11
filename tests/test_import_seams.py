import pytest

import statbtrfs


def test_module_imports_without_exiting():
    assert hasattr(statbtrfs, "version")
    assert callable(statbtrfs.main)


def test_ensure_privileges_exits_when_sudo_missing(monkeypatch, capsys):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", True)
    monkeypatch.setattr(statbtrfs, "_SUDO_CHECKED", False)

    def fake_run(cmd, **kwargs):
        # which sudo fails -> non-zero truthy return_code_only
        return 1

    monkeypatch.setattr(statbtrfs.multiCMD, "run_command", fake_run)
    with pytest.raises(SystemExit) as ei:
        statbtrfs.ensure_privileges()
    assert ei.value.code == 1
    assert "sudo is required" in capsys.readouterr().out


def test_ensure_privileges_noop_when_root(monkeypatch):
    monkeypatch.setattr(statbtrfs, "USE_SUDO", False)
    monkeypatch.setattr(statbtrfs, "_SUDO_CHECKED", False)
    calls = []
    monkeypatch.setattr(
        statbtrfs.multiCMD,
        "run_command",
        lambda *a, **k: calls.append(1) or 0,
    )
    statbtrfs.ensure_privileges()
    assert calls == []
