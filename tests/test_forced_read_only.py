"""A btrfs the kernel forced read-only after an error: reported in every mode, never scrubbed as healthy."""
import errno

import pytest

import statbtrfs
from fakes import (
    FakeBtrfs,
    SCRUB_FAILED_LOCKED_WARNING,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_OLD_INTERRUPTED,
    STATS_NONZERO,
    STATS_ZERO,
    install_mountinfo,
    install_status,
    make_show,
    mountinfo_line,
    uuid_for,
)

# The unpatched reader (conftest serves an empty mountinfo to everything else).
read_mountinfo = getattr(statbtrfs, "read_mountinfo", None)
real_start_sync_errno = getattr(statbtrfs, "start_sync_errno", None)

FORCED = mountinfo_line("/mnt/a", "rw,relatime", "ro,space_cache")
ON_PURPOSE = mountinfo_line("/mnt/a", "ro,relatime", "ro,space_cache")
HEALTHY = mountinfo_line("/mnt/a")


@pytest.fixture(autouse=True)
def _btrfs_says_forced(monkeypatch):
    """BTRFS_IOC_START_SYNC on a mount reading rw on a read-only filesystem: EROFS, as on a forced one."""
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: errno.EROFS, raising=False)


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
# `mount -o remount,ro` of one of two mounts: the other keeps rw on a read-only filesystem, as when forced, so
# it is a candidate; BTRFS_IOC_START_SYNC then tells (EL7: success here, EROFS on a forced one).
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
    assert rows[0][0] == f"{statbtrfs.RED}forced read-only{statbtrfs.RESET}: /mnt/a"
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
    assert rows[0][0].endswith(": /mnt/a, /mnt/a2")


def test_unreadable_mountinfo_says_it_was_not_checked(monkeypatch, capsys):
    _status(monkeypatch, "/mnt/a")
    install_mountinfo(monkeypatch, statbtrfs, None)
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE
    assert "Could not read /proc/self/mountinfo: not checked whether a filesystem was forced read-only" in \
        capsys.readouterr().out


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


# --- the ioctl tells a forced filesystem from one remounted read-only ---------------

def test_a_remounted_read_only_filesystem_is_not_forced(monkeypatch, capsys):
    # BTRFS_IOC_START_SYNC succeeds there: the mountinfo candidate is not reported, like a mount -o ro.
    _status(monkeypatch, "/mnt/a")
    install_mountinfo(monkeypatch, statbtrfs, [FORCED])
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: 0)
    assert _run(monkeypatch, []) == statbtrfs.EXIT_OK
    assert "forced" not in capsys.readouterr().out


@pytest.mark.parametrize("error", [errno.EPERM, errno.ENOTTY, errno.ENOENT, errno.EIO])
def test_a_candidate_the_ioctl_cannot_tell_about_is_exit_2(monkeypatch, capsys, error):
    _status(monkeypatch, "/mnt/a")
    install_mountinfo(monkeypatch, statbtrfs, [FORCED])
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: error)
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE
    out = capsys.readouterr().out
    assert "/mnt/a: read-only, though mounted read-write, and btrfs could not be asked whether it was forced" in out
    assert "forced read-only:" not in out


def test_the_first_mount_that_answers_decides(monkeypatch):
    install_status(monkeypatch, statbtrfs, {
        "/mnt/a": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK),
        "/mnt/b": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK),
    })
    install_mountinfo(monkeypatch, statbtrfs, [FORCED, mountinfo_line("/mnt/b", "rw,relatime", "ro,space_cache", n=41)])
    asked = []
    answers = {"/mnt/a": errno.EPERM, "/mnt/b": errno.EROFS}
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: asked.append(mount) or answers[mount])
    assert _run(monkeypatch, []) == statbtrfs.EXIT_PROBLEMS
    assert asked == ["/mnt/a", "/mnt/b"]


def test_only_candidates_are_asked(monkeypatch):
    _status(monkeypatch, "/mnt/a", "/mnt/b")
    install_mountinfo(monkeypatch, statbtrfs, [ON_PURPOSE, mountinfo_line("/mnt/b", n=41)])
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: pytest.fail("asked " + mount))
    assert _run(monkeypatch, []) == statbtrfs.EXIT_OK


def test_start_sync_errno_is_the_errno_of_open_or_the_ioctl(tmp_path):
    real = real_start_sync_errno
    assert real(str(tmp_path / "missing")) == errno.ENOENT
    assert real(str(tmp_path)) in (errno.ENOTTY, errno.EINVAL, errno.ENOSYS, errno.EOPNOTSUPP)  # not a btrfs
    assert statbtrfs.BTRFS_IOC_START_SYNC == 0x80089418


def test_a_scrub_does_not_start_on_a_remounted_read_only_filesystem_as_forced(monkeypatch, capsys):
    fake = FakeBtrfs(["/mnt/a"], polls=1).install(monkeypatch, statbtrfs)
    install_mountinfo(monkeypatch, statbtrfs, [FORCED])
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: 0)
    _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    assert [m for m, _ in fake.started] == ["/mnt/a"]
    assert "forced" not in capsys.readouterr().out


# --- -d skips the scrub, never the check ----------------------------------------

def _recent(monkeypatch):
    """SCRUB_FINISHED_OK's scrub finished a day ago."""
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 24 * 3600)
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: None)


def _skipped_fs(monkeypatch, stats):
    _recent(monkeypatch)
    install_status(monkeypatch, statbtrfs, {"/mnt/a": (make_show(uuid_for(1)), stats, SCRUB_FINISHED_OK)})


@pytest.mark.parametrize("argv", [["-d", "7"], ["-s", "-d", "7", "--scrub_command_lockout", "0", "-i", "1"],
                                  ["-w", "-d", "7"]], ids=["plain", "scrub", "watch"])
def test_d_does_not_hide_a_forced_filesystem(monkeypatch, capsys, argv):
    _skipped_fs(monkeypatch, STATS_ZERO)
    install_mountinfo(monkeypatch, statbtrfs, [FORCED])
    assert _run(monkeypatch, argv) == statbtrfs.EXIT_PROBLEMS
    out = capsys.readouterr().out
    assert "/mnt/a: read-only, though mounted read-write" in out
    assert "nothing to do" not in out


@pytest.mark.parametrize("argv", [["-d", "7"], ["-s", "-d", "7", "--scrub_command_lockout", "0", "-i", "1"],
                                  ["-w", "-d", "7"]], ids=["plain", "scrub", "watch"])
def test_d_does_not_hide_device_errors(monkeypatch, capsys, argv):
    _skipped_fs(monkeypatch, STATS_NONZERO)
    assert _run(monkeypatch, argv) == statbtrfs.EXIT_PROBLEMS
    assert "nothing to do" not in capsys.readouterr().out


def test_d_with_a_healthy_skipped_filesystem_still_says_nothing_to_do(monkeypatch, capsys):
    _skipped_fs(monkeypatch, STATS_ZERO)
    assert _run(monkeypatch, ["-d", "7"]) == statbtrfs.EXIT_OK
    assert "nothing to do" in capsys.readouterr().out


def test_d_lists_a_skipped_problem_beside_the_kept_and_not_a_healthy_skipped(monkeypatch):
    _recent(monkeypatch)
    install_status(monkeypatch, statbtrfs, {
        "/mnt/a": (make_show(uuid_for(1)), STATS_NONZERO, SCRUB_FINISHED_OK),   # skipped, device errors
        "/mnt/b": (make_show(uuid_for(2)), STATS_ZERO, SCRUB_NEVER),            # kept
        "/mnt/c": (make_show(uuid_for(3)), STATS_ZERO, SCRUB_FINISHED_OK),      # skipped, healthy
    })
    rows = []
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda r, header=None: rows.extend(r) or "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-d", "7"])
    assert statbtrfs.main() == statbtrfs.EXIT_PROBLEMS
    assert sorted(row[0] for row in rows) == ["/mnt/a", "/mnt/b"]


# -d reads a skipped filesystem as a one-shot read does: again while a reading tells nothing.

def _skipped_with_replies(monkeypatch, replies):
    """/mnt/a scrubbed a day ago; its status polls answer ``replies`` in turn (the first is -d's own filter)."""
    _recent(monkeypatch)
    return FakeBtrfs(["/mnt/a"], finished=["/mnt/a"], replies={"/mnt/a": replies}).install(monkeypatch, statbtrfs)


@pytest.mark.parametrize("reading", [SCRUB_FAILED_LOCKED_WARNING, SCRUB_OLD_INTERRUPTED],
                         ids=["locked", "interrupted"])
def test_d_reads_a_skipped_filesystem_again_after_a_reading_that_tells_nothing(monkeypatch, capsys, reading):
    fake = _skipped_with_replies(monkeypatch, [None, reading])
    assert _run(monkeypatch, ["-d", "7"]) == statbtrfs.EXIT_OK
    assert fake.status_polls == 3  # the filter, the check, its re-read
    assert "nothing to do" in capsys.readouterr().out


def test_d_with_a_skipped_status_that_stays_unknown_exits_2(monkeypatch, capsys):
    fake = _skipped_with_replies(monkeypatch, [None] + [SCRUB_FAILED_LOCKED_WARNING] * 9)
    assert _run(monkeypatch, ["-d", "7"]) == statbtrfs.EXIT_FAILURE
    assert fake.status_polls == 5  # the filter, the check, 3 re-reads
    assert "Could not read the scrub status of /mnt/a." in capsys.readouterr().out


# --- the ioctl answers for the whole filesystem ------------------------------------

def _two_mounts():
    return {"uuid": uuid_for(1), "mounts": ["/mnt/a", "/mnt/b"]}


@pytest.mark.parametrize("other, forced", [(0, False), (errno.EROFS, True), (errno.EACCES, statbtrfs.UNTOLD)],
                         ids=["ok", "erofs", "none-answers"])
def test_a_candidate_that_cannot_be_opened_leaves_it_to_the_filesystems_other_mounts(monkeypatch, other, forced):
    # As a user who can't enter /mnt/a (mode 700 root: EACCES), /mnt/b answers for the filesystem.
    asked = []
    answers = {"/mnt/a": errno.EACCES, "/mnt/b": other}
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: asked.append(mount) or answers[mount])
    assert statbtrfs.forced_state(_two_mounts(), {"/mnt/a"}) == forced
    assert asked == ["/mnt/a", "/mnt/b"]


def test_a_filesystem_with_no_candidate_is_not_asked(monkeypatch):
    monkeypatch.setattr(statbtrfs, "start_sync_errno", lambda mount: pytest.fail("asked " + mount))
    assert statbtrfs.forced_state(_two_mounts(), set()) is False


# --- the -s summary names what -d skipped, and the mountinfo note comes once ----------

def test_scrub_summary_names_a_skipped_filesystem_whose_problem_sets_the_exit_code(monkeypatch, capsys):
    class Fake(FakeBtrfs):
        def _answer(self, command):  # /mnt/a has device errors
            if command[:3] == ["btrfs", "device", "stats"] and command[-1] == "/mnt/a":
                return list(STATS_NONZERO)
            return super()._answer(command)

    _recent(monkeypatch)
    fake = Fake(["/mnt/a", "/mnt/b"], polls=1, finished=["/mnt/a"]).install(monkeypatch, statbtrfs)
    code = _run(monkeypatch, ["-s", "-d", "7", "--scrub_command_lockout", "0", "-i", "1"])
    out = capsys.readouterr().out
    assert [m for m, _ in fake.started] == ["/mnt/b"]          # /mnt/a is skipped
    assert "All scrubs finished" not in out
    assert "Scrubs ended; 1 skipped by -d need attention." in out
    assert "/mnt/a: skipped by -d, but it has a problem: see the table above" in out
    assert "/mnt/b: finished, OK" in out
    assert code == statbtrfs.EXIT_PROBLEMS


def test_unreadable_mountinfo_is_noted_once_per_run_with_d(monkeypatch, capsys):
    _recent(monkeypatch)
    install_status(monkeypatch, statbtrfs, {
        "/mnt/a": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK),   # skipped
        "/mnt/b": (make_show(uuid_for(2)), STATS_ZERO, SCRUB_FINISHED_OK),   # skipped
        "/mnt/c": (make_show(uuid_for(3)), STATS_ZERO, SCRUB_NEVER),         # kept
    })
    install_mountinfo(monkeypatch, statbtrfs, None)
    assert _run(monkeypatch, ["-d", "7"]) == statbtrfs.EXIT_FAILURE
    assert capsys.readouterr().out.count("Could not read /proc/self/mountinfo") == 1
