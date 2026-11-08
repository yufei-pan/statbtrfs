# Lessons

What this project's past changes taught us. Read all of this before changing an API, a format or an
agreed behaviour here. For the full story of a line, find the entry with the same date and name in
`lessons-full.md`.

When one has to change, add the full entry to `lessons-full.md` and one line here, newest last, in the
same commit as the change. Keep this file under 20 KB: at the cap, merge lines before adding.

- **2026-11-07 statbtrfs 0.41: a check that could not tell, or did not finish, is not OK**: a monitor's exit code keeps three answers (fine, not fine, could not tell), and an unreadable status or an incomplete scrub is never the first. Then a one-shot read must read again where the "could not tell" is a transient of the tool it reads from (a lock collision, a scrub's last millisecond), or the new honesty alerts on every collision.
- **2026-11-07 statbtrfs 0.43: a filter skips the work, never the check**: an option that leaves things out (`-d`) must leave out only what is healthy; whatever it skips is still asked, and a problem in it is shown and counted. And a signal that looks the same for two causes (a mount rw on a ro superblock: forced, or remounted) is settled by asking the system, by errno, before it is reported.
