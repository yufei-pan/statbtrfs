import statbtrfs
from fakes import MOUNT_LINES_MULTI, CommandMap, install_command_map, install_mounts


def test_parse_proc_mounts_keeps_btrfs_only():
    lines = [
        "proc /proc proc rw,nosuid 0 0",
        "/dev/sda1 /mnt/a btrfs rw,relatime 0 0",
        "/dev/sdb1 /boot ext4 rw 0 0",
        "/dev/sdc1 /data btrfs rw 0 0",
    ]
    assert statbtrfs.parse_proc_mounts(lines) == ["/mnt/a", "/data"]


def test_parse_proc_mounts_decodes_octal_escapes():
    lines = [
        r"/dev/sda1 /mnt/my\040pool btrfs rw 0 0",
        r"/dev/sdb1 /mnt/tab\011and\134slash btrfs rw 0 0",
    ]
    assert statbtrfs.parse_proc_mounts(lines) == ["/mnt/my pool", "/mnt/tab\tand\\slash"]


def test_parse_proc_mounts_skips_short_lines():
    assert statbtrfs.parse_proc_mounts(["", "garbage", "/dev/sda1 /mnt/a"]) == []


def test_read_proc_mounts_reads_file(tmp_path):
    f = tmp_path / "mounts"
    f.write_text("/dev/sda1 /mnt/a btrfs rw 0 0\n/dev/sdb1 /boot ext4 rw 0 0\n")
    assert statbtrfs.read_proc_mounts(str(f)) == [
        "/dev/sda1 /mnt/a btrfs rw 0 0",
        "/dev/sdb1 /boot ext4 rw 0 0",
    ]


def test_read_proc_mounts_unreadable_returns_empty(tmp_path, capsys):
    assert statbtrfs.read_proc_mounts(str(tmp_path / "missing")) == []
    assert "Could not read" in capsys.readouterr().out


def test_find_btrfs_mounts_runs_no_commands(monkeypatch):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    install_mounts(monkeypatch, statbtrfs, MOUNT_LINES_MULTI)
    statbtrfs.find_btrfs_mounts()
    assert cm.calls == []


def test_find_btrfs_mounts_empty(monkeypatch):
    install_mounts(monkeypatch, statbtrfs, [])
    assert statbtrfs.find_btrfs_mounts() == []


def test_find_btrfs_mounts_all(monkeypatch):
    install_mounts(monkeypatch, statbtrfs, MOUNT_LINES_MULTI)
    assert statbtrfs.find_btrfs_mounts() == ["/data", "/mnt/a", "/mnt/b"]
