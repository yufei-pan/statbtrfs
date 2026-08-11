# statbtrfs Hybrid Test Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete hybrid pytest suite for `statbtrfs` (offline unit coverage of parsers/CLI/full scrub orchestration + optional status-only live smoke) with an 85% line-coverage floor.

**Architecture:** Flat `tests/` package mirroring `statblk`: shared `fakes.py`/`conftest.py`, focused modules per concern, default `pytest` excluding `live`. Stub `statbtrfs.execute_command` / `execute_commands` and `time.*`. One small production tweak: defer import-time sudo exit so tests can import the module.

**Tech Stack:** Python 3.6+, pytest, pytest-cov, monkeypatch; production module `statbtrfs.py` + dependency `multiCMD`.

**Spec:** `docs/superpowers/specs/2026-08-11-statbtrfs-test-suite-design.md`

## Global Constraints

- Do not change runtime `setup.py` `install_requires` for test deps; use `requirements-dev.txt`.
- Do not enable global `--doctest-modules` (embedded multiCMD blob must not be scanned).
- Default `addopts` must exclude `live`.
- Unit tests: no root, no real btrfs dependence, never call real `btrfs scrub start`.
- Live tests: status-only; never pass `-s` / never issue scrub start.
- Plain `test_*` functions (CAS sibling style); no unittest TestCase classes.
- Do not bump package version solely for adding tests.
- Prefer monkeypatching `statbtrfs.execute_command` / `execute_commands` / `time.*`.
- Public CLI flags and user-facing messages stay the same aside from moving the sudo probe off import.
- Coverage success: `pytest --cov=statbtrfs --cov-fail-under=85`.

## File Structure

| File | Responsibility |
|------|----------------|
| `pytest.ini` | testpaths, `live` marker, default addopts |
| `requirements-dev.txt` | pytest, pytest-cov |
| `tests/conftest.py` | sys.path, markers, live skip helpers |
| `tests/fakes.py` | sample command outputs + `CommandMap` stub |
| `tests/test_import_seams.py` | import works without sudo exit; privilege helper |
| `tests/test_parse_show.py` | `parse_show_info` |
| `tests/test_parse_stats.py` | `parse_device_stats` |
| `tests/test_parse_scrub.py` | `parse_scrub_status`, `parse_scrub_time_to_epoch` |
| `tests/test_color.py` | `color_error_count` |
| `tests/test_mounts.py` | `find_btrfs_mounts` |
| `tests/test_filter_recent.py` | `filter_recently_scrubbed_mounts` |
| `tests/test_cli.py` | `main()` status / argv paths |
| `tests/test_scrub_orchestration.py` | `issue_scrub_command` + `-s` loop |
| `tests/test_live.py` | `@pytest.mark.live` status smoke |
| `statbtrfs.py` | lazy/guarded sudo probe only |
| `README.txt` | Development: how to run tests |

---

### Task 1: Scaffold + import-safe sudo seam

**Files:**
- Create: `pytest.ini`
- Create: `requirements-dev.txt`
- Create: `tests/conftest.py`
- Create: `tests/fakes.py`
- Create: `tests/test_import_seams.py`
- Modify: `statbtrfs.py` (sudo probe only — around lines 105–113 and call sites in `execute_command` / `execute_commands`)

**Interfaces:**
- Consumes: `statbtrfs` importable from repo root
- Produces:
  - `statbtrfs.ensure_privileges()` — no-op if root or already checked; if `USE_SUDO` and `which sudo` fails, print existing message and `sys.exit(1)`
  - `fakes.CommandMap(mapping=None, default=None)` with:
    - `.calls: list` of `("cmd", command_list, wait)` / `("cmds", list_of_command_lists, wait)`
    - `.execute_command(command, wait=True) -> list`
    - `.execute_commands(commands, wait=True) -> list` (one result per command)
    - Lookup: exact `tuple(command)` after stripping a leading `"sudo"` if present; else `default` (default `[]`)
  - Fixture constants listed in Step 3

- [ ] **Step 1: Write failing import/seam test**

Create `tests/test_import_seams.py`:

```python
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
```

Add `import pytest` at top.

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /mnt/klein/work/cas/statbtrfs
pip install -q 'pytest>=7,<9' 'pytest-cov>=4,<6'
# Without conftest yet, run via PYTHONPATH:
PYTHONPATH=. pytest tests/test_import_seams.py -v
```

Expected: FAIL (missing `ensure_privileges` and/or import-time `SystemExit` if sudo missing in env). If import already succeeds on this host because sudo exists, still expect `AttributeError: ensure_privileges`.

- [ ] **Step 3: Write scaffold files**

`pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
markers =
    live: soft smoke against real host btrfs (status only; deselect by default)
addopts = -m "not live"
```

`requirements-dev.txt`:
```
pytest>=7,<9
pytest-cov>=4,<6
```

`tests/conftest.py`:
```python
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: soft smoke against real host btrfs (status only)",
    )


def skip_unless_live_btrfs():
    if sys.platform != "linux":
        pytest.skip("Linux only")
    if not shutil.which("btrfs"):
        pytest.skip("btrfs binary required")
    import statbtrfs

    mounts = statbtrfs.find_btrfs_mounts([])
    if not mounts:
        pytest.skip("no btrfs mounts")
```

`tests/fakes.py`:
```python
MOUNT_LINES_MULTI = [
    "/dev/sda1 on /mnt/a type btrfs (rw,relatime)",
    "/dev/sdb1 on /mnt/b type btrfs (rw,relatime)",
    "/dev/sdc1 on /data type btrfs (rw,relatime)",
]

MOUNT_LINES_SINGLE = [
    "/dev/sda1 on /mnt/a type btrfs (rw,relatime)",
]

SHOW_SINGLE = [
    "Label: none  uuid: 11111111-2222-3333-4444-555555555555",
    "Total devices 1 FS bytes used 12.34GiB",
    "devid    1 size 100.00GiB used 50.00GiB path /dev/sda1",
]

SHOW_MULTI_DEVICE = [
    "Label: none  uuid: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "Total devices 2 FS bytes used 1.00GiB",
    "devid    1 size 10.00GiB used 2.00GiB path /dev/nvme0n1",
    "devid    2 size 10.00GiB used 2.00GiB path /dev/nvme1n1",
]

SHOW_INCOMPLETE = [
    "Label: none  uuid: 11111111-2222-3333-4444-555555555555",
    "Total devices 1 FS bytes used 1.00GiB",
]

STATS_ZERO = [
    "[/dev/sda1].write_io_errs    0",
    "[/dev/sda1].read_io_errs     0",
    "[/dev/sda1].flush_io_errs    0",
    "[/dev/sda1].corruption_errs  0",
    "[/dev/sda1].generation_errs  0",
]

STATS_NONZERO = [
    "[/dev/sda1].write_io_errs    0",
    "[/dev/sda1].read_io_errs     3",
    "[/dev/sda1].corruption_errs  12",
    "[/dev/sda1].generation_errs  1",
    "not-a-stat-line",
]

SCRUB_NEVER = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "no stats available",
]

SCRUB_FINISHED_OK = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           finished",
    "Duration:         0:10:00",
    "Total to scrub:   10.00GiB",
    "Rate:             17.00MiB/s",
    "Error summary:    no errors found",
]

SCRUB_RUNNING = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           running",
    "Time left:        0:05:00",
    "Total to scrub:   100.00GiB",
    "Bytes scrubbed:   40.00GiB",
    "Rate:             20.00MiB/s",
    "Error summary:    no errors found",
]

SCRUB_FINISHED_ERRORS = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           finished",
    "Duration:         0:10:00",
    "Total to scrub:   10.00GiB",
    "Rate:             17.00MiB/s",
    "Error summary:    csum=3",
    "  Corrected:      0",
    "  Uncorrectable:  3",
    "  Unverified:     0",
]

SCRUB_TIME_BASIC = "Thu May  2 09:56:55 2024"
SCRUB_TIME_ISO = "2024-05-02 09:56:55"


class CommandMap:
    """Stub for execute_command / execute_commands."""

    def __init__(self, mapping=None, default=None):
        self.mapping = dict(mapping or {})
        self.default = [] if default is None else list(default)
        self.calls = []

    @staticmethod
    def _norm(command):
        cmd = tuple(command)
        if cmd and cmd[0] == "sudo":
            cmd = cmd[1:]
        return cmd

    def _lookup(self, command):
        key = self._norm(command)
        if key in self.mapping:
            return list(self.mapping[key])
        return list(self.default)

    def execute_command(self, command, wait=True):
        self.calls.append(("cmd", list(command), wait))
        return self._lookup(command)

    def execute_commands(self, commands, wait=True):
        self.calls.append(("cmds", [list(c) for c in commands], wait))
        return [self._lookup(c) for c in commands]


def install_command_map(monkeypatch, command_map, module):
    monkeypatch.setattr(module, "execute_command", command_map.execute_command)
    monkeypatch.setattr(module, "execute_commands", command_map.execute_commands)
    return command_map
```

- [ ] **Step 4: Implement sudo seam in `statbtrfs.py`**

Replace the import-time block:

```python
USE_SUDO = True
if os.geteuid() == 0:
    USE_SUDO = False

if USE_SUDO:
    #check if sudo is available
    if multiCMD.run_command(['which','sudo'],quiet=True,return_code_only=True):
        print(f"{RED}sudo is required to run this script.{RESET}")
        sys.exit(1)
```

with:

```python
USE_SUDO = os.geteuid() != 0
_SUDO_CHECKED = False

def ensure_privileges():
    """Fail fast if non-root and sudo is unavailable. Safe to call repeatedly."""
    global _SUDO_CHECKED
    if not USE_SUDO or _SUDO_CHECKED:
        return
    _SUDO_CHECKED = True
    if multiCMD.run_command(['which', 'sudo'], quiet=True, return_code_only=True):
        print(f"{RED}sudo is required to run this script.{RESET}")
        sys.exit(1)
```

At the start of both `execute_command` and `execute_commands`, call `ensure_privileges()` before prepending sudo / running.

Do not change CLI flags, messages, or scrub logic.

- [ ] **Step 5: Run seam tests to verify they pass**

```bash
cd /mnt/klein/work/cas/statbtrfs
pytest tests/test_import_seams.py -v
```

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add pytest.ini requirements-dev.txt tests/conftest.py tests/fakes.py tests/test_import_seams.py statbtrfs.py
git commit -m "$(cat <<'EOF'
Add pytest scaffold and defer sudo check off import.

EOF
)"
```

---

### Task 2: Parser unit tests (show, stats, color)

**Files:**
- Create: `tests/test_parse_show.py`
- Create: `tests/test_parse_stats.py`
- Create: `tests/test_color.py`

**Interfaces:**
- Consumes: `fakes.SHOW_*`, `STATS_*`; `statbtrfs.parse_show_info`, `parse_device_stats`, `color_error_count`, color constants
- Produces: none (tests only)

- [ ] **Step 1: Write failing parser tests**

`tests/test_parse_show.py`:
```python
import statbtrfs
from fakes import SHOW_INCOMPLETE, SHOW_MULTI_DEVICE, SHOW_SINGLE


def test_parse_show_single_device():
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_SINGLE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "12.34GiB"
    assert device_path == "/dev/sda1"


def test_parse_show_multi_device_paths_joined():
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_MULTI_DEVICE)
    assert uuid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert fs_used == "1.00GiB"
    assert device_path == "/dev/nvme0n1, /dev/nvme1n1"


def test_parse_show_incomplete_returns_nones(capsys):
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_INCOMPLETE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "1.00GiB"
    assert device_path is None
    out = capsys.readouterr().out
    assert "Could not parse btrfs show info" in out
```

`tests/test_parse_stats.py`:
```python
import statbtrfs
from fakes import STATS_NONZERO, STATS_ZERO


def test_parse_device_stats_zero():
    d = statbtrfs.parse_device_stats(STATS_ZERO)
    assert d["write_io_errs"] == "0"
    assert d["read_io_errs"] == "0"
    assert d["corruption_errs"] == "0"
    assert d["generation_errs"] == "0"


def test_parse_device_stats_skips_malformed_and_reads_nonzero():
    d = statbtrfs.parse_device_stats(STATS_NONZERO)
    assert d["read_io_errs"] == "3"
    assert d["corruption_errs"] == "12"
    assert d["generation_errs"] == "1"
    assert "not-a-stat-line" not in d


def test_parse_device_stats_empty():
    assert statbtrfs.parse_device_stats([]) == {}
```

`tests/test_color.py`:
```python
import statbtrfs


def test_color_error_count_thresholds():
    assert statbtrfs.GREEN in statbtrfs.color_error_count(0)
    assert statbtrfs.YELLOW in statbtrfs.color_error_count(1)
    assert statbtrfs.YELLOW in statbtrfs.color_error_count(9)
    assert statbtrfs.RED in statbtrfs.color_error_count(10)
    assert "0" in statbtrfs.color_error_count(0)
    assert "12" in statbtrfs.color_error_count(12)
```

- [ ] **Step 2: Run tests (expect PASS — pure existing functions)**

```bash
pytest tests/test_parse_show.py tests/test_parse_stats.py tests/test_color.py -v
```

Expected: PASS. If any fail, fix the test expectation to match actual parser behavior (do not change parsers unless they clearly contradict the spec’s documented behavior).

- [ ] **Step 3: Commit**

```bash
git add tests/test_parse_show.py tests/test_parse_stats.py tests/test_color.py
git commit -m "$(cat <<'EOF'
Add unit tests for show/stats parsers and error coloring.

EOF
)"
```

---

### Task 3: Scrub status + scrub time parsing

**Files:**
- Create: `tests/test_parse_scrub.py`

**Interfaces:**
- Consumes: `fakes.SCRUB_*`, `SCRUB_TIME_*`; `statbtrfs.parse_scrub_status`, `parse_scrub_time_to_epoch`, `GREEN`, `RED`
- Produces: none

- [ ] **Step 1: Write tests**

```python
from datetime import datetime

import statbtrfs
from fakes import (
    SCRUB_FINISHED_ERRORS,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_RUNNING,
    SCRUB_TIME_BASIC,
    SCRUB_TIME_ISO,
)


def test_parse_scrub_never_defaults():
    data = statbtrfs.parse_scrub_status(SCRUB_NEVER)
    assert data["scrub_status"] == "Never"
    assert data["scrub_time"] == "N/A"
    assert data["scrub_rate"] == "N/A"
    assert data["scrubbed_data"] == "N/A"
    assert data["error_summary"] == "N/A"


def test_parse_scrub_empty_defaults():
    data = statbtrfs.parse_scrub_status([])
    assert data["scrub_status"] == "Never"


def test_parse_scrub_finished_ok_uses_total_to_scrub():
    data = statbtrfs.parse_scrub_status(SCRUB_FINISHED_OK)
    assert data["scrub_status"] == "finished"
    assert data["scrub_time"] == "Thu May  2 09:56:55 2024"
    assert data["scrub_rate"] == "17.00MiB/s"
    assert data["scrubbed_data"] == "10.00GiB"
    assert "OK" in data["error_summary"]
    assert statbtrfs.GREEN in data["error_summary"]


def test_parse_scrub_running_uses_bytes_scrubbed():
    data = statbtrfs.parse_scrub_status(SCRUB_RUNNING)
    assert data["scrub_status"] == "running"
    assert data["scrubbed_data"] == "40.00GiB"


def test_parse_scrub_finished_with_errors_is_red():
    data = statbtrfs.parse_scrub_status(SCRUB_FINISHED_ERRORS)
    assert "csum=3" in data["error_summary"]
    assert statbtrfs.RED in data["error_summary"]


def test_parse_scrub_time_formats():
    epoch = statbtrfs.parse_scrub_time_to_epoch(SCRUB_TIME_BASIC)
    assert epoch == datetime.strptime(SCRUB_TIME_BASIC, "%a %b %d %H:%M:%S %Y").timestamp()
    epoch_iso = statbtrfs.parse_scrub_time_to_epoch(SCRUB_TIME_ISO)
    assert epoch_iso == datetime.strptime(SCRUB_TIME_ISO, "%Y-%m-%d %H:%M:%S").timestamp()
    assert statbtrfs.parse_scrub_time_to_epoch("N/A") is None
    assert statbtrfs.parse_scrub_time_to_epoch("not a time") is None
```

Note on `%Z` format: `strptime` with `%Z` is platform-dependent. Do **not** assert a timezone-suffixed string unless it parses on the host; the `None`/basic/ISO cases above are required. Optionally try `"Thu May  2 09:56:55 2024 UTC"` and accept either a float epoch or `None`.

- [ ] **Step 2: Run tests**

```bash
pytest tests/test_parse_scrub.py -v
```

Expected: PASS (adjust only if real parser splits differ — e.g. scrub_time capturing after first `:`).

- [ ] **Step 3: Commit**

```bash
git add tests/test_parse_scrub.py
git commit -m "$(cat <<'EOF'
Add unit tests for scrub status and scrub time parsing.

EOF
)"
```

---

### Task 4: Mount discovery + exclude-recent filtering

**Files:**
- Create: `tests/test_mounts.py`
- Create: `tests/test_filter_recent.py`

**Interfaces:**
- Consumes: `CommandMap`, `install_command_map`, mount/scrub fakes; `find_btrfs_mounts`, `filter_recently_scrubbed_mounts`
- Produces: none

- [ ] **Step 1: Write mount tests**

```python
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
```

- [ ] **Step 2: Write filter-recent tests**

```python
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
```

- [ ] **Step 3: Run tests**

```bash
pytest tests/test_mounts.py tests/test_filter_recent.py -v
```

Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_mounts.py tests/test_filter_recent.py
git commit -m "$(cat <<'EOF'
Add unit tests for mount discovery and recent-scrub filtering.

EOF
)"
```

---

### Task 5: CLI status path

**Files:**
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: `CommandMap` / `install_command_map`, fakes; `statbtrfs.main`
- Produces: none

- [ ] **Step 1: Write CLI tests**

```python
import pytest

import statbtrfs
from fakes import (
    MOUNT_LINES_MULTI,
    MOUNT_LINES_SINGLE,
    SCRUB_FINISHED_OK,
    SHOW_SINGLE,
    STATS_ZERO,
    CommandMap,
    install_command_map,
)


def _status_map_for_mounts(mount_lines, mounts_show_stats_scrub):
    """Build CommandMap for mount + per-mount show/stats/scrub triples."""
    mapping = {("mount", "-t", "btrfs"): mount_lines}
    # execute_commands looks up each subcommand individually via _lookup
    for mount, (show, stats, scrub) in mounts_show_stats_scrub.items():
        mapping[("btrfs", "filesystem", "show", mount)] = show
        mapping[("btrfs", "device", "stats", mount)] = stats
        mapping[("btrfs", "scrub", "status", mount)] = scrub
    return CommandMap(mapping=mapping)


def test_main_no_mounts_message(monkeypatch, capsys):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    statbtrfs.main()
    assert "No Btrfs mounts found." in capsys.readouterr().out


def test_main_status_prints_table_once(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        MOUNT_LINES_SINGLE,
        {"/mnt/a": (SHOW_SINGLE, STATS_ZERO, SCRUB_FINISHED_OK)},
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs"])
    sleeps = []
    monkeypatch.setattr(statbtrfs.time, "sleep", lambda s: sleeps.append(s))
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "TABLE" in out
    assert sleeps == []  # no -s => single pass, no sleep


def test_main_pattern_filters_mounts(monkeypatch, capsys):
    cm = _status_map_for_mounts(
        MOUNT_LINES_MULTI,
        {
            "/data": (SHOW_SINGLE, STATS_ZERO, SCRUB_FINISHED_OK),
        },
    )
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: f"ROWS={len(rows)}")
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "data"])
    statbtrfs.main()
    assert "ROWS=1" in capsys.readouterr().out


def test_main_version(monkeypatch):
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-V"])
    with pytest.raises(SystemExit) as ei:
        statbtrfs.main()
    assert ei.value.code == 0


def test_main_exclude_recent_prints_skip(monkeypatch, capsys):
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    monkeypatch.setattr(statbtrfs.time, "time", lambda: scrub_epoch + 24 * 3600)

    mapping = {
        ("mount", "-t", "btrfs"): MOUNT_LINES_SINGLE,
        ("btrfs", "scrub", "status", "/mnt/a"): list(SCRUB_FINISHED_OK),
    }
    cm = CommandMap(mapping=mapping, default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    monkeypatch.setattr(statbtrfs.sys, "argv", ["statbtrfs", "-d", "7"])
    statbtrfs.main()
    out = capsys.readouterr().out
    assert "Skipping mounts scrubbed within the last 7d" in out
    assert "/mnt/a" in out
    assert "No Btrfs mounts found." in out
```

- [ ] **Step 2: Run tests**

```bash
pytest tests/test_cli.py -v
```

Expected: PASS. If `pretty_format_table` signature differs, adapt the lambda to match `statbtrfs.main` call (`header=header`).

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "$(cat <<'EOF'
Add CLI unit tests for status path, patterns, version, and -d.

EOF
)"
```

---

### Task 6: Scrub orchestration (full mocked path)

**Files:**
- Create: `tests/test_scrub_orchestration.py`

**Interfaces:**
- Consumes: `CommandMap`, fakes, `issue_scrub_command`, `main`
- Produces: none

- [ ] **Step 1: Write `issue_scrub_command` generator test**

```python
import statbtrfs
from fakes import CommandMap, install_command_map


def test_issue_scrub_command_yields_cumulative_and_starts(monkeypatch):
    cm = CommandMap(default=[])
    install_command_map(monkeypatch, cm, statbtrfs)
    mounts = ["/mnt/a", "/mnt/b"]
    gen = statbtrfs.issue_scrub_command(mounts)
    assert next(gen) == ["/mnt/a"]
    assert next(gen) == ["/mnt/a", "/mnt/b"]
    starts = [c for c in cm.calls if c[0] == "cmd" and c[1][:3] == ["btrfs", "scrub", "start"]]
    assert [c[1][3] for c in starts] == ["/mnt/a", "/mnt/b"]
    assert all(c[2] is False for c in starts)  # wait=False
```

- [ ] **Step 2: Write full `-s` loop tests with controlled time + status transitions**

Use a mutable clock and per-mount scrub status that flips from `running` to `finished` after the first status poll wave.

```python
import pytest

import statbtrfs
from fakes import (
    MOUNT_LINES_MULTI,
    SCRUB_FINISHED_OK,
    SCRUB_NEVER,
    SCRUB_RUNNING,
    SHOW_SINGLE,
    STATS_ZERO,
    CommandMap,
    install_command_map,
)


def test_main_scrub_first_wave_respects_max_count(monkeypatch, capsys):
    mounts = ["/mnt/a", "/mnt/b", "/data"]
    # mount output order is not set order; provide all three lines
    mount_lines = [
        "/dev/sda1 on /mnt/a type btrfs (rw)",
        "/dev/sdb1 on /mnt/b type btrfs (rw)",
        "/dev/sdc1 on /data type btrfs (rw)",
    ]

    state = {"polls": 0}
    clock = {"now": 1_000_000.0}

    def fake_time():
        return clock["now"]

    def fake_sleep(seconds):
        clock["now"] += seconds

    def lookup(command, wait=True):
        cmd = tuple(command)
        if cmd[:3] == ("mount", "-t", "btrfs"):
            return mount_lines
        if cmd[:3] == ("btrfs", "scrub", "start"):
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return list(SHOW_SINGLE)
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        if cmd[:3] == ("btrfs", "scrub", "status"):
            state["polls"] += 1
            # First table poll(s): still running so loop continues; then finished
            if state["polls"] <= len(mounts):
                return list(SCRUB_RUNNING)
            return list(SCRUB_FINISHED_OK)
        return []

    started = []

    def execute_command(command, wait=True):
        if tuple(command)[:3] == ("btrfs", "scrub", "start"):
            started.append(command[3])
        return lookup(command, wait=wait)

    def execute_commands(commands, wait=True):
        return [lookup(c, wait=wait) for c in commands]

    monkeypatch.setattr(statbtrfs, "execute_command", execute_command)
    monkeypatch.setattr(statbtrfs, "execute_commands", execute_commands)
    monkeypatch.setattr(statbtrfs.time, "time", fake_time)
    monkeypatch.setattr(statbtrfs.time, "sleep", fake_sleep)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(
        statbtrfs.sys,
        "argv",
        ["statbtrfs", "-s", "-m", "2", "--scrub_command_lockout", "1", "-i", "1"],
    )

    # Force deterministic iteration order for the set of mounts by patching find_btrfs_mounts
    monkeypatch.setattr(statbtrfs, "find_btrfs_mounts", lambda patterns: set(mounts))
    # And make issue_scrub_command iterate a stable list:
    real_issue = statbtrfs.issue_scrub_command

    def stable_issue(ms):
        return real_issue(sorted(ms))

    monkeypatch.setattr(statbtrfs, "issue_scrub_command", stable_issue)

    statbtrfs.main()
    out = capsys.readouterr().out
    assert "All Scrubs finished." in out
    # First wave size 2; later wave should start the remaining mount
    assert len(started) == 3
    assert started[:2] == sorted(mounts)[:2]
    assert started[2] == sorted(mounts)[2]


def test_main_scrub_exclude_recent_never_starts_skipped(monkeypatch, capsys):
    # /mnt/new finished recently -> skipped by -d 7
    # /mnt/old never scrubbed -> kept and started
    scrub_epoch = statbtrfs.parse_scrub_time_to_epoch("Thu May  2 09:56:55 2024")
    clock = {"now": scrub_epoch + 24 * 3600}

    monkeypatch.setattr(statbtrfs.time, "time", lambda: clock["now"])

    def sleep_and_advance(s):
        clock["now"] += max(s, 1)

    monkeypatch.setattr(statbtrfs.time, "sleep", sleep_and_advance)

    started = []

    def execute_command(command, wait=True):
        cmd = tuple(command)
        if cmd[:3] == ("mount", "-t", "btrfs"):
            return [
                "/dev/sda1 on /mnt/old type btrfs (rw)",
                "/dev/sdb1 on /mnt/new type btrfs (rw)",
            ]
        if cmd[:3] == ("btrfs", "scrub", "status"):
            mount = cmd[3]
            if mount == "/mnt/new":
                return list(SCRUB_FINISHED_OK)
            return list(SCRUB_NEVER)
        if cmd[:3] == ("btrfs", "scrub", "start"):
            started.append(cmd[3])
            return []
        if cmd[:3] == ("btrfs", "filesystem", "show"):
            return list(SHOW_SINGLE)
        if cmd[:3] == ("btrfs", "device", "stats"):
            return list(STATS_ZERO)
        return []

    def execute_commands(commands, wait=True):
        return [execute_command(c, wait=wait) for c in commands]

    monkeypatch.setattr(statbtrfs, "execute_command", execute_command)
    monkeypatch.setattr(statbtrfs, "execute_commands", execute_commands)
    monkeypatch.setattr(statbtrfs.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
    monkeypatch.setattr(
        statbtrfs.sys,
        "argv",
        ["statbtrfs", "-s", "-d", "7", "-m", "8", "--scrub_command_lockout", "1", "-i", "1"],
    )

    # Import SCRUB_NEVER at module top with the other fakes.
    statbtrfs.main()
    assert started == ["/mnt/old"]
    assert "/mnt/new" not in started
    assert "Skipping mounts scrubbed within the last 7d" in capsys.readouterr().out
```

At the top of `tests/test_scrub_orchestration.py`, import `SCRUB_NEVER` alongside the other fakes.

In `test_main_scrub_first_wave_respects_max_count`, snapshot `len(started)` inside `fake_sleep` on the first sleep after the initial wave and assert it equals 2 before the third start appears — proving concurrency capping before lockout advancement.


- [ ] **Step 3: Run orchestration tests**

```bash
pytest tests/test_scrub_orchestration.py -v
```

Expected: PASS. Iterate on clock/poll bookkeeping if the loop exits early or hangs — hangs usually mean `running_scrubs` never empties or lockout never elapses; fix the fake time/status, do not weaken production exit conditions.

- [ ] **Step 4: Commit**

```bash
git add tests/test_scrub_orchestration.py
git commit -m "$(cat <<'EOF'
Add mocked scrub orchestration coverage for -s concurrency and -d.

EOF
)"
```

---

### Task 7: Live smoke + README + coverage gate

**Files:**
- Create: `tests/test_live.py`
- Modify: `README.txt` (append Development section)

**Interfaces:**
- Consumes: `conftest.skip_unless_live_btrfs`; real `statbtrfs.main` without `-s`
- Produces: documented run commands

- [ ] **Step 1: Write live test**

```python
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
```

Note: live may need root/sudo for `btrfs` queries. If `main` fails with sudo message on unprivileged hosts that still have mounts, `skip_unless_live_btrfs` should also skip when status commands are not runnable — extend helper if needed:

```python
# In conftest.skip_unless_live_btrfs, after mounts discovered:
sample = next(iter(mounts))
out = statbtrfs.execute_command(["btrfs", "scrub", "status", sample])
if out is None or (isinstance(out, list) and not out and not statbtrfs.USE_SUDO):
    pass  # still try; main will surface errors
```

Prefer: if `ensure_privileges` would exit, skip with reason `"sudo/root required for live btrfs queries"`. Implement by catching SystemExit around a probe call.

- [ ] **Step 2: Update README.txt**

Append:

```
Development:
  pip install -r requirements-dev.txt
  pytest                                 # unit tests (offline)
  pytest --cov=statbtrfs --cov-fail-under=85
  pytest -m live                         # optional status-only smoke on a btrfs host
```

Keep existing usage/install text intact.

- [ ] **Step 3: Run full unit suite + coverage gate**

```bash
cd /mnt/klein/work/cas/statbtrfs
pip install -r requirements-dev.txt
pytest
pytest --cov=statbtrfs --cov-fail-under=85 --cov-report=term-missing
```

Expected: both PASS. If coverage < 85%, add the smallest missing unit tests for uncovered maintainable lines (often edge branches in `main` / `max_scrub_count < 1` cpu_count path). Optional thin test:

```python
def test_max_scrub_count_lt_one_uses_cpu_count(monkeypatch, capsys):
    # patch os.cpu_count -> 2, two mounts, -m 0, statuses finish quickly...
```

Only add if needed for the gate.

- [ ] **Step 4: Confirm live is deselected by default and selectable**

```bash
pytest -m live -v
# Either SKIP (no mounts/privileges) or PASS; must not issue scrub start
pytest -q  # must not collect/run live
```

- [ ] **Step 5: Commit**

```bash
git add tests/test_live.py README.txt
git commit -m "$(cat <<'EOF'
Add live status smoke, README test docs, and coverage gate.

EOF
)"
```

---

## Spec coverage checklist (self-review)

| Spec requirement | Task |
|------------------|------|
| pytest.ini + requirements-dev + layout | Task 1 |
| fakes + CommandMap | Task 1 |
| Lazy sudo / import-safe | Task 1 |
| parse_show / stats / color | Task 2 |
| parse_scrub + time | Task 3 |
| find_btrfs_mounts | Task 4 |
| filter_recently_scrubbed_mounts | Task 4 |
| CLI status / patterns / -V / -d | Task 5 |
| Full scrub orchestration mocks | Task 6 |
| live status-only | Task 7 |
| README Development | Task 7 |
| cov-fail-under=85 | Task 7 |
| No live scrub start | Tasks 6–7 |
| No setup.py install_requires change | Global + all tasks |
| No version bump for tests | Global |

## Placeholder / consistency notes

- `CommandMap` + `install_command_map` names are stable across Tasks 4–6.
- `ensure_privileges` / `_SUDO_CHECKED` introduced in Task 1 and used by execute_* thereafter.
- Scrub orchestration tests must control `time.time` and `time.sleep` — never rely on wall clock.
- Set iteration order is nondeterministic; Task 6 sorts mounts when asserting start order.
