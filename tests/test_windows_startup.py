from unittest.mock import MagicMock, patch

from utils.startup_analysis import get_startup_analysis


def test_startup_analysis_rejects_non_windows():
    with patch(
        "utils.startup_analysis.platform.system",
        return_value="Linux",
    ):
        result = get_startup_analysis()

    assert result["success"] is False
    assert "Windows only" in result["error"]


def test_startup_analysis_windows():
    fake_winreg = MagicMock()

    fake_winreg.HKEY_CURRENT_USER = "HKCU"
    fake_winreg.HKEY_LOCAL_MACHINE = "HKLM"

    fake_key = MagicMock()

    fake_winreg.OpenKey.return_value = fake_key
    fake_winreg.QueryInfoKey.return_value = (0, 2, 0)

    fake_winreg.EnumValue.side_effect = [
        ("Discord", r"C:\Discord\Discord.exe", 1),
        ("OneDrive", r"C:\OneDrive\OneDrive.exe", 1),
    ] * 3

    with patch(
        "utils.startup_analysis.platform.system",
        return_value="Windows",
    ), patch(
        "utils.startup_analysis.winreg",
        fake_winreg,
    ):
        result = get_startup_analysis()

    assert result["success"] is True
    assert result["platform"] == "Windows"
    assert result["total_startup_items"] == 6

    names = [item["Name"] for item in result["startup_items"]]

    assert "Discord" in names
    assert "OneDrive" in names