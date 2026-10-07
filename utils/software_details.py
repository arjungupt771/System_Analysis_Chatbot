import datetime
import json
import os
import platform
import shutil
import subprocess

try:
    import psutil
except ImportError:
    psutil = None
    print(
        "Warning: psutil library not found. "
        "Some system hardware details will be unavailable."
    )
    print("Install it with: pip install psutil")


def get_appx_packages():
    """Get Windows Store/AppX applications using PowerShell."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "Get-AppxPackage -AllUsers | "
                "Select Name, InstallLocation | ConvertTo-Json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print(f"PowerShell error while getting AppX packages: {result.stderr}")
            return []

        if not result.stdout.strip():
            return []

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError, Exception) as e:
        print(f"Error getting AppX packages: {e}")
        return []


def get_win32_apps():
    """Get traditional Windows applications from uninstall registry keys."""

    powershell_script = r"""
$keys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

$apps = foreach ($key in $keys) {
    Get-ItemProperty $key -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } |
    Select-Object DisplayName, InstallLocation
}

$uniqueApps = $apps | Sort-Object DisplayName -Unique
$uniqueApps | ConvertTo-Json
"""

    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print(
                "PowerShell script for get_win32_apps returned an error. "
                f"Stderr: {result.stderr}"
            )
            return []

        if not result.stdout.strip():
            return []

        parsed_output = json.loads(result.stdout)

        if isinstance(parsed_output, dict):
            return [parsed_output]

        if isinstance(parsed_output, list):
            return parsed_output

        print(
            "Warning: Unexpected data type from PowerShell JSON: "
            f"{type(parsed_output)}"
        )
        return []

    except json.JSONDecodeError as e:
        print(f"Error parsing Windows application data: {e}")
        return []

    except OSError as e:
        print(f"Could not execute PowerShell: {e}")
        return []

    except Exception as e:
        print(f"Unexpected error in get_win32_apps: {e}")
        return []


def get_folder_size(path):
    """Recursively calculate folder size in bytes."""

    total_size = 0

    if not path or not os.path.exists(path):
        return 0

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            try:
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
            except (OSError, PermissionError):
                continue

    return total_size


def get_last_updated_date(path):
    """Get the last modified date of an installation folder."""

    try:
        timestamp = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except (OSError, TypeError, ValueError):
        return "Unknown"


def scan_apps_and_storage():
    """Scan Windows applications and calculate their storage usage."""

    system_apps = get_appx_packages()
    downloaded_apps = get_win32_apps()

    system_total = 0
    downloaded_total = 0

    system_list = []
    downloaded_list = []

    # Windows Store / AppX applications
    for app in system_apps:
        path = app.get("InstallLocation")
        name = app.get("Name", "Unknown")

        if path and os.path.exists(path):
            size = get_folder_size(path)
            last_updated = get_last_updated_date(path)

            system_total += size

            system_list.append(
                {
                    "App": name,
                    "Size(MB)": f"{size / 1e6:.2f}",
                    "Last Updated": last_updated,
                }
            )

    # Traditional Windows applications
    for app in downloaded_apps:
        path = app.get("InstallLocation")
        name = app.get("DisplayName", "Unknown")

        if name and path and os.path.exists(path):
            size = get_folder_size(path)
            downloaded_total += size
            last_updated = get_last_updated_date(path)

            downloaded_list.append(
                {
                    "App": name,
                    "Size(MB)": f"{size / 1e6:.2f}",
                    "Last Updated": last_updated,
                }
            )
        else:
            downloaded_list.append(
                {
                    "App": name,
                    "Size(MB)": "N/A",
                    "Last Updated": "N/A",
                }
            )

    return (
        system_list,
        downloaded_list,
        system_total,
        downloaded_total,
    )


def get_hardware_details():
    """Collect Windows hardware and system information."""

    details = {}

    # Operating system
    details["os_version"] = (
        f"{platform.system()} {platform.release()} "
        f"(Version: {platform.version()})"
    )
    details["os_architecture"] = platform.machine()

    # C: drive
    try:
        usage_c = shutil.disk_usage("C:\\")

        details["disk_c_total_gb"] = usage_c.total / (1024**3)
        details["disk_c_used_gb"] = usage_c.used / (1024**3)
        details["disk_c_free_gb"] = usage_c.free / (1024**3)

    except (OSError, ValueError) as e:
        print(f"Could not get disk usage for C: drive: {e}")

        details["disk_c_total_gb"] = "N/A"
        details["disk_c_used_gb"] = "N/A"
        details["disk_c_free_gb"] = "N/A"

    # All available disks
    all_disks_info = []
    total_system_storage_bytes = 0
    processed_devices = set()

    if psutil:
        try:
            partitions = psutil.disk_partitions(all=False)

            for partition in partitions:

                if (
                    "cdrom" in partition.opts
                    or not partition.fstype
                    or "loop" in partition.device.lower()
                    or not partition.mountpoint
                    or not os.path.exists(partition.mountpoint)
                ):
                    continue

                try:
                    usage = shutil.disk_usage(partition.mountpoint)

                    current_disk_total_gb = usage.total / (1024**3)
                    current_disk_used_gb = usage.used / (1024**3)
                    current_disk_free_gb = usage.free / (1024**3)

                    all_disks_info.append(
                        {
                            "mountpoint": partition.mountpoint,
                            "device": partition.device,
                            "fstype": partition.fstype,
                            "total_gb": current_disk_total_gb,
                            "used_gb": current_disk_used_gb,
                            "free_gb": current_disk_free_gb,
                        }
                    )

                    if partition.device not in processed_devices:
                        total_system_storage_bytes += usage.total
                        processed_devices.add(partition.device)

                    if partition.mountpoint.upper() == "C:\\":
                        details["disk_c_total_gb"] = current_disk_total_gb
                        details["disk_c_used_gb"] = current_disk_used_gb
                        details["disk_c_free_gb"] = current_disk_free_gb

                except (OSError, PermissionError):
                    continue

        except Exception as e:
            print(f"Could not get all disk partitions info: {e}")

    details["all_disks"] = all_disks_info
    details["total_system_storage_gb"] = (
        total_system_storage_bytes / (1024**3)
        if total_system_storage_bytes > 0
        else None
    )

    # RAM information
    if psutil:
        try:
            memory = psutil.virtual_memory()

            details["ram_total_gb"] = memory.total / (1024**3)
            details["ram_available_gb"] = memory.available / (1024**3)
            details["ram_used_gb"] = memory.used / (1024**3)
            details["ram_percent_used"] = memory.percent

        except Exception as e:
            print(f"Could not get RAM information: {e}")

            details["ram_total_gb"] = "N/A"
            details["ram_available_gb"] = "N/A"
            details["ram_used_gb"] = "N/A"
            details["ram_percent_used"] = "N/A"

    else:
        details["ram_total_gb"] = "N/A (psutil not found)"
        details["ram_available_gb"] = "N/A (psutil not found)"
        details["ram_used_gb"] = "N/A (psutil not found)"
        details["ram_percent_used"] = "N/A (psutil not found)"

    # CPU information
    details["cpu_model"] = platform.processor()

    if psutil:
        try:
            cpu_frequency = psutil.cpu_freq()

            details["cpu_physical_cores"] = psutil.cpu_count(logical=False)
            details["cpu_logical_cores"] = psutil.cpu_count(logical=True)
            details["cpu_current_freq_mhz"] = (
                cpu_frequency.current if cpu_frequency else "N/A"
            )
            details["cpu_max_freq_mhz"] = (
                cpu_frequency.max if cpu_frequency else "N/A"
            )
            details["cpu_usage_percent"] = psutil.cpu_percent(interval=0.1)

        except Exception as e:
            print(f"Could not get detailed CPU information: {e}")

    return details