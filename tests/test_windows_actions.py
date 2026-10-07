from unittest.mock import patch

from utils.command_router import route_command
from utils.tool_executor import execute_tool
from utils.windows_actions import launch_application, open_url


def test_open_url_rejects_non_windows():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Linux",
    ):
        result = open_url("https://example.com")

    assert result["success"] is False
    assert "Windows only" in result["error"]


def test_launch_application_rejects_non_windows():
    with patch(
        "utils.windows_actions.platform.system",
        return_value="Linux",
    ):
        result = launch_application("notepad")

    assert result["success"] is False
    assert "Windows only" in result["error"]


def test_open_url_router_and_executor():
    command = route_command("open https://example.com")

    assert command.intent.value == "open_url"
    assert command.confidence == 0.98
    assert command.requires_confirmation is False

    with patch(
        "utils.tool_executor.get_tool",
        return_value={
            "name": "Open URL",
            "function": lambda url: {
                "success": True,
                "action": "open_url",
                "url": url,
            },
            "requires_confirmation": False,
        },
    ):
        result = execute_tool(command)

    assert result.success is True
    assert result.requires_confirmation is False
    assert result.risk == "low"
    assert result.result["url"] == "https://example.com"


def test_launch_application_requires_confirmation():
    command = route_command("open notepad")

    assert command.intent.value == "launch_application"

    result = execute_tool(command)

    assert result.success is False
    assert result.requires_confirmation is True
    assert result.risk == "medium"


def test_software_install_requires_high_risk_confirmation():
    command = route_command("install vlc")

    assert command.intent.value == "software_install"
    assert command.requires_confirmation is True

    result = execute_tool(command)

    assert result.success is False
    assert result.requires_confirmation is True
    assert result.risk == "high"


def test_launch_application_executes_after_confirmation():
    command = route_command("open notepad")

    with patch(
        "utils.tool_executor.get_tool",
        return_value={
            "name": "Launch Windows Application",
            "function": lambda application: {
                "success": True,
                "action": "launch_application",
                "application": application,
            },
            "requires_confirmation": False,
        },
    ):
        result = execute_tool(command, confirmed=True)

    assert result.success is True
    assert result.requires_confirmation is False
    assert result.risk == "medium"
    assert result.result["application"] == "notepad"


def test_open_url_does_not_require_confirmation():
    command = route_command("open https://example.com")

    with patch(
        "utils.tool_executor.get_tool",
        return_value={
            "name": "Open URL",
            "function": lambda url: {
                "success": True,
                "url": url,
            },
            "requires_confirmation": False,
        },
    ):
        result = execute_tool(command, confirmed=False)

    assert result.success is True
    assert result.requires_confirmation is False
