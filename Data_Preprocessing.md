# Data Preprocessing

## Data exploration, Data cleansing & Data preparation
### FoodBoost
Toen wij de dataset met ingredienten kregen voor het FoodBoost project hoorden wij van Tony dat het belangrijk was dat de ingredienten niet als tekst in de rijen stond, maar dat het binair was. Ik heb samen met Bram gezorgd dat de ingredienten in de kolommen stond en dat er voor elk gerecht bij elk ingredient een 1 of een 0 staat.

Verder kwam ik er tijdens het bekijken van de dataset achter dat veel ingredienten "grote" of "middelgrote" in de naam hadden. De woorden die aangeven hoe veel of hoe groot een ingredient is heb ik eruit gefilterd met een [script](code/foodboost/scripts/ingredients.py). 

Het is belangrijk dat de ingredienten en keukens als 0 of 1 staan bij gerechten, omdat het model dat voor een bepaalde kolom makkelijk kan voorspellen of dit een 0 of een 1 moet zijn. Uiteindelijk hadden wij hierdoor meer kolommen dan rijen, dus daarna heb ik met een ander script ervoor gezorgd dat alleen de 200 meest voorkomende ingredienten zijn meegenomen in de dataset.

Het idee van de app die wij gingen maken was om voor een bepaalde user te voorspellen welke gerechten zij allemaal lekker vinden op basis van de ingevoerde data. Om dit mogelijk te maken, heb ik userdata gesimuleerd om ervoor te zorgen dat het model hierop kan trainen. Nadat de user gerechten heeft geliked, wordt er een extra user_row aangemaakt en op basis hiervan wordt de voorspelling gedaan. De code voor het simuleren van de userdata is hieronder te vinden:
```python
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
```

## Data explanation & Data visualization
In onze uiteindelijke dataset stonden de keukens en ingredienten in de kolommen en de rijen waren de gerechten. Als een gerecht uit een bepaalde keuken kwam, dan stond er bij die kolom een 1 en anders een 0. Hetzelfde geldt voor de ingredienten. Hieronder is een afbeelding te zien van onze uiteindelijke dataset.

**Dataset ingredienten**
![image](https://user-images.githubusercontent.com/123479172/214669280-0284d380-fec4-4acd-92e2-9a39944c9b5a.png)

**Dataset users**
![image](https://user-images.githubusercontent.com/123479172/214670812-5d746a1e-2ee4-47f5-80c0-1052c4a0511b.png)
