import time

import statbtrfs
from fakes import SCRUB_FINISHED_OK, SCRUB_NEVER, SCRUB_RUNNING, CommandMap, install_command_map


def test_filter_recent_days_nonpositive_noop(monkeypatch):
    mounts = {"/mnt/a", "/mnt/b"}
    kept, skipped = statbtrfs.filter_recently_scrubbed_mounts(mounts, 0)
    assert kept == mounts
    assert skipped == []
    kept, skipped = statbtrfs.filter_recently_scrubbed_mounts(mounts, -1)
    assert kept == mounts
    assert skipped == []


def test_filter_recent_skips_finished_within_window(monkeypatch):
    # SCRUB_FINISHED_OK time is May 2 2024 — freeze "now" to a few days later
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 2 * 24 * 3600)

    def fake_exec(command, wait=True):
        return list(SCRUB_FINISHED_OK)

    monkeypatch.setattr(statbtrfs, "execute_command", fake_exec)
    kept, skipped = statbtrfs.filter_recently_scrubbed_mounts({"/mnt/a"}, 7)
    assert kept == set()
    assert skipped == ["/mnt/a"]


def test_filter_recent_keeps_old_finished(monkeypatch):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 30 * 24 * 3600)
    monkeypatch.setattr(statbtrfs, "execute_command", lambda *a, **k: list(SCRUB_FINISHED_OK))
    kept, skipped = statbtrfs.filter_recently_scrubbed_mounts({"/mnt/a"}, 7)
    assert kept == {"/mnt/a"}
    assert skipped == []


def test_filter_recent_keeps_never_and_running(monkeypatch):
    responses = {
        "/mnt/never": SCRUB_NEVER,
        "/mnt/run": SCRUB_RUNNING,
    }

    def fake_exec(command, wait=True):
        mount = command[-1]
        return list(responses[mount])

    monkeypatch.setattr(statbtrfs, "execute_command", fake_exec)
    kept, skipped = statbtrfs.filter_recently_scrubbed_mounts({"/mnt/never", "/mnt/run"}, 7)
    assert kept == {"/mnt/never", "/mnt/run"}
    assert skipped == []
