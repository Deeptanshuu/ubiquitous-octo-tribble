import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Clock, Users, ChefHat, Utensils } from 'lucide-react';

const Recipe = () => {
  const location = useLocation();
  const [recipeId, setRecipeId] = useState(null);
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    if (id) {
      setRecipeId(id);
      fetchRecipe(id);
    }
  }, [location]);

  const fetchRecipe = async (id) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/recpie`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
      });
      if (!response.ok) {
        throw new Error('Failed to fetch recipe');
      }

      const data = await response.json();
      setRecipe(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center mt-8">Loading...</div>;
  if (error) return <div className="text-center mt-8 text-red-500">Error: {error}</div>;
  if (!recipe) return <div className="text-center mt-8">No recipe data available</div>;
  const formatRecipeText = (text) => {
    if (!text) return null;
    
    // Split text by line breaks
    const lines = text.split('\n');
    
    // Format each line as a paragraph or list item
    return lines.map((line, index) => {
      if (line.startsWith('- ')) {
        return <li key={index}>{line.substring(2)}</li>; // Remove the leading "- "
      } else {
        return <p key={index}>{line}</p>;
      }
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg">
      <h1 className="text-3xl font-bold mb-4 text-dark-600">{recipe.name}</h1>
      <p className="text-gray-600 mb-6">{recipe.description}</p>
      {recipe.veg ? <p className="px-3 py-1 w-20 my-2 text-center rounded-full font-semibold bg-green-300 text-green-800">Veg</p> : <p className="px-3 py-1 w-24 my-2 text-center rounded-full font-semibold bg-red-300 text-red-800">Non-Veg</p>}

      <img src={recipe.image} alt={recipe.name} className="w-full h-96 object-cover rounded-lg mb-6" />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        
        <div className="flex items-center">
          <Clock className="w-5 h-5 mr-2 text-dark-600" />
          <span>{recipe.cooking_time}</span>
        </div>
        <div className="flex items-center">
          <Users className="w-5 h-5 mr-2 text-dark-600" />
          <span>{recipe.serving_size}</span>
        </div>
        <div className="flex items-center">
          <ChefHat className="w-5 h-5 mr-2 text-dark-600" />
          <span>{recipe.difficulty}</span>
        </div>
        <div className="flex items-center">
          <Utensils className="w-5 h-5 mr-2 text-dark-600" />
          <span>{recipe.course}</span>
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-3 text-dark-600">Ingredients</h2>
        <ul>{formatRecipeText(recipe.cooking_ingredients)}</ul>
      </div>

      <div>
        <h2 className="text-2xl font-semibold mb-3 text-dark-600">Instructions</h2>
        <div>{formatRecipeText(recipe.cooking_instruction)}</div>
      </div>
    </div>
  );
};

export default Recipe;
