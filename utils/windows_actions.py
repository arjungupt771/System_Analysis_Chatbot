import platform
import subprocess
import webbrowser
from typing import Any, Dict


WINDOWS_APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
}


def _windows_only_error() -> Dict[str, Any]:
    return {
        "success": False,
        "error": "Windows actions are currently supported on Windows only.",
    }


def open_url(url: str) -> Dict[str, Any]:
    if platform.system() != "Windows":
        return _windows_only_error()

    if not url:
        return {
            "success": False,
            "error": "No URL was provided.",
        }

    try:
        webbrowser.open(url)

        return {
            "success": True,
            "action": "open_url",
            "url": url,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


def launch_application(application: str) -> Dict[str, Any]:
    if platform.system() != "Windows":
        return _windows_only_error()

    if not application:
        return {
            "success": False,
            "error": "No application was provided.",
        }

    normalized_application = application.strip().lower()

    executable = WINDOWS_APPLICATIONS.get(normalized_application)

    if executable is None:
        return {
            "success": False,
            "error": (
                f"Application '{application}' is not allowed. "
                f"Supported applications: "
                f"{', '.join(sorted(WINDOWS_APPLICATIONS.keys()))}."
            ),
        }

    try:
        subprocess.Popen(
            [executable],
            shell=False,
        )

        return {
            "success": True,
            "action": "launch_application",
            "application": normalized_application,
            "executable": executable,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }