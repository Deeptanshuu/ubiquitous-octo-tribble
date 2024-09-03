import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load the dataset
recipes_data = pd.read_csv('7k-dataset.csv')

# Clean column names
recipes_data.columns = recipes_data.columns.str.strip()

# Extract and join ingredients into text
recipes_data["ingredients_list"] = recipes_data["ingredients_name"].apply(lambda x: str(x).strip().split(","))
recipes_data["ingredients_text"] = recipes_data["ingredients_list"].apply(lambda x: " ".join(x))

# Prepare TF-IDF vectorizer
vectorizer = TfidfVectorizer(binary=True)
recipe_vectors = vectorizer.fit_transform(recipes_data["ingredients_text"])

# Save the vectorizer for later use
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Convert the sparse matrix to a dense format
recipe_vectors_dense = recipe_vectors.todense()

# Add the vectors as a new column in the DataFrame
recipes_data['tfidf_vectors'] = recipe_vectors_dense.tolist()

# Save the DataFrame back to CSV
recipes_data.to_csv('7k-dataset-with-vectors.csv', index=False)
