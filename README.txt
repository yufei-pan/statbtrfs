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
check failed (no matching mounts, an unreadable filesystem, no root); 130 interrupted; 141 the
reader of stdout went away (| head).

Known limitation: when each btrfs command has to run through sudo, a missing btrfs shows as "Could not fetch
complete info … Skipping…" rather than "btrfs not found on PATH" (see docs/limitations.md).

Upgrading to 0.39 from 0.38:
  - The embedded multiCMD is now 1.57. It runs whenever the installed multiCMD is older, so nothing needs upgrading (stock pip 9.0.3 on EL7 and EL8 cannot upgrade multiCMD, and does not have to).
  - Faster command starts on Python 3.6 - 3.10, where the embedded multiCMD 1.57 imports only built-in
    modules in the wrapper that puts each command in its own process group (about 7 ms to 3.5 ms of CPU
    per command on Python 3.6.8). Nothing else about starting a command changes.

Upgrading to 0.38 from 0.37:
  - multiCMD 1.56 or newer is required (the embedded copy is 1.56).
  - An unreadable filesystem now prints only the note under the table, "Could not fetch complete info for
    <mounts>. Skipping...". The three lines before it ("Could not parse btrfs show info.", "Output from btrfs
    filesystem show was:" and the raw output) are gone.
  - statbtrfs | head, or any reader that exits early, now ends quietly with exit 141 (128 + SIGPIPE)
    instead of a BrokenPipeError traceback and exit 1.
  - Ctrl-C outside -s and -w (say while btrfs hangs on a dying device) exits 130 quietly instead of a
    traceback.
  - -s and -w clear the screen with ESC[H ESC[J, so a long run no longer pushes tables into the scrollback of
    terminals that treat ESC[2J that way.
  - Library callers: find_btrfs_mounts() takes no argument and execute_command(s) lose wait=.

Install:
sudo pip install statbtrfs

Development:
  pip install -r requirements-dev.txt
  pytest                                 # unit tests (offline)
  pytest --cov=statbtrfs --cov-fail-under=85
  pytest -m live                         # optional status-only smoke on a btrfs host (as root)
