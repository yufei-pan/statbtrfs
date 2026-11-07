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

### A scrub that did not complete still says OK
- Kind: deferred
- What the operator sees: `-s` ends with `aborted, OK` (a read-only mount) or `interrupted, OK` (after a kill) and exit 0, so a scrub that never covered the filesystem reads as healthy. It should say so and not exit 0.
- Why: the fix changes the exit contract, so it goes in a release that says so.
- Revisit when: statbtrfs 0.41.

### scrub_rate is N/A on EL7
- Kind: deferred
- What the operator sees: btrfs-progs 4.9.1 prints no rate, so `scrub_rate` stays `N/A` there. The other columns fill in.
- Why: it has to be computed from the bytes and the duration, which takes a size parser.
- Revisit when: statbtrfs 0.41.
