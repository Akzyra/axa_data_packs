from pathlib import Path
import json
from typing import Any, Tuple, Generator

VANILLA_RECIPES_PATH = Path('../_mc_assets/data/minecraft/recipes')


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with path.open("w+", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def read_all_recipes() -> Generator[tuple[str, dict], None, None]:
    for file in VANILLA_RECIPES_PATH.glob('*.json'):
        yield file.name, read_json(file)


def handle_multiple_choice(recipe: dict, key: str, preferred: list) -> Tuple[str, str]:
    result_item: str = recipe['result']['item']
    key_entry = recipe["key"][key]

    if isinstance(key_entry, dict):
        return key_entry['item'], result_item
    elif isinstance(key_entry, list):
        input_items = []
        for entry in key_entry:
            if entry['item'] in preferred:
                return entry['item'], result_item

            input_items.append(entry['item'])

        if len(input_items) == 1:
            return input_items[0], result_item

        print(f' - multiple choice: {result_item}')
        for i, ip in enumerate(input_items):
            print(f'     {i + 1}. {ip}')
        idx = input('   Enter Number: ')
        input_item = input_items[int(idx) - 1]
        return input_item, result_item

    raise TypeError(f'{result_item}: cannot handle key.{key}: {key_entry}')


def fix_result(result: Any) -> Tuple[str, int]:
    if isinstance(result, str):
        return result, 1
    elif isinstance(result, dict):
        return result['item'], result.get('count', 1)
    else:
        return '', 0


def recipe_unpack(packed_item: str, unpacked_item: str, output: int, group: str = None) -> dict:
    recipe = {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "group": group,
        "ingredients": [{"item": packed_item}],
        "result": {"item": unpacked_item, "count": output}
    }
    if not group:
        del recipe['group']
    return recipe


def recipe_stair_uncraft(stair_item: str, block_item: str, stair_craft_output: int) -> dict:
    # calculate ratio from crafting stairs to correctly uncraft
    output = 6 / stair_craft_output * 4
    recipe = {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "uncraft_stairs",
        "pattern": ["##", "##"],
        "key": {"#": {"item": stair_item}},
        "result": {"item": block_item, "count": int(output)}
    }
    return recipe


def recipe_slab_uncraft(slab_item: str, block_item: str) -> dict:
    recipe = {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "uncraft_slabs",
        "pattern": ["##"],
        "key": {"#": {"item": slab_item}},
        "result": {"item": block_item}
    }
    return recipe
