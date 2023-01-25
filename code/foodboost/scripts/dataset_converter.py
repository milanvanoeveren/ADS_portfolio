import pandas as pd
from csv import writer

recipes = pd.read_csv("../assets/final_bram.csv")

# Get all tags
tags = []

for index, row in recipes.iterrows():
    tag_row = row['tags'].replace("'", "").strip('][').split(',')
    for tag in tag_row:
        if tag[0] == " ":
            tag = tag.replace(" ", "", 1)

        if tag not in tags:
            tags.append(tag)

ingredients = []


for index, row in recipes.iterrows():
    ingredient_row = row['ingredients'].replace("'", "").strip('][').split(',')
    for ingredient in ingredient_row:
        if ingredient[0] == " ":
            ingredient = ingredient.replace(" ", "", 1)

        if ingredient not in ingredients:
            ingredients.append(ingredient)


with open('../assets/recipes_new.csv', 'w', newline='', encoding="utf-8") as f_object:
    writer_object = writer(f_object)

    header = ['index', 'name'] + tags + ingredients

    writer_object.writerow(header)
    for index, row in recipes.iterrows():
        print(index)
        recipe_row = [row['id'], row['name']]
        for tag in tags:
            if tag in row['tags']:
                recipe_row.append(1)
            else:
                recipe_row.append(0)

        for ingredient in ingredients:
            if ingredient in row['ingredients']:
                recipe_row.append(1)
            else:
                recipe_row.append(0)

        writer_object.writerow(recipe_row)

    f_object.close()
