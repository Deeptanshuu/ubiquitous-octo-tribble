const express = require('express');
const app = express();
const port = 3000;
const csv = require('csv-parser');
const fs = require('fs');

app.use(express.json());

const recipes = [];

// Load recipes from CSV file
fs.createReadStream('./7k-dataset-with-vectors.csv')
  .pipe(csv())
  .on('data', (row) => {
    recipes.push(row);
  })
  .on('end', () => {
    console.log('CSV file successfully processed');
  });

app.post('/api/recommend', (req, res) => {
  const userIngredients = req.body.ingredients; // Array of user ingredients

  if (!userIngredients || !Array.isArray(userIngredients)) {
    return res.status(400).json({ error: 'Invalid input' });
  }

  // Get recipe recommendations
  const recommendations = recipes.map(recipe => {
    const recipeIngredients = recipe.ingredients_list.split(',').map(ingredient => ingredient.trim());
    const commonIngredients = userIngredients.filter(ingredient => recipeIngredients.includes(ingredient)).length;
    return {
      name: recipe.name,
      description: recipe.description,
      commonIngredients,
    };
  });

  // Filter recipes to include only those with more than one common ingredient
  const filteredRecommendations = recommendations.filter(recipe => recipe.commonIngredients > 1);

  // Sort filtered recipes by the number of common ingredients in descending order
  filteredRecommendations.sort((a, b) => b.commonIngredients - a.commonIngredients);

  res.json(filteredRecommendations);
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
