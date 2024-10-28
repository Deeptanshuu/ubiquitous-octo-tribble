import csv
from collections import Counter
import json

# Dictionary mapping ingredients to emojis
EMOJI_MAPPING = {
    # Basics & Grains
    'flour': '🌾', 'sugar': '🍬', 'salt': '🧂', 'rice': '🍚', 'oats': '🌾',
    'quinoa': '🌾', 'pasta': '🍝', 'noodles': '🍜', 'bread': '🥖', 'tortilla': '🌯',
    'cornstarch': '🌽', 'baking': '🥄',
    
    # Dairy & Eggs
    'eggs': '🥚', 'butter': '🧈', 'milk': '🥛', 'cheese': '🧀', 'cream': '🥛',
    'yogurt': '🥛', 'mascarpone': '🧀', 'mozzarella': '🧀', 'parmesan': '🧀',
    'ricotta': '🧀', 'feta': '🧀',
    
    # Fruits
    'apple': '🍎', 'banana': '🍌', 'lemon': '🍋', 'lime': '🍋', 'orange': '🍊',
    'strawberry': '🍓', 'berry': '🫐', 'mango': '🥭', 'coconut': '🥥', 'grape': '🍇',
    'watermelon': '🍉', 'pear': '🍐', 'peach': '🍑', 'pineapple': '🍍',
    
    # Vegetables
    'tomato': '🍅', 'potato': '🥔', 'carrot': '🥕', 'corn': '🌽', 'broccoli': '🥦',
    'cucumber': '🥒', 'lettuce': '🥬', 'garlic': '🧄', 'onion': '🧅', 'eggplant': '🍆',
    'mushroom': '🍄', 'pepper': '🌶️', 'avocado': '🥑', 'olive': '🫒',
    
    # Proteins
    'chicken': '🍗', 'beef': '🥩', 'pork': '🍖', 'fish': '🐟', 'shrimp': '🍤',
    'tofu': '🧊', 'beans': '🫘', 'lentils': '🫘', 'nuts': '🥜', 'peanuts': '🥜',
    'bacon': '🥓', 'sausage': '🌭', 'lamb': '🍖', 'turkey': '🦃',
    
    # Beverages & Liquids
    'wine': '🍷', 'beer': '🍺', 'coffee': '☕', 'tea': '🍵', 'juice': '🧃',
    'water': '💧', 'oil': '🫗', 'vinegar': '🫗', 'sake': '🍶',
    
    # Condiments & Sauces
    'sauce': '🥫', 'ketchup': '🥫', 'mustard': '🥫', 'mayonnaise': '🥫',
    'soy': '🍶', 'honey': '🍯', 'jam': '🍯', 'syrup': '🍯',
    
    # Sweets & Desserts
    'chocolate': '🍫', 'candy': '🍬', 'cookie': '🍪', 'cake': '🍰',
    'ice cream': '🍨', 'pie': '🥧', 'donut': '🍩',
    
    # Prepared Foods
    'pizza': '🍕', 'burger': '🍔', 'taco': '🌮', 'burrito': '🌯',
    'sandwich': '🥪', 'sushi': '🍱', 'curry': '🍛',
    
    # Herbs & Spices
    'herbs': '🌿', 'spices': '🌶️', 'basil': '🌿', 'mint': '🌿',
    'cilantro': '🌿', 'parsley': '🌿', 'thyme': '🌿', 'rosemary': '🌿',
    'ginger': '🍂', 'cinnamon': '🍂', 'vanilla': '🌸', 'wasabi': '🌶️',
    'chili': '🌶️', 'paprika': '🌶️', 'turmeric': '🍂', 'cardamom': '🍂',
    'cumin': '🍂', 'coriander': '🌿', 'dill': '🌿', 'sage': '🌿',
    
    # Sprouts & Leaves
    'sprouts': '🌱', 'spinach': '🌿', 'cabbage': '🥬', 'kale': '🥬',
    'seaweed': '🌊', 'nori': '🌊',
    
    # Additional Categories
    'soup': '🥣', 'broth': '🥣', 'stock': '🥣', 'dressing': '🥗',
    'marinade': '🧂', 'seasoning': '🧂', 'powder': '🧂',
    'alcohol': '🍾', 'liquor': '🥃', 'vodka': '🍸', 'rum': '🥃',
    'whiskey': '🥃', 'tequila': '🥃'
}

def get_emoji_for_ingredient(ingredient):
    for key, emoji in EMOJI_MAPPING.items():
        if key in ingredient.lower():
            return f"{ingredient} {emoji}"
    return f"{ingredient} 🥄"  # Default emoji for ingredients without a specific one

def get_unique_ingredients(file_path):
    ingredients = []
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ingredients_list = row['ingredients_name'].split(',')
            ingredients.extend([ingredient.strip().lower() for ingredient in ingredients_list])
    
    # Use Counter to get unique ingredients and their counts
    ingredient_counts = Counter(ingredients)
    
    # Sort ingredients by count (descending) and then alphabetically
    sorted_ingredients = sorted(ingredient_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Add emojis to ingredients
    ingredients_with_emojis = [get_emoji_for_ingredient(ingredient) for ingredient, _ in sorted_ingredients]
    
    return ingredients_with_emojis

if __name__ == "__main__":
    file_path = "7k-dataset.csv"
    unique_ingredients = get_unique_ingredients(file_path)
    
    print(f"Total unique ingredients: {len(unique_ingredients)}")
    
    # Create the JSON structure matching the desired format
    ingredients_json = {
        "ingredients": unique_ingredients
    }
    
    # Convert to JSON with proper formatting
    json_output = json.dumps(ingredients_json, indent=2, ensure_ascii=False)
    
    # Print the JSON output
    print("\nJSON output:")
    print(json_output)
    
    # Save the JSON to a file ignore this
    output_file = "yes-chef/src/ingredients-2.json"
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(ingredients_json, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"\nJSON data has been saved to {output_file}")
