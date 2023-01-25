import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# loading the data from the csv file to a pandas dataframe
recipes_data = pd.read_csv('../assets/recipes_2.0.csv')

# printing the first 5 rows of the dataframe
recipes_data.head()

# combining all features
combined_features = recipes_data['Ingredients']

# converting the text data to feature vectors
vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined_features)

# getting the similarity scores using cosine similarity
similarity = cosine_similarity(feature_vectors)

# getting the recipe name from the user
recipe_name = input(' Enter your favourite recipe : ')

# creating a list with all the recipe names given in the dataset
list_of_all_recipes = recipes_data['name'].tolist()

# finding the close match for the recipe name given by the user
find_close_match = difflib.get_close_matches(recipe_name, list_of_all_recipes)
print("Close match:", find_close_match)

close_match = find_close_match[0]

# finding the index of the recipe with title
index_of_the_recipe = recipes_data[recipes_data.name == close_match]['id'].values[0]

# getting a list of similar recipes
similarity_score = list(enumerate(similarity[index_of_the_recipe]))

# sorting the recipes based on their similarity score
sorted_similar_recipes = sorted(similarity_score, key=lambda x: x[1], reverse=True)

# print the name of similar recipes based on the index
print('Recipes suggested for you : \n')

i = 1
for recipe in sorted_similar_recipes:
    index = recipe[0]
    title_from_index = recipes_data[recipes_data.index == index]['name'].values[0]
    if i <= 30:
        print(i, '.', title_from_index)
        i += 1
