import pandas as pd

recipes = pd.read_csv("../assets/recipes.csv")
recipes = recipes.drop(columns=['Unnamed: 0'])

all_ingredients = []
ingredients = []


def filter_ingredient(ingredient_str):
    if "grote" in ingredient_str:
        ingredient_str = ingredient_str.replace("grote ", "")
    if "kleine" in ingredient_str:
        ingredient_str = ingredient_str.replace("kleine ", "")
    if "middelgrote" in ingredient_str:
        ingredient_str = ingredient_str.replace("grote ", "")
    if "grote" in ingredient_str:
        ingredient_str = ingredient_str.replace("grote ", "")
    if "grote" in ingredient_str:
        ingredient_str = ingredient_str.replace("grote ", "")


    return ingredient_str


for index, row in recipes.iterrows():
    ingredient_row = row['Ingredients'].replace("'", "").strip('][').split(',')
    for ingredient in ingredient_row:
        ingredient = ingredient.replace(" ", "", 1)

        if ingredient not in ingredients:
            all_ingredients.append(ingredient)

        ingredient = filter_ingredient(ingredient)

        if ingredient not in ingredients:
            ingredients.append(ingredient)


print(str(len(all_ingredients)) + " - " + str(len(ingredients)))
