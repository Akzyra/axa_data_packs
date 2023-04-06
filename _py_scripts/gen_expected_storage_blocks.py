from pathlib import Path

from utils import recipe_unpack, save_json

RECIPES_PATH = Path('../expected_storage_blocks/data/axa_expected_storage_blocks/recipes')
RECIPES_PATH_EXT = Path('../expected_storage_blocks/data/axa_expected_storage_blocks_ext/recipes')

UNPACKING = [
    # earthy
    ('minecraft:dripstone_block', 'minecraft:pointed_dripstone', 4),
    ('minecraft:clay', 'minecraft:clay_ball', 4),
    ('minecraft:bricks', 'minecraft:brick', 4, 'ext'),
    ('minecraft:nether_bricks', 'minecraft:nether_brick', 4, 'ext'),
    ('minecraft:sandstone', 'minecraft:sand', 4, 'ext'),
    ('minecraft:red_sandstone', 'minecraft:red_sand', 4, 'ext'),

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

    # nether 
    ('minecraft:glowstone', 'minecraft:glowstone_dust', 4),
    ('minecraft:nether_wart_block', 'minecraft:nether_wart', 9, 'ext'),
    ('minecraft:magma_block', 'minecraft:magma_cream', 4, 'ext'),

    # prismarine
    ('minecraft:prismarine', 'minecraft:prismarine_shard', 4),
    ('minecraft:prismarine_bricks', 'minecraft:prismarine_shard', 9),

    # misc
    # ('minecraft:white_wool', 'minecraft:string', 4), # handled manually because of wool colors
    ('minecraft:amethyst_block', 'minecraft:amethyst_shard', 4),
    ('minecraft:melon', 'minecraft:melon_slice', 9),
    ('minecraft:honeycomb_block', 'minecraft:honeycomb', 4),
]


def main():
    RECIPES_PATH.mkdir(parents=True, exist_ok=True)
    RECIPES_PATH_EXT.mkdir(parents=True, exist_ok=True)

    for u in UNPACKING:
        in_item = u[0].split(':', 1)[1]
        out_item = u[1].split(':', 1)[1]
        recipe = recipe_unpack(*u[:3], group=out_item)

        is_ext = len(u) > 3 and u[3] == 'ext'
        base = RECIPES_PATH_EXT if is_ext else RECIPES_PATH
        filepath = base / f'{out_item}_from_{in_item}.json'
        save_json(filepath, recipe)
        print(filepath)


if __name__ == '__main__':
    main()
