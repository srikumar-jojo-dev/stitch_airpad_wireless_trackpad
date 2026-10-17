"""Project entry point for AirPad.

This launcher forwards to the real server implementation in the server/ package.
"""

from __future__ import annotations


def main() -> None:
    from server.server import main as server_main

    server_main()


if __name__ == "__main__":
    main()
