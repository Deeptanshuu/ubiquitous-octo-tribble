import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(file_path='7k-dataset.csv'):
    """Load and prepare the dataset."""
    try:
        df = pd.read_csv(file_path)
        if 'ingredients_name' not in df.columns:
            raise ValueError("The dataset must contain an 'ingredients_name' column")
        return df
    except FileNotFoundError:
        logger.error(f"Could not find the file: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def tokenize_ingredients(text):
    """Split ingredients by comma."""
    return text.split(',')

def create_binary_matrix(ingredients_series):
    """Create binary matrix from ingredients."""
    try:
        # Initialize the vectorizer with binary=True for presence/absence encoding
        vectorizer = CountVectorizer(
            tokenizer=tokenize_ingredients,
            strip_accents='unicode',
            lowercase=True,
            stop_words='english',
            min_df=2,
            binary=True  # This makes it output 1/0 instead of counts
        )

        # Fit and transform the data
        binary_matrix = vectorizer.fit_transform(ingredients_series)
        
        # Convert to DataFrame
        ingredient_matrix = pd.DataFrame(
            binary_matrix.toarray(), 
            columns=vectorizer.get_feature_names_out()
        )
        
        return ingredient_matrix, vectorizer
    except Exception as e:
        logger.error(f"Error creating binary matrix: {str(e)}")
        raise

def save_matrix(matrix, output_path='ingredient_matrix.csv'):
    """Save the matrix to a CSV file."""
    try:
        matrix.to_csv(output_path, index=False)
        logger.info(f"Matrix saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error saving matrix: {str(e)}")
        raise

def main():
    try:
        # Load the dataset
        logger.info("Loading dataset...")
        df = load_data()
        
        # Ensure ingredients column is string type
        df['ingredients_name'] = df['ingredients_name'].astype(str)
        
        # Create binary matrix
        logger.info("Creating binary matrix...")
        ingredient_matrix, vectorizer = create_binary_matrix(df['ingredients_name'])
        
        # Save the matrix
        logger.info("Saving matrix...")
        save_matrix(ingredient_matrix)
        
        # Optional: Save the vectorizer for later use
        import joblib
        joblib.dump(vectorizer, 'binary_vectorizer.joblib')
        
        logger.info("Process completed successfully!")
        
        return ingredient_matrix, vectorizer
        
    except Exception as e:
        logger.error(f"An error occurred in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
