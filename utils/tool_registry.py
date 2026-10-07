from utils.command_router import CommandIntent
from utils.software_details import scan_apps_and_storage
from utils.software_details import get_hardware_details
from utils.installexe import download_and_install_software
from utils.process_analysis import get_process_analysis
from utils.startup_analysis import get_startup_analysis
from utils.storage_analysis import get_storage_analysis
from utils.windows_actions import open_url, launch_application


TOOLS = {
    CommandIntent.SYSTEM_INFO: {
        "name": "System Information",
        "function": get_hardware_details,
        "requires_confirmation": False,
    },

    CommandIntent.SOFTWARE_SCAN: {
        "name": "Software Scanner",
        "function": scan_apps_and_storage,
        "requires_confirmation": False,
    },

    CommandIntent.SOFTWARE_INSTALL: {
        "name": "Software Installer",
        "function": download_and_install_software,
        "requires_confirmation": True,
    },

    CommandIntent.PROCESS_ANALYSIS: {
        "name": "Process Analysis",
        "function": get_process_analysis,
        "requires_confirmation": False,
    },
    CommandIntent.STARTUP_ANALYSIS: {
        "name": "Windows Startup Analyzer",
        "function": get_startup_analysis,
        "requires_confirmation": False,
    },
    CommandIntent.STORAGE_ANALYSIS: {
        "name": "Windows Storage Analyzer",
        "function": get_storage_analysis,
        "requires_confirmation": False,
    },
    CommandIntent.OPEN_URL: {
        "name": "Open URL",
        "function": open_url,
        "requires_confirmation": False,
    },
    CommandIntent.LAUNCH_APPLICATION: {
        "name": "Launch Windows Application",
        "function": launch_application,
        "requires_confirmation": False,
    },
}


def get_tool(intent):
    """
    Return the registered tool for an intent.

    Returns None when no executable tool is registered yet.
    """
    return TOOLS.get(intent)


def list_available_tools():
    """Return metadata for all registered tools."""
    return {
        intent.value: {
            "name": tool["name"],
            "requires_confirmation": tool[
                "requires_confirmation"
            ],
        }
        for intent, tool in TOOLS.items()
    }
