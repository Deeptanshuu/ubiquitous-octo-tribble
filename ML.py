import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

# Load data
recipes_data = pd.read_csv("recipe.csv")

# Remove leading and trailing spaces from column names
recipes_data.columns = recipes_data.columns.str.strip()

# Convert 'cooking_time' to minutes
recipes_data['cooking_time'] = recipes_data['cooking_time'].str.extract('(\d+)', expand=False).astype(int)

# Convert 'serving_size' to numerical value
recipes_data['serving_size'] = recipes_data['serving_size'].str.extract('(\d+)', expand=False).astype(int)

# Check column names
print(recipes_data.columns)

# Ensure 'ingredients' column exists
if 'ingredients' in recipes_data.columns:
    recipes_data["ingredients_text"] = recipes_data["ingredients"].apply(lambda x: " ".join(x.strip().split(",")))

# Create feature preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("ingredients", TfidfVectorizer(binary=True), "ingredients_text"),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), ["cuisine", "course", "craving"]),
        ("numerical", MinMaxScaler(), ["cooking_time", "serving_size"])
    ],
    remainder="drop"
)

# Fit preprocessor and transform data
recipe_features = preprocessor.fit_transform(recipes_data)


# Function to get recommendations
def get_recommendations(user_ingredients, user_cuisine, user_course, user_craving, user_veg, top_n=5):
    user_input = pd.DataFrame({
        "ingredients_text": [" ".join(user_ingredients)],
        "cuisine": [user_cuisine],
        "course": [user_course],
        "craving": [user_craving],
        "veg": [user_veg],
        "cooking_time": [0],  # Placeholder value
        "serving_size": [0]   # Placeholder value
    })
    
    user_input.columns = user_input.columns.str.strip()
    
    if 'ingredients' in user_input.columns:
        user_input["ingredients_text"] = user_input["ingredients"].apply(lambda x: " ".join(x.strip().split(",")))
    
    user_features = preprocessor.transform(user_input)
    
    # Calculate cosine similarity
    similarities = cosine_similarity(user_features, recipe_features).flatten()
    
    # Get top N similar recipes
    top_indices = similarities.argsort()[-top_n:][::-1]
    top_recipes = recipes_data.iloc[top_indices]
    
    return top_recipes[["id", "name", "cuisine", "course", "craving", "veg", "cooking_time", "serving_size", "difficulty"]]

# Example usage
user_ingredients = ["rice noodles", "tofu", "eggs", "peanuts"]
user_cuisine = "Thai"
user_course = "Main Course"
user_craving = "savory"
user_veg = True

recommendations = get_recommendations(user_ingredients, user_cuisine, user_course, user_craving, user_veg)
print("Top 5 Recommended Recipes:")
print(recommendations)