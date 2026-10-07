from utils.command_router import CommandIntent, route_command


def test_software_install():
    result = route_command("install vlc")

    assert result.intent == CommandIntent.SOFTWARE_INSTALL
    assert result.confidence == 1.0
    assert result.requires_confirmation is True


def test_software_scan():
    result = route_command("scan apps")

    assert result.intent == CommandIntent.SOFTWARE_SCAN
    assert result.confidence >= 0.9


def test_process_analysis():
    result = route_command("show running processes")

    assert result.intent == CommandIntent.PROCESS_ANALYSIS
    assert result.confidence >= 0.9


def test_startup_analysis():
    result = route_command("startup apps")

    assert result.intent == CommandIntent.STARTUP_ANALYSIS
    assert result.confidence >= 0.9


def test_storage_analysis():
    result = route_command("largest files")

    assert result.intent == CommandIntent.STORAGE_ANALYSIS
    assert result.confidence >= 0.9


def test_system_info():
    result = route_command("system info")

    assert result.intent == CommandIntent.SYSTEM_INFO
    assert result.confidence >= 0.9


def test_open_url():
    result = route_command("open https://example.com")

    assert result.intent == CommandIntent.OPEN_URL
    assert result.confidence >= 0.9


def test_launch_application():
    result = route_command("open notepad")

    assert result.intent == CommandIntent.LAUNCH_APPLICATION
    assert result.confidence >= 0.9


def test_conversational_command():
    result = route_command("hello")

    assert result.intent == CommandIntent.CHAT


def test_unknown_command():
    result = route_command("tell me a joke")

    assert result.intent == CommandIntent.UNKNOWN
