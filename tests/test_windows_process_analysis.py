from unittest.mock import patch

from utils.process_analysis import get_process_analysis


@patch("utils.process_analysis.platform.system", return_value="Windows")
@patch("utils.process_analysis.psutil.process_iter")
def test_process_analysis_returns_windows_data(mock_process_iter, mock_system):
    class FakeProcess:
        info = {
            "pid": 1234,
            "name": "test.exe",
            "status": "running",
        }

        def cpu_percent(self, interval=None):
            return 25.5

        def memory_info(self):
            class Memory:
                rss = 200 * 1024 * 1024

            return Memory()

        def username(self):
            return "TEST\\User"

        def status(self):
            return "running"

    mock_process_iter.return_value = [FakeProcess()]

    result = get_process_analysis(limit=5)

    assert result["success"] is True
    assert result["platform"] == "Windows"
    assert result["total_processes"] == 1
    assert result["processes"][0]["Name"] == "test.exe"
    assert result["processes"][0]["PID"] == 1234
    assert result["processes"][0]["CPU %"] == 25.5
    assert result["processes"][0]["Memory (MB)"] == 200.0


@patch("utils.process_analysis.platform.system", return_value="Linux")
def test_process_analysis_rejects_non_windows(mock_system):
    result = get_process_analysis()

    assert result["success"] is False
    assert "Windows only" in result["error"]