# Limitations

Approved known limitations and deferrals. Reviewers: read this first, and don't raise these again.

### Missing btrfs not named behind the sudo fallback
- Kind: known limitation
- What the operator sees: run as a non-root user who can't re-exec statbtrfs under sudo, so that each btrfs
  command runs through `sudo`, with btrfs-progs missing (or not on sudo's PATH): statbtrfs prints "Could not
  fetch complete info … Skipping…" and exits 2, as 0.36 did, instead of "btrfs not found on PATH: …".
- Why: sudo exits 1, not 127, for a missing command, and statbtrfs checks its own PATH only. Telling the case
  apart would take another command and code path (asking sudo's PATH) for a rare setup.
- Revisit when: someone hits it.
- Approved: 2026-10-23, the user chose "Known limitation (Recommended)".

### EL7's btrfs-progs 4.9.1 scrub status is not read
- Kind: deferred
- What the operator sees: on EL7, `statbtrfs -s` printed "All scrubs finished ... Never", exit 0, after 10 s while `btrfs scrub status` said it was running, and the status columns stay `Never` and `N/A` even after a scrub finishes. A real checksum error still shows, with `bit_rot=1` and exit 1. `-m` probably cannot hold scrubs back there, since the `running` list stays empty (read, not shown). Same in 0.38.
- Why: `parse_scrub_status` knows only the modern `Status:` and `Scrub started:` lines, and the test fixtures are modern only.
- Revisit when: statbtrfs 0.40.
