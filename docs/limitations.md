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

### On a terminal, a sudo that signs in with no question is refused when it remembers nothing
- Kind: known limitation
- What the operator sees: statbtrfs run as a user (not root) through the per-command sudo fallback, on a
  terminal, where sudo authenticates with no question and no NOPASSWD rule (an ssh agent through
  pam_ssh_agent_auth, Kerberos) and remembers nothing at that moment: the status and cancel commands run as
  `sudo -n`, which does not try, so they are refused: "Could not fetch complete info for <mount>. Skipping...",
  exit 2, where 0.45 worked. That happens with sudo set to ask every time (`timestamp_timeout=0`); with -s or -w
  and -i longer than sudo's timeout (5 minutes by default), from the first poll after the remembered sign-in ran
  out, and a Ctrl-C cancel then says "Could not cancel the scrub on <mount>: sudo: a password is required."; and
  in a background job whose input is not the terminal (`nohup statbtrfs -s &`, `statbtrfs </dev/null &`), from
  the first command, also for a user whose sudo may run everything. Runs with no terminal (cron, ssh, mssh) are
  not affected. Measured on sudo 1.9.16 and 1.8.23. sudo 1.9.9 (Ubuntu 22.04) runs PAM for `sudo -n`, so such a
  sudo passes there, and each refusal of a password sudo there counts as a failed login where pam_faillock is on.
- Why: telling "would ask" from "would not" takes running sudo without `-n`: on a terminal that is 0.45's hang (a
  stopped sudo, and a password typed into it shown in clear), and with no terminal a failed login that
  pam_faillock counts. The re-review after 0.46's second fix round looked for a design that removes this (a probe
  at the start, asking in the background, a retry in a session of its own) and found none.
- Workarounds: NOPASSWD for btrfs; or `Defaults noninteractive_auth` on sudo 1.9.10 or later (EL7's 1.8.23 and
  EL8's 1.9.5 lack it), which makes `sudo -n` sign in with no question, but then pam_faillock counts each refusal
  of a password sudo as a failed login, so it is no workaround where faillock is set.
- Revisit when: someone hits it.
- Approved: 2026-11-26, the user's pick "Known limitation, release (Recommended)" (relayed by the chief session).

### -s through the per-command sudo fallback needs btrfs without a password
- Kind: deferred
- What the operator sees: statbtrfs runs as a user whose sudo may run btrfs but not statbtrfs, with a password
  (no NOPASSWD), so each btrfs command runs through sudo. Where sudo is asked for the password at the start
  (statbtrfs is in its terminal's foreground, whatever its input is, or its input is the terminal: a background
  job stops at the prompt until `fg`), status and -w work on it (not with timestamp_timeout=0, and -w only while
  -i is shorter than sudo's timestamp_timeout), but `statbtrfs -s` starts no scrub: each start fails with "sudo:
  a terminal is required to read the password …" (sudo 1.8: "no tty present and no askpass program specified"),
  and the run ends "Scrubs ended; N could not be started.", exit 2 when nothing else is wrong. A sudo with an
  askpass helper set (SUDO_ASKPASS, sudo.conf) asks the helper instead and waits for it, as in 0.45. Where sudo
  is not asked at the start (cron, ssh without -t, a background job of an interactive shell whose input is not
  the terminal) and no askpass helper is set, every command fails at once,
  "Could not fetch complete info …", exit 2. Running statbtrfs as root, or NOPASSWD for statbtrfs or for btrfs,
  works; a password rule for statbtrfs itself works where sudo is asked at the start.
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
  has no remembered password for (timestamp_timeout=0, -i longer than sudo's timeout, a run statbtrfs could not ask
  in at the start), or one that sudoers does not allow: statbtrfs prints "Could not fetch complete info for
  <mount>. Skipping...", "Could not read the scrub status of <mount>." or "Could not read the device stats of
  <mount>." and exits 2 (1 when a problem is found elsewhere), without sudo's own words ("a password is
  required", "Sorry, user … is not allowed to execute …").
- Why: these notes never showed the reply of the command that failed. Before 0.46 the cases on a terminal hung
  instead.
- Plan: add the reply's last line to each note, as the cancel does (the scrub start's failure shows the first
  line); that also names a btrfs missing behind sudo, which settles the known limitation above (it leaves this
  file then).
- Revisit when: 0.47.

### With no terminal, a password sudo counts each refused command as a failed login
- Kind: deferred
- What the operator sees: statbtrfs runs with no terminal (cron, `ssh host statbtrfs`, mssh) as a user whose
  sudo wants a password for btrfs, on a system that counts failed logins with pam_faillock (EL8 authselect
  with-faillock, EL7 authconfig --enablefaillock, STIG and CIS profiles). Every btrfs command fails ("Could
  not fetch complete info …", exit 2), and each counts as a failed login: one run locks the account, and the
  user's right password is refused (sudo, su, password logins) until faillock's unlock_time passes or an
  admin runs `faillock --reset`. As in 0.45. NOPASSWD for btrfs, or running statbtrfs as root, avoids it.
- Why: with no terminal statbtrfs runs plain sudo, which can't ask but still runs PAM's authentication, and
  pam_faillock records its failure. `sudo -n` records nothing, but also refuses a sudo that authenticates
  with no question (an ssh agent, Kerberos), which works there now.
- Plan: with no terminal, ask once at the start (acquire_root's `sudo -l` without -n), then `-n` on every
  later command; measure that the later commands find the record a no-question sudo leaves. If they don't,
  ask the user between `-n` and this behaviour.
- Revisit when: 0.47.

### A device stats reply that lacks one device's counters reads as the others' sum
- Kind: deferred
- What the operator sees: a filesystem of several devices where `btrfs device stats` fails for one of them
  (btrfs-progs v6.14 has the message "device stats ioctl failed on <device>" for it, which would reach stderr), or
  where a device's path holds a space: that device's counters are missing from the row, which shows the sum of
  the others' (0 when they have no errors), with no note, and an exit code that ignores it (0 when nothing else is
  wrong). A reply with no counters at all is reported (N/A, "Could not read the device stats of <mount>.", exit 2,
  or 1 when a problem is found elsewhere).
- Why: the row sums the lines statbtrfs can parse (`[<path>].<name> <count>`; any other shape is skipped), and a
  reply with none is the only one it takes for unreadable.
- Plan: first check what btrfs-progs prints and exits with for a device whose query failed (v6.14's message is
  read from its binary only; EL7's 4.9.1 is not checked) and for a path with a space. Then read a counter by its
  last two fields, and call the reply unreadable when it holds an error line, or the counters of fewer devices than
  `btrfs filesystem show` lists.
- Revisit when: 0.47.

### -s with -d calls a skipped filesystem that could not be read "a problem"
- Kind: deferred
- What the operator sees: `statbtrfs -s -d N` that scrubs at least one filesystem, with another skipped as recently
  scrubbed whose only failure is a read that failed (its device stats or scrub status): the run ends "<mount>:
  skipped by -d, but it has a problem: see the table above" and "Scrubs ended; 1 skipped by -d needs attention.",
  where nothing was found wrong and the filesystem could not be checked. The table, its notes and the exit code (2,
  or 1 when a problem is found elsewhere) say it right. A run that skips every filesystem prints no such lines.
- Why: the end lines take every skipped filesystem with a problem or a failure for one with "a problem".
- Plan: say it "could not be checked" for one with only failures.
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
