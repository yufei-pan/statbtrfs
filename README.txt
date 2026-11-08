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
check failed (no matching mounts, an unreadable filesystem, a scrub status that could not be read,
a scrub that did not complete, no root); 130 interrupted; 141 the reader of stdout went away (|
head).

Known limitation: when each btrfs command has to run through sudo, a missing btrfs shows as "Could not fetch
complete info … Skipping…" rather than "btrfs not found on PATH" (see docs/limitations.md).

Upgrading to 0.42 from 0.41:
  - -s on a read-only mount now starts a read-only scrub (`btrfs scrub start -r`), which checks it and repairs
    nothing, so the run completes and exits 0 (1 if it finds errors). 0.41 started a read-write scrub, which btrfs
    aborts at once there, so it ended "did not complete" with exit 2. A read-write mount still scrubs read-write.
    The mount is asked with statvfs(); when it can't be asked, the scrub starts as before. On a filesystem
    with several mounts, -s scrubs through the first in sort order, so it is read-only when that mount is.
  - Advice to resume a scrub that did not complete says `btrfs scrub resume -r <mount>` on a read-only mount:
    a plain resume is aborted there too, as btrfs does not keep -r for a resume.

Upgrading to 0.41 from 0.40:
  - A scrub that did not complete (`aborted`: cancelled, or a read-only mount; `interrupted`: its process was
    killed) no longer reads OK: its error_summary shows `incomplete` (errors it found still show, and exit 1),
    a note under the table says to continue it with `btrfs scrub resume <mount>`, `-s` ends with "Scrubs ended;
    N did not complete or could not be read." instead of "All scrubs finished.", and the exit code is 2, the
    check failed: it found nothing wrong, but it did not check everything. This holds without -s too, for as
    long as the last scrub is the incomplete one, so a monitor running plain `statbtrfs` exits 2 until a scrub
    completes.
  - A scrub status that could not be read (`unknown`: another reader held the status file's lock, or the read
    failed) now exits 2 with the note "Could not read the scrub status of <mount>." In -s and -w that is only
    when it is still unreadable once the run ends (a reading like this holds a run for 10 s, as in 0.40).
    Without -s, a status that could not be read, or that reads `interrupted` (as one does for a millisecond as a
    scrub ends), is read again, up to 3 times 0.5 s apart, so a collision with another reader does not exit 2;
    -w's first poll does the same for `interrupted`.
  - btrfs's stderr now reaches the parsers, after its stdout. A status read that failed part way, which
    btrfs-progs report only there and with exit 0 (seen at the very end of a `btrfs scrub start -B` started
    elsewhere), reads as unknown instead of Never, so -s and -w read on to the finished record and its errors.
  - EL7 (btrfs-progs 4.9.1): scrub_rate is now filled in, computed as the bytes scrubbed over the duration, as
    current btrfs-progs compute it. A scrub that took under a second still shows N/A.

Upgrading to 0.40 from 0.39:
  - EL7's btrfs-progs 4.9.1 scrub status is now read: -s and -w follow a running scrub, -m holds the next
    scrub back, -d skips recent ones, and the status columns fill in. It prints no rate, so scrub_rate stays
    N/A there. For about the first 5 s of a scrub it prints only "no stats available", so the columns show
    Never.
  - -s and -w no longer take a failed status read for "no scrub running". `btrfs scrub status` fails when
    another reader has its file locked, so two watchers could end each other's runs. A failed read (shown as
    unknown), `interrupted`, or on EL7 Never, now ends a run or frees a -m slot only once it has held for 10 s,
    so -w on an idle, never-scrubbed EL7 filesystem takes 10 s to exit, and a really interrupted scrub is
    reported 10 s later. Other hosts exit at once.
  - A resumed scrub's time is now read on current btrfs-progs, so -d skips it.
  - The embedded multiCMD is now 1.58: no change to how commands run. The embedded copy also runs when the
    installed multiCMD fails to import in any way, not only when it is older or missing. multiCMD itself need
    not be upgraded.
  - With multiCMD 1.57 or earlier installed, pip 9 (stock on EL7 and EL8) without `--user` stops `pip3 install -U statbtrfs` with `configparser.DuplicateOptionError`, because it upgrades dependencies too: use `pip3 install statbtrfs==0.40`, `pip3 install -U --no-deps statbtrfs`, or run `pip3 install -U pip` once. With `--user` it does not stop.

Upgrading to 0.39 from 0.38:
  - The embedded multiCMD is now 1.57. It runs whenever the installed multiCMD is older, so multiCMD itself need not be upgraded. With multiCMD 1.57 or earlier installed, pip 9 (stock on EL7 and EL8) without `--user` stops `pip3 install -U statbtrfs` with `configparser.DuplicateOptionError`, because it upgrades dependencies too: use `pip3 install statbtrfs==0.39`, `pip3 install -U --no-deps statbtrfs`, or run `pip3 install -U pip` once. With `--user` it does not stop.
  - Known: on EL7, btrfs-progs 4.9.1's scrub status is not read, so `-s` can say a scrub finished while it runs and the status columns stay `Never`. A checksum error still shows. Planned for 0.40.
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
