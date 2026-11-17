import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path = "config.json") -> dict[str, Any]:
    return json.loads(Path(path).read_text())
