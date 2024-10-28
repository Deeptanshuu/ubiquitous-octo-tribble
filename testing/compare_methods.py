from flask import Flask
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from recipe_matcher import RecipeMatcher
import logging
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionMatcher:
    def __init__(self, dataset_path='7k-dataset.csv'):
        # Load dataset
        self.recipes_data = pd.read_csv(dataset_path)
        self.recipes_data.columns = self.recipes_data.columns.str.strip()
        
        # Prepare TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(binary=True)
        
        # Check for ingredients column
        self.ingredients_column = 'ingredients' if 'ingredients' in self.recipes_data.columns else 'ingredients_name'
        
        # Prepare ingredients
        self.recipes_data["ingredients_list"] = self.recipes_data[self.ingredients_column].apply(lambda x: str(x).strip().split(","))
        self.recipes_data["ingredients_text"] = self.recipes_data["ingredients_list"].apply(lambda x: " ".join(x))
        
        # Fit vectorizer
        self.recipe_vectors = self.vectorizer.fit_transform(self.recipes_data["ingredients_text"])

    def recommend(self, user_ingredients, user_cuisine=None, user_course=None, user_veg=False, top_n=24):
        # Transform user input
        user_ingredients_text = " ".join(user_ingredients)
        user_vector = self.vectorizer.transform([user_ingredients_text])
        
        # Calculate similarities
        similarities = cosine_similarity(user_vector, self.recipe_vectors).flatten()
        
        # Get top recommendations
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        return [(
            self.recipes_data.iloc[idx]['name'],
            similarities[idx],
            self.recipes_data.iloc[idx]['cuisine'],
            self.recipes_data.iloc[idx]['course']
        ) for idx in top_indices]

def create_comparison_output(test_cases):
    # Initialize both matchers
    matrix_matcher = RecipeMatcher()
    prod_matcher = ProductionMatcher()
    
    # Open file for writing results with UTF-8 encoding
    with open('comparison_results.txt', 'w', encoding='utf-8') as f:
        for case in test_cases:
            ingredients_str = ', '.join(case['ingredients'])
            f.write(f"\n{'='*80}\n")
            f.write(f"Test Case: {ingredients_str}\n")
            f.write(f"{'='*80}\n\n")
            
            # Test Matrix-based method
            start_time = time.time()
            matrix_results = matrix_matcher.find_similar_recipes(
                user_ingredients=case['ingredients'],
                top_n=24
            )
            matrix_time = (time.time() - start_time) * 1000
            
            # Test Production method
            start_time = time.time()
            prod_results = prod_matcher.recommend(
                user_ingredients=case['ingredients'],
                user_cuisine=case.get('cuisine', []),
                user_course=case.get('course', ''),
                user_veg=case.get('veg', False)
            )
            prod_time = (time.time() - start_time) * 1000
            
            # Write performance metrics
            f.write("Performance Metrics:\n")
            f.write(f"Matrix Method Time: {matrix_time:.2f}ms\n")
            f.write(f"Production Method Time: {prod_time:.2f}ms\n")
            f.write(f"Speed Difference: {abs(matrix_time - prod_time):.2f}ms\n\n")
            
            # Compare top 5 recipes
            f.write("Top 5 Recipes Comparison:\n")
            f.write(f"{'='*40} Matrix Method {'='*40}\n")
            for i, recipe in enumerate(matrix_results[:5], 1):
                try:
                    f.write(f"{i}. {recipe['name']}\n")
                    f.write(f"   Score: {recipe['similarity_score']:.3f}\n")
                    f.write(f"   Cuisine: {recipe['cuisine']}\n")
                    f.write(f"   Course: {recipe['course']}\n\n")
                except Exception as e:
                    logger.error(f"Error writing recipe: {e}")
                    continue
            
            f.write(f"\n{'='*40} Production Method {'='*40}\n")
            for i, (name, score, cuisine, course) in enumerate(prod_results[:5], 1):
                try:
                    f.write(f"{i}. {name}\n")
                    f.write(f"   Score: {score:.3f}\n")
                    f.write(f"   Cuisine: {cuisine}\n")
                    f.write(f"   Course: {course}\n\n")
                except Exception as e:
                    logger.error(f"Error writing recipe: {e}")
                    continue
            
            # Calculate and write agreement metrics
            matrix_recipes = set(r['name'] for r in matrix_results)
            prod_recipes = set(name for name, _, _, _ in prod_results)
            common_recipes = matrix_recipes.intersection(prod_recipes)
            
            f.write("\nAgreement Metrics:\n")
            f.write(f"Common Recipes: {len(common_recipes)} out of 24\n")
            f.write(f"Agreement Percentage: {(len(common_recipes) / 24 * 100):.2f}%\n")
            f.write(f"Matrix Unique: {len(matrix_recipes - prod_recipes)}\n")
            f.write(f"Production Unique: {len(prod_recipes - matrix_recipes)}\n")
            
            f.write("\n" + "-"*80 + "\n")

def main():
    # Define test cases
    test_cases = [
        {
            'ingredients': ['chicken', 'rice', 'onion'],
            'cuisine': ['Indian'],
            'course': 'main course'
        },
        {
            'ingredients': ['pasta', 'tomato', 'garlic', 'basil'],
            'cuisine': ['Italian'],
            'course': 'main course'
        },
        {
            'ingredients': ['chocolate', 'flour', 'sugar', 'eggs'],
            'cuisine': [],
            'course': 'dessert'
        }
    ]
    
    # Run comparison and write to file
    create_comparison_output(test_cases)
    logger.info("Comparison results saved to comparison_results.txt")

if __name__ == "__main__":
    main()
