from flask import Flask, request, jsonify
from flask_cors import CORS
from recipe_matcher import RecipeMatcher
import logging
import time
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize RecipeMatcher with pre-computed matrix
matcher = RecipeMatcher(
    matrix_path='ingredient_matrix.csv',
    recipes_path='7k-dataset.csv'
)

# Define weights for user preferences
cuisine_weight = 0.2
course_weight = 0.3

def calculate_weighted_similarity(similarity, recipe, user_cuisine, user_course):
    """Calculate weighted similarity score based on user preferences."""
    user_pref_similarity = 0
    if user_cuisine and recipe['cuisine']:
        if any(c.lower() in recipe['cuisine'].lower() for c in user_cuisine):
            user_pref_similarity += cuisine_weight
    if user_course and recipe['course']:
        if user_course.lower() in recipe['course'].lower():
            user_pref_similarity += course_weight
    weighted_similarity = similarity * (1 - (cuisine_weight + course_weight)) + user_pref_similarity
    return weighted_similarity

def calculate_difficulty(prep_time, cooking_time):
    """Calculate recipe difficulty based on total time."""
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
    """Calculate servings based on total time."""
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

def prepare_recommendation(count, recipe):
    """Format recipe data for API response."""
    return {
        'id': count,
        'title': recipe['name'].strip(),
        'difficulty': calculate_difficulty(recipe['prep_time'], recipe['cook_time']),
        'cooking_time': recipe['cook_time'].strip(),
        'image': recipe['image_url'].strip(),
        'veg': recipe['diet'].strip().lower() == 'vegetarian',
        'cuisine': recipe['cuisine'].strip(),
        'course': recipe['course'].strip(),
        'servings': calculate_servings(recipe['prep_time'], recipe['cook_time']),
    }

@app.route('/api/recommend-ai', methods=['POST'])
def recommend_recipes_api():
    """API endpoint for recipe recommendations."""
    start_time = time.time()
    data = request.json

    user_ingredients = data.get('ingredients', [])
    user_cuisine = data.get('cuisine', [])
    user_course = data.get('course', '')
    user_veg = data.get('veg', False)

    # Get initial recommendations using RecipeMatcher
    raw_recommendations = matcher.find_similar_recipes(
        user_ingredients=user_ingredients,
        top_n=24
    )

    # Apply additional filtering and weighting
    filtered_recommendations = []
    for recipe in raw_recommendations:
        # Apply vegetarian filter if requested
        if user_veg and recipe['diet'].strip().lower() != 'vegetarian':
            continue
            
        # Calculate weighted similarity
        recipe['similarity_score'] = calculate_weighted_similarity(
            recipe['similarity_score'],
            recipe,
            user_cuisine,
            user_course
        )
        filtered_recommendations.append(recipe)

    # Sort by weighted similarity and get top 24
    filtered_recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    filtered_recommendations = filtered_recommendations[:24]

    # Format recommendations for response
    with concurrent.futures.ThreadPoolExecutor() as executor:
        recommendations = list(executor.map(
            lambda args: prepare_recommendation(*args),
            [(count, recipe) for count, recipe in enumerate(filtered_recommendations, start=1)]
        ))

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

    return jsonify({
        'recommendations': recommendations,
        'execution_time': round(execution_time, 2),
    })

@app.route('/')
def root():
    """Root endpoint returning API information."""
    return jsonify({
        "message": "Recipe Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "/api/recommend-ai": "POST - Get recipe recommendations based on ingredients"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
