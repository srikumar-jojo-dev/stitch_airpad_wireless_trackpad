# AirPad — Wireless Trackpad, Keyboard & Media Remote

Turn your Android phone into a wireless mouse, keyboard, and media remote for your **Windows** laptop. Works over your local Wi-Fi network (or phone hotspot). No app to install on the phone — just open a URL in Chrome.

---

## Quick Start

### 1. Install Python dependencies

```
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the server

```
python server.py
```

You'll see output like:

```
========================================================
     ✈  AirPad Server v1.0
========================================================
     PC Name :  YOUR-PC
     LAN IP  :  192.168.1.42
     URL     :  http://192.168.1.42:8080
     PIN     :  7291
========================================================
  Open http://192.168.1.42:8080 on your phone
  Enter PIN: 7291
========================================================
```

### 3. Connect your phone

1. Make sure your **phone and laptop are on the same Wi-Fi** (a phone hotspot also works).
2. Open the **URL** shown in the terminal on your phone's Chrome browser.
3. Enter the **4-digit PIN** displayed in the terminal.
4. That's it — start using AirPad!

---

## Features

| Tab | What it does |
|---|---|
| **Touchpad** | Move the cursor, tap to click, two-finger scroll, left/middle/right buttons, drag lock |
| **Keys** | Type text remotely, quick keys (Esc, Tab, Alt+Tab, Win, Ctrl+C/V, Backspace, Enter, Space, Delete), arrow pad, Page Up/Down |
| **Media** | Volume slider & mute, play/pause/next/prev, presentation slide control, power (Lock, Sleep, Shutdown) |
| **Settings** | Pointer speed, scroll speed, tap-to-click, vibration, PIN, theme (Charcoal / OLED Black) |

---

## Important Notes

- **Windows Firewall**: On first run, Windows will ask to allow Python through the firewall. **Allow it for Private networks only.**
- **Same network**: Both devices must be on the same Wi-Fi or hotspot.
- **Port 8080 already in use**: Close the application using that port, then restart AirPad. AirPad will not terminate other applications.
- **Never use on public Wi-Fi** — the connection is not encrypted.
- **Shutdown** has a 5-second delay. Cancel with `shutdown /a` in a terminal.
- **Sleep and Shutdown** require a 2-second long press to confirm.

---

## Project Structure

```
stitch_airpad_wireless_trackpad/
├── server/
│   ├── server.py           # Python server (aiohttp + WebSocket)
│   └── requirements.txt    # Python dependencies
├── web/
│   └── index.html          # Mobile web app (single page, no build)
├── README.md               # This file
└── stitch_airpad_wireless_trackpad/   # Original Stitch designs (do not modify)
```

---

## Tech Stack

- **Server**: Python 3.10+, aiohttp, pynput, pycaw (optional, for volume slider)
- **Client**: Vanilla HTML + CSS + JavaScript (no framework, no build step)
- **Transport**: WebSocket over Wi-Fi (same port as HTTP: 8080)

## Tests

From the repository root, run the test suite with:

```
.\server\venv\Scripts\python.exe -m pytest -q
```
