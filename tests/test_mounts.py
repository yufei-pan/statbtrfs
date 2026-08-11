import statbtrfs
from fakes import MOUNT_LINES_MULTI, CommandMap, install_command_map


def test_find_btrfs_mounts_empty(monkeypatch):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    assert statbtrfs.find_btrfs_mounts([]) == set()
    assert statbtrfs.find_btrfs_mounts(None) == set()


def test_find_btrfs_mounts_none_output(monkeypatch):
    monkeypatch.setattr(statbtrfs, "execute_command", lambda *a, **k: None)
    assert statbtrfs.find_btrfs_mounts([]) == set()


def test_find_btrfs_mounts_all(monkeypatch):
    cm = CommandMap({("mount", "-t", "btrfs"): MOUNT_LINES_MULTI})
    install_command_map(monkeypatch, cm, statbtrfs)
    assert statbtrfs.find_btrfs_mounts([]) == {"/mnt/a", "/mnt/b", "/data"}


def test_find_btrfs_mounts_pattern_filter(monkeypatch):
    cm = CommandMap({("mount", "-t", "btrfs"): MOUNT_LINES_MULTI})
    install_command_map(monkeypatch, cm, statbtrfs)
    assert statbtrfs.find_btrfs_mounts(["mnt"]) == {"/mnt/a", "/mnt/b"}
    assert statbtrfs.find_btrfs_mounts(["data"]) == {"/data"}
