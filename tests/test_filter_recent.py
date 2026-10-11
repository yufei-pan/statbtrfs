import statbtrfs
from fakes import SCRUB_FINISHED_OK, SCRUB_NEVER, SCRUB_RUNNING


def _fs(*mounts):
    return {"uuid": None, "mounts": list(mounts)}


def _serve_scrub_status(monkeypatch, responses):
    def fake_exec(command, wait=True):
        return list(responses[command[-1]])

    def fake_execs(commands, wait=True):
        return [fake_exec(c) for c in commands]

    monkeypatch.setattr(statbtrfs, "execute_command", fake_exec)
    monkeypatch.setattr(statbtrfs, "execute_commands", fake_execs)


def test_filter_recent_days_nonpositive_noop(monkeypatch):
    filesystems = [_fs("/mnt/a"), _fs("/mnt/b")]
    assert statbtrfs.filter_recently_scrubbed(filesystems, 0) == (filesystems, [])
    assert statbtrfs.filter_recently_scrubbed(filesystems, -1) == (filesystems, [])


def test_filter_recent_skips_finished_within_window(monkeypatch):
    # SCRUB_FINISHED_OK time is May 2 2024 — freeze "now" to a few days later
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 2 * 24 * 3600)
    _serve_scrub_status(monkeypatch, {"/mnt/a": SCRUB_FINISHED_OK})
    fs = _fs("/mnt/a", "/mnt/a2")
    assert statbtrfs.filter_recently_scrubbed([fs], 7) == ([], [fs])


def test_filter_recent_keeps_old_finished(monkeypatch):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 30 * 24 * 3600)
    _serve_scrub_status(monkeypatch, {"/mnt/a": SCRUB_FINISHED_OK})
    fs = _fs("/mnt/a")
    assert statbtrfs.filter_recently_scrubbed([fs], 7) == ([fs], [])


def test_filter_recent_keeps_never_and_running(monkeypatch):
    _serve_scrub_status(monkeypatch, {"/mnt/never": SCRUB_NEVER, "/mnt/run": SCRUB_RUNNING})
    filesystems = [_fs("/mnt/never"), _fs("/mnt/run")]
    assert statbtrfs.filter_recently_scrubbed(filesystems, 7) == (filesystems, [])
