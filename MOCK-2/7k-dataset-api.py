from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)


# Load your dataset
recipes_data = pd.read_csv('7k-dataset.csv')

# Clean column names
recipes_data.columns = recipes_data.columns.str.strip()

# Define weights for user preferences
cuisine_weight = 0.2
course_weight = 0.3

# Prepare TF-IDF vectorizer
vectorizer = TfidfVectorizer(binary=True)

# Check if 'ingredients' column exists, if not, use 'ingredients_name'
ingredients_column = 'ingredients' if 'ingredients' in recipes_data.columns else 'ingredients_name'

if ingredients_column not in recipes_data.columns:
    raise ValueError(f"Neither 'ingredients' nor 'ingredients_name' column found in the dataset. Available columns are: {recipes_data.columns.tolist()}")

# Extract and join ingredients into text
recipes_data["ingredients_list"] = recipes_data[ingredients_column].apply(lambda x: str(x).strip().split(","))
recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

# Fit vectorizer and transform recipe ingredients
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

def calculate_difficulty(prep_time, cooking_time):
    try:
        total_time = float(prep_time) + float(cooking_time)
        if total_time < 30:
            return 'Easy'
        elif total_time < 60:
            return 'Medium'
        else:
            return 'Hard'
    except ValueError:
        return 'unknown'
def calculate_servings(prep_time, cooking_time):
    try:
        total_time = float(prep_time) + float(cooking_time)
        if total_time < 30:
            return '1 - 2 Servings'
        elif total_time < 60:
            return '4 - 6 Servings'
        else:
            return '6+ Servings'
    except ValueError:
        return 'unknown'
def calculate_weighted_similarity(similarity, recipe, user_cuisine, user_course):
    user_pref_similarity = 0
    if user_cuisine and 'cuisine' in recipe and user_cuisine == recipe['cuisine']:
        user_pref_similarity += cuisine_weight
    if user_course and 'course' in recipe and user_course.strip().lower() == recipe['course'].strip().lower():
        user_pref_similarity += course_weight
    weighted_similarity = similarity * (1 - (cuisine_weight + course_weight)) + user_pref_similarity
    return weighted_similarity

@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    data = request.json
    user_ingredients = data.get('ingredients', [])
    user_cuisine = data.get('cuisine')
    user_course = data.get('course')
    user_veg = data.get('veg', False)

    # Filter vegetarian recipes if requested
    filtered_recipes = recipes_data[recipes_data['diet'].str.strip().str.lower() == "vegetarian"] if user_veg else recipes_data

    # Transform user input
    user_ingredients_text = " ".join(user_ingredients)
    user_vector = vectorizer.transform([user_ingredients_text])

    # Calculate cosine similarity
    similarities = cosine_similarity(user_vector, vectorizer.transform(filtered_recipes["ingredients_text"])).flatten()

    # Calculate weighted similarity for each recipe
    weighted_similarities = [
        calculate_weighted_similarity(sim, filtered_recipes.iloc[idx], user_cuisine, user_course)
        for idx, sim in enumerate(similarities)
    ]

    # Get top 12 recommendations
    top_n_indices = np.argsort(weighted_similarities)[-12:][::-1]
    top_recipes = filtered_recipes.iloc[top_n_indices]

    recommendations = []
    for count, (_, row) in enumerate(top_recipes.iterrows(), start=1):
        recommendations.append({
            'id': count,
            'title': row['name'].strip(),
            #'description': row['description'].strip(),
            'difficulty': calculate_difficulty(row['prep_time'], row['cook_time']),
            'cooking_time': row['cook_time'].strip(),
            'image': row['image_url'].strip(),
            'veg': row['diet'].strip().lower() == 'vegetarian',
            'cuisine': row['cuisine'].strip(),
            'course': row['course'].strip(),
            'servings': calculate_servings( row['prep_time'], row['cook_time']),
        })


    return jsonify(recommendations)

@app.route('/api/recipe', methods=['POST'])
def recipe():
    data = request.json
    name = data.get('name', '').strip().lower()  # Normalize input

    if not name:
        return jsonify({"error": "Recipe name is required"}), 400

    recipes_data = pd.read_csv("7k-dataset.csv")

    # Strip spaces from column names
    recipes_data.columns = recipes_data.columns.str.strip()

    # Normalize recipe names in the dataset for comparison
    recipes_data['name'] = recipes_data['name'].str.strip().str.lower()

    # Find the recipe
    recipe_list = recipes_data[recipes_data['name'] == name].to_dict('records')

    if not recipe_list:
        return jsonify({"error": "Recipe not found"}), 404

    recipe = recipe_list[0]

    # Calculate difficulty and servings
    difficulty = calculate_difficulty(recipe.get('prep_time'), recipe.get('cook_time'))
    servings = calculate_servings(recipe.get('prep_time'), recipe.get('cook_time'))

    # Prepare the response
    response = {
        'name': recipe.get('name').title(),  # Convert back to title case for response
        'description': recipe.get('description'),
        'veg': recipe.get('diet').strip().lower() == 'vegetarian',  # Handle potential extra spaces
        'image': recipe.get('image_url'),
        'cooking_time': f"{recipe.get('prep_time', 0)} + {recipe.get('cook_time', 0)} mins",
        'serving_size': servings,
        'difficulty': difficulty,
        'course': recipe.get('course'),
        'cooking_ingredients': recipe.get('ingredients_name'),
        'cooking_instruction': recipe.get('instructions')
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)