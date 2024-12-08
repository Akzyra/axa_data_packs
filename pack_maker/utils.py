import json
from pathlib import Path
from typing import Generator

from pack_maker import JAR_FILES


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    with path.open("w+", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def format_json(path: Path) -> None:
    data = read_json(path)
    save_json(path, data)


def read_all_json(folder: Path) -> Generator[tuple[str, dict], None, None]:
    for file in folder.glob("*.json"):
        yield file.name, read_json(file)


lang: dict[str, str] = read_json(JAR_FILES / "assets/minecraft/lang/en_us.json")
lang_fallback = {
    "#minecraft:wool": "Any Wool",
}


def item_name(item_id: str) -> str:
    bare_id = item_id.removeprefix("minecraft:")
    block_key = f"block.minecraft.{bare_id}"
    if block_key in lang:
        return lang[block_key]

    item_key = f"item.minecraft.{bare_id}"
    if item_key in lang:
        return lang[item_key]

    if item_id in lang_fallback:
        return lang_fallback[item_id]

    raise KeyError(f"no lang key for {item_id}")
