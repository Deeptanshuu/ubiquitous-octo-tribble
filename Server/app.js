const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const pandas = require('pandas-js'); // or use a similar library or direct CSV parsing
const fetch = require('node-fetch'); // To read CSVs from file
const port = 5000;
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Load your dataset (This is a basic example; adapt as needed)
let recipes_data;
fetch('7k-dataset.csv')
  .then(res => res.text())
  .then(data => {
    recipes_data = pandas.read_csv(data);
    // Clean column names
    recipes_data.columns = recipes_data.columns.map(col => col.trim());
  });

// Define weights for user preferences
const cuisine_weight = 0.2;
const course_weight = 0.3;

// Helper functions
function calculateDifficulty(prep_time, cooking_time) {
  const total_time = parseFloat(prep_time) + parseFloat(cooking_time);
  if (total_time < 30) {
    return 'Easy';
  } else if (total_time < 60) {
    return 'Medium';
  } else {
    return 'Hard';
  }
}

function calculateServings(prep_time, cooking_time) {
  const total_time = parseFloat(prep_time) + parseFloat(cooking_time);
  if (total_time < 30) {
    return '1 - 2 Servings';
  } else if (total_time < 60) {
    return '4 - 6 Servings';
  } else {
    return '6+ Servings';
  }
}

function calculateWeightedSimilarity(similarity, recipe, user_cuisine, user_course) {
  let user_pref_similarity = 0;
  if (user_cuisine && recipe.cuisine && user_cuisine === recipe.cuisine) {
    user_pref_similarity += cuisine_weight;
  }
  if (user_course && recipe.course && user_course.trim().toLowerCase() === recipe.course.trim().toLowerCase()) {
    user_pref_similarity += course_weight;
  }
  return similarity * (1 - (cuisine_weight + course_weight)) + user_pref_similarity;
}

// Define routes
app.post('/api/recommend', (req, res) => {
  const { ingredients, cuisine, course, veg } = req.body;

  // Filter vegetarian recipes if requested
  let filtered_recipes = recipes_data;
  if (veg) {
    filtered_recipes = filtered_recipes.filter(recipe => recipe.diet.trim().toLowerCase() === 'vegetarian');
  }

  // TODO: Implement vectorization and cosine similarity in JavaScript

  // Send response
  res.json([]);  // Adjust with actual recommendations
});

app.post('/api/recipe', (req, res) => {
  const name = req.body.name.trim().toLowerCase();
  const recipe_list = recipes_data.filter(recipe => recipe.name.trim().toLowerCase() === name);

  if (recipe_list.length === 0) {
    return res.status(404).json({ error: 'Recipe not found' });
  }

  const recipe = recipe_list[0];
  const response = {
    name: recipe.name,
    description: recipe.description,
    veg: recipe.diet.trim().toLowerCase() === 'vegetarian',
    image: recipe.image_url,
    cooking_time: `${recipe.prep_time} + ${recipe.cook_time} mins`,
    serving_size: calculateServings(recipe.prep_time, recipe.cook_time),
    difficulty: calculateDifficulty(recipe.prep_time, recipe.cook_time),
    course: recipe.course,
    cooking_ingredients: recipe.ingredients_name,
    cooking_instruction: recipe.instructions
  };

  res.json(response);
});

// Start the server
app.listen(port, () => {
  console.log('Express server running on port {$port}');
});
