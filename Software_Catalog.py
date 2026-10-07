# Software_Catalog.py

SOFTWARE_CATALOG = {
    "vlc media player": {
        "name": "VLC Media Player",
        "url": "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
        "installer": "vlc_installer.exe",
        "silent_flag": "/S",
        "install_path": r"C:\Program Files\VideoLAN\VLC",
    },
    "vlc": {
        "name": "VLC Media Player",
        "url": "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
        "installer": "vlc_installer.exe",
        "silent_flag": "/S",
        "install_path": r"C:\Program Files\VideoLAN\VLC",
    },
    "notepad++": {
        "name": "Notepad++",
        "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.8/npp.8.5.8.Installer.x64.exe",
        "installer": "notepadpp_installer.exe",
        "silent_flag": "/S",
        "install_path": r"C:\Program Files\Notepad++",
    },
}


def get_software_info(name):

    if not name:
        return None

    normalized_name = name.lower().strip()

    return SOFTWARE_CATALOG.get(normalized_name)