import json
import os

from utils import list_recipes, save_json, handle_multiple_choice, recipe_stair_uncraft, recipe_slab_uncraft

STAIR_CRAFTING = '../logical_stair_slab_un_crafting/data/minecraft/recipes'
STAIR_UNCRAFTING = '../logical_stair_slab_un_crafting/data/axa_stair_uncrafting/recipes'
SLAB_UNCRAFTING = '../logical_stair_slab_un_crafting/data/axa_slab_uncrafting/recipes'

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
        un_recipe = recipe_stair_uncraft(stair_item=result_item, block_item=input_item)
        un_path = os.path.join(STAIR_UNCRAFTING, filename)

        with open(os.path.join(STAIR_CRAFTING, filename), 'w+') as f:
            recipe['result']['count'] = 8
            f.write(json.dumps(recipe, indent=2))
            print(' - patched')
    else:
        print(f'SLAB: {filename}')
        un_recipe = recipe_slab_uncraft(slab_item=result_item, block_item=input_item)
        un_path = os.path.join(SLAB_UNCRAFTING, filename)

    save_json(un_path, un_recipe)
    print(' - uncrafted')


if __name__ == '__main__':
    for filename, recipe in list_recipes():
        try:
            if recipe['type'] != 'minecraft:crafting_shaped':
                continue

            result_item = recipe['result']['item']
            if 'slab' not in result_item and 'stair' not in result_item:
                continue

            joined = ''.join(recipe['pattern'])
            x = joined[0]
            if x != ' ' and joined == x * 3:
                handle_stair_slab(filename, recipe, key=x, is_stair=False)
            elif len(joined) == 9:
                if x != ' ':
                    expected = f'{x}  {x}{x} {x}{x}{x}'
                else:
                    # if for some reason there is a mirror recipe
                    x = joined[2]
                    expected = f'  {x} {x}{x}{x}{x}{x}'
                if joined == expected:
                    handle_stair_slab(filename, recipe, key=x, is_stair=True)

        except Exception as e:
            print(e, recipe)
