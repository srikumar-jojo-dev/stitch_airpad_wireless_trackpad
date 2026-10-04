"""Project entry point for AirPad.

This launcher forwards to the real server implementation in the server/ package.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER_FILE = ROOT / "server" / "server.py"


def main() -> None:
    spec = importlib.util.spec_from_file_location("airpad_server", SERVER_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load server implementation from {SERVER_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


if __name__ == "__main__":
    main()
