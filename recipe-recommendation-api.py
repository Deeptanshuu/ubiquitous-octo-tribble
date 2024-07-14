from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def calculate_weighted_similarity(similarity, recipe, user_cuisine, user_course, user_craving):
    """
    Calculates weighted similarity score based on TF-IDF and user preferences.
    """
    # Define weights for user preferences (adjust as needed)
    cuisine_weight = 0.2
    course_weight = 0.3
    craving_weight = 0.5

    user_pref_similarity = 0
    if user_cuisine and user_cuisine == recipe['cuisine']:
        user_pref_similarity += cuisine_weight
    if user_course and user_course == recipe['course']:
        user_pref_similarity += course_weight
    if user_craving and user_craving == recipe['craving']:
        user_pref_similarity += craving_weight
    weighted_similarity = similarity * (1 - (cuisine_weight + course_weight + craving_weight)) + user_pref_similarity
    return weighted_similarity

@app.route('/api/recommend', methods=['POST'])
def recommend():
    # Read recipe data
    global recipes_data
    recipes_data = pd.read_csv("recipe.csv")

    # Optional: Clean recipe descriptions (replace with your cleaning steps)
    # Consider stemming or lemmatization here

    # Extract and join ingredients into text
    recipes_data["ingredients_list"] = recipes_data["ingredients"].apply(lambda x: x.strip().split(","))
    recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

    # Get user input from request
    data = request.json
    user_ingredients = data.get('ingredients', [])
    user_cuisine = data.get('cuisine',[])
    user_course = data.get('course')
    user_craving = data.get('craving',[])
    user_veg = data.get('veg', False)
    
    user_ingredients_text = " ".join(user_ingredients)
    
    # Filter vegetarian recipes
    if 'veg' in recipes_data.columns:
        if user_veg:
            recipes_data = recipes_data[recipes_data['veg'] == True]
        print(f"Filtered to {len(recipes_data)} {'vegetarian' if user_veg else 'all'} recipes.")
    else:
        return jsonify("Warning: 'veg' column not found in data. Vegetarian filtering not possible.")
    
    
    # Create TF-IDF vectorizer (consider adjusting binary parameter and stop words)
    vectorizer = TfidfVectorizer(binary=True)

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
    top_n = 15
    top_n_indices = np.argsort(weighted_similarities)[-top_n:][::-1]
    top_recipes = recipes_data.iloc[top_n_indices]

    # Prepare response
    recommendations = []
    for _, row in top_recipes.iterrows():
        recommendations.append({
            'id': row['id'],
            'title': row['name'],
            'description': row['description'],
            #'course': row['course'],
            #'cuisine': row['cuisine'],
            'difficulty': row['difficulty'],
            'cooking_time': row['cooking_time'],
            'servings': row['serving_size'],
            'image': f"./src/assets/id-{row['id']}/id-{row['id']}-cover.jpeg",
            #'craving': row['craving'],
            #'ingredients': row['ingredients'],
            #'vegetarian': row['veg'],
            
        })

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
