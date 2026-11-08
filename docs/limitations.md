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

### `-s` on a read-only mount never completes
- Kind: deferred (0.42)
- What the operator sees: `statbtrfs -s` on a btrfs mounted read-only starts a scrub that btrfs aborts at once (EL7: `aborted after 00:00:00`, 0 bytes scrubbed), so since 0.41 the run ends "did not complete" with exit 2. The note's advice, `btrfs scrub resume <mount>`, fails the same way there.
- Why: `start_scrub` starts a read-write scrub whatever the mount; a read-only mount needs `btrfs scrub start -r`. Found while building 0.41; whether 4.9.1's `-r` works there is not checked yet.
- Revisit when: 0.42: add `-r` when `os.statvfs(mount).f_flag & os.ST_RDONLY`, after checking `-r` on EL7's btrfs-progs 4.9.1 and on 6.x.
