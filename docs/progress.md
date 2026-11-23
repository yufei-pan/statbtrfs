# statbtrfs: progress

Open work lives here and nowhere else (RULES, "Long work: the progress file"). Edit rows in place, in the commit that changes the work.

## Goal
- 2026-11-05, for every cas tool: "we improve the cas scripts iteratively. feel free to add scope / tasks if when doing some work, you noticed some other thing that can be improved with cas scripts." (the user; no goal for this repo alone is written in the repo)

## Open work

### statbtrfs 0.46 (no written plan; the main session's list from the 0.45 reviews)
- **Small items from the 0.45 reviews, and the embedded multiCMD 1.69 (v1.70 if it is released before the review).** State: built on feat/046 (888dd7c to 8682b89, 2026-11-23), in final review. Item 1 was a real hang: a sudo that wants a password stops in multiCMD's process group and statbtrfs waits until a Ctrl-C (sudo 1.8.23, 1.9.5, 1.9.16); every per-command sudo now runs as `sudo -n` and fails at once with sudo's message. Where:
  - A sudo password prompt from the per-command sudo fallback runs in multiCMD's own process group with stdin from /dev/null; check on a real terminal whether the prompt reaches it, and whether a Ctrl-C cancel can stop there (0.45 second opinion, from reading only; the same spawn path as every sudo call since the fallback came).
  - `cancel_scrub()`'s docstring says the reply is the last line btrfs or sudo printed; with btrfs or sudo missing it is multiCMD's own error text.
  - Tests: tests/test_filter_recent.py:16 patches `execute_command()`, which nothing calls now; the run_command fakes in tests/test_privileges.py ignore `return_object`; `CommandMap.run_scrub_cancel` cannot model a failed cancel.
  From: the 0.45 reviews (the main session's plan, 2026-11-15).

### statbtrfs 0.47 (no written plan: the entry of kind "deferred (0.47)" in docs/limitations.md, on feat/046 until 0.46 merges)
- **Through the per-command fallback, `-s` starts no scrub when sudo wants a password for btrfs** (`run_detached`'s new session has no terminal, so sudo cannot find the password it remembers per terminal; 0.45 failed too, with another message). State: not started. From: 0.46's build (2026-11-23), a deferral, not asked.

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
- 0.45 (tag v0.45, the merge of feat/045, released 2026-11-15): a Ctrl-C cancel that btrfs refused says what btrfs answered and points to `btrfs scrub status` (0.44 printed "Cancelled scrub" whatever it answered); no multiCMD install requirement (the user's pick 2026-11-14, "Drop it, as hpcp did (Recommended)"); the embedded multiCMD 1.67; the SPDX license metadata on setuptools 77 and later; Python 3.11 in CI; the macOS-only test bug; the lessons header's 80 KB rule. Built on feat/045, final review release, a second opinion found `execute_command()` (listed for library callers) had changed its return: back to 0.44's in fix round 1 (3f145d0, 8c29c32), re-review release.
