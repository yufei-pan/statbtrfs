# statbtrfs: progress

Open work lives here and nowhere else (RULES, "Long work: the progress file"). Edit rows in place, in the commit that changes the work.

## Goal
- 2026-11-05, for every cas tool: "we improve the cas scripts iteratively. feel free to add scope / tasks if when doing some work, you noticed some other thing that can be improved with cas scripts." (the user; no goal for this repo alone is written in the repo)

## Open work

### statbtrfs 0.45 (no written plan; the main session's list from the 0.44 reviews and the week-47 gate)
- **Building (started 2026-11-14):** branch feat/045 (worktree statbtrfs-045); the rows of this section are in the build.
- **Say what `btrfs scrub cancel` answered.** State: not started. Where: `cancel_scrub()` in statbtrfs.py drops the command's output and exit code, and the Ctrl-C path prints "Cancelled scrub on X: it keeps its progress, continue it with ..." whatever btrfs said. Fix: read the exit code and print what btrfs said when the cancel failed (a scrub that finished while the prompt waited gives "not running", where the resume advice is wrong; a failed cancel under the per-command sudo fallback leaves the scrub running). This is also the deferred entry '"Cancelled scrub" is printed whatever `btrfs scrub cancel` answered' in docs/limitations.md ("Revisit when: 0.45", noted 2026-11-11 from the 0.44 final review; the entry stays there until the fix ships). From: a deferral, not asked.
- **A macOS-only test bug: `test_main_scrub_starts_once_per_filesystem` calls the real `os.statvfs`.** State: not started. Where: tests/test_cli.py (the test stubs `start_scrub` but not `is_read_only()`, statbtrfs.py, which calls `os.statvfs(mount).f_flag`), so on macOS, or on any host where one of the test's mount points is read-only, `scrub_mount()` picks a different mount and the expected starts differ. Same on 0.43. Fix: stub `statbtrfs.is_read_only` (or `os.statvfs`) in the test. Test-only; found by the week-47 gate. From: the main session's plan (2026-11-13).
- **Add Python 3.11 to the CI matrix.** State: not started. Where: .github/workflows/test.yml has 3.9, 3.12, 3.14 and the 3.6 container; no 3.11. From: the user, 2026-11-12: "Add 3.11 to CI (Recommended)", for every repo's next release.
- **Embed multiCMD 1.67.** State: not started (multiCMD 1.67 was released 2026-11-14). Where: statbtrfs.py embeds 1.61 (gate `< (1, 61)` near the top of the file). Paste the `multiCMD_min_zlib_a85.py` block from the 1.67 tag (not a fresh regeneration), update the gate, and the README's "The embedded multiCMD is now ..." note. From: the main session's plan.
- **Drop `install_requires` multiCMD.** State: not started; the user's pick 2026-11-14, "Drop it, as hpcp did (Recommended)" (their 2026-11-06 pick had kept the floor at 1.56; hpcp dropped it in 9.89). Where: setup.py `install_requires=['multiCMD>=1.56']`; the `multiCMD` line in requirements.txt; the README's pip 9 `-U` notes in the "Upgrading to ..." sections. Why: the embedded copy makes the dependency moot, and it is what makes pip 9 (stock on EL7 and EL8) stop `pip3 install -U statbtrfs` when multiCMD 1.57 or earlier is installed. From: the main session's plan (2026-11-11).
- **setup.py needs multiSSH3's conditional `license_expression`.** State: not started. Where: setup.py still has the `License :: ...` classifier and `license='GPLv3+'`, so setuptools 77 and later warn "License classifiers are deprecated"; multiSSH3/setup.py has the pattern (setuptools 77 and later: `license_expression` and `license_files`; older: the free-text `license` and the classifier). The repo has a LICENSE and no MANIFEST.in, so the sdist's LICENSE for old setuptools needs one too. From: the main session's plan (the 2026-11-07 license survey).

### Standing rows
- **Deferred work** is in `docs/limitations.md` (entries of kind "deferred"); each names when it is revisited.

## Standing decisions
The user's rulings on how the cas repos are worked, one line each; a line changes only on the user's word. The cas monorepo's CLAUDE.md holds the same list, with how to reach the test machines.
- Deferrals (2026-11-05): "please do not ask me about features you think should defer to next version anymore. instead, note them down and after getting the current version done, start the next version right away. only ask me to approve things that are going into limitations that we do not have plans to fix it any time soon."
- The release gate (2026-11-09): "releasing a new version gate is only if it does not make an existing issue worse. even if the fix does not completely resolve the problem, if it makes the result more tolerable, we shall not gate it for release because there are still issues."
- Review before upload (2026-10-18): "commit and push is fine but when packaging, please follow the rule that need a code review before uvpack / upload to pypi".
- A test that passed only on a rerun (2026-11-06, "Green with a warning (Recommended)"): CI stays green with a warning, and "Before any upload, every such test still needs a written cause either way."
- Release pushes (2026-11-10, "Release OK covers it (Recommended)"): an OK for a release covers its push of main, the version tag and the GitHub release.
- Tests (2026-11-12, "Core per release, full at roll-up (Recommended)"): CI's own command on Python 3.14 and 3.11 in Docker before each release; the full gate (every Python in CI, macOS, EL7 on Python 3.11) before a Monday roll-up pin moves.
- CentOS 7 (2026-11-04): "for centos 7, which is already EOL, we only target all the last packages released for it. this also includes EPEL which is also in archive right now."
- EL8 (2026-11-05): "yes rocky 8 it is. let's also only test on them when you think test on real kernel is needed."
- macOS (2026-11-11): tests run on the user's own always-on Mac, as a standard user made for them, never with sudo.

## Questions waiting for the user
- None.

## Closed
- (none yet)
