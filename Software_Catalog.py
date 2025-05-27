# software_catalog.py

SOFTWARE_CATALOG = {
    "vlc media player": {
        "name":"vlc",
        "url": "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
        "installer": "vlc_installer.exe",
        "silent_flag": "/S",
        "install_path":"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VideoLAN"
    },
    "notepad++": {
        "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.8/npp.8.5.8.Installer.x64.exe",
        "installer": "notepadpp_installer.exe",
        "silent_flag": "/S"
    },
    # Add more software here as needed
}

def get_software_info(name):
    """Return catalog entry for a given software name, or None if not found."""
    name = name.lower().strip()
    return SOFTWARE_CATALOG.get(name)
