import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_ENTRYPOINT = ROOT / "server.py"


def test_root_server_entrypoint_exposes_main():
    spec = importlib.util.spec_from_file_location("root_server_entrypoint", SERVER_ENTRYPOINT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(getattr(module, "main", None))
