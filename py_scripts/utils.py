import os

import json
from typing import Any, Tuple

VANILLA_RECIPES_PATH = '../../mc_assets/data/minecraft/recipes'


def read_json(path: str) -> dict:
    with open(path) as f:
        return json.loads(f.read())


def save_json(path: str, data: dict):
    with open(path, 'w+') as f:
        f.write(json.dumps(data, indent=2))


def list_recipes():
    for filename in sorted(os.listdir(VANILLA_RECIPES_PATH)):
        filepath = os.path.join(VANILLA_RECIPES_PATH, filename)
        if filename.endswith('.json') and os.path.isfile(filepath):
            yield filename, read_json(filepath)


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
        "group": group,
        "ingredients": [{"item": packed_item}],
        "result": {"item": unpacked_item, "count": output}
    }
    if not group: recipe.pop('group')
    return recipe


def recipe_stair_uncraft(stair_item: str, block_item: str, output=3, group: str = None) -> dict:
    recipe = {
        "type": "minecraft:crafting_shaped",
        "group": group,
        "pattern": ["##", "##"],
        "key": {"#": {"item": stair_item}},
        "result": {"item": block_item, "count": output}
    }
    if not group: recipe.pop('group')
    return recipe


def recipe_slab_uncraft(slab_item: str, block_item: str, group: str = None) -> dict:
    recipe = {
        "type": "minecraft:crafting_shaped",
        "group": group,
        "pattern": ["##"],
        "key": {"#": {"item": slab_item}},
        "result": {"item": block_item}
    }
    if not group: recipe.pop('group')
    return recipe
