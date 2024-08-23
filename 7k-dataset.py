import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define weights for user preferences (adjust as needed)
cuisine_weight = 0.2
course_weight = 0.3

# Read recipe data
recipes_data = pd.read_csv("7k-dataset.csv")

# Print column names to verify
print("Columns in the dataset:", recipes_data.columns.tolist())

# Check if 'ingredients' column exists, if not, use 'ingredients_name'
ingredients_column = 'ingredients' if 'ingredients' in recipes_data.columns else 'ingredients_name'

if ingredients_column not in recipes_data.columns:
    raise ValueError(f"Neither 'ingredients' nor 'ingredients_name' column found in the dataset. Available columns are: {recipes_data.columns.tolist()}")

# Extract and join ingredients into text
recipes_data["ingredients_list"] = recipes_data[ingredients_column].apply(lambda x: str(x).strip().split(","))
recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

# Get user input for ingredients, cuisine, course, and craving (optional)
user_ingredients = ["curry paste", "coconut milk", "vegetables"]
user_ingredients_text = " ".join(user_ingredients)
user_cuisine = None  # Replace with user input (optional)
user_course = "Main Course"  # Replace with user input (optional)
#user_craving = "spicy"
user_veg = True  # Replace with user input (optional)

# Filter vegetarian recipes
if 'diet' in recipes_data.columns:
    if user_veg:
        recipes_data = recipes_data[recipes_data['diet'] == "Vegetarian"]
    print(f"Filtered to {len(recipes_data)} {'vegetarian' if user_veg else 'all'} recipes.")
else:
    print("Warning: 'diet' column not found in data. Vegetarian filtering not possible.")

# Create TF-IDF vectorizer (consider adjusting binary parameter and stop words)
vectorizer = TfidfVectorizer(binary=True)

# Fit vectorizer and transform recipe ingredients
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

# Transform user input
user_vector = vectorizer.transform([user_ingredients_text])

# Calculate cosine similarity (TF-IDF)
similarities = cosine_similarity(user_vector, recipe_vectors).flatten()

def calculate_weighted_similarity(similarity, recipe, user_cuisine, user_course):
    """
    Calculates weighted similarity score based on TF-IDF and user preferences.
    """
    user_pref_similarity = 0
    if user_cuisine and 'cuisine' in recipe and user_cuisine == recipe['cuisine']:
        user_pref_similarity += cuisine_weight
    if user_course and 'course' in recipe and user_course == recipe['course']:
        user_pref_similarity += course_weight
    # if user_craving and 'craving' in recipe and user_craving == recipe['craving']:
    #     user_pref_similarity += craving_weight
    weighted_similarity = similarity * (1 - (cuisine_weight + course_weight )) + user_pref_similarity
    return weighted_similarity

# Calculate weighted similarity for each recipe
weighted_similarities = [
    calculate_weighted_similarity(sim, recipes_data.iloc[idx], user_cuisine, user_course)
    for idx, sim in enumerate(similarities)
]

# Get top N recommendations
top_n = 5
top_n_indices = np.argsort(weighted_similarities)[-top_n:][::-1]
top_recipes = recipes_data.iloc[top_n_indices]

# Print recommendations
print("Top 5 Recommended Recipes:")
for index, row in top_recipes.iterrows():
    print(f"- id: {row['id'] if 'id' in row else 'N/A'}")
    print(f"  name: {row['name']}")
    print(f"  course: {row['course'] if 'course' in row else 'N/A'}")
    print(f"  cuisine: {row['cuisine'] if 'cuisine' in row else 'N/A'}")
    print(f"  diet: {row['diet'] if 'diet' in row else 'N/A'}")
    print(f"  ingredients: {row[ingredients_column]}")
    print()