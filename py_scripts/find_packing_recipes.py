import json

from utils import list_recipes, fix_result

# 'minecraft:stonecutting',
# 'minecraft:smelting',
# 'minecraft:smoking',
# 'minecraft:blasting',
# 'minecraft:campfire_cooking',
# 'minecraft:smithing',
# 'minecraft:crafting_shapeless',
# 'minecraft:crafting_shaped',


if __name__ == '__main__':
    for path in list_recipes():
        try:
            recipe: dict = json.loads(open(path).read())
            t = recipe['type']
            if t not in ('minecraft:crafting_shapeless', 'minecraft:crafting_shaped'):
                continue

            res_item, res_count = fix_result(recipe['result'])
            if res_count != 1:
                continue

            if t == 'minecraft:crafting_shapeless':
                ingredients = recipe.get('ingredients')
                in_count = len(ingredients)
                in_first = ingredients[0]
                in_same = all(i == in_first for i in ingredients)

                if in_same and in_count in (4, 9):
                    in_item = in_first.get('item', in_first.get('tag', '<err>'))
                    print(f"('{res_item}', '{in_item}', {in_count}),")
            else:
                joined = ''.join(recipe['pattern'])
                in_count = len(joined)
                p_first = joined[0]
                p_same = all(c == p_first for c in joined)

                if p_same and in_count in (4, 9):
                    in_item = recipe['key'][p_first]
                    in_item = in_item.get('item', in_item.get('tag', '<err>'))
                    print(f"('{res_item}', '{in_item}', {in_count}),")


        except Exception as e:
            print(e, recipe)
