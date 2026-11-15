# Lessons: full entries

Why this project's APIs, formats and agreed behaviours had to change. `lessons.md` has one line per
entry: read that first, and look entries up here by date and name rather than reading this whole. New
entries go last, in the same commit as the change:

```markdown
## YYYY-MM-DD <short name>
- Changed: ...
- Why we had to change: ...
- Original design was wrong because: ...
- Lesson: ...
```

## 2026-11-07 statbtrfs 0.41: a check that could not tell, or did not finish, is not OK
- Changed: exit code 2 (the check failed) now also stands for a scrub status that could not be read (`unknown`) and a last scrub that did not complete (`aborted`, `interrupted`), where 0.40 exited 0 for both; a scrub that found errors still exits 1. `-s` ends "Scrubs ended; N could not be started, M did not complete or could not be read." where it said "Scrubs finished; N could not be started." A plain run reads again while a reading is `unknown` or `interrupted`, and `-w`'s first poll while one is `interrupted` (`unknown` there takes the 10 s hold); 3 times, 0.5 s apart.
- Why we had to change: 0.40 read "no record" and "the scrub did not end well" as healthy, so a cron monitor on the exit code stayed green after a cancelled or killed scrub, or when btrfs gave no reply. Making those exit 2 first made a plain run exit 2 whenever it collided with another status reader (`btrfs scrub status` takes the status file with `flock(LOCK_EX|LOCK_NB)`; the loser gets no reply): 12 of 300 and 11 of 300 pairs of runs started together on EL7 (btrfs-progs 4.9.1), up to 7% during a background scrub. A finishing scrub also reads `interrupted` for about a millisecond.
- Original design was wrong because: 0.40 had two answers (healthy, problems) for a check with three: it could not tell whether it was healthy. The first fix of that treated one transient read as the final answer, though both transients last about a millisecond and the next read is clean.
- Lesson: a monitor's exit code keeps three answers (fine, not fine, could not tell), and "could not tell" is never "fine". Where the tool read from can fail for a moment (a lock held by another reader, the end of a job), read again a few times with a stated bound before reporting it; the bound caps what a real failure costs (here 1.5 s per run).

## 2026-11-07 statbtrfs 0.43: a filter skips the work, never the check
- Changed: `-d N` still skips the scrub of a filesystem scrubbed within N days, but no longer its check: a skipped filesystem with device errors, scrub errors, a forced read-only state or an unreadable status is shown (row and note) and counts in the exit code, in plain, `-s` and `-w`. A healthy skipped one stays out of the table. So `statbtrfs -s -d 7` and plain `-d 7` exit 1 (or 2) where 0.42 said "nothing to do" and exited 0. Also: a mount that reads read-write on a read-only filesystem is reported as forced only when `BTRFS_IOC_START_SYNC` on it fails with EROFS; success means a deliberate remount (not reported); any other errno means could not tell (exit 2).
- Why we had to change: a weekly `statbtrfs -s -d 7` on a filesystem scrubbed 3 days ago that was then forced read-only (or had device errors) printed "nothing to do" and exited 0, so the monitor stayed green. And the mountinfo signature of a forced filesystem is the same as that of `mount -o remount,ro` on one of several mounts of a filesystem: 0.43's first version reported the remount as an error that never happened.
- Original design was wrong because: `-d` was applied before the check, so what it skipped it also stopped looking at; and one observable (rw mount, ro superblock) was taken to have one cause.
- Lesson: an option that leaves things out must leave out only what is healthy; the skipped part is still checked. When a signal has two causes, ask the system which (here one ioctl, decided by its errno, never by text) before reporting it, and say "could not tell" when it can't answer.

## 2026-11-14 statbtrfs 0.45: a copy you carry is no requirement
- Changed: statbtrfs's package metadata requires no multiCMD (`install_requires` drops `multiCMD>=1.56`, and requirements.txt, which held only `multiCMD`, is gone). statbtrfs runs the multiCMD it embeds (1.67 in 0.45) wherever the installed one is older than that copy, missing, or does not import, and an installed one at least as new, as before.
- Why we had to change: the floor (1.56) was below the copy statbtrfs uses (1.61 in 0.44), so the requirement guaranteed nothing statbtrfs relied on; it only made pip install or upgrade a multiCMD that statbtrfs then passed over. And pip 9.0.3 (stock on EL7 and EL8) upgrades every requirement under `-U`, which stopped the install: with multiCMD 1.55 or 1.57 installed, `pip install -U statbtrfs==0.44` exited 2 with `configparser.DuplicateOptionError` (those versions' `mcmd`, `multicmd` and `multiCMD` entry points, which pip 9 reads as one name). Without the requirement, pip 9.0.3 upgrades 0.44 to 0.45 there (exit 0, multiCMD left as it was, statbtrfs running its embedded 1.67), and with multiCMD 1.67 installed statbtrfs imports that one (the CI's python:3.6 image, 2026-11-14). hpcp dropped its requirement for the same reason in 9.89; the user chose "Drop it, as hpcp did (Recommended)".
- Original design was wrong because: the requirement dates from when statbtrfs needed an installed multiCMD; once statbtrfs carried its own copy and chose between the two by version at import, it stated no need, and a requirement that states no need still hands the installer's own failures to every install.
- Lesson: declare as a requirement only what the program needs from outside it. A library it carries a copy of and picks by version at import is not one.
