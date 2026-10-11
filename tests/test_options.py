"""Command-line options (#10): dash-style names, underscore spellings kept as hidden aliases."""
import pytest

import statbtrfs


@pytest.mark.parametrize("flag", ["-m", "--max-scrub-count", "--max_scrub_count"])
def test_max_scrub_count_spellings(flag):
    assert statbtrfs.build_parser().parse_args([flag, "3"]).max_scrub_count == 3


@pytest.mark.parametrize("flag", ["--scrub-command-lockout", "--scrub_command_lockout"])
def test_scrub_command_lockout_spellings(flag):
    assert statbtrfs.build_parser().parse_args([flag, "4"]).scrub_command_lockout == 4


def test_defaults():
    args = statbtrfs.build_parser().parse_args([])
    assert (args.max_scrub_count, args.scrub_command_lockout, args.interval) == (32, 10, 2)
    assert (args.scrub, args.watch, args.color, args.pattern) == (False, False, "auto", [])


def test_help_shows_only_dash_spellings():
    text = statbtrfs.build_parser().format_help()
    assert "--max-scrub-count" in text and "--scrub-command-lockout" in text
    assert "--max_scrub_count" not in text and "--scrub_command_lockout" not in text


def test_help_documents_exit_codes():
    text = " ".join(statbtrfs.build_parser().format_help().split())
    assert "0 healthy" in text and "1 problems found" in text and "2 the check failed" in text
