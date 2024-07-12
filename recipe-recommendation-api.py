from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Define weights for user preferences (adjust as needed)
cuisine_weight = 0.2
course_weight = 0.3
craving_weight = 0.5

# Read recipe data
recipes_data = pd.read_csv("recipe.csv")

# Extract and join ingredients into text
recipes_data["ingredients_list"] = recipes_data["ingredients"].apply(lambda x: x.strip().split(","))
recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(binary=True)

# Fit vectorizer and transform recipe ingredients
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

def calculate_weighted_similarity(similarity, user_cuisine, user_course, user_craving):
    """
    Calculates weighted similarity score based on TF-IDF and user preferences.
    """
    user_pref_similarity = 0
    if user_cuisine in recipes_data["cuisine"].unique():
        user_pref_similarity += cuisine_weight
    if user_course in recipes_data["course"].unique():
        user_pref_similarity += course_weight
    if user_craving in recipes_data["craving"].unique():
        user_pref_similarity += craving_weight
    weighted_similarity = -similarity * (1 - user_pref_similarity) + user_pref_similarity
    return weighted_similarity

@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    data = request.json
    user_ingredients = data.get('ingredients', [])
    user_cuisine = data.get('cuisine')
    user_course = data.get('course')
    user_craving = data.get('craving')
    user_veg = data.get('veg',True)
    
    
    user_ingredients_text = " ".join(user_ingredients)

    # Filter vegetarian recipes
    filtered_recipes = recipes_data[recipes_data['veg'] == user_veg] if user_veg else recipes_data

    # Transform user input
    user_vector = vectorizer.transform([user_ingredients_text])[0]

    # Calculate cosine similarity (TF-IDF)
    similarities = cosine_similarity(user_vector.reshape(1, -1), recipe_vectors)

    # Calculate weighted similarity for each recipe
    weighted_similarities = [calculate_weighted_similarity(sim, user_cuisine, user_course, user_craving) for sim in similarities[0]]

    # Get top 3 recommendations
    top_n_indices = np.argsort(weighted_similarities)[-10:][::-1]
    top_recipes = filtered_recipes.iloc[top_n_indices]

    # Prepare results
    results = []
    for _, row in top_recipes.iterrows():
        results.append({
            'id': int(row['id']),
            'name': row['name'],
            'course': row['course'],
            'cuisine': row['cuisine'],
            'craving': row['craving'],
            'ingredients': row['ingredients'],
            'vegetarian': (row['veg'])
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
