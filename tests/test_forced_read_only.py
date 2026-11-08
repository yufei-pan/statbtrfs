"""A btrfs the kernel forced read-only after an error: reported in every mode, never scrubbed as healthy."""
import pytest

import statbtrfs
from fakes import (
    FakeBtrfs,
    SCRUB_FINISHED_OK,
    STATS_ZERO,
    install_mountinfo,
    install_status,
    make_show,
    mountinfo_line,
    uuid_for,
)

# The unpatched reader (conftest serves an empty mountinfo to everything else).
read_mountinfo = getattr(statbtrfs, "read_mountinfo", None)

FORCED = mountinfo_line("/mnt/a", "rw,relatime", "ro,space_cache")
ON_PURPOSE = mountinfo_line("/mnt/a", "ro,relatime", "ro,space_cache")
HEALTHY = mountinfo_line("/mnt/a")


def _run(monkeypatch, argv):
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"] + argv)
    return statbtrfs.main()


def _status(monkeypatch, *mounts):
    install_status(monkeypatch, statbtrfs, {
        mount: (make_show(uuid_for(n)), STATS_ZERO, SCRUB_FINISHED_OK) for n, mount in enumerate(mounts, 1)})


# --- reading mountinfo --------------------------------------------------------

# Real /proc/self/mountinfo, EL7 (3.10.0-1160.119.1), a filesystem with a subvolume mount, on VM 902.
REAL_HEALTHY = [
    "85 40 0:39 / /root/sb043/a rw,relatime shared:67 - btrfs /dev/mapper/sb043 rw,seclabel,space_cache,subvolid=5,subvol=/",
    "86 40 0:39 /sv /root/sb043/b rw,relatime shared:69 - btrfs /dev/mapper/sb043 rw,seclabel,space_cache,subvolid=257,subvol=/sv",
]
# The device swapped for dm-error, a write and sync: "error ... in cleanup_transaction: errno=-5 IO failure".
REAL_FORCED = [
    "85 40 0:39 / /root/sb043/a rw,relatime shared:67 - btrfs /dev/mapper/sb043 ro,seclabel,space_cache,subvolid=5,subvol=/",
    "86 40 0:39 /sv /root/sb043/b rw,relatime shared:69 - btrfs /dev/mapper/sb043 ro,seclabel,space_cache,subvolid=257,subvol=/sv",
]
# mount -o ro.
REAL_MOUNTED_RO = [
    "85 40 0:39 / /root/sb043/a ro,relatime shared:67 - btrfs /dev/mapper/sb043 ro,seclabel,space_cache,subvolid=5,subvol=/",
]
# A subvolume mounted -o ro beside a read-write mount of the same filesystem.
REAL_ONE_MOUNT_RO = [
    "85 40 0:39 / /root/sb043/a rw,relatime shared:67 - btrfs /dev/mapper/sb043 rw,seclabel,space_cache,subvolid=5,subvol=/",
    "86 40 0:39 /sv /root/sb043/b ro,relatime shared:69 - btrfs /dev/mapper/sb043 rw,seclabel,space_cache,subvolid=257,subvol=/sv",
]
# `mount -o remount,ro` of one of two mounts: the other keeps rw on a read-only filesystem, as when forced. It
# takes no writes either, so it is reported (the note says what was seen, read-only though mounted read-write).
REAL_REMOUNTED_RO_BESIDE = [
    "85 40 0:39 / /root/sb043/a ro,relatime shared:67 - btrfs /dev/mapper/sb043 ro,seclabel,space_cache,subvolid=5,subvol=/",
    "86 40 0:39 /sv /root/sb043/b rw,relatime shared:69 - btrfs /dev/mapper/sb043 ro,seclabel,space_cache,subvolid=257,subvol=/sv",
]


@pytest.mark.parametrize("lines, forced", [
    (REAL_HEALTHY, set()),
    (REAL_FORCED, {"/root/sb043/a", "/root/sb043/b"}),
    (REAL_MOUNTED_RO, set()),
    (REAL_ONE_MOUNT_RO, set()),
    (REAL_REMOUNTED_RO_BESIDE, {"/root/sb043/b"}),
], ids=["healthy", "forced", "mounted-ro", "one-mount-ro", "remounted-ro-beside"])
def test_forced_read_only_on_real_el7_mountinfo(lines, forced):
    assert statbtrfs.parse_forced_read_only(lines) == forced

def test_forced_is_read_write_mount_on_a_read_only_filesystem():
    lines = [
        FORCED,
        mountinfo_line("/mnt/b", "ro,relatime", "ro,space_cache"),           # mounted -o ro
        mountinfo_line("/mnt/c"),                                            # healthy
        mountinfo_line("/mnt/d", "ro,relatime", "rw,space_cache"),           # one mount ro, the filesystem rw
        "41 1 0:41 / /mnt/e rw,relatime shared:41 - ext4 /dev/sde ro,errors=remount-ro",  # not btrfs
    ]
    assert statbtrfs.parse_forced_read_only(lines) == {"/mnt/a"}


def test_forced_reads_the_options_after_the_optional_tags():
    # No optional tag, or several, before "-"; an escaped space in the mountpoint.
    lines = [
        "40 1 0:40 / /mnt/a rw,relatime - btrfs /dev/x ro,space_cache,subvolid=5,subvol=/",
        "41 1 0:41 /sv /mnt/my\\040b rw,relatime shared:4 master:2 - btrfs /dev/x ro,space_cache,subvol=/sv",
    ]
    assert statbtrfs.parse_forced_read_only(lines) == {"/mnt/a", "/mnt/my b"}


@pytest.mark.parametrize("line", ["", "garbage", "40 1 0:40 / /mnt/a rw,relatime shared:1", "40 1 0:40 / /mnt/a rw - btrfs"])
def test_forced_skips_lines_it_cannot_read(line):
    assert statbtrfs.parse_forced_read_only([line]) == set()


def test_read_mountinfo_reads_the_file_and_none_when_it_cannot(tmp_path):
    f = tmp_path / "mountinfo"
    f.write_text(FORCED + "\n" + HEALTHY + "\n")
    assert read_mountinfo(str(f)) == [FORCED, HEALTHY]
    assert read_mountinfo(str(tmp_path / "missing")) is None


# --- what the operator sees -----------------------------------------------------

def test_plain_status_reports_a_forced_read_only_filesystem(monkeypatch, capsys):
    _status(monkeypatch, "/mnt/a", "/mnt/b")
    install_mountinfo(monkeypatch, statbtrfs, [FORCED, mountinfo_line("/mnt/b", n=41)])
    rows = []
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda r, header=None: rows.extend(r) or "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    assert statbtrfs.main() == statbtrfs.EXIT_PROBLEMS
    out = capsys.readouterr().out
    assert rows[0][0] == f"/mnt/a, {statbtrfs.RED}forced read-only{statbtrfs.RESET}"
    assert rows[1][0] == "/mnt/b"
    assert "/mnt/a: read-only, though mounted read-write, so it takes no writes" in out
    assert "dmesg" in out and "unmount and mount it again, or reboot" in out
    assert "/mnt/b:" not in out


@pytest.mark.parametrize("line", [ON_PURPOSE, HEALTHY], ids=["mounted-ro", "healthy"])
def test_a_filesystem_not_forced_is_not_reported(monkeypatch, capsys, line):
    _status(monkeypatch, "/mnt/a")
    install_mountinfo(monkeypatch, statbtrfs, [line])
    assert _run(monkeypatch, []) == statbtrfs.EXIT_OK
    assert "forced" not in capsys.readouterr().out


def test_one_forced_mount_marks_the_whole_filesystem(monkeypatch):
    # Subvolume mounts share the filesystem, and its read-only state.
    install_status(monkeypatch, statbtrfs, {
        "/mnt/a": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK),
        "/mnt/a2": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK),
    })
    install_mountinfo(monkeypatch, statbtrfs, [mountinfo_line("/mnt/a2", "rw,relatime", "ro,space_cache")])
    rows = []
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda r, header=None: rows.extend(r) or "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    assert statbtrfs.main() == statbtrfs.EXIT_PROBLEMS
    assert rows[0][0].startswith("/mnt/a, /mnt/a2, ")


def test_unreadable_mountinfo_says_it_was_not_checked(monkeypatch, capsys):
    _status(monkeypatch, "/mnt/a")
    install_mountinfo(monkeypatch, statbtrfs, None)
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE
    assert "not checked whether /mnt/a was forced read-only" in capsys.readouterr().out


def test_watch_reports_a_filesystem_forced_read_only_during_the_run(monkeypatch):
    fake = FakeBtrfs(["/mnt/a"], polls=3, running=["/mnt/a"]).install(monkeypatch, statbtrfs)
    reads = iter([[HEALTHY], [HEALTHY], [FORCED]])
    monkeypatch.setattr(statbtrfs, "read_mountinfo", lambda path=None: next(reads, [FORCED]))
    assert _run(monkeypatch, ["-w"]) == statbtrfs.EXIT_PROBLEMS
    assert fake.status_polls == 4


def test_scrub_does_not_scrub_a_forced_filesystem(monkeypatch, capsys):
    # It would be scrubbed read-only (statvfs says read-only) and could end "finished, OK".
    fake = FakeBtrfs(["/mnt/a", "/mnt/b"], polls=1).install(monkeypatch, statbtrfs)
    install_mountinfo(monkeypatch, statbtrfs, [FORCED, mountinfo_line("/mnt/b", n=41)])
    code = _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert [m for m, _ in fake.started] == ["/mnt/b"]
    assert "Could not start scrub on /mnt/a: forced read-only after an error, not scrubbed" in out
    assert "/mnt/a: failed to start: forced read-only after an error, not scrubbed" in out
    assert "/mnt/b: finished, OK" in out
    assert code == statbtrfs.EXIT_PROBLEMS
