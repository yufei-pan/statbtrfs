import statbtrfs
from fakes import SUBVOL_SHOWS, CommandMap, install_command_map, uuid_for


def _show_map(monkeypatch, shows):
    cm = CommandMap({("btrfs", "filesystem", "show", m): show for m, show in shows.items()})
    return install_command_map(monkeypatch, cm, statbtrfs)


def test_discover_groups_mounts_by_uuid(monkeypatch):
    _show_map(monkeypatch, SUBVOL_SHOWS)
    filesystems = statbtrfs.discover_filesystems(["/home", "/mnt/pool", "/", "/var/log"])
    by_uuid = {fs["uuid"]: fs["mounts"] for fs in filesystems}
    assert by_uuid == {
        uuid_for(1): ["/", "/home", "/var/log"],
        uuid_for(2): ["/mnt/pool"],
    }


def test_discover_orders_filesystems_by_first_mountpoint(monkeypatch):
    _show_map(monkeypatch, SUBVOL_SHOWS)
    filesystems = statbtrfs.discover_filesystems(["/mnt/pool", "/var/log", "/home", "/"])
    assert [fs["mounts"][0] for fs in filesystems] == ["/", "/mnt/pool"]


def test_discover_keeps_unparseable_mounts_separate(monkeypatch):
    _show_map(monkeypatch, {})  # every show returns []
    filesystems = statbtrfs.discover_filesystems(["/x", "/y"])
    assert sorted(fs["mounts"] for fs in filesystems) == [["/x"], ["/y"]]
    assert all(fs["uuid"] is None for fs in filesystems)


def test_discover_no_mounts_finds_nothing(monkeypatch):
    _show_map(monkeypatch, {})
    assert statbtrfs.discover_filesystems([]) == []


def test_select_filesystems_matches_any_mountpoint():
    filesystems = [
        {"uuid": uuid_for(1), "mounts": ["/", "/home", "/var/log"]},
        {"uuid": uuid_for(2), "mounts": ["/mnt/pool"]},
    ]
    assert statbtrfs.select_filesystems(filesystems, []) == filesystems
    assert statbtrfs.select_filesystems(filesystems, ["home"]) == filesystems[:1]
    assert statbtrfs.select_filesystems(filesystems, ["pool", "log"]) == filesystems
    assert statbtrfs.select_filesystems(filesystems, ["nothing"]) == []
