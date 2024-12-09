from pack_maker import JAR_FILES, PACKS_FOLDER
from pack_maker.utils import read_all_json, save_json

PACK_NAME = "uncraft_stairs_slabs"

# True = perfect math gives 8x stairs ; False = same as stonecutter gives 6x stairs
STAIR_MATH_MODE = False


def generate_pack():
    uncraft_dir = PACKS_FOLDER / PACK_NAME / "data" / PACK_NAME / "recipe"
    uncraft_dir.mkdir(parents=True, exist_ok=True)

    stair_dir = PACKS_FOLDER / PACK_NAME / "data/minecraft/recipe"
    stair_dir.mkdir(parents=True, exist_ok=True)

    for filename, recipe in read_all_json(JAR_FILES / "data/minecraft/recipe"):
        if recipe["type"] != "minecraft:crafting_shaped":
            continue

        out_item = recipe["result"]["id"]
        if "slab" not in out_item and "stair" not in out_item:
            continue

        pattern_str = "".join(recipe["pattern"])
        in_key, in_item = next(iter(recipe["key"].items()))

        expected_slab = "###".replace("#", in_key)
        expected_stair = "#  ## ###".replace("#", in_key)
        expected_stair_alt = "  # #####".replace("#", in_key)

        if pattern_str == expected_slab:
            # uncraft slab
            uncraft_path = uncraft_dir / filename
            uncraft = {
                "type": "minecraft:crafting_shaped",
                "group": "uncraft_slabs",
                "category": "building",
                "key": {"#": out_item},
                "pattern": ["##"],
                "result": {"count": 1, "id": in_item},
            }
            save_json(uncraft_path, uncraft)

        elif pattern_str == expected_stair or pattern_str == expected_stair_alt:
            # uncraft stair
            uncraft_path = uncraft_dir / filename
            output = 3 if STAIR_MATH_MODE else 4
            uncraft = {
                "type": "minecraft:crafting_shaped",
                "group": "uncraft_slabs",
                "category": "building",
                "key": {"#": out_item},
                "pattern": ["##", "##"],
                "result": {"count": output, "id": in_item},
            }
            save_json(uncraft_path, uncraft)

            # patch stair recipe
            recipe["result"]["count"] = 8 if STAIR_MATH_MODE else 6
            stair_path = stair_dir / filename
            save_json(stair_path, recipe)


if __name__ == "__main__":
    generate_pack()
