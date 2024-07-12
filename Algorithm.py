import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define weights for user preferences (adjust as needed)
cuisine_weight = 0.2
course_weight = 0.3
craving_weight = 0.5

# Read recipe data
recipes_data = pd.read_csv("recipe.csv")

# Optional: Clean recipe descriptions (replace with your cleaning steps)
# Consider stemming or lemmatization here


# Extract and join ingredients into text
recipes_data["ingredients_list"] = recipes_data["ingredients"].apply(lambda x: x.strip().split(","))
recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))


# Get user input for ingredients, cuisine, course, and craving (optional)
user_ingredients = ["curry paste", "coconut milk", "vegetables", "chicken"]
#user_ingredients = ["flour", "sugar", "eggs", "butter", "chocolate chips"]
user_ingredients_text = " ".join(user_ingredients)
user_cuisine = None  # Replace with user input (optional)
user_course = "Main Course"  # Replace with user input (optional)
user_craving = None 
user_veg = True  # Replace with user input (optional)

# Filter vegetarian recipes
if 'veg' in recipes_data.columns:
    if user_veg:
        recipes_data = recipes_data[recipes_data['veg'] == True]
    print(f"Filtered to {len(recipes_data)} {'vegetarian' if user_veg else 'all'} recipes.")
else:
    print("Warning: 'veg' column not found in data. Vegetarian filtering not possible.")

# Create TF-IDF vectorizer (consider adjusting binary parameter and stop words)
vectorizer = TfidfVectorizer(binary=True)

# Fit vectorizer and transform recipe ingredients
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

# Transform user input
user_vector = vectorizer.transform([user_ingredients_text])[0]

# Calculate cosine similarity (TF-IDF)
similarities = cosine_similarity(user_vector.reshape(1, -1), recipe_vectors)

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

# Calculate weighted similarity for each recipe
weighted_similarities = [calculate_weighted_similarity(sim, user_cuisine, user_course, user_craving) for sim in similarities]

# Print debugging information
#print("TF-IDF Similarities:")
#print(similarities)  # Print raw TF-IDF similarities

#print("Weighted Similarities:")
#print(weighted_similarities)  # Print weighted similarities

# Assuming you want top 3 recommendations
top_n_indices = np.argsort(weighted_similarities) # Use NumPy for efficient sorting (import numpy as np)
top_recipes = recipes_data.iloc[top_n_indices.flatten()]  # Flatten top_n_indices for indexing

# Print recommendations
print("Top Recommended Recipes:")
for index, row in top_recipes.iterrows():
    print(f"- id: {row['id']} \n"
          f"  name: {row['name']}\n"
          f"  course: {row['course']}\n"
          f"  cuisine: {row['cuisine']}\n"
          f"  craving: {row['craving']}\n"
          f"  ingredients: {row['ingredients']}\n"
          f"  vegetarian: {row['veg']}\n")
