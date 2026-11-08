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
- Changed: exit code 2 (the check failed) now also stands for a scrub status that could not be read (`unknown`) and a last scrub that did not complete (`aborted`, `interrupted`), where 0.40 exited 0 for both; a scrub that found errors still exits 1. `-s` ends "Scrubs ended; N could not be started, M did not complete or could not be read." where it said "Scrubs finished; N could not be started." A plain run, and `-w`'s first poll for `interrupted`, read again (3 times, 0.5 s apart) while a reading is `unknown` or `interrupted`.
- Why we had to change: 0.40 read "no record" and "the scrub did not end well" as healthy, so a cron monitor on the exit code stayed green after a cancelled or killed scrub, or when btrfs gave no reply. Making those exit 2 first made a plain run exit 2 whenever it collided with another status reader (`btrfs scrub status` takes the status file with `flock(LOCK_EX|LOCK_NB)`; the loser gets no reply): 12 of 300 and 11 of 300 pairs of runs started together on EL7 (btrfs-progs 4.9.1), up to 7% during a background scrub. A finishing scrub also reads `interrupted` for about a millisecond.
- Original design was wrong because: 0.40 had two answers (healthy, problems) for a check with three: it could not tell whether it was healthy. The first fix of that treated one transient read as the final answer, though both transients last about a millisecond and the next read is clean.
- Lesson: a monitor's exit code keeps three answers (fine, not fine, could not tell), and "could not tell" is never "fine". Where the tool read from can fail for a moment (a lock held by another reader, the end of a job), read again a few times with a stated bound before reporting it; the bound caps what a real failure costs (here 1.5 s per run).
