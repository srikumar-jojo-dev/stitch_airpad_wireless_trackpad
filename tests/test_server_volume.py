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

    def SetMute(self, muted, _):
        self.calls.append(("set_mute", muted))


def test_build_qr_login_url_includes_pin_and_ip():
    url = server.build_qr_login_url("http://10.0.0.5:8080", "1234")
    assert url == "http://10.0.0.5:8080/?pin=1234"


def test_free_port_if_in_use_terminates_stale_listener(monkeypatch):
    calls = []
    states = {8080}

    def fake_is_port_in_use(port):
        return port in states

    def fake_run(cmd, capture_output, text):
        calls.append(cmd)
        states.discard(8080)

        class Result:
            stdout = ""
            stderr = ""
            returncode = 0
        return Result()

    monkeypatch.setattr(server, "is_port_in_use", fake_is_port_in_use)
    monkeypatch.setattr(server.subprocess, "run", fake_run)

    assert server.free_port_if_in_use(8080) is True
    assert calls


def test_handle_volume_sets_master_volume_and_unmutes(monkeypatch):
    fake = FakeVolume()
    monkeypatch.setattr(server, "get_volume_interface", lambda: fake)

    server.handle_volume({"value": 25})

    assert ("set_volume", 0.25) in fake.calls
    assert ("set_mute", False) in fake.calls


def test_handle_media_mute_sets_windows_mute(monkeypatch):
    fake = FakeVolume()
    monkeypatch.setattr(server, "get_volume_interface", lambda: fake)

    server.handle_media({"action": "mute"})

    assert ("set_mute", True) in fake.calls


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
