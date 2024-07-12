from sklearn.feature_extraction.text import TfidfVectorizer

# Sample recipe data (preprocessed)
recipe_1_ingredients = ["flour", "milk", "sugar" ,"veg"]
recipe_2_ingredients = ["eggs", "butter", "chocolate" , "non-veg"]
user_ingredients = ["flour", "eggs", "milk", "chocolate" , "non-veg"]

recipe_1_text = " ".join(recipe_1_ingredients)
recipe_2_text = " ".join(recipe_2_ingredients)
user_ingredients_text = " ".join(user_ingredients)

# One-hot encode
vectorizer = TfidfVectorizer(binary=True)
recipe_vectors = vectorizer.fit_transform([recipe_1_text, recipe_2_text])
user_vector = vectorizer.transform([user_ingredients_text])[0]


# Calculate cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(user_vector.reshape(1, -1), recipe_vectors)
recipe_1_similarity = similarities[0][0]
recipe_2_similarity = similarities[0][1]

print("Similarity between recipe 1 and user:", recipe_1_similarity)
print("Similarity between recipe 2 and user:", recipe_2_similarity)
