import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def tokenize_ingredients(text):
    """Split ingredients by comma."""
    return text.split(',')

def create_vectorizer():
    """Create a new vectorizer with the same parameters."""
    return CountVectorizer(
        tokenizer=tokenize_ingredients,
        strip_accents='unicode',
        lowercase=True,
        stop_words='english',
        min_df=2,
        binary=True
    )

class RecipeMatcher:
    def __init__(self, matrix_path='ingredient_matrix.csv', recipes_path='7k-dataset.csv'):
        """Initialize the recipe matcher with necessary data files."""
        try:
            # Load the ingredient matrix and recipes data
            self.ingredient_matrix = pd.read_csv(matrix_path)
            self.recipes_df = pd.read_csv(recipes_path)
            logger.info("Successfully loaded all required files")
        except Exception as e:
            logger.error(f"Error loading files: {str(e)}")
            raise

    def process_user_ingredients(self, ingredients_list):
        """Convert user ingredients list to binary vector."""
        try:
            # Create a zero-filled vector with the same columns as ingredient matrix
            user_vector = pd.DataFrame(0, 
                index=[0], 
                columns=self.ingredient_matrix.columns)
            
            # Mark 1 for ingredients that are present
            for ingredient in ingredients_list:
                ingredient = ingredient.strip().lower()
                matching_columns = [col for col in self.ingredient_matrix.columns 
                                 if ingredient in col.lower()]
                for col in matching_columns:
                    user_vector[col] = 1
            
            return user_vector
            
        except Exception as e:
            logger.error(f"Error processing user ingredients: {str(e)}")
            raise

    def find_similar_recipes(self, user_ingredients, top_n=5, threshold=0.0):
        """Find the most similar recipes based on ingredients."""
        try:
            # Convert user ingredients to vector
            user_vector = self.process_user_ingredients(user_ingredients)

            # Calculate cosine similarity between user vector and all recipes
            similarities = cosine_similarity(
                user_vector,
                self.ingredient_matrix
            )[0]

            # Filter by threshold and get top N similar recipes
            valid_indices = np.where(similarities >= threshold)[0]
            top_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1][:top_n]]
            
            # Create results with similarity scores
            results = []
            for idx in top_indices:
                recipe = self.recipes_df.iloc[idx]
                results.append({
                    'name': recipe['name'],
                    'similarity_score': similarities[idx],
                    'ingredients': recipe['ingredients_name'],
                    'instructions': recipe['instructions'],
                    'image_url': recipe['image_url'],
                    'cuisine': recipe['cuisine'],
                    'course': recipe['course'],
                    'prep_time': recipe['prep_time'],
                    'cook_time': recipe['cook_time'],
                    'diet': recipe['diet']
                })
            
            return results

        except Exception as e:
            logger.error(f"Error finding similar recipes: {str(e)}")
            raise

    def print_recipe(self, recipe):
        """Helper method to print a recipe in a formatted way."""
        print(f"\nRecipe: {recipe['name']}")  # Changed from recipe_name
        print(f"Similarity Score: {recipe['similarity_score']:.2f}")
        print(f"URL: {recipe['link']}")  # Changed from url
        print("\nIngredients:")
        print(recipe['ingredients'])
        print("\nInstructions:")
        print(recipe['instructions'])
        print("-" * 50)

def main():
    """Example usage of the RecipeMatcher class."""
    try:
        # Initialize the matcher
        matcher = RecipeMatcher()
        
        # Example user ingredients
        user_ingredients = [
            'chicken',
            'rice',
            'onions',
            'garlic'
        ]
        
        # Find similar recipes
        logger.info(f"Finding recipes similar to ingredients: {user_ingredients}")
        similar_recipes = matcher.find_similar_recipes(user_ingredients, threshold=0.1)
        
        # Print results
        print("\nTop 5 Similar Recipes:")
        print("-" * 50)
        for i, recipe in enumerate(similar_recipes, 1):
            print(f"\n{i}. {recipe['name']}")
            print(f"Cuisine: {recipe['cuisine']}")
            print(f"Course: {recipe['course']}")
            print(f"Similarity Score: {recipe['similarity_score']:.2f}")
            # print(f"Prep Time: {recipe['prep_time']}")
            # print(f"Cook Time: {recipe['cook_time']}")
            # print(f"Image URL: {recipe['image_url']}")
            print("\nIngredients:")
            print("Ingredients:", recipe['ingredients'])
            # print("Quantities:", recipe['quantities'])
            # print("\nInstructions:")
            # print(recipe['instructions'][:200] + "...")
            print("-" * 50)

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
