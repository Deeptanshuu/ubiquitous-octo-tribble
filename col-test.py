import pandas as pd

# Load the CSV file
recipes_data = pd.read_csv("recipe.csv")

# Print the columns to check if 'ingredients' exists
print(recipes_data.columns)
