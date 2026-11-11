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

### A forced read-only filesystem behind mounts statbtrfs can't open
- Kind: known limitation
- What the operator sees: statbtrfs runs as a user who can open no mount of a filesystem (for example a non-root user behind the
  per-command `sudo` fallback, with the mount point's directory closed to them), and that filesystem reads read-only in
  /proc/self/mountinfo as a forced one would: its row says statbtrfs could not tell whether the kernel forced it read-only, and
  the exit code is 2.
- Why: the forced state is told apart from an `-o ro` mount only by BTRFS_IOC_START_SYNC on an open mount, which needs a
  descriptor of statbtrfs's own; running that call through sudo would take a second process and code path for a rare setup. Running
  statbtrfs as root avoids it.
- Revisit when: an operator hits it on a setup where statbtrfs can't run as root.
- Approved: 2026-11-08, the user chose "Approve (Recommended)".

### "Cancelled scrub" is printed whatever `btrfs scrub cancel` answered
- Kind: deferred
- What the operator sees: a Ctrl-C during `-s`, answered y, makes statbtrfs print "Cancelled scrub on X: it keeps its
  progress, continue it with `btrfs scrub resume ...`" for each scrub, whatever btrfs said. If the scrub finished while
  the prompt waited, btrfs said "not running" and the resume advice is wrong; if the cancel failed (the per-command sudo
  fallback refused it), the scrub is still running while statbtrfs says it was cancelled.
- Why: `cancel_scrub()` drops the command's output and exit code. Found by the 0.44 final review (read from the code and
  btrfs-progs' `cmd_scrub_cancel`, which exits non-zero with an error; not run). Not this release's change.
- Revisit when: 0.45: read the exit code and print what btrfs said when the cancel failed.
- Noted: 2026-11-11, from the 0.44 final review; a deferral, not asked.
