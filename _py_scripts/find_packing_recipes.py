from operator import itemgetter

from utils import read_all_recipes, fix_result
from gen_expected_storage_blocks import UNPACKING


# interesting recipe types:
#     minecraft:crafting_shaped
#     minecraft:crafting_shapeless
#     minecraft:smelting
#     minecraft:smoking
#     minecraft:blasting
#     minecraft:campfire_cooking
#     minecraft:smithing
#     minecraft:stonecutting


def _dict_get_multi(d: dict, keys: list, default=None):
    for key in keys:
        val = d.get(key)
        if val:
            return val
    return default


def hande_shapeless(recipe: dict) -> tuple[bool, int, str]:
    ingredients = recipe['ingredients']
    ingredients_count = len(ingredients)

    first_ingredient = ingredients[0]
    all_ingredients_equal = all(i == first_ingredient for i in ingredients)
    first_identifier = _dict_get_multi(
        first_ingredient, ['item', 'tag'], '<err>')

    return all_ingredients_equal, ingredients_count, first_identifier


def handle_shaped(recipe: dict) -> tuple[bool, int, str]:
    joined_pattern = ''.join(recipe['pattern'])
    no_space_pattern = ''.join(joined_pattern.split())
    ingredients_count = len(no_space_pattern)

    first_key = no_space_pattern[0]
    all_keys_equal = all(key == first_key for key in no_space_pattern)

    first_ingredient = recipe['key'][first_key]
    first_identifier = _dict_get_multi(
        first_ingredient, ['item', 'tag'], '<err>')

    return all_keys_equal, ingredients_count, first_identifier


def main():
    all_types = set()
    vanilla = []
    missing = []
    covered = []
    skipped = []

    for filename, recipe in read_all_recipes():
        try:
            all_types.add(recipe['type'])
            mode = recipe['type'].replace('minecraft:crafting_', '')

            if mode not in ('shapeless', 'shaped'):
                continue

            unpack_tuple = None
            skip_reason = None

            res_item, res_count = fix_result(recipe['result'])
            if any(s in res_item for s in ('slab', 'stairs', 'button', 'dye')):
                continue  # silent skip

            if res_count in (4, 9) and mode == 'shapeless':
                # possible vanilla unpacking recipe
                all_equal, in_count, in_item = hande_shapeless(recipe)
                if all_equal:
                    # items are reversed from found packing recipes
                    vanilla.append((in_item, res_item, res_count))
                    continue  # silent skip

                else:
                    # handle the same as below
                    skip_reason = f'expected result of 1, got {res_count}'

            elif res_count != 1:
                skip_reason = f'expected result of 1, got {res_count}'

            else:
                handler = handle_shaped if mode == 'shaped' else hande_shapeless
                all_equal, in_count, in_item = handler(recipe)

                if not all_equal:
                    skip_reason = f'mixed ingredients - {mode}'
                elif in_count not in (4, 9):
                    skip_reason = f'expected count of 4 or 9, got {in_count} - {mode}'
                else:
                    unpack_tuple = (res_item, in_item, in_count)

            if skip_reason:
                skipped.append((filename, skip_reason))
            elif unpack_tuple in UNPACKING or unpack_tuple + ('ext',) in UNPACKING:
                covered.append(unpack_tuple)
            elif unpack_tuple:
                missing.append(unpack_tuple)
            else:
                raise ValueError('unpacked_tuple is None!')

        except Exception as e:
            print(e, filename, recipe)

    print(f'\n=== COVERED {len(covered)} ===')
    for tup in covered:
        print(f' - {tup}')

    print(f'\n=== MISSING {len(missing)} ===')
    for tup in missing:
        if tup not in vanilla:
            print(f' - {tup}')

    print(f'\n=== SKIPPED {len(skipped)} ===')
    skipped.sort(key=lambda tup: tup[1])
    for filename, reason in sorted(skipped, key=itemgetter(1)):
        print(f' - {filename}: {reason}')

    print('\n--- all types ---')
    for typ in all_types:
        print(f' - {typ}')


if __name__ == '__main__':
    main()
