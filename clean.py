import pandas as pd

file_path = 'recipe.csv'
recipe_df = pd.read_csv(file_path)


recipe_df.columns = recipe_df.columns.str.strip()

allowed_ingredients = [ 'flour', 'sugar', 'eggs', 'chocolate chips', 'butter', 'vanilla extract', 'rice noodles', 'tofu', 'bean sprouts', 'peanuts', 'lime', 'fish sauce', 'tamarind paste', 'garlic', 'shallots', 'chicken', 'onions', 'tomatoes', 'coconut milk', 'curry paste', 'ginger', 'cilantro', 'cocoa powder', 'milk', 'vegetable oil', 'baking powder', 'salt', 'ground beef', 'pasta', 'carrots', 'celery', 'red wine', 'beef broth', 'noodles', 'thyme', 'parsley', 'apples', 'cinnamon', 'nutmeg', 'lemon juice', 'mixed vegetables', 'vegetable broth', 'sushi rice', 'nori', 'fish (salmon/tuna)', 'cucumber', 'avocado', 'rice vinegar', 'wasabi', 'soy sauce', 'romaine lettuce', 'croutons', 'parmesan cheese', 'caesar dressing', 'anchovies', 'cream', 'basil', 'taco shells', 'lettuce', 'cheese', 'sour cream', 'taco seasoning', 'sesame oil', 'rice', 'pie crust', 'lemons', 'cornstarch', 'arborio rice', 'mushrooms', 'white wine', 'pork ribs', 'bbq sauce', 'brown sugar', 'paprika', 'garlic powder', 'onion powder', 'cucumbers', 'red onions', 'feta cheese', 'olives', 'olive oil', 'oregano', 'yogurt', 'tomato sauce', 'garam masala', 'bananas', 'baking soda', 'beef strips', 'egg noodles', 'fresh mozzarella', 'balsamic vinegar', 'beef/chicken', 'herbs', 'chili', 'star anise', 'ladyfingers', 'espresso', 'mascarpone cheese', 'chickpeas', 'cumin', 'coriander', 'corn tortillas', 'chicken/beef/cheese', 'enchilada sauce', 'red onion', 'beef', 'broccoli', 'red bell pepper', 'potatoes', 'rice paper wrappers', 'pork/shrimp/vegetables', 'vermicelli noodles', 'mint', 'eggplant', 'zucchini', 'bell peppers', 'assorted vegetables (peas, asparagus, broccoli)', 'sausage', 'shrimp', 'cajun seasoning', 'ground beef/turkey', 'kidney beans', 'black beans', 'chili powder', 'beans (black beans, pinto beans)', 'meat (chicken, steak, carnitas)', 'salsa', 'guacamole', 'bacon', 'hard-boiled egg', 'cashews', 'rice vinegar', 'chili paste', 'nutritional yeast', 'black pepper', 'vegetables (onion, bell pepper, spinach)', 'lentils', 'herbs (thyme, bay leaf)', 'salmon fillet', 'lemon slices', 'fresh herbs (dill, parsley)', 'pepper', 'quinoa', 'cherry tomatoes', 'chicken breast', 'breadcrumbs', 'mozzarella cheese', 'lasagna noodles', 'ricotta cheese', 'spinach', 'beef chuck', 'Guinness beer', 'dashi stock', 'miso paste', 'wakame seaweed', 'green onions', 'chicken thighs', 'pita bread', 'turmeric', 'basmati rice', 'biryani spices', 'saffron', 'white fish', 'tartar sauce', 'lemon wedges', 'cauliflower', 'blue cheese dressing', 'beef slices', 'pizza dough', 'tortillas', 'bell peppers', 'beef sirloin', 'green onions', 'tempura batter', 'dipping sauce', 'clams', 'heavy cream', 'phyllo dough', 'dill', 'beef tenderloin', 'mushroom duxelles', 'prosciutto', 'puff pastry', 'dijon mustard', 'maple syrup', 'almond milk' ]

def clean_ingredients(ingredient_list, allowed_ingredients):
    cleaned_ingredients = [ingredient.strip() for ingredient in ingredient_list.split(',') if ingredient.strip() in allowed_ingredients]
    return ', '.join(cleaned_ingredients)

recipe_df['ingredients'] = recipe_df['ingredients'].apply(clean_ingredients, allowed_ingredients=allowed_ingredients)


cleaned_file_path = 'cleaned_recipe.csv'
recipe_df.to_csv(cleaned_file_path, index=False)
