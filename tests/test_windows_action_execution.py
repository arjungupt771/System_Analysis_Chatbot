from unittest.mock import patch

from utils.windows_actions import launch_application, open_url


def test_open_url_calls_browser_on_windows():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Windows",
    ), patch(
        "utils.windows_actions.webbrowser.open",
        return_value=True,
    ) as mock_open:

        result = open_url("https://example.com")

    assert result["success"] is True
    assert result["action"] == "open_url"
    assert result["url"] == "https://example.com"

    mock_open.assert_called_once_with("https://example.com")


def test_open_url_handles_browser_failure():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Windows",
    ), patch(
        "utils.windows_actions.webbrowser.open",
        side_effect=RuntimeError("Browser failed"),
    ):

        result = open_url("https://example.com")

    assert result["success"] is False
    assert "Browser failed" in result["error"]


def test_launch_application_calls_popen_on_windows():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Windows",
    ), patch(
        "utils.windows_actions.subprocess.Popen",
    ) as mock_popen:

        result = launch_application("notepad")

    assert result["success"] is True
    assert result["action"] == "launch_application"
    assert result["application"] == "notepad"
    assert result["executable"] == "notepad.exe"

    mock_popen.assert_called_once_with(
        ["notepad.exe"],
        shell=False,
    )


def test_launch_application_handles_process_failure():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Windows",
    ), patch(
        "utils.windows_actions.subprocess.Popen",
        side_effect=RuntimeError("Application launch failed"),
    ):

        result = launch_application("notepad")

    assert result["success"] is False
    assert "Application launch failed" in result["error"]

def test_launch_application_blocks_unapproved_application():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Windows",
    ), patch(
        "utils.windows_actions.subprocess.Popen",
    ) as mock_popen:

        result = launch_application("powershell")

    assert result["success"] is False
    assert "not allowed" in result["error"]

    mock_popen.assert_not_called()
