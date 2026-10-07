from unittest.mock import patch

from utils.storage_analysis import get_storage_analysis


def test_storage_analysis_rejects_non_windows():
    with patch(
        "utils.storage_analysis.platform.system",
        return_value="Linux",
    ):
        result = get_storage_analysis()

    assert result["success"] is False
    assert "Windows only" in result["error"]


def test_storage_analysis_windows():
    fake_files = {
        r"C:\Users\Test\video.mp4": 500 * 1024 * 1024,
        r"C:\Users\Test\archive.zip": 250 * 1024 * 1024,
        r"C:\Users\Test\document.pdf": 50 * 1024 * 1024,
    }

    def fake_walk(root, topdown=True):
        yield (
            r"C:\Users\Test",
            [],
            [
                "video.mp4",
                "archive.zip",
                "document.pdf",
            ],
        )

    def fake_getsize(path):
        if path in fake_files:
            return fake_files[path]

        raise FileNotFoundError(path)

    def fake_join(directory, name):
        return directory.rstrip("\\/") + "\\" + name

    with patch(
        "utils.storage_analysis.platform.system",
        return_value="Windows",
    ), patch(
        "utils.storage_analysis.os.path.exists",
        return_value=True,
    ), patch(
        "utils.storage_analysis.os.path.abspath",
        side_effect=lambda path: path,
    ), patch(
        "utils.storage_analysis.os.path.join",
        side_effect=fake_join,
    ), patch(
        "utils.storage_analysis.os.walk",
        side_effect=fake_walk,
    ), patch(
        "utils.storage_analysis.os.path.getsize",
        side_effect=fake_getsize,
    ), patch(
        "utils.storage_analysis._directory_depth",
        return_value=1,
    ), patch(
        "utils.storage_analysis._should_skip_directory",
        return_value=False,
    ):

        result = get_storage_analysis(
            root="C:\\",
            max_files=2,
            max_depth=5,
        )

    assert result["success"] is True
    assert result["platform"] == "Windows"

    assert result["scanned_files"] == 3
    assert result["skipped_files"] == 0
    assert result["showing"] == 2

    assert result["files"][0]["File"] == "video.mp4"
    assert result["files"][1]["File"] == "archive.zip"

    assert result["files"][0]["Path"] == r"C:\Users\Test\video.mp4"
    assert result["files"][1]["Path"] == r"C:\Users\Test\archive.zip"

    assert result["files"][0]["Size (MB)"] == 500.0
    assert result["files"][1]["Size (MB)"] == 250.0

    assert result["files"][0]["Size (GB)"] == 0.488
    assert result["files"][1]["Size (GB)"] == 0.244