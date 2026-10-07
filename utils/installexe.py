import os
import platform
import re
import subprocess
import tempfile

import requests
import streamlit as st

from Software_Catalog import get_software_info


def _is_windows():
    """Return True when running on Windows."""
    return platform.system().lower() == "windows"


def install_exe(exe_file):
    """
    Install a user-uploaded Windows executable.

    The executable is written to a temporary directory and executed.
    This function is intended for Windows only.
    """
    if not _is_windows():
        st.error(
            "❌ EXE installation is supported only on Windows."
        )
        return False

    tmp_exe_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".exe",
        ) as tmp_exe_file:

            tmp_exe_file.write(
                exe_file.getbuffer()
            )

            tmp_exe_path = tmp_exe_file.name

        st.info(
            f"⚙️ Starting installation: {os.path.basename(tmp_exe_path)}"
        )

        subprocess.run(
            [tmp_exe_path],
            check=True,
            timeout=300,
        )

        st.success(
            "✅ Installation completed successfully."
        )

        return True

    except subprocess.TimeoutExpired:
        st.error(
            "❌ Installation timed out after 5 minutes."
        )
        return False

    except subprocess.CalledProcessError as e:
        st.error(
            f"❌ Installer exited with error code {e.returncode}."
        )
        return False

    except Exception as e:
        st.error(
            f"❌ An error occurred while installing the software: {e}"
        )
        return False

    finally:
        if tmp_exe_path and os.path.exists(tmp_exe_path):
            try:
                os.remove(tmp_exe_path)
            except OSError:
                pass


def parse_software_name(command):
    """
    Extract a software name from an install command.

    Example:
        install vlc media player
        -> vlc media player
    """
    match = re.search(
        r"^\s*install\s+(.+?)\s*$",
        command,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).strip().lower()

    return None


def is_software_installed(
    path_check=None,
    software_name=None,
):
    """
    Check whether software is installed on Windows.

    Uses both:
    1. Windows installation path, when provided.
    2. Windows uninstall registry entries.
    """

    if not _is_windows():
        return False

    # ---------------------------------
    # Fast path: explicit installation path
    # ---------------------------------
    if path_check and os.path.exists(path_check):
        return True

    if not software_name:
        return False

    # ---------------------------------
    # Windows Registry detection
    # ---------------------------------
    try:
        import winreg

        registry_locations = [
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
        ]

        target = software_name.lower().strip()

        for hive, registry_path in registry_locations:

            try:
                with winreg.OpenKey(
                    hive,
                    registry_path,
                ) as uninstall_key:

                    for index in range(
                        winreg.QueryInfoKey(uninstall_key)[0]
                    ):

                        try:
                            subkey_name = winreg.EnumKey(
                                uninstall_key,
                                index,
                            )

                            with winreg.OpenKey(
                                uninstall_key,
                                subkey_name,
                            ) as software_key:

                                try:
                                    display_name = winreg.QueryValueEx(
                                        software_key,
                                        "DisplayName",
                                    )[0]

                                except FileNotFoundError:
                                    continue

                                if (
                                    isinstance(
                                        display_name,
                                        str,
                                    )
                                    and target
                                    in display_name.lower()
                                ):
                                    return True

                        except (
                            OSError,
                            FileNotFoundError,
                        ):
                            continue

            except (
                OSError,
                FileNotFoundError,
            ):
                continue

    except ImportError:
        # winreg exists only on Windows.
        return False

    return False


def download_and_install_software(software_key):
    """
    Download and silently install software from the local catalog.

    This function is Windows-only.
    """
    if not _is_windows():
        st.error(
            "❌ Software installation is supported only on Windows."
        )
        return False

    info = get_software_info(software_key)

    if not info:
        st.error(
            "❌ The software is not available in the catalog."
        )
        return False

    software_name = info.get(
        "name",
        software_key,
    ).title()

    install_path = info.get(
        "install_path"
    )

    # Check whether the software is already installed.
    if is_software_installed(
        path_check=install_path,
        software_name=software_name,
    ):
        st.success(
            f"✅ {software_name} is already available on this system."
        )
        return True

    url = info.get("url")
    installer_name = info.get(
        "installer",
        f"{software_key.replace(' ', '_')}_installer.exe",
    )
    silent_flag = info.get(
        "silent_flag"
    )

    if not url:
        st.error(
            f"❌ No download URL configured for {software_name}."
        )
        return False

    # Use a temporary directory instead of the project directory.
    with tempfile.TemporaryDirectory() as temp_dir:

        installer_path = os.path.join(
            temp_dir,
            installer_name,
        )

        st.info(
            f"⬇️ Downloading {software_name}..."
        )

        try:
            with requests.get(
                url,
                stream=True,
                timeout=60,
            ) as response:

                response.raise_for_status()

                with open(
                    installer_path,
                    "wb",
                ) as installer_file:

                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):

                        if chunk:
                            installer_file.write(chunk)

            st.success(
                "📥 Download complete."
            )

        except requests.RequestException as e:
            st.error(
                f"❌ Download failed: {e}"
            )
            return False

        except OSError as e:
            st.error(
                f"❌ Could not save installer: {e}"
            )
            return False

        # Build installer command.
        command = [installer_path]

        if silent_flag:
            command.append(silent_flag)

        st.info(
            f"⚙️ Installing {software_name}..."
        )

        try:
            subprocess.run(
                command,
                check=True,
                timeout=600,
            )

            st.success(
                f"✅ {software_name} installed successfully!"
            )

            return True

        except subprocess.TimeoutExpired:
            st.error(
                f"❌ {software_name} installation timed out."
            )
            return False

        except subprocess.CalledProcessError as e:
            st.error(
                f"❌ {software_name} installer exited "
                f"with error code {e.returncode}."
            )
            return False

        except OSError as e:
            st.error(
                f"❌ Could not start {software_name} installer: {e}"
            )
            return False