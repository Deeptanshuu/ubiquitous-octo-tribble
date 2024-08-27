import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache


app = Flask(__name__)
CORS(app)


cuisine_weight = 0.2
course_weight = 0.3

# Load and preprocess dataset
@lru_cache(maxsize=None)
def load_and_preprocess_data():
    df = pd.read_csv('7k-dataset.csv')
    df.columns = df.columns.str.strip()
    
    # Handle missing columns
    if 'ingredients' in df.columns:
        ingredients_column = 'ingredients'
    elif 'ingredients_name' in df.columns:
        ingredients_column = 'ingredients_name'
    else:
        raise ValueError("Required column 'ingredients' or 'ingredients_name' not found.")

    df["ingredients_list"] = df[ingredients_column].apply(lambda x: str(x).strip().split(","))
    df["ingredients_text"] = df["ingredients_list"].apply(lambda x: " ".join(x))
    
    return df

recipes_data = load_and_preprocess_data()
vectorizer = TfidfVectorizer(binary=True)
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

# Cached preprocessed data
@lru_cache(maxsize=None)
def get_vectorized_data():
    return recipe_vectors

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


@lru_cache(maxsize=None)
def get_recommendations_original(user_ingredients, user_cuisine, user_course, user_veg):
    start_time = time.time()
    
    filtered_recipes = recipes_data[recipes_data['diet'].str.strip().str.lower() == "vegetarian" ] if user_veg else recipes_data

    if filtered_recipes.empty:
        print("No recipes found for the given filter criteria.")
        return [], 0

    user_ingredients_text = " ".join(user_ingredients)
    user_vector = vectorizer.transform([user_ingredients_text])

    similarities = cosine_similarity(user_vector, get_vectorized_data()).flatten()

    if len(similarities) != len(recipes_data):
        print(f"Mismatch in lengths: similarities length is {len(similarities)}, recipes_data length is {len(recipes_data)}")
    
    weighted_similarities = []
    for idx, sim in enumerate(similarities):
        if idx >= len(filtered_recipes):
            #print(f"Index {idx} out of bounds for filtered_recipes with length {len(filtered_recipes)}")
            continue
        weighted_similarity = calculate_weighted_similarity(sim, filtered_recipes.iloc[idx], user_cuisine, user_course)
        weighted_similarities.append(weighted_similarity)

    if not weighted_similarities:
        print("No weighted similarities calculated.")
        return [], 0

    top_n_indices = np.argsort(weighted_similarities)[-10:][::-1]

    if len(top_n_indices) == 0:
        print("No top indices found.")
        return [], 0

    top_recipes = filtered_recipes.iloc[top_n_indices]

    recommendations = []
    for count, (_, row) in enumerate(top_recipes.iterrows(), start=1):
        recommendations.append({
            'id': count,
            'title': row['name'].strip(),
            'difficulty': calculate_difficulty(row['prep_time'], row['cook_time']),
            'cooking_time': row['cook_time'].strip(),
            'image': row['image_url'].strip(),
            'veg': row['diet'].strip().lower() == 'vegetarian',
            'cuisine': row['cuisine'].strip(),
            'course': row['course'].strip(),
            'servings': calculate_servings(row['prep_time'], row['cook_time']),
        })

    end_time = time.time()
    execution_time = end_time - start_time
    
    return tuple(recommendations), execution_time



def get_recommendations_brute_force(user_ingredients, user_cuisine, user_course, user_veg):
    start_time = time.time()
    
    filtered_recipes = recipes_data[recipes_data['diet'].str.strip().str.lower() == "vegetarian"] if user_veg else recipes_data

    def calculate_match_score(recipe):
        ingredient_match = len(set(user_ingredients) & set(recipe['ingredients_list']))
        cuisine_match = 1 if user_cuisine and user_cuisine == recipe['cuisine'] else 0
        course_match = 1 if user_course and user_course.strip().lower() == recipe['course'].strip().lower() else 0
        return ingredient_match + cuisine_weight * cuisine_match + course_weight * course_match

    filtered_recipes.loc[:, 'match_score'] = filtered_recipes.apply(calculate_match_score, axis=1)
    top_recipes = filtered_recipes.nlargest(10, 'match_score')

    recommendations = []
    for count, (_, row) in enumerate(top_recipes.iterrows(), start=1):
        recommendations.append({
            'id': count,
            'title': row['name'].strip(),
            'difficulty': calculate_difficulty(row['prep_time'], row['cook_time']),
            'cooking_time': row['cook_time'].strip(),
            'image': row['image_url'].strip(),
            'veg': row['diet'].strip().lower() == 'vegetarian',
            'cuisine': row['cuisine'].strip(),
            'course': row['course'].strip(),
            'servings': calculate_servings(row['prep_time'], row['cook_time']),
        })

    end_time = time.time()
    execution_time = end_time - start_time
    
    return recommendations, execution_time

@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    data = request.json
    user_ingredients = tuple(data.get('ingredients', []))
    user_cuisine = data.get('cuisine')
    user_course = data.get('course')
    user_veg = data.get('veg', False)

    brute_force_recommendations, brute_force_time = get_recommendations_brute_force(user_ingredients, user_cuisine, user_course, user_veg)
    original_recommendations, original_time = get_recommendations_original(user_ingredients, user_cuisine, user_course, user_veg)
    
    return jsonify({
        'original': {
            'recommendations': original_recommendations,
            'execution_time': original_time
        },
        'brute_force': {
            'recommendations': brute_force_recommendations,
            'execution_time': brute_force_time
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
    
