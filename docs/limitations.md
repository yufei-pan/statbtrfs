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
