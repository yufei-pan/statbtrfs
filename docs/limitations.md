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

### -s through the per-command sudo fallback needs btrfs without a password
- Kind: deferred
- What the operator sees: statbtrfs runs as a user whose sudo may run btrfs but not statbtrfs, with a password
  (no NOPASSWD), so each btrfs command runs through sudo. With input from a terminal, status and -w work on the
  password asked for at the start (while -i is shorter than sudo's timestamp_timeout, and not with
  timestamp_timeout=0), but `statbtrfs -s` starts no scrub: each start fails with "sudo: a terminal is required
  to read the password …" (sudo 1.8: "no tty present and no askpass program specified"), and the run ends
  "Scrubs ended; N could not be started.", exit 2 when nothing else is wrong. With any other input (cron, ssh
  without -t, a file) nothing is asked at the start, and every command fails at once, "Could not fetch complete
  info …", exit 2. Running statbtrfs as root, a sudoers rule that lets the user run statbtrfs itself, or btrfs
  with NOPASSWD, works.
- Why: run_detached() starts each scrub in a session of its own, so the terminal's Ctrl-C and hangup never reach
  `btrfs scrub start`'s forked process, which cancels the scrub on SIGINT. That session has no terminal, and sudo
  keeps the password it remembers per terminal (timestamp_type=tty, the default), so it finds none there and can't
  ask (measured on a pty with sudo 1.8.23, 1.9.5 and 1.9.16, 2026-11-23).
- Plan: start the scrub in a process group of its own within the terminal's session, as multiCMD does, so sudo
  finds its remembered password while the terminal's Ctrl-C still reaches only statbtrfs; Python 3.6 to 3.10 have
  no Popen(process_group=) and need another way to start it there. Measure on a real btrfs that the scrub outlives
  statbtrfs and the terminal's hangup, also with sudo 1.9.14 or later, whose use_pty (on by default) runs the
  command on a pty of sudo's own.
- Revisit when: 0.47.

### A sudo that refuses a status command is not named
- Kind: deferred
- What the operator sees: each btrfs command runs through sudo (with `-n` on a terminal) and sudo refuses one it
  has no remembered password for (timestamp_timeout=0, -i longer than sudo's timeout, input not from a terminal),
  or one that sudoers does not allow: statbtrfs prints "Could not fetch complete info for <mount>. Skipping...",
  "Could not read the scrub status of <mount>." or "Could not read the device stats of <mount>." and exits 2,
  without sudo's own words ("a password is required", "Sorry, user … is not allowed to execute …").
- Why: these notes never showed the reply of the command that failed. Before 0.46 the cases on a terminal hung
  instead.
- Plan: add the reply's last line to each note, as the scrub start and cancel do; that also names a btrfs
  missing behind sudo (the known limitation above).
- Revisit when: 0.47.

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
