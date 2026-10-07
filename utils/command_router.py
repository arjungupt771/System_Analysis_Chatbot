import re
from dataclasses import dataclass
from enum import Enum


class CommandIntent(str, Enum):
    CHAT = "chat"
    SYSTEM_INFO = "system_info"
    PROCESS_ANALYSIS = "process_analysis"
    STARTUP_ANALYSIS = "startup_analysis"
    STORAGE_ANALYSIS = "storage_analysis"
    SOFTWARE_SCAN = "software_scan"
    SOFTWARE_INSTALL = "software_install"
    OPEN_URL = "open_url"
    LAUNCH_APPLICATION = "launch_application"
    UNKNOWN = "unknown"


@dataclass
class RoutedCommand:
    intent: CommandIntent
    command: str
    confidence: float
    requires_confirmation: bool = False


def route_command(command):
    """
    Classify a user command into a safe system-assistant intent.

    This function only identifies intent.
    It does not execute any system action.
    """

    if not command or not isinstance(command, str):
        return RoutedCommand(
            intent=CommandIntent.UNKNOWN,
            command="",
            confidence=0.0,
        )

    text = command.strip().lower()

    if not text:
        return RoutedCommand(
            intent=CommandIntent.UNKNOWN,
            command="",
            confidence=0.0,
        )

    # ---------------------------------------------------------
    # Software installation
    # ---------------------------------------------------------

    install_match = re.match(
        r"^\s*install\s+(.+?)\s*$",
        text,
        re.IGNORECASE,
    )

    if install_match:
        return RoutedCommand(
            intent=CommandIntent.SOFTWARE_INSTALL,
            command=command.strip(),
            confidence=1.0,
            requires_confirmation=True,
        )

    # ---------------------------------------------------------
    # Software scan
    # ---------------------------------------------------------

    software_keywords = (
        "scan apps",
        "scan applications",
        "installed software",
        "installed applications",
        "list installed apps",
        "show installed apps",
        "software inventory",
        "application inventory",
    )

    if any(keyword in text for keyword in software_keywords):
        return RoutedCommand(
            intent=CommandIntent.SOFTWARE_SCAN,
            command=command.strip(),
            confidence=0.95,
        )

    # ---------------------------------------------------------
    # Process analysis
    # ---------------------------------------------------------

    process_keywords = (
        "processes",
        "running processes",
        "running apps",
        "cpu usage",
        "ram usage",
        "memory usage",
        "high cpu",
        "high memory",
        "task manager",
        "what is using my cpu",
        "what is using my ram",
    )

    if any(keyword in text for keyword in process_keywords):
        return RoutedCommand(
            intent=CommandIntent.PROCESS_ANALYSIS,
            command=command.strip(),
            confidence=0.90,
        )

    # ---------------------------------------------------------
    # Startup analysis
    # ---------------------------------------------------------

    startup_keywords = (
        "startup apps",
        "startup programs",
        "startup applications",
        "boot apps",
        "boot programs",
        "what starts with windows",
        "windows startup",
    )

    if any(keyword in text for keyword in startup_keywords):
        return RoutedCommand(
            intent=CommandIntent.STARTUP_ANALYSIS,
            command=command.strip(),
            confidence=0.95,
        )

    # ---------------------------------------------------------
    # Storage analysis
    # ---------------------------------------------------------

    storage_keywords = (
        "disk space",
        "storage usage",
        "storage analysis",
        "disk usage",
        "large files",
        "largest files",
        "what is using my disk",
        "what is taking space",
        "free space",
    )

    if any(keyword in text for keyword in storage_keywords):
        return RoutedCommand(
            intent=CommandIntent.STORAGE_ANALYSIS,
            command=command.strip(),
            confidence=0.90,
        )

    # ---------------------------------------------------------
    # System information
    # ---------------------------------------------------------

    system_keywords = (
        "system information",
        "system info",
        "hardware information",
        "hardware info",
        "pc specifications",
        "pc specs",
        "computer specifications",
        "computer specs",
        "system specifications",
        "system specs",
    )

    if any(keyword in text for keyword in system_keywords):
        return RoutedCommand(
            intent=CommandIntent.SYSTEM_INFO,
            command=command.strip(),
            confidence=0.90,
        )

    # ---------------------------------------------------------
    # Normal conversational request
    # ---------------------------------------------------------

    conversational_keywords = (
        "hello",
        "hi",
        "hey",
        "what can you do",
        "help",
        "who are you",
    )

    if any(keyword == text for keyword in conversational_keywords):
        return RoutedCommand(
            intent=CommandIntent.CHAT,
            command=command.strip(),
            confidence=0.85,
        )

    if text.startswith("open http://") or text.startswith("open https://"):
        return RoutedCommand(
            intent=CommandIntent.OPEN_URL,
            command=command,
            confidence=0.98,
            requires_confirmation=False,
        )

    launch_patterns = (
        "open notepad",
        "open calculator",
        "open calc",
        "launch notepad",
        "launch calculator",
        "launch calc",
    )

    if text in launch_patterns:
        return RoutedCommand(
            intent=CommandIntent.LAUNCH_APPLICATION,
            command=command,
            confidence=0.95,
            requires_confirmation=False,
        )

    # ---------------------------------------------------------
    # Unknown → allow Gemini to handle it as normal chat
    # ---------------------------------------------------------

    return RoutedCommand(
        intent=CommandIntent.UNKNOWN,
        command=command.strip(),
        confidence=0.30,
    )
