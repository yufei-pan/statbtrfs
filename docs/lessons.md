# Lessons

What this project's past changes taught us. Read all of this before changing an API, a format or an
agreed behaviour here. For the full story of a line, find the entry with the same date and name in
`lessons-full.md`.

When one has to change, add the full entry to `lessons-full.md` and one line here, newest last, in the
same commit as the change. Never merge lines to save space; before this file passes 80 KB (what one
Claude Code read returns, measured 2026-11-15), ask the user.

- **2026-11-07 statbtrfs 0.41: a check that could not tell, or did not finish, is not OK**: a monitor's exit code keeps three answers (fine, not fine, could not tell), and an unreadable status or an incomplete scrub is never the first. Then a one-shot read must read again where the "could not tell" is a transient of the tool it reads from (a lock collision, a scrub's last millisecond), or the new honesty alerts on every collision.
- **2026-11-07 statbtrfs 0.43: a filter skips the work, never the check**: an option that leaves things out (`-d`) must leave out only what is healthy; whatever it skips is still asked, and a problem in it is shown and counted. And a signal that looks the same for two causes (a mount rw on a ro superblock: forced, or remounted) is settled by asking the system, by errno, before it is reported.
- **2026-11-14 statbtrfs 0.45: a copy you carry is no requirement**: declare only what the program needs from outside it. A library it embeds and picks by version at import needs no install requirement, and one left behind guarantees nothing while the installer's own failures (pip 9 upgrading an old multiCMD, `DuplicateOptionError`) stop your install.
- **2026-11-14 statbtrfs 0.45: say what a command did from its answer, not from having asked**: a report of an action ("Cancelled scrub") reads the action's exit code and shows its words when it failed; an action asked for after a wait can find its target already gone ("not running"), and one run through a gatekeeper (sudo) can be refused.
- **2026-11-23 statbtrfs 0.46: a command no one can answer must not ask**: a command started outside the terminal's foreground (a process group or session of its own) runs in its non-interactive form (`sudo -n`), so what it would ask for fails at once in its own words; whatever it needs from the person is asked in the foreground, before. A prompt there stops the command (SIGTTIN, SIGTTOU), which its parent never sees, and shows what the person types.
