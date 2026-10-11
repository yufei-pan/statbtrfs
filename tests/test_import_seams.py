import statbtrfs


def test_module_imports_without_exiting():
    assert hasattr(statbtrfs, "version")
    assert callable(statbtrfs.main)
