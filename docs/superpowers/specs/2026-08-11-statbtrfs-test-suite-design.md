# statbtrfs test suite design

Date: 2026-08-11  
Status: approved for spec review (pending user sign-off of this document)

## Goal

Build a complete hybrid test suite for `statbtrfs` that mirrors sibling `statblk` conventions: offline unit/regression coverage of parsers, mount discovery, CLI, and full scrub orchestration (mocked), plus optional live soft smoke that is **status/read-only only** (never issues `btrfs scrub start`). Enforce a line-coverage floor on `statbtrfs.py`. Allow small behavior-preserving production tweaks for testability.

## Decisions (from brainstorming)

| Topic | Choice |
|-------|--------|
| Strategy | Hybrid: mocked unit core + optional live soft smoke (`statblk`-style) |
| Scrub depth | Full mocked orchestration (`-s` loop, concurrency, lockout, exclude-recent, finish/break) |
| Production changes | Small testability tweaks only; public CLI unchanged |
| Done bar | Sibling parity + coverage floor (`--cov-fail-under=85` on `statbtrfs`) |
| Layout | Flat `tests/` with focused modules (approach 1: mirror `statblk`) |
| Live scrub | Explicitly forbidden in all live/default tests |

## Layout

```
statbtrfs/
  statbtrfs.py
  pytest.ini
  requirements-dev.txt          # pytest, pytest-cov
  tests/
    conftest.py
    fakes.py
    test_parse_show.py
    test_parse_stats.py
    test_parse_scrub.py
    test_color.py
    test_mounts.py
    test_filter_recent.py
    test_cli.py
    test_scrub_orchestration.py
    test_live.py
  docs/superpowers/specs/
    2026-08-11-statbtrfs-test-suite-design.md
```

Runtime `setup.py` `install_requires` stays unchanged. Document `pip install -r requirements-dev.txt` in README under Development.

## Runner configuration (`pytest.ini`)

- `testpaths = tests`
- `python_files = test_*.py`
- Marker: `live` (soft smoke only)
- Default `addopts = -m "not live"` so offline CI/dev is unit-only
- Do **not** enable global `--doctest-modules` (the embedded multiCMD base85/lzma blob in `statbtrfs.py` must not be scanned as doctest text)
- No `live_strict` marker unless a clear host oracle appears later; initial suite uses **`live` only**

### How to run

```bash
pip install -r requirements-dev.txt
pytest                                          # unit only (offline)
pytest --cov=statbtrfs --cov-fail-under=85      # unit + coverage gate
pytest -m live                                  # soft smoke on real btrfs host (status only)
```

## Shared fakes (`tests/fakes.py`)

Synthetic but realistic command outputs:

- `mount -t btrfs` lines (single mount, multi-mount, empty)
- `btrfs filesystem show` blobs (single device, multi-device `path` lines, incomplete/missing fields)
- `btrfs device stats` lines (all-zero counters, non-zero, malformed)
- `btrfs scrub status` blobs for: never / finished / running / with errors / “no errors found”
- Helper scrub timestamps in formats accepted by `parse_scrub_time_to_epoch`

Helper:

- Dict-keyed command stub that maps a normalized argv tuple (or argv prefix) → `list[str]` stdout lines, usable from both `execute_command` and `execute_commands` monkeypatches

## `conftest.py`

- Put repo root on `sys.path` so `import statbtrfs` works without install
- Ensure import does not `sys.exit` due to sudo probe (depends on production tweak below)
- Register `live` marker
- Skip helpers for live tests: not Linux, no `btrfs` binary, or no btrfs mounts discovered

## Production seams (small, behavior-preserving)

Allowed tweaks only where they unblock testing without changing public CLI:

1. **Lazy/guarded sudo probe** — importing `statbtrfs` under non-root / no-sudo must not exit the process. Defer the hard fail to runtime command execution (or gate behind a function callable from `main` / `execute_*`), preserving the same user-facing error when commands actually need elevation.
2. Keep **`execute_command` / `execute_commands`** as the primary stub points for unit tests.
3. No public flag renames/additions solely for tests; no large `main` extraction unless a stub cannot otherwise drive the scrub loop.

## Coverage matrix

### Parsers

**`test_parse_show.py`**

- Happy path: uuid, FS bytes used, single device path
- Multi-device: joined path string
- Missing uuid / used / path → returns `None`s and prints parse error (capture stdout)

**`test_parse_stats.py`**

- Normal write/read/corruption/generation counters
- Malformed lines skipped
- Empty input → empty dict

**`test_parse_scrub.py`**

- Defaults when never scrubbed / empty output
- Finished: status, time, rate, total-to-scrub → `scrubbed_data`
- Running: bytes scrubbed used for `scrubbed_data` (not total-to-scrub)
- Error summary: “no errors found” → green OK; otherwise red error text
- `parse_scrub_time_to_epoch`: `%a %b %d %H:%M:%S %Y`, with `%Z`, `%Y-%m-%d %H:%M:%S`, unparseable → `None`

**`test_color.py`**

- `0` green; `1..9` yellow; `≥10` red

### Mounts & filtering

**`test_mounts.py`**

- Empty / `None` mount output → empty set
- No filters → all mount points
- Pattern filters use `*{pattern}*` fnmatch semantics

**`test_filter_recent.py`**

- `exclude_recent_days <= 0` → unchanged mounts, empty skipped
- Finished + recent scrub time → skipped
- Finished + older than cutoff → kept
- Status not finished or unparseable time → kept (not skipped)

### CLI (`test_cli.py`)

Drive `main()` via `sys.argv` monkeypatch; stub `execute_command` / `execute_commands`, `time.sleep`, and table formatter as needed.

- No mounts → “No Btrfs mounts found.” and return (no crash)
- Status path once without `-s` → prints table and exits loop
- Pattern args filter mounts
- `-V` / `--version` exits 0 and prints version
- `-d` prints skipping message for recently scrubbed mounts when applicable

### Scrub orchestration (`test_scrub_orchestration.py`)

All mocked; never call real `btrfs scrub start`.

1. `issue_scrub_command` yields cumulative started-mount lists and issues start per mount
2. `-s` with N mounts and `max_scrub_count=k` starts ≤k in the first wave
3. While mounts report `running`, loop continues and does not exceed concurrency intent
4. After `scrub_command_lockout`, additional mounts receive start
5. When no running scrubs and lockout elapsed → “All Scrubs finished.” and clean exit
6. Exclude-recent interacts with `-s` so skipped mounts are never started

Control `time.time` / `time.sleep` so lockout and interval logic are deterministic and fast.

### Live (`test_live.py`)

**Soft (`@pytest.mark.live`) only**

- Skip if not Linux, `btrfs` missing, or no btrfs mounts
- Run status-only CLI path without `-s` (never pass scrub flags)
- Assert: process does not crash; stdout includes the status table header fields (`Mount`, `scrub_status`, etc.) and at least one data row
- **Hard rule:** live tests must not invoke `btrfs scrub start`

## Error / skip policy

- Unit tests: no root, no real btrfs, no network, no destructive commands
- Live soft: skip when environment lacks btrfs; fail only on unexpected crashes / broken status path when mounts exist
- Unparseable filesystem show for a mount: skip that mount with message (covered in unit/CLI)
- Import without privileges must not abort pytest collection/import

## Coverage gate

- Dev dependency: `pytest-cov`
- Success requires: `pytest --cov=statbtrfs --cov-fail-under=85`
- Measure the whole `statbtrfs` module. The embedded multiCMD payload is a string literal assigned to `_SRC_B85`, so it does not inflate line coverage the way executed code would; no `.coveragerc` omit is required unless measurement proves otherwise.
- Do not treat “covering blob decompress/exec paths” as a goal; stubbing/importing real `multiCMD` in the test env is fine and preferred when available.

## Out of scope

- Fuzzing or validating the embedded multiCMD blob contents
- Live scrub start / destructive filesystem operations
- Loopback btrfs fixture / root-requiring integration harness
- Performance benchmarks
- Changing production packaging beyond documenting test deps
- Bumping package version solely for adding tests unless releasing

## Success criteria

1. `pytest` (default markers) passes with no live host / root requirements
2. `pytest --cov=statbtrfs --cov-fail-under=85` passes under the agreed coverage config
3. Scrub orchestration scenarios above are covered with mocks (no real scrub)
4. `pytest -m live` soft smoke is status-only and skips cleanly when btrfs is absent
5. README Development section documents unit / coverage / live commands
6. Public CLI behavior unchanged aside from any necessary sudo-probe deferral (same failure mode when elevation is actually required)

## Implementation notes (non-goals for this spec’s approval)

- Prefer monkeypatching `statbtrfs.execute_command` / `execute_commands` / `time.*` over full OS emulation
- Mirror sibling CAS style: plain `test_*` functions, pytest, no unittest classes
- Prefer focused modules over one mega-file
- Do not bump package version solely for adding tests unless releasing
