import asyncio

import pytest
from aiohttp import WSMsgType
from aiohttp.test_utils import TestClient, TestServer

from server import server as airpad_server


def test_http_ui_and_authenticated_websocket(monkeypatch):
    async def exercise():
        moves = []
        monkeypatch.setattr(airpad_server, "PIN", "1234")
        monkeypatch.setattr(airpad_server, "ip_tracker", {})
        monkeypatch.setattr(airpad_server, "ensure_cursor_visible", lambda: None)
        monkeypatch.setitem(airpad_server.HANDLERS, "move", moves.append)

        async with TestClient(TestServer(airpad_server.create_app())) as client:
            response = await client.get("/")
            assert response.status == 200
            assert "<title>AirPad Remote</title>" in await response.text()

            ws = await client.ws_connect("/ws")
            await ws.send_json({"type": "move", "dx": 10, "dy": 4})
            await ws.send_json({"type": "auth", "pin": "1234"})
            assert await ws.receive_json() == {
                "type": "auth",
                "ok": True,
                "name": airpad_server.PC_NAME,
            }
            assert moves == []

            await ws.send_json({"type": "move", "dx": 10, "dy": 4})
            await ws.send_json({"type": "ping", "t": 42})
            assert await ws.receive_json() == {"type": "pong", "t": 42}
            assert moves == [{"type": "move", "dx": 10, "dy": 4}]
            await ws.close()

    asyncio.run(exercise())


def test_websocket_blocks_ip_after_pin_attempt_limit(monkeypatch):
    async def exercise():
        tracker = {}
        monkeypatch.setattr(airpad_server, "PIN", "1234")
        monkeypatch.setattr(airpad_server, "ip_tracker", tracker)

        async with TestClient(TestServer(airpad_server.create_app())) as client:
            ws = await client.ws_connect("/ws")
            for attempt in range(airpad_server.MAX_PIN_ATTEMPTS):
                await ws.send_json({"type": "auth", "pin": "0000"})
                response = await ws.receive_json()
                assert response["ok"] is False
                assert response.get("blocked", False) is (
                    attempt == airpad_server.MAX_PIN_ATTEMPTS - 1
                )

            close_message = await ws.receive()
            assert close_message.type == WSMsgType.CLOSE
            assert tracker["127.0.0.1"]["fails"] == airpad_server.MAX_PIN_ATTEMPTS
            assert tracker["127.0.0.1"]["blocked_until"] > airpad_server.time.time()

    asyncio.run(exercise())


def test_websocket_releases_mouse_button_after_disconnect(monkeypatch):
    async def exercise():
        class FakeMouse:
            def __init__(self):
                self.releases = []

            def press(self, button):
                self.pressed = button

            def release(self, button):
                self.releases.append(button)

            def click(self, button, count=1):
                self.clicked = (button, count)

        fake_mouse = FakeMouse()
        monkeypatch.setattr(airpad_server, "PIN", "1234")
        monkeypatch.setattr(airpad_server, "ip_tracker", {})
        monkeypatch.setattr(airpad_server, "mouse", fake_mouse)
        monkeypatch.setattr(airpad_server, "ensure_cursor_visible", lambda: None)

        async with TestClient(TestServer(airpad_server.create_app())) as client:
            ws = await client.ws_connect("/ws")
            await ws.send_json({"type": "auth", "pin": "1234"})
            await ws.receive_json()
            await ws.send_json({"type": "click", "button": "left", "action": "down"})
            await asyncio.sleep(0)
            await ws.close()
            assert fake_mouse.releases == [airpad_server.MButton.left]

    asyncio.run(exercise())


def test_root_launcher_propagates_server_startup_errors(monkeypatch):
    import importlib.util
    from pathlib import Path

    launcher_path = Path(__file__).resolve().parents[1] / "server.py"
    spec = importlib.util.spec_from_file_location("root_server_entrypoint", launcher_path)
    launcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launcher)

    def fail_startup():
        raise RuntimeError("startup failed")

    monkeypatch.setattr(airpad_server, "main", fail_startup)

    with pytest.raises(RuntimeError, match="startup failed"):
        launcher.main()
