"""Exit codes, colour, buffering and the redraw screen (#4)."""
import functools

import pytest

import statbtrfs
from fakes import (
    SCRUB_FINISHED_ERRORS,
    SCRUB_FINISHED_OK,
    SHOW_DEGRADED,
    SHOW_INCOMPLETE,
    STATS_MULTI_DEVICE,
    STATS_ZERO,
    install_status,
    make_show,
    uuid_for,
)

HEALTHY = (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_OK)


def _run(monkeypatch, argv, table=True):
    if table:
        monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"] + argv)
    return statbtrfs.main()


def _tty(monkeypatch, is_tty):
    monkeypatch.setattr(statbtrfs.sys.stdout, "isatty", lambda: is_tty, raising=False)


# --- exit codes ---------------------------------------------------------------

def test_exit_ok_when_healthy(monkeypatch):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": HEALTHY})
    assert _run(monkeypatch, []) == statbtrfs.EXIT_OK == 0


@pytest.mark.parametrize(
    "status",
    [
        (make_show(uuid_for(1), "/dev/nvme0n1", "/dev/nvme1n1"), STATS_MULTI_DEVICE, SCRUB_FINISHED_OK),
        (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_ERRORS),
        (SHOW_DEGRADED, STATS_ZERO, SCRUB_FINISHED_OK),
    ],
    ids=["device-errors", "scrub-errors", "degraded"],
)
def test_exit_problems_found(monkeypatch, status):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": status, "/mnt/b": (make_show(uuid_for(2)),) + HEALTHY[1:]})
    assert _run(monkeypatch, []) == statbtrfs.EXIT_PROBLEMS == 1


def test_exit_failure_when_no_mounts(monkeypatch):
    install_status(monkeypatch, statbtrfs, {})
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE == 2


def test_exit_failure_when_pattern_matches_nothing(monkeypatch):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": HEALTHY})
    assert _run(monkeypatch, ["nothing-matches"]) == statbtrfs.EXIT_FAILURE


def test_exit_failure_when_a_filesystem_cannot_be_read(monkeypatch):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": HEALTHY, "/mnt/b": (SHOW_INCOMPLETE, STATS_ZERO, SCRUB_FINISHED_OK)})
    assert _run(monkeypatch, []) == statbtrfs.EXIT_FAILURE


def test_problems_take_precedence_over_failures(monkeypatch):
    install_status(monkeypatch, statbtrfs, {
        "/mnt/a": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_ERRORS),
        "/mnt/b": (SHOW_INCOMPLETE, STATS_ZERO, SCRUB_FINISHED_OK),
    })
    assert _run(monkeypatch, []) == statbtrfs.EXIT_PROBLEMS


def test_exclude_recent_skipping_everything_is_ok(monkeypatch, capsys):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 24 * 3600)
    install_status(monkeypatch, statbtrfs, {"/mnt/a": HEALTHY})
    assert _run(monkeypatch, ["-d", "7"]) == statbtrfs.EXIT_OK
    out = capsys.readouterr().out
    assert "Skipping mounts scrubbed within the last 7d: /mnt/a" in out
    assert "nothing to do" in out


# --- colour --------------------------------------------------------------------

@pytest.mark.parametrize(
    "mode,is_tty,no_color,expected",
    [
        ("always", False, "1", True),
        ("never", True, None, False),
        ("auto", True, None, True),
        ("auto", True, "1", False),
        ("auto", True, "", True),  # NO_COLOR only counts when non-empty
        ("auto", False, None, False),
    ],
)
def test_resolve_color(monkeypatch, mode, is_tty, no_color, expected):
    _tty(monkeypatch, is_tty)
    if no_color is None:
        monkeypatch.delenv("NO_COLOR", raising=False)
    else:
        monkeypatch.setenv("NO_COLOR", no_color)
    assert statbtrfs.resolve_color(mode) is expected


def _errors_table(monkeypatch, argv, capsys):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": (make_show(uuid_for(1)), STATS_ZERO, SCRUB_FINISHED_ERRORS)})
    _run(monkeypatch, argv, table=False)
    return capsys.readouterr().out


def test_color_never_prints_no_escape_codes(monkeypatch, capsys):
    out = _errors_table(monkeypatch, ["--color=never"], capsys)
    assert "csum=3" in out
    assert "\033[" not in out


def test_color_always_prints_escape_codes(monkeypatch, capsys):
    out = _errors_table(monkeypatch, ["--color", "always"], capsys)
    assert "\033[91m" in out


def test_reexec_passes_the_color_decision_on(monkeypatch):
    # sudo drops NO_COLOR and may allocate its own pty, so decide before re-exec.
    install_status(monkeypatch, statbtrfs, {})
    seen = []
    monkeypatch.setattr(statbtrfs, "acquire_root", lambda argv: seen.append(argv))
    _tty(monkeypatch, False)
    _run(monkeypatch, ["-s", "pool"])
    assert seen == [["--color=never", "-s", "pool"]]


# --- buffering ------------------------------------------------------------------

def test_print_flushes_every_line():
    assert isinstance(statbtrfs.print, functools.partial)
    assert statbtrfs.print.keywords == {"flush": True}


# --- redraw ---------------------------------------------------------------------

def test_screen_appends_without_redraw(capsys):
    screen = statbtrfs.Screen(redraw=False)
    screen.event("started /mnt/a")
    screen.show("TABLE", notes=["note"])
    assert capsys.readouterr().out == "started /mnt/a\nTABLE\nnote\n"


def test_screen_redraw_clears_and_keeps_recent_messages(capsys):
    screen = statbtrfs.Screen(redraw=True)
    screen.event("started /mnt/a")
    assert capsys.readouterr().out == ""  # held for the next frame
    screen.show("TABLE", notes=["note"])
    assert capsys.readouterr().out == statbtrfs.CLEAR_SCREEN + "TABLE\n\nnote\nstarted /mnt/a\n"


def test_screen_redraw_keeps_only_the_last_messages(capsys):
    screen = statbtrfs.Screen(redraw=True)
    for i in range(statbtrfs.EVENT_LINES + 3):
        screen.event(f"m{i}")
    screen.show("TABLE")
    out = capsys.readouterr().out
    assert "m2\n" not in out and "m3\n" in out


def _scrub_run(monkeypatch, capsys, is_tty):
    install_status(monkeypatch, statbtrfs, {"/mnt/a": HEALTHY})
    monkeypatch.setattr(statbtrfs, "start_scrub", lambda mount: ("started", ""))
    clock = {"now": 1_000_000.0}
    monkeypatch.setattr(statbtrfs.time, "time", lambda: clock["now"])
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: clock.__setitem__("now", clock["now"] + s))
    _tty(monkeypatch, is_tty)
    _run(monkeypatch, ["-s", "--scrub_command_lockout", "0", "-i", "1"])
    return capsys.readouterr().out


def test_scrub_redraws_in_place_on_a_terminal(monkeypatch, capsys):
    assert statbtrfs.CLEAR_SCREEN in _scrub_run(monkeypatch, capsys, is_tty=True)


def test_scrub_appends_when_not_a_terminal(monkeypatch, capsys):
    assert statbtrfs.CLEAR_SCREEN not in _scrub_run(monkeypatch, capsys, is_tty=False)


def test_screen_flush_prints_held_messages_once(capsys):
    screen = statbtrfs.Screen(redraw=True)
    screen.event("skipping /mnt/a")
    screen.flush()
    screen.flush()
    assert capsys.readouterr().out == "skipping /mnt/a\n"
