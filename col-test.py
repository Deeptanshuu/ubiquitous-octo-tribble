import pandas as pd

# Load the CSV file and remove any extra spaces from column names
df = pd.read_csv('7k-dataset-translated.csv')
df.columns = df.columns.str.strip()

# Check if the 'ingredients_name' column exists
if 'ingredients_name' not in df.columns:
    raise ValueError("The column 'ingredients_name' does not exist in the CSV file.")

# Initialize a set to store unique ingredient names
ingredient_names_set = set()


# Iterate through the 'ingredients_name' column and add each item to the set
for ingredients in df['ingredients_name'].dropna():
    # Split ingredients by a delimiter if necessary (e.g., comma)
    # Assuming ingredients are separated by commas
    ingredients_list = ingredients.split(',')
    ingredient_names_set.update([ingredient.strip() for ingredient in ingredients_list])

# Print the number of unique ingredients found
print(f"Number of unique ingredients: {len(ingredient_names_set)}")

#print("\nUnique ingredients:")
for ingredient in sorted(ingredient_names_set):
    print(ingredient)