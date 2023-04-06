from pathlib import Path

from utils import read_all_recipes, save_json, handle_multiple_choice, recipe_stair_uncraft, recipe_slab_uncraft

# only use the following values: 4 (vanilla), 6 (stonecutter), 8 (math), 12, 24
STAIR_CRAFT_OUTPUT = 8

STAIR_CRAFTING = Path('../logical_stair_slab_un_crafting/data/minecraft/recipes')
STAIR_UNCRAFTING = Path('../logical_stair_slab_un_crafting/data/axa_stair_uncrafting/recipes')
SLAB_UNCRAFTING = Path('../logical_stair_slab_un_crafting/data/axa_slab_uncrafting/recipes')

# automatically pick these if multiple items are possible
UNCRAFTING_PREFERRED = [
    'minecraft:red_sandstone',
    'minecraft:quartz_block',
    'minecraft:purpur_block',
    'minecraft:sandstone',
]


def handle_stair_slab(filename: str, recipe: dict, key: str, is_stair: bool):
    input_item, result_item = handle_multiple_choice(recipe, key, UNCRAFTING_PREFERRED)

    if is_stair:
        print(f'STAIR: {filename}')
        un_recipe = recipe_stair_uncraft(
            stair_item=result_item,
            block_item=input_item,
            stair_craft_output=STAIR_CRAFT_OUTPUT
        )
        un_path = STAIR_UNCRAFTING / filename

        # change amount for stair craft
        recipe['result']['count'] = STAIR_CRAFT_OUTPUT
        craft_path = STAIR_CRAFTING / filename
        save_json(craft_path, recipe)
        print(' - patched')
    else:
        print(f'SLAB: {filename}')
        un_recipe = recipe_slab_uncraft(slab_item=result_item, block_item=input_item)
        un_path = SLAB_UNCRAFTING / filename

    save_json(un_path, un_recipe)
    print(' - uncrafted')


def main():
    STAIR_CRAFTING.mkdir(parents=True, exist_ok=True)
    STAIR_UNCRAFTING.mkdir(parents=True, exist_ok=True)
    SLAB_UNCRAFTING.mkdir(parents=True, exist_ok=True)

    for filename, recipe in read_all_recipes():
        try:
            if recipe['type'] != 'minecraft:crafting_shaped':
                continue

            result_item = recipe['result']['item']
            if 'slab' not in result_item and 'stair' not in result_item:
                continue

            pattern = ''.join(recipe['pattern'])
            if len(pattern) not in (3, 9):
                continue

            key = pattern[0]
            key_alt = pattern[2]
            expected_slab = '###'.replace('#', key)
            expected_stair = '#  ## ###'.replace('#', key)
            expected_stair_alt = '  # #####'.replace('#', key_alt)

            if pattern == expected_slab:
                handle_stair_slab(filename, recipe, key=key, is_stair=False)
            elif pattern == expected_stair:
                handle_stair_slab(filename, recipe, key=key, is_stair=True)
            elif pattern == expected_stair_alt:
                handle_stair_slab(filename, recipe, key=key_alt, is_stair=True)


        except Exception as e:
            print(e, recipe)


if __name__ == '__main__':
    main()
