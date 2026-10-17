import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "server" / "server.py"
spec = importlib.util.spec_from_file_location("airpad_server", MODULE_PATH)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class FakeVolume:
    def __init__(self):
        self.calls = []

    def SetMasterVolumeLevelScalar(self, value, _):
        self.calls.append(("set_volume", value))

    def GetMute(self):
        return False

    def SetMute(self, muted, _):
        self.calls.append(("set_mute", muted))


def test_build_qr_login_url_includes_pin_and_ip():
    url = server.build_qr_login_url("http://10.0.0.5:8080", "1234")
    assert url == "http://10.0.0.5:8080/?pin=1234"


def test_main_does_not_kill_process_when_port_is_in_use(monkeypatch):
    process_calls = []
    monkeypatch.setattr(server, "is_port_in_use", lambda port: port == 8080)

    def fake_run(*args, **kwargs):
        process_calls.append((args, kwargs))

    monkeypatch.setattr(server.subprocess, "run", fake_run)

    try:
        server.main()
    except RuntimeError as exc:
        assert "Port 8080 is already in use" in str(exc)
    else:
        raise AssertionError("startup should fail when the configured port is occupied")
    assert process_calls == []


def test_handle_volume_sets_master_volume_and_unmutes(monkeypatch):
    fake = FakeVolume()
    monkeypatch.setattr(server, "get_volume_interface", lambda: fake)

    server.handle_volume({"value": 25})

    assert ("set_volume", 0.25) in fake.calls
    assert ("set_mute", False) in fake.calls


def test_handle_volume_clamps_out_of_range_values(monkeypatch):
    fake = FakeVolume()
    monkeypatch.setattr(server, "get_volume_interface", lambda: fake)

    server.handle_volume({"value": 150})
    server.handle_volume({"value": -10})

    assert ("set_volume", 1.0) in fake.calls
    assert ("set_volume", 0.0) in fake.calls


def test_handle_media_mute_sets_windows_mute(monkeypatch):
    fake = FakeVolume()
    monkeypatch.setattr(server, "get_volume_interface", lambda: fake)

    server.handle_media({"action": "mute"})

    assert ("set_mute", True) in fake.calls


def test_handle_media_mute_uses_toggle_key_when_volume_api_unavailable(monkeypatch):
    calls = []

    class FakeKbd:
        def press(self, key):
            calls.append(("press", key))

        def release(self, key):
            calls.append(("release", key))

    monkeypatch.setattr(server, "get_volume_interface", lambda: None)
    monkeypatch.setattr(server, "kbd", FakeKbd())

    server.handle_media({"action": "mute"})

    assert calls == [
        ("press", server.Key.media_volume_mute),
        ("release", server.Key.media_volume_mute),
    ]


def test_keyboard_and_slide_handlers_map_supported_keys(monkeypatch):
    calls = []

    class FakeKbd:
        def press(self, key):
            calls.append(("press", key))

        def release(self, key):
            calls.append(("release", key))

    monkeypatch.setattr(server, "kbd", FakeKbd())

    server.handle_key({"key": "enter"})
    server.handle_hotkey({"keys": ["ctrl", "c"]})
    server.handle_slide({"action": "next"})
    server.handle_slide({"action": "prev"})

    assert calls == [
        ("press", server.Key.enter), ("release", server.Key.enter),
        ("press", server.Key.ctrl_l), ("press", "c"),
        ("release", "c"), ("release", server.Key.ctrl_l),
        ("press", server.Key.right), ("release", server.Key.right),
        ("press", server.Key.left), ("release", server.Key.left),
    ]


def test_mouse_handlers_clamp_movement_and_release_held_click(monkeypatch):
    moves = []
    scrolls = []
    clicks = []

    class FakeMouse:
        def press(self, button):
            clicks.append(("press", button))

        def release(self, button):
            clicks.append(("release", button))

        def click(self, button, count=1):
            clicks.append(("click", button, count))

        def scroll(self, dx, dy):
            scrolls.append((dx, dy))

    monkeypatch.setattr(server, "mouse", FakeMouse())
    monkeypatch.setattr(server, "ensure_cursor_visible", lambda: None)
    monkeypatch.setattr(server, "safe_mouse_move", lambda dx, dy: moves.append((dx, dy)))

    server.handle_move({"dx": server.MAX_DX_DY + 1, "dy": -server.MAX_DX_DY - 1})
    server.handle_scroll({"dx": server.MAX_DX_DY + 1, "dy": -server.MAX_DX_DY - 1})
    server.handle_click({"button": "left", "action": "down"}, 123)
    server.handle_click({"button": "left", "action": "up"}, 123)
    server.handle_click({"button": "right", "action": "double"}, 123)

    assert moves == [(server.MAX_DX_DY, -server.MAX_DX_DY)]
    assert scrolls == [(server.MAX_DX_DY, -server.MAX_DX_DY)]
    assert clicks == [
        ("press", server.MButton.left),
        ("release", server.MButton.left),
        ("click", server.MButton.right, 2),
    ]
    assert server.ws_held_buttons[123] == set()


def test_handle_text_types_characters_one_by_one(monkeypatch):
    calls = []

    class FakeKbd:
        def press(self, key):
            calls.append(("press", key))

        def release(self, key):
            calls.append(("release", key))

    monkeypatch.setattr(server, "kbd", FakeKbd())
    server.handle_text({"text": "AB\n"})

    assert calls == [
        ("press", "A"), ("release", "A"),
        ("press", "B"), ("release", "B"),
        ("press", server.Key.enter), ("release", server.Key.enter),
    ]


def test_handle_text_accepts_carriage_return_newlines(monkeypatch):
    calls = []

    class FakeKbd:
        def press(self, key):
            calls.append(("press", key))

        def release(self, key):
            calls.append(("release", key))

    monkeypatch.setattr(server, "kbd", FakeKbd())
    server.handle_text({"text": "A\rB\n"})

    assert calls == [
        ("press", "A"), ("release", "A"),
        ("press", server.Key.enter), ("release", server.Key.enter),
        ("press", "B"), ("release", "B"),
        ("press", server.Key.enter), ("release", server.Key.enter),
    ]


def test_handle_power_uses_safe_creation_flags_when_windows_flag_missing(monkeypatch):
    captured = {}

    class FakePopen:
        def __init__(self, args, **kwargs):
            captured["args"] = args
            captured.update(kwargs)

    monkeypatch.setattr(server.subprocess, "Popen", FakePopen)
    monkeypatch.delattr(server.subprocess, "CREATE_NO_WINDOW", raising=False)

    server.handle_power({"action": "lock"})

    assert captured["args"] == ["rundll32.exe", "user32.dll,LockWorkStation"]
    assert captured["creationflags"] == 0


def test_ensure_cursor_visible_forces_windows_pointer_visible(monkeypatch):
    calls = []

    class FakeUser32:
        @staticmethod
        def ShowCursor(show):
            calls.append(show)
            return -1 if len(calls) < 3 else 0

    monkeypatch.setattr(server, "ctypes", type("CtypesShim", (), {"windll": type("WindllShim", (), {"user32": FakeUser32()})}), raising=False)

    server.ensure_cursor_visible()

    assert calls == [True, True, True]


def test_safe_mouse_move_uses_screen_center_when_cursor_missing(monkeypatch):
    class FakeMouse:
        def __init__(self):
            self._position = None

        @property
        def position(self):
            return self._position

        @position.setter
        def position(self, value):
            self._position = value

    fake_mouse = FakeMouse()
    monkeypatch.setattr(server, "mouse", fake_mouse)
    monkeypatch.setattr(server, "get_primary_screen_center", lambda: (960, 540))

    server.safe_mouse_move(25, -10)

    assert fake_mouse.position == (985, 530)


def test_get_volume_interface_uses_endpoint_volume_property(monkeypatch):
    fake_endpoint = object()

    class FakeDevice:
        EndpointVolume = fake_endpoint

    monkeypatch.setattr(server, "pycaw_available", True)
    monkeypatch.setattr(server, "AudioUtilities", type("AudioUtilities", (), {"GetSpeakers": staticmethod(lambda: FakeDevice())}))
    monkeypatch.setattr(server, "CLSCTX_ALL", object())
    monkeypatch.setattr(server, "IAudioEndpointVolume", type("IAudioEndpointVolume", (), {"_iid_": object()}))

    assert server.get_volume_interface() is fake_endpoint
