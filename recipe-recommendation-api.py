from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import heapq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

def calculate_weighted_similarity(similarity, recipe, user_cuisine, user_course, user_craving):
    """
    Calculates weighted similarity score based on TF-IDF and user preferences.
    """
    # Define weights for user preferences (adjust as needed)
    cuisine_weight = 15
    course_weight = 20
    craving_weight = 15

    # Normalize user inputs
    user_cuisine_normalized = [c.strip().lower() for c in user_cuisine] if user_cuisine else []
    user_course_normalized = user_course.strip().lower() if user_course else ""
    user_craving_normalized = [c.strip().lower() for c in user_craving] if user_craving else []

    # Normalize recipe fields
    recipe_cuisine_normalized = [c.strip().lower() for c in recipe['cuisine'].split(',')] if recipe['cuisine'] else []
    recipe_course_normalized = recipe['course'].strip().lower() if recipe['course'] else ""
    recipe_craving_normalized = [c.strip().lower() for c in recipe['craving'].split(',')] if recipe['craving'] else []

    # Debugging outputs
    #print(f"User cuisine: {user_cuisine_normalized}, Recipe cuisine: {recipe_cuisine_normalized}")
    #print(f"User course: {user_course_normalized}, Recipe course: {recipe_course_normalized}")
    #print(f"User craving: {user_craving_normalized}, Recipe craving: {recipe_craving_normalized}")

    user_pref_similarity = 0
    if user_cuisine_normalized and any(c in recipe_cuisine_normalized for c in user_cuisine_normalized):
        user_pref_similarity += cuisine_weight
        print(f"Cuisine match: +{cuisine_weight}")
    if user_course_normalized and user_course_normalized == recipe_course_normalized:
        user_pref_similarity += course_weight
        print(f"Course match: +{course_weight}")
    if user_craving_normalized and any(c in recipe_craving_normalized for c in user_craving_normalized):
        user_pref_similarity += craving_weight
        print(f"Craving match: +{craving_weight}")

    weighted_similarity = similarity * (cuisine_weight + course_weight + craving_weight) + user_pref_similarity
    #print(f"Weighted similarity: {weighted_similarity}")
    return weighted_similarity



@app.route('/api/recommend', methods=['POST'])
def recommend():
    # Read recipe data
    recipes_data = pd.read_csv("recipe.csv")

    # Strip spaces from column names
    recipes_data.columns = recipes_data.columns.str.strip()

    # Print the cleaned columns to verify
    #print("Columns:", recipes_data.columns)

    # Check if 'ingredients' column exists
    if 'ingredients' not in recipes_data.columns:
        return jsonify("Error: 'ingredients' column not found in the data.")

    # Process ingredients column
    recipes_data["ingredients_list"] = recipes_data["ingredients"].apply(lambda x: x.strip().split(","))
    recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

    # Get user input from request
    data = request.json
    user_ingredients = data.get('ingredients', [])
    user_cuisine = data.get('cuisine', [])
    user_course = data.get('course')
    user_craving = data.get('craving', [])
    user_veg = data.get('veg', False)

    user_ingredients_text = " ".join(user_ingredients)

    # Filter vegetarian recipes if the column exists
    if 'veg' in recipes_data.columns:
        if user_veg:
            recipes_data = recipes_data[recipes_data['veg'] == True]
        print(f"Filtered to {len(recipes_data)} {'vegetarian' if user_veg else 'all'} recipes.")
    else:
        return jsonify("Warning: 'veg' column not found in data. Vegetarian filtering not possible.")

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer( ngram_range=(1, 2))

    # Fit vectorizer and transform recipe ingredients
    recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

    # Transform user input
    user_vector = vectorizer.transform([user_ingredients_text])

    # Calculate cosine similarity (TF-IDF)
    similarities = cosine_similarity(user_vector, recipe_vectors).flatten()

    # Calculate weighted similarity for each recipe
    weighted_similarities = [
        calculate_weighted_similarity(sim, recipes_data.iloc[idx], user_cuisine, user_course, user_craving)
        for idx, sim in enumerate(similarities)
    ]

    # Get top N recommendations
    top_n = 9
    top_n_indices = heapq.nlargest(top_n, range(len(weighted_similarities)), weighted_similarities.__getitem__)
    top_recipes = recipes_data.iloc[top_n_indices]

    # Prepare response
    recommendations = []
    for _, row in top_recipes.iterrows():
        recommendations.append({
            'title': row['name'],
            'id': row['id'],
            'description': row['description'],
            'difficulty': row['difficulty'],
            'cooking_time': row['cooking_time'],
            'servings': row['serving_size'],
            'image': f"./id-{row['id']}/id-{row['id']}-cover.jpeg",
            #'craving': row['craving'],
            #'ingredients': row['ingredients'],
            'veg': row['veg'],
            #'course': row['course'],
            #'cuisine': row['cuisine'],
            
        })

    return jsonify(recommendations)

@app.route('/api/recpie', methods=['POST'])
def recipe():
    data = request.json
    id = data.get('id')
    id = int(id)
    global recipes_data
    recipes_data = pd.read_csv("recipe.csv")
    # Strip spaces from column names
    recipes_data.columns = recipes_data.columns.str.strip()
    recipe = recipes_data[recipes_data['id'] == id].to_dict('records')[0]
    recipe_data = {
        'image': f"./id-{id}/id-{id}-cover (2).jpeg",
        #'image-2': f"./src/assets/id-{id}/id-{id}-cover (2).jpeg"
    }
    recipe.update(recipe_data)
    return jsonify(recipe)


if __name__ == '__main__':
    app.run(debug=True)
