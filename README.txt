usage: statbtrfs [-h] [-s | -w] [-i INTERVAL] [-m MAX_SCRUB_COUNT]
                 [-d EXCLUDE_RECENT_SCRUBBED_DAYS] [--scrub-command-lockout SCRUB_COMMAND_LOCKOUT]
                 [--color {auto,always,never}] [-V]
                 [pattern ...]

Check Btrfs filesystem status.

positional arguments:
  pattern               Patterns to filter btrfs mounts. Default="*"

options:
  -h, --help            show this help message and exit
  -s, --scrub           Issue scrub to all pools
  -w, --watch           Refresh every -i seconds while any scrub is running, then exit (never
                        starts scrubs)
  -i, --interval INTERVAL
                        Interval for status check in seconds
  -m, --max-scrub-count MAX_SCRUB_COUNT
                        Maximum number of scrubs running at the same time (0: one per CPU)
  -d, --exclude-recent-scrubbed-days EXCLUDE_RECENT_SCRUBBED_DAYS
                        Exclude mounts scrubbed within this many days
  --scrub-command-lockout SCRUB_COMMAND_LOCKOUT
                        Seconds to wait after starting a scrub before starting another
  --color {auto,always,never}
                        Colour output: auto (default) on a terminal unless NO_COLOR is set
  -V, --version         show program's version number and exit

Exit status: 0 healthy; 1 problems found (device errors, scrub errors or missing devices); 2 the
check failed (no matching mounts, an unreadable filesystem, no root); 130 interrupted.

Known limitation: when each btrfs command has to run through sudo, a missing btrfs shows as "Could not fetch
complete info … Skipping…" rather than "btrfs not found on PATH" (see docs/limitations.md).

Upgrading to 0.38 from 0.37:
  - multiCMD 1.56 or newer is required (the embedded copy is 1.56).
  - An unreadable filesystem now prints only the note under the table, "Could not fetch complete info for
    <mounts>. Skipping...". The three lines before it ("Could not parse btrfs show info.", "Output from btrfs
    filesystem show was:" and the raw output) are gone.
  - statbtrfs | head, or any reader that exits early, now ends quietly with exit 1 instead of a
    BrokenPipeError traceback.
  - -s and -w clear the screen with ESC[H ESC[J, so a long run no longer pushes tables into the scrollback of
    terminals that treat ESC[2J that way.
  - Library callers: find_btrfs_mounts() takes no argument, execute_command(s) lose wait=, and run_detached
    raises OSError for a missing command instead of returning 127.

Install:
sudo pip install statbtrfs

Development:
  pip install -r requirements-dev.txt
  pytest                                 # unit tests (offline)
  pytest --cov=statbtrfs --cov-fail-under=85
  pytest -m live                         # optional status-only smoke on a btrfs host (as root)
