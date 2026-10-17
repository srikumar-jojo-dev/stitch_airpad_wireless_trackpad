"""
AirPad Server – aiohttp WebSocket + static file server.
Turns an Android phone into a wireless mouse, keyboard & media remote for Windows.
"""

import ctypes
import hmac
import json
import logging
import platform
import secrets
import socket
import string
import subprocess
import sys
import time
from pathlib import Path

from aiohttp import web

# ── Input control ──────────────────────────────────────────────
from pynput.mouse import Button as MButton, Controller as MouseCtrl
from pynput.keyboard import Key, Controller as KbdCtrl

mouse = MouseCtrl()
kbd = KbdCtrl()

# ── Volume control (optional, Windows only) ────────────────────
pycaw_available = False
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    pycaw_available = True
except ImportError:
    pass

# ── Logging ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-5s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("airpad")

# ── Constants ──────────────────────────────────────────────────
PORT = 8080
MAX_PIN_ATTEMPTS = 5
BLOCK_DURATION = 60  # seconds
MAX_DX_DY = 2000
MAX_TEXT_LEN = 500
PC_NAME = platform.node() or "Windows-PC"
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# ── PIN generation ─────────────────────────────────────────────
PIN = "".join(secrets.choice(string.digits) for _ in range(4))

# ── Rate-limit / brute-force tracking ──────────────────────────
# { ip: { "fails": int, "blocked_until": float } }
ip_tracker: dict[str, dict] = {}

# ── Track held buttons per websocket so we can release on disconnect ──
ws_held_buttons: dict[int, set] = {}


# ═══════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════

def constant_time_compare(a: str, b: str) -> bool:
    """Compare two strings in constant time."""
    return hmac.compare_digest(a.encode(), b.encode())


def get_lan_ip() -> str:
    """Best-effort LAN IP detection."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def build_qr_login_url(base_url: str, pin: str) -> str:
    """Create a QR-friendly login URL that auto-fills the PIN on mobile."""
    return f"{base_url.rstrip('/')}/?pin={pin}"


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def ensure_cursor_visible() -> None:
    """Force the system cursor visible on Windows lock/login surfaces.

    On secure login screens Windows can hide the pointer after inactivity or when
    a remote control sequence runs. Repeated calls to ShowCursor(True) keep the
    pointer visible so mouse movement and password entry stay usable.
    """
    try:
        user32 = ctypes.windll.user32
        while user32.ShowCursor(True) < 0:
            pass
    except Exception:
        pass


def get_primary_screen_center() -> tuple[int, int]:
    """Fallback position when the real cursor is unavailable on secure desktop."""
    try:
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        return max(0, int(width // 2)), max(0, int(height // 2))
    except Exception:
        return (960, 540)


def is_port_in_use(port: int) -> bool:
    """Check whether TCP port is already bound by another process."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", port))
            return False
    except OSError:
        return True


def safe_mouse_move(dx: int, dy: int) -> None:
    """Move the pointer without crashing when Windows returns no cursor position."""
    try:
        current = mouse.position
    except Exception:
        current = None

    if current is None:
        current = get_primary_screen_center()
        try:
            mouse.position = current
        except Exception:
            pass

    mouse.position = (current[0] + dx, current[1] + dy)


def get_volume_interface():
    """Return the active Windows endpoint volume interface.

    pycaw changed API shape across versions: newer builds expose
    ``AudioDevice.EndpointVolume``, while older releases expect the legacy
    ``Activate(...)`` call.
    """
    if not pycaw_available:
        return None

    try:
        devices = AudioUtilities.GetSpeakers()
        if devices is not None and hasattr(devices, "EndpointVolume"):
            return devices.EndpointVolume

        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception:
        return None


# Key mapping for pynput
KEY_MAP = {
    "esc": Key.esc,
    "tab": Key.tab,
    "enter": Key.enter,
    "backspace": Key.backspace,
    "delete": Key.delete,
    "space": Key.space,
    "win": Key.cmd,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "pageup": Key.page_up,
    "pagedown": Key.page_down,
}

MODIFIER_MAP = {
    "ctrl": Key.ctrl_l,
    "alt": Key.alt_l,
    "shift": Key.shift_l,
    "win": Key.cmd,
}

MEDIA_MAP = {
    "playpause": Key.media_play_pause,
    "next": Key.media_next,
    "prev": Key.media_previous,
    "volume_up": Key.media_volume_up,
    "volume_down": Key.media_volume_down,
    "mute": Key.media_volume_mute,
}

BUTTON_MAP = {
    "left": MButton.left,
    "right": MButton.right,
    "middle": MButton.middle,
}


# ═══════════════════════════════════════════════════════════════
#  Message handlers
# ═══════════════════════════════════════════════════════════════

def handle_move(data: dict) -> None:
    ensure_cursor_visible()
    dx = clamp(int(data.get("dx", 0)), -MAX_DX_DY, MAX_DX_DY)
    dy = clamp(int(data.get("dy", 0)), -MAX_DX_DY, MAX_DX_DY)
    safe_mouse_move(dx, dy)


def handle_click(data: dict, ws_id: int) -> None:
    ensure_cursor_visible()
    btn_name = data.get("button", "left")
    action = data.get("action", "click")
    btn = BUTTON_MAP.get(btn_name)
    if not btn:
        return

    if action == "click":
        mouse.click(btn)
    elif action == "double":
        mouse.click(btn, 2)
    elif action == "down":
        mouse.press(btn)
        ws_held_buttons.setdefault(ws_id, set()).add(btn)
    elif action == "up":
        mouse.release(btn)
        ws_held_buttons.get(ws_id, set()).discard(btn)


def handle_scroll(data: dict) -> None:
    ensure_cursor_visible()
    dx = clamp(int(data.get("dx", 0)), -MAX_DX_DY, MAX_DX_DY)
    dy = clamp(int(data.get("dy", 0)), -MAX_DX_DY, MAX_DX_DY)
    mouse.scroll(dx, dy)


def handle_key(data: dict) -> None:
    ensure_cursor_visible()
    key_name = data.get("key", "").lower()
    key = KEY_MAP.get(key_name)
    if key:
        kbd.press(key)
        kbd.release(key)


def handle_hotkey(data: dict) -> None:
    ensure_cursor_visible()
    keys = data.get("keys", [])
    if not keys or len(keys) > 5:
        return
    pressed = []
    try:
        for k in keys:
            mapped = MODIFIER_MAP.get(k.lower()) or KEY_MAP.get(k.lower())
            if mapped:
                kbd.press(mapped)
                pressed.append(mapped)
            else:
                # Single character key
                kbd.press(k.lower())
                pressed.append(k.lower())
    finally:
        for k in reversed(pressed):
            try:
                kbd.release(k)
            except Exception:
                pass


def type_text(text: str) -> None:
    """Type text reliably for the current focused field, including Windows login screens.

    Per-character press/release events are more robust than a single batched type call,
    which can lose focus on secure password fields or other UI surfaces.
    """
    ensure_cursor_visible()
    text = str(text)[:MAX_TEXT_LEN]
    for ch in text:
        if ch in ("\n", "\r"):
            kbd.press(Key.enter)
            kbd.release(Key.enter)
        elif ch == "\t":
            kbd.press(Key.tab)
            kbd.release(Key.tab)
        else:
            kbd.press(ch)
            kbd.release(ch)


def handle_text(data: dict) -> None:
    text = data.get("text", "")
    if text:
        type_text(text)


def handle_media(data: dict) -> None:
    action = data.get("action", "")
    if action == "mute":
        vol = get_volume_interface()
        if vol:
            try:
                current = bool(vol.GetMute())
                vol.SetMute(not current, None)
                return
            except Exception:
                pass
    key = MEDIA_MAP.get(action)
    if key:
        kbd.press(key)
        kbd.release(key)


def handle_volume(data: dict) -> None:
    value = clamp(int(data.get("value", 50)), 0, 100)
    vol = get_volume_interface()
    if vol:
        try:
            vol.SetMasterVolumeLevelScalar(value / 100.0, None)
            try:
                vol.SetMute(False, None)
            except Exception:
                pass
            return
        except Exception:
            pass
    # Fallback: not practical to set exact volume without pycaw
    log.warning("pycaw unavailable – volume slider ignored (use media keys)")


def handle_slide(data: dict) -> None:
    action = data.get("action", "")
    if action == "next":
        kbd.press(Key.right)
        kbd.release(Key.right)
    elif action == "prev":
        kbd.press(Key.left)
        kbd.release(Key.left)


def handle_power(data: dict) -> None:
    action = data.get("action", "")
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    if action == "lock":
        log.info("⚡ Locking workstation")
        subprocess.Popen(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            creationflags=creation_flags,
        )
    elif action == "sleep":
        log.info("⚡ Suspending (sleep)")
        subprocess.Popen(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"],
            creationflags=creation_flags,
        )
    elif action == "shutdown":
        log.info("⚡ Shutdown in 5 seconds (cancel with: shutdown /a)")
        subprocess.Popen(
            ["shutdown", "/s", "/t", "5"],
            creationflags=creation_flags,
        )


HANDLERS = {
    "move": handle_move,
    "click": handle_click,
    "scroll": handle_scroll,
    "key": handle_key,
    "hotkey": handle_hotkey,
    "text": handle_text,
    "media": handle_media,
    "volume": handle_volume,
    "slide": handle_slide,
    "power": handle_power,
}


# ═══════════════════════════════════════════════════════════════
#  WebSocket handler
# ═══════════════════════════════════════════════════════════════

async def ws_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse(heartbeat=30.0)
    await ws.prepare(request)

    ip = request.remote or "unknown"
    ws_id = id(ws)
    authenticated = False
    log.info(f"↗  WebSocket opened from {ip}")

    # Check IP block
    tracker = ip_tracker.get(ip, {})
    if tracker.get("blocked_until", 0) > time.time():
        log.warning(f"🔒 Blocked IP {ip} tried to connect")
        await ws.close(code=4003, message=b"Blocked")
        return ws

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    continue

                msg_type = data.get("type", "")

                # ── Auth gate ──────────────────────────
                if not authenticated:
                    if msg_type != "auth":
                        continue
                    pin = str(data.get("pin", ""))
                    if constant_time_compare(pin, PIN):
                        authenticated = True
                        ip_tracker.pop(ip, None)
                        ensure_cursor_visible()
                        try:
                            current = mouse.position
                            if current is None:
                                mouse.position = get_primary_screen_center()
                        except Exception:
                            pass
                        await ws.send_json({"type": "auth", "ok": True, "name": PC_NAME})
                        log.info(f"✅ Authenticated: {ip}")
                    else:
                        tracker = ip_tracker.setdefault(ip, {"fails": 0, "blocked_until": 0})
                        tracker["fails"] += 1
                        log.warning(f"❌ Bad PIN from {ip} (attempt {tracker['fails']}/{MAX_PIN_ATTEMPTS})")
                        if tracker["fails"] >= MAX_PIN_ATTEMPTS:
                            tracker["blocked_until"] = time.time() + BLOCK_DURATION
                            log.warning(f"🔒 IP {ip} blocked for {BLOCK_DURATION}s")
                            await ws.send_json({"type": "auth", "ok": False, "blocked": True})
                            await ws.close(code=4003, message=b"Blocked")
                            return ws
                        await ws.send_json({"type": "auth", "ok": False})
                    continue

                # ── Ping/pong ──────────────────────────
                if msg_type == "ping":
                    await ws.send_json({"type": "pong", "t": data.get("t", 0)})
                    continue

                # ── Dispatch handler ───────────────────
                handler = HANDLERS.get(msg_type)
                if handler:
                    try:
                        # click handler needs ws_id
                        if msg_type == "click":
                            handler(data, ws_id)
                        else:
                            handler(data)
                    except Exception as e:
                        log.error(f"Handler error ({msg_type}): {e}")

            elif msg.type in (web.WSMsgType.ERROR, web.WSMsgType.CLOSE):
                break

    except Exception as e:
        log.error(f"WebSocket error: {e}")
    finally:
        # Release any held mouse buttons
        for btn in ws_held_buttons.pop(ws_id, set()):
            try:
                mouse.release(btn)
                log.info(f"Released held button on disconnect: {btn}")
            except Exception:
                pass
        log.info(f"↙  WebSocket closed: {ip}")

    return ws


# ═══════════════════════════════════════════════════════════════
#  HTTP routes
# ═══════════════════════════════════════════════════════════════

async def index_handler(_request: web.Request) -> web.FileResponse:
    return web.FileResponse(get_web_dir() / "index.html")


# ═══════════════════════════════════════════════════════════════
#  App factory & startup
# ═══════════════════════════════════════════════════════════════

def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/ws", ws_handler)
    app.router.add_get("/", index_handler)
    # Serve static files from the bundled UI directory when frozen
    web_dir = get_web_dir()
    app.router.add_static("/", web_dir, show_index=False)
    return app


def get_web_dir() -> Path:
    """Return the directory containing the browser UI, including bundled app builds."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "web"
    return Path(__file__).resolve().parent.parent / "web"


def print_banner() -> None:
    ip = get_lan_ip()
    url = f"http://{ip}:{PORT}"

    print()
    print("=" * 56)
    print("     ✈  AirPad Server v1.0")
    print("=" * 56)
    print(f"     PC Name :  {PC_NAME}")
    print(f"     LAN IP  :  {ip}")
    print(f"     URL     :  {url}")
    print(f"     PIN     :  {PIN}")
    print("=" * 56)
    print(f"  Open {url} on your phone")
    print(f"  Enter PIN: {PIN}")
    print("=" * 56)
    print()


def main() -> None:
    if is_port_in_use(PORT):
        raise RuntimeError(
            f"Port {PORT} is already in use. Close the application using it and retry."
        )

    print_banner()
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=PORT, print=lambda _: None)


if __name__ == "__main__":
    main()
