import platform
from typing import Any, Dict, List


if platform.system() == "Windows":
    import winreg
else:
    winreg = None


def get_startup_analysis() -> Dict[str, Any]:
    """
    Analyze applications configured to start automatically with Windows.
    """

    if platform.system() != "Windows":
        return {
            "success": False,
            "error": "Startup analysis is currently supported on Windows only.",
            "startup_items": [],
        }

    startup_locations = [
        (
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            "HKCU",
        ),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            "HKLM",
        ),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
            "HKLM 32-bit",
        ),
    ]

    startup_items: List[Dict[str, Any]] = []

    for hive, path, source in startup_locations:
        try:
            with winreg.OpenKey(hive, path) as key:
                value_count = winreg.QueryInfoKey(key)[1]

                for index in range(value_count):
                    try:
                        name, command, _ = winreg.EnumValue(key, index)

                        startup_items.append(
                            {
                                "Name": name,
                                "Command": str(command),
                                "Source": source,
                            }
                        )

                    except OSError:
                        continue

        except (FileNotFoundError, PermissionError, OSError):
            continue

    startup_items.sort(
        key=lambda item: item["Name"].lower()
    )

    return {
        "success": True,
        "platform": "Windows",
        "total_startup_items": len(startup_items),
        "startup_items": startup_items,
    }