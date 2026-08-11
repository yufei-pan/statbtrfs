import statbtrfs
from fakes import SHOW_INCOMPLETE, SHOW_MULTI_DEVICE, SHOW_SINGLE


def test_parse_show_single_device():
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_SINGLE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "12.34GiB"
    assert device_path == "/dev/sda1"


def test_parse_show_multi_device_paths_joined():
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_MULTI_DEVICE)
    assert uuid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert fs_used == "1.00GiB"
    assert device_path == "/dev/nvme0n1, /dev/nvme1n1"


def test_parse_show_incomplete_returns_nones(capsys):
    uuid, fs_used, device_path = statbtrfs.parse_show_info(SHOW_INCOMPLETE)
    assert uuid == "11111111-2222-3333-4444-555555555555"
    assert fs_used == "1.00GiB"
    assert device_path is None
    out = capsys.readouterr().out
    assert "Could not parse btrfs show info" in out
