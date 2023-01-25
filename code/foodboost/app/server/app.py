import json

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from csv import writer
import ast
import html

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        recipes = pd.read_csv("../assets/recipes_min_40_v2.csv")

        data = request.json
        if data:
            preferences = data['preferences']
            preferences_list = preferences.strip('][').split(',')
            for preference in preferences_list:
                preference = preference.replace('"', '')
                recipes = recipes[recipes.tags.str.contains(preference)]

        response_object['recipes'] = recipes.to_json(orient="records")

    return jsonify(response_object)


@app.route('/post_get_user_result', methods=['POST'])
def post_get_user_result():
    data = request.json

    if data and data['likedRecipes'] is not None:
        # try:
        #     # Write the user row to the csv
        #     recipes = data['likedRecipes']
        #     row = generate_user_row(recipes)
        #     write_user_data(row)
        #
        #     # Predict the kitchen
        #     kitchen = predict_user_kitchen()
        #
        #     # Get recommended recipe ids
        #     recommended_recipe_ids = get_recommended_recipe_ids()
        #
        #     # Get list of recipes
        #     df_recipes = pd.read_csv('final_recipes_min_40.csv')
        #     df_recipes = df_recipes.drop[6:]
        #
        #     recommended_recipes = []
        #     for recipe in recommended_recipe_ids:
        #         recipe_row = df_recipes.iloc[recipe[0]]
        #         recommended_recipes.append(recipe_row)
        #
        #     response_object = {'status': 'success', 'data': {'kitchen': kitchen, 'recipes': recommended_recipes}}
        #
        # except Exception as e:
        #     response_object = {'status': 'failed', 'error': str(e)}

        recipes = data['likedRecipes']
        row = generate_user_row(recipes)
        write_user_data(row)

        # Predict the kitchen
        kitchen = predict_user_kitchen()

        # Get recommended recipe ids
        recommended_recipe_ids = get_recommended_recipe_ids(kitchen)

        # Get list of recipes
        df_recipes = pd.read_csv('final_recipes_min_40.csv')
        df_recipes = df_recipes.drop(df_recipes.columns[6:], axis=1)

        recommended_recipes = []
        for recipe in recommended_recipe_ids:
            recipe_row = df_recipes.iloc[recipe]
            json_row = {'index': int(recipe_row['index']), 'name': recipe_row['name'], 'url': recipe_row['url'], 'image': recipe_row['image']}
            recommended_recipes.append(json_row)

        response_object = {'status': 'success', 'data': {'kitchen': kitchen, 'recipes': recommended_recipes}}

    else:
        response_object = {'status': 'failed'}

    return jsonify(response_object)


def write_user_data(row):
    with open('final_userdata_min_40.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()


def get_user_id():
    user_data = pd.read_csv("final_userdata_min_40.csv", encoding='latin-1')
    user_id_column = user_data["user_id"]
    user_id = int(user_id_column.max()) + 1

    return user_id


def generate_user_row(recipes):
    user_row = [get_user_id()]

    df_recipes = pd.read_csv("final_recipes_min_40.csv")
    indices = []

    column_names = list(df_recipes.columns.values)

    first_ingredient_index = df_recipes.columns.get_loc("tag_end") + 1
    ingredients = column_names[first_ingredient_index:]

    print(ingredients)

    recipes = ast.literal_eval(recipes)
    for recipe in recipes:
        recipe_ingredient_list = df_recipes.iloc[recipe].tolist()
        recipe_ingredient_list = recipe_ingredient_list[first_ingredient_index:]

        for idx, value in enumerate(recipe_ingredient_list):
            if value == 1:
                if idx not in indices:
                    indices.append(idx)

    # 0 for all tags and 1 for tag_end
    for i in range(7):
        user_row.append(0)
    user_row.append(1)

    # all ingredients
    for i in range(len(ingredients)):
        if i in indices:
            user_row.append(1)
        else:
            user_row.append(0)

    # kitchen and list of recipe_indexes
    user_row.append('geen')
    user_row.append(recipes)

    return user_row


def predict_user_kitchen():
    df_userdata = pd.read_csv('final_userdata_min_40.csv')

    df_userdata_min = df_userdata.drop(df_userdata.columns[0:9], axis=1)
    df_userdata_min = df_userdata_min.drop('liked_recipes', axis=1)

    df_train = df_userdata_min[:599]
    df_predict = df_userdata_min[-1:]
    X_df_predict = df_predict.drop('kitchen', axis=1)

    kitchens = ['aziatisch', 'frans', 'hollands', 'italiaans', 'mexicaans', 'amerikaans', 'mediterraan']

    for kitchen in range(len(df_train)):
        df_train['kitchen'].iloc[kitchen] = kitchens.index(df_train['kitchen'].iloc[kitchen])

    X = df_train.drop('kitchen', axis=1)
    y = df_train['kitchen'].astype('int')

    model = KNeighborsClassifier(leaf_size=1, metric='euclidean', weights='distance')
    model.fit(X, y)
    y_proba = model.predict(X_df_predict)

    kitchen = ""

    for index in y_proba:
        kitchen = kitchens[index]

    df_userdata.kitchen.iloc[-1] = kitchen

    df_userdata.to_csv("final_userdata_min_40.csv", index=False)

    return kitchen


def get_recommended_recipe_ids(kitchen):
    df_userdata = pd.read_csv('final_userdata_min_40.csv')
    df_userdata = df_userdata.drop(df_userdata.columns[1:9], axis=1)

    df_recipes = pd.read_csv("final_recipes_min_40.csv")
    first_ingredient_index = df_recipes.columns.get_loc("tag_end") + 1
    all_ingredients = df_recipes.columns.values[first_ingredient_index:].tolist()

    # Convert the userdata
    df_converted_userdata = pd.DataFrame(columns=['user_id', 'ingredients'])

    for index, row in df_userdata.iterrows():
        user_ingredients = ""

        for ingredient in all_ingredients:
            if row[ingredient] == 1:
                user_ingredients += " " + ingredient

        user_row = {'user_id': row['user_id'], 'ingredients': user_ingredients, 'liked_recipes': row['liked_recipes']}

        df_converted_userdata = pd.concat([df_converted_userdata, pd.DataFrame.from_records([user_row])], ignore_index=True)

    # Convert the recipe
    df_converted_recipes = pd.DataFrame(columns=['index', 'name'])

    recipe_row = {'index': 0, 'name': 'user_row', 'ingredients': df_converted_userdata.iloc[-1].ingredients}
    df_converted_recipes = pd.concat([df_converted_recipes, pd.DataFrame.from_records([recipe_row])], ignore_index=True)

    liked_recipes_indexes = ast.literal_eval(df_converted_userdata.iloc[-1].liked_recipes)

    for index, row in df_recipes.iterrows():
        if row[kitchen] == 1:
            print(kitchen, row[kitchen], row['name'], row['index'])
            recipe_ingredients = ""

            for ingredient in all_ingredients:
                if row[ingredient] == 1:
                    recipe_ingredients += " " + ingredient

            recipe_row = {'index': row['index'], 'name': html.unescape(row['name']), 'ingredients': recipe_ingredients}

            if row['index'] not in liked_recipes_indexes:
                df_converted_recipes = pd.concat([df_converted_recipes, pd.DataFrame.from_records([recipe_row])], ignore_index=True)

    print(df_converted_recipes)

    # Calculate the recommended recipes
    combined_features = df_converted_recipes['ingredients']

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    similarity_score = list(enumerate(similarity[0]))

    sorted_similar_scores = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    top_recipes = sorted_similar_scores[1:11]
    recommended_recipe_ids = []

    for top_recipe in top_recipes:
        recommended_recipe_ids.append(int(df_converted_recipes.iloc[top_recipe[0]]['index']))

    return recommended_recipe_ids


if __name__ == '__main__':
    app.run()
