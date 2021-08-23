import json
import os

from py_scripts.utils import recipe_unpack

RECIPES_PATH = '../expected_storage_blocks/data/axa_expected_storage_blocks/recipes'
RECIPES_PATH_EXT = '../expected_storage_blocks/data/axa_expected_storage_blocks_ext/recipes'

UNPACKING = [
    # clay and bricks
    ('minecraft:clay', 'minecraft:clay_ball', 4),
    ('minecraft:bricks', 'minecraft:brick', 4, True),
    ('minecraft:nether_bricks', 'minecraft:nether_brick', 4, 'ext'),

    # icey
    ('minecraft:blue_ice', 'minecraft:packed_ice', 9),
    ('minecraft:packed_ice', 'minecraft:ice', 9),
    ('minecraft:snow_block', 'minecraft:snowball', 4),

    # quartz
    ('minecraft:quartz_block', 'minecraft:quartz', 4),
    ('minecraft:chiseled_quartz_block', 'minecraft:quartz', 4, 'ext'),
    ('minecraft:quartz_bricks', 'minecraft:quartz', 4, 'ext'),
    ('minecraft:quartz_pillar', 'minecraft:quartz', 4, 'ext'),
    ('minecraft:smooth_quartz', 'minecraft:quartz', 4, 'ext'),

    # misc
    ('minecraft:glowstone', 'minecraft:glowstone_dust', 4),
    ('minecraft:amethyst_block', 'minecraft:amethyst_shard', 4),

    ('minecraft:melon', 'minecraft:melon_slice', 9),

    ('minecraft:nether_wart_block', 'minecraft:nether_wart', 9, 'ext'),
    ('minecraft:magma_block', 'minecraft:magma_cream', 4, 'ext'),
]

if __name__ == '__main__':
    os.makedirs(RECIPES_PATH, exist_ok=True)
    for u in UNPACKING:
        in_item = u[0].split(':', 1)[1]
        out_item = u[1].split(':', 1)[1]
        recipe = recipe_unpack(*u[:3], group=out_item)

        base = RECIPES_PATH_EXT if (len(u) >= 4 and u[3] == 'ext') else RECIPES_PATH
        filepath = os.path.join(base, f'{out_item}_from_{in_item}.json')
        with open(filepath, 'w+') as f:
            f.write(json.dumps(recipe, indent=2))
