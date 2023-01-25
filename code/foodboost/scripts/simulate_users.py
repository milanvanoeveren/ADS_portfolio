from _csv import writer
import pandas as pd

# ======================================= Initialize variables =======================================================

requirements = ['frans', 'aziatisch', 'hollands', 'mexicaans', 'italiaans', 'mediterraan', 'amerikaans']
kitchen_empty = ['', '', '', '', '', '', '']

user_id = 1
min_values = 40
amount_of_users = 200
amount_of_recipes = 10

new_recipes = pd.read_csv("../assets/recipes_min_40.csv")

# ======================================= Filtering recipes ==========================================================

print("Start filtering recipes..")

filtered_recipes = new_recipes
first_ingredient_index = filtered_recipes.columns.get_loc("tag_end") + 1

for column in new_recipes.columns.values[first_ingredient_index:]:
    total_values = new_recipes[column].sum()

    if total_values < min_values:
        filtered_recipes = filtered_recipes.drop([column], axis=1)

print("Done. Filtered recipes shape:", filtered_recipes.shape, '\n')


# ======================================= Setting tags and ingredients ================================================


column_names = list(filtered_recipes.columns.values)

first_ingredient_index = filtered_recipes.columns.get_loc("tag_end") + 1
tags = column_names[2:first_ingredient_index]
ingredients = column_names[first_ingredient_index:]

print(str(len(tags)), "tags:", tags)
print(str(len(ingredients)), "ingredients:", ingredients, '\n')


# ======================================= Looping for user data ======================================================


print("Start writing user data..")

with open('../assets/userdata_min_40_v5.csv', 'w', newline='', encoding="utf-8") as f_object:
    writer_object = writer(f_object)

    header = ['user_id'] + tags + ingredients + ['kitchen', 'liked_recipes']
    writer_object.writerow(header)

    for requirement in requirements:
        for user in range(amount_of_users):
            user_row = [user_id]

            temp_df = filtered_recipes[filtered_recipes[requirement] == 1]
            indices = []

            for recipe in range(amount_of_recipes):
                row_list = temp_df.sample().values.tolist()[0][2:]
                for idx, value in enumerate(row_list):
                    if value == 1:
                        if idx not in indices:
                            indices.append(idx)

            for i in range(len(tags) + len(ingredients)):
                if i in indices:
                    user_row.append(1)
                else:
                    user_row.append(0)

            user_row.append(requirement)

            writer_object.writerow(user_row)
            user_id += 1


f_object.close()
print("Done.")

