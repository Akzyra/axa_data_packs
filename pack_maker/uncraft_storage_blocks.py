from dataclasses import dataclass

from pack_maker import JAR_FILES, PACKS_FOLDER
from pack_maker.utils import read_all_json, item_name, save_json

PACK_NAME = "uncraft_storage_blocks"


@dataclass
class Unpacking:
    packed_item: str
    loose_item: str
    loose_count: int

    def __str__(self) -> str:
        return f"{item_name(self.packed_item)} -> {self.loose_count}x {item_name(self.loose_item)}"

    def __repr__(self):
        return f"Unpacking({self.packed_item!r}, {self.loose_item!r}, {self.loose_count!r})"

    def to_row(self, packed_width: int, loose_width: int) -> str:
        loose = f"{self.loose_count}x {item_name(self.loose_item)}"
        return f"| {item_name(self.packed_item):<{packed_width}} | {loose:<{loose_width}} |\n"


UNPACKINGS = [
    # bricks
    Unpacking("minecraft:bricks", "minecraft:brick", 4),
    Unpacking("minecraft:nether_bricks", "minecraft:nether_brick", 4),
    Unpacking("minecraft:resin_bricks", "minecraft:resin_brick", 4),
    # earthy
    Unpacking("minecraft:clay", "minecraft:clay_ball", 4),
    Unpacking("minecraft:sandstone", "minecraft:sand", 4),
    Unpacking("minecraft:red_sandstone", "minecraft:red_sand", 4),
    Unpacking("minecraft:dripstone_block", "minecraft:pointed_dripstone", 4),
    # icey
    Unpacking("minecraft:blue_ice", "minecraft:packed_ice", 9),
    Unpacking("minecraft:packed_ice", "minecraft:ice", 9),
    Unpacking("minecraft:snow_block", "minecraft:snowball", 4),
    # quartz
    Unpacking("minecraft:quartz_block", "minecraft:quartz", 4),
    Unpacking("minecraft:chiseled_quartz_block", "minecraft:quartz", 4),
    Unpacking("minecraft:quartz_bricks", "minecraft:quartz", 4),
    Unpacking("minecraft:quartz_pillar", "minecraft:quartz", 4),
    Unpacking("minecraft:smooth_quartz", "minecraft:quartz", 4),
    # nether
    Unpacking("minecraft:glowstone", "minecraft:glowstone_dust", 4),
    Unpacking("minecraft:nether_wart_block", "minecraft:nether_wart", 9),
    Unpacking("minecraft:magma_block", "minecraft:magma_cream", 4),
    # prismarine
    Unpacking("minecraft:prismarine", "minecraft:prismarine_shard", 4),
    Unpacking("minecraft:prismarine_bricks", "minecraft:prismarine_shard", 9),
    # misc
    Unpacking("#minecraft:wool", "minecraft:string", 4),
    Unpacking("minecraft:amethyst_block", "minecraft:amethyst_shard", 4),
    Unpacking("minecraft:melon", "minecraft:melon_slice", 9),
    Unpacking("minecraft:bamboo_block", "minecraft:bamboo", 9),
    Unpacking("minecraft:honeycomb_block", "minecraft:honeycomb", 4),
]

IGNORE = [
    # special cases: handled by vanilla
    Unpacking("minecraft:honey_block", "minecraft:honey_bottle", 4),
    # special cases: handled by datapack
    Unpacking("minecraft:white_wool", "minecraft:string", 4),
    # unpacking does not make sense
    Unpacking("minecraft:crafting_table", "#minecraft:planks", 4),
    Unpacking("minecraft:iron_trapdoor", "minecraft:iron_ingot", 4),
    Unpacking("minecraft:leather", "minecraft:rabbit_hide", 4),
    Unpacking("minecraft:music_disc_5", "minecraft:disc_fragment_5", 9),
]


def check_recipes() -> None:
    candidates: list[Unpacking] = []
    vanilla: list[Unpacking] = []

    for filename, recipe in read_all_json(JAR_FILES / "data/minecraft/recipe"):
        match recipe:
            # vanilla unpacking: one simple input and 4 or 9 outputs
            case {
                "type": "minecraft:crafting_shapeless",
                "ingredients": [str() as in_item],
                "result": {"count": (4 | 9) as out_count, "id": out_item},
            }:
                vanilla.append(
                    Unpacking(
                        packed_item=in_item,
                        loose_item=out_item,
                        loose_count=out_count,
                    )
                )

            # shaped packing: 2x2 or 3x3 with one input key and one output
            case {
                "type": "minecraft:crafting_shaped",
                "key": dict() as key,
                "result": {"count": 1, "id": out_item},
            } if len(key) == 1:
                pattern_str = "".join(recipe["pattern"])

                # get the single pattern key and item
                in_key, in_item = next(iter(key.items()))
                in_count = pattern_str.count(in_key)
                empty_count = pattern_str.count(" ")

                if in_count in (4, 9) and empty_count == 0:
                    # reverse in and out items
                    candidates.append(
                        Unpacking(
                            packed_item=out_item,
                            loose_item=in_item,
                            loose_count=in_count,
                        )
                    )

            # shapeless packing: >1 of same input and one output
            case {
                "type": "minecraft:crafting_shapeless",
                "ingredients": list() as ingredients,
                "result": {"count": 1, "id": out_item},
            } if len(ingredients) > 1 and all(x == ingredients[0] for x in ingredients):
                in_count = len(ingredients)
                in_item = ingredients[0]

                candidates.append(
                    Unpacking(
                        packed_item=out_item,
                        loose_item=in_item,
                        loose_count=in_count,
                    )
                )

            case _:
                continue

    covered_vanilla, missing = [], []
    for candidate in candidates:
        if candidate in vanilla:
            covered_vanilla.append(candidate)
        elif candidate not in IGNORE and candidate not in UNPACKINGS:
            missing.append(candidate)

    print(f"\n=== Vanilla: {len(covered_vanilla)} ===")
    for candidate in covered_vanilla:
        print(f" - {candidate}")

    print(f"\n=== Datapack:{len(UNPACKINGS)} ===")
    for candidate in UNPACKINGS:
        print(f" - {candidate}")

    print(f"\n=== MISSING: {len(missing)} ===")
    for candidate in missing:
        print(f" - {candidate!r}")


def generate_pack() -> None:
    readme = """# Uncraft storage blocks

Makes most 2x2 or 3x3 recipes of a single item reversible.

Table of added unpacking recipes:

"""
    packed_width = 25
    loose_width = 20

    readme += f"| {"Block":<{packed_width}} | {"Result":<{loose_width}} |\n"
    readme += f"|-{"-"*packed_width}-|-{"-"*loose_width}-|\n"

    recipe_path = PACKS_FOLDER / PACK_NAME / "data" / PACK_NAME / "recipe"
    recipe_path.mkdir(parents=True, exist_ok=True)

    for unpacking in UNPACKINGS:
        loose_item_raw = unpacking.loose_item.removeprefix("minecraft:")
        packed_item_raw = unpacking.packed_item.removeprefix("#").removeprefix(
            "minecraft:"
        )

        filepath = recipe_path / f"{loose_item_raw}_from_{packed_item_raw}.json"
        recipe = {
            "type": "minecraft:crafting_shapeless",
            "category": "misc",
            "group": loose_item_raw,
            "ingredients": [unpacking.packed_item],
            "result": {
                "count": unpacking.loose_count,
                "id": unpacking.loose_item,
            },
        }
        save_json(filepath, recipe)

        readme += unpacking.to_row(packed_width, loose_width)

    readme_file = PACKS_FOLDER / PACK_NAME / "README.md"
    readme_file.write_text(readme)


if __name__ == "__main__":
    check_recipes()
    generate_pack()
