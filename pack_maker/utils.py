import json
from pathlib import Path
from typing import Generator


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with path.open("w+", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def read_all_json_files(folder: Path) -> Generator[tuple[str, dict], None, None]:
    for file in folder.glob("*.json"):
        yield file.name, read_json(file)
