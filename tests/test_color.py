import statbtrfs


def test_color_error_count_thresholds():
    assert statbtrfs.GREEN in statbtrfs.color_error_count(0)
    assert statbtrfs.YELLOW in statbtrfs.color_error_count(1)
    assert statbtrfs.YELLOW in statbtrfs.color_error_count(9)
    assert statbtrfs.RED in statbtrfs.color_error_count(10)
    assert "0" in statbtrfs.color_error_count(0)
    assert "12" in statbtrfs.color_error_count(12)
