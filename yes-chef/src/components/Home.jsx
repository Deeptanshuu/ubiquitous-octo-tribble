import React, { useState } from 'react';
import { X, ChevronDown, ChevronUp, Search } from 'lucide-react';
import { Clock, Utensils } from 'lucide-react';
import VegToggle from './VegToggle';
import Loading from './Loading';

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [selectedCuisines, setSelectedCuisines] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedCravings, setSelectedCravings] = useState([]);
  const [expandedSections, setExpandedSections] = useState({
    ingredients: true,
    cuisines: true,
    courses: true,
    cravings: false,
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isVeg, setIsVeg] = useState(false);

  const handleVegToggle = (newState) => {
    setIsVeg(newState);
  };
  

  function removeEmojis(str) {
    return str.replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
              .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Symbols & Pictographs
              .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport & Map Symbols
              .replace(/[\u{1F700}-\u{1F77F}]/gu, '') // Alchemical Symbols
              .replace(/[\u{1F780}-\u{1F7FF}]/gu, '') // Geometric Shapes Extended
              .replace(/[\u{1F800}-\u{1F8FF}]/gu, '') // Supplemental Arrows-C
              .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols and Pictographs
              .replace(/[\u{1FA00}-\u{1FA6F}]/gu, '') // Chess Symbols
              .replace(/[\u{1FA70}-\u{1FAFF}]/gu, '') // Symbols and Pictographs Extended-A
              .replace(/[\u{1FB00}-\u{1FBFF}]/gu, '') // Symbols for Legacy Computing
              .replace(/[\u{1F1E6}-\u{1F1FF}]/gu, ''); // Flags
  }
  //hi this is a private repo now 

  const ingredients = [
    'flour 🌾', 'sugar 🍬', 'eggs 🥚', 'chocolate 🍫', 'butter 🧈', 'vanilla extract 🌼',
    'rice noodles 🍜', 'tofu 🍶', 'bean sprouts 🌱', 'peanuts 🥜', 'lime 🍋', 'fish sauce 🐟',
    'tamarind paste 🌰', 'garlic 🧄', 'shallots 🧅', 'chicken 🍗', 'onions 🧅', 'tomatoes 🍅',
    'coconut milk 🥥', 'curry paste 🍛', 'ginger 🍂', 'cilantro 🌿', 'cocoa powder 🍫', 'milk 🥛',
    'vegetable oil 🌻', 'baking powder 🥄', 'salt 🧂', 'ground beef 🥩', 'pasta 🍝', 'carrots 🥕',
    'celery 🌿', 'red wine 🍷', 'beef broth 🍲', 'noodles 🍜', 'thyme 🌿', 'parsley 🌿', 'apples 🍎',
    'cinnamon 🍂', 'nutmeg 🍂', 'lemon juice 🍋', 'mixed vegetables 🥗', 'vegetable broth 🥣',
    'sushi rice 🍚', 'nori 🍙', 'fish (salmon/tuna) 🐟', 'cucumber 🥒', 'avocado 🥑',
    'wasabi 🌶️', 'soy sauce 🍶', 'romaine lettuce 🥬', 'croutons 🥖', 'parmesan cheese 🧀', 'caesar dressing 🥗',
    'anchovies 🐟', 'cream 🥛', 'basil 🌿', 'taco shells 🌮', 'lettuce 🥬', 'cheese 🧀', 'sour cream 🍶',
    'taco seasoning 🌶️', 'sesame oil 🌻', 'rice 🍚', 'pie crust 🥧', 'lemons 🍋', 'cornstarch 🌽',
    'arborio rice 🍚', 'mushrooms 🍄', 'white wine 🍷', 'pork ribs 🍖', 'bbq sauce 🍖', 'brown sugar 🍬',
    'paprika 🌶️', 'garlic powder 🧄', 'onion powder 🧅', 'cucumbers 🥒', 'red onions 🧅', 'feta cheese 🧀',
    'olives 🫒', 'olive oil 🌿', 'oregano 🌿', 'yogurt 🥛', 'tomato sauce 🍅', 'garam masala 🌶️', 'bananas 🍌',
    'baking soda 🥄', 'beef strips 🥩', 'egg noodles 🍜', 'fresh mozzarella 🧀', 'balsamic vinegar 🍶',
    'beef/chicken 🥩🍗', 'herbs 🌿', 'chili 🌶️', 'star anise 🌟', 'ladyfingers 🍰', 'espresso ☕', 'mascarpone cheese 🧀',
    'chickpeas 🌱', 'cumin 🌿', 'coriander 🌿', 'corn tortillas 🌽', 'chicken/beef/cheese 🍗🥩🧀', 'enchilada sauce 🌶️',
    'red onion 🧅', 'beef 🥩', 'broccoli 🥦', 'red bell pepper 🌶️', 'potatoes 🥔', 'rice paper wrappers 🍚',
    'pork/shrimp/vegetables 🍖🍤🥗', 'vermicelli noodles 🍜', 'mint 🌿', 'eggplant 🍆', 'zucchini 🥒', 
    'assorted vegetables 🥗', 'sausage 🌭', 'shrimp 🍤', 'cajun seasoning 🌶️', 'ground beef/turkey 🥩🦃',
    'kidney beans 🌱', 'black beans 🌱', 'chili powder 🌶️', 'beans (black beans, pinto beans) 🌱',
    'meat (chicken, steak, carnitas) 🍗🥩', 'salsa 🌶️', 'guacamole 🥑', 'bacon 🥓', 'hard-boiled egg 🥚', 'cashews 🥜',
    'rice vinegar 🍚', 'chili paste 🌶️', 'nutritional yeast 🌾', 'black pepper 🌶️', 'vegetables (onion, bell pepper, spinach) 🧅🌶️🌿',
    'lentils 🌱', 'herbs (thyme, bay leaf) 🌿', 'salmon fillet 🐟', 'lemon slices 🍋', 'fresh herbs (dill, parsley) 🌿',
    'pepper 🌶️', 'quinoa 🍚', 'cherry tomatoes 🍅', 'chicken breast 🍗', 'breadcrumbs 🥖', 'mozzarella cheese 🧀',
    'lasagna noodles 🍜', 'ricotta cheese 🧀', 'spinach 🌿', 'beef chuck 🥩', 'Guinness beer 🍺', 'dashi stock 🍲',
    'miso paste 🍲', 'wakame seaweed 🌿', 'chicken thighs 🍗', 'pita bread 🥖', 'turmeric 🌿',
    'basmati rice 🍚', 'biryani spices 🌿', 'saffron 🌼', 'white fish 🐟', 'tartar sauce 🐟', 'lemon wedges 🍋',
    'cauliflower 🥦', 'blue cheese dressing 🥗', 'beef slices 🥩', 'pizza dough 🍕', 'tortillas 🌮', 'bell peppers 🌶️',
    'beef sirloin 🥩', 'green onions 🧅', 'tempura batter 🍤', 'dipping sauce 🥣', 'clams 🐚', 'heavy cream 🥛',
    'phyllo dough 🥐', 'dill 🌿', 'beef tenderloin 🥩', 'mushroom duxelles 🍄', 'prosciutto 🥓', 'puff pastry 🥐',
    'dijon mustard 🌶️', 'maple syrup 🍁', 'almond milk 🥛'
  ];


  const cuisines = [
    'American 🍔', 'Thai 🇹🇭', 'Indian 🇮🇳', 'International 🌎', 'Italian 🍝', 'Japanese 🍣',
    'Mexican 🌮', 'Asian 🥢', 'Greek 🇬🇷', 'Russian 🇷🇺', 'Vietnamese 🇻🇳', 'Middle Eastern 🥙',
    'French 🇫🇷', 'Vegan 🌱', 'Mediterranean 🌊', 'Italian-American 🍕', 'Irish 🇮🇪',
    'British 🇬🇧', 'Korean 🇰🇷'
  ];


  const courses = [
    'Dessert 🍰', 'Main Course 🍽️', 'Breakfast 🍳', 'Soup 🍜', 'Appetizer 🥟', 'Salad 🥗', 'Side Dish 🍲'
  ];


  const cravings = ['Sweet🍦', 'Savory😋', 'Spicy🌶️'];


  const toggleSection = (section) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const handleIngredientToggle = (ingredient) => {
    setSelectedIngredients(prev =>
      prev.includes(ingredient)
        ? prev.filter(i => i !== ingredient)
        : [...prev, ingredient]
    );
  };

  const handleCuisineChange = (cuisine) => {
    setSelectedCuisines(prev =>
      prev.includes(cuisine)
        ? prev.filter(c => c !== cuisine)
        : [...prev, cuisine]
    );
  };

  const handleCourseChange = (course) => {
    setSelectedCourse(course); // Directly set the selected course
  };

  const handleCravingChange = (craving) => {
    setSelectedCravings(prev =>
      prev.includes(craving)
        ? prev.filter(c => c !== craving)
        : [...prev, craving]
    );
  };

  const filteredIngredients = ingredients.filter(ingredient =>
    ingredient.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const cleanedIngredients = selectedIngredients.map(removeEmojis);
  const cleanedCuisines = selectedCuisines.map(removeEmojis);
  const cleanedCourses = removeEmojis(selectedCourse);
  const cleanedCravings = selectedCravings.map(removeEmojis);

  const handleClick = (id) => {
    window.open('/recpie?id=' + id);
 
  }
  const handleSubmit = async () => {
    const cleanedIngredients = selectedIngredients.map(removeEmojis);
    const cleanedCravings = selectedCravings.map(removeEmojis);
    const cleanedCuisine = selectedCuisines.map(removeEmojis);
    const cleanedCourse = removeEmojis(selectedCourse);

    console.log(cleanedIngredients);
    console.log(cleanedCuisines);
    console.log(cleanedCourses);
    console.log(cleanedCravings);

    const data = {
      ingredients: cleanedIngredients,
      craving: cleanedCravings,
      cuisine: cleanedCuisine,
      course: cleanedCourse,
      veg: isVeg
    };

    try {
      setLoading(true);
      const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      
      setTimeout(() => {
              setSearchResults(result);
              setLoading(false);
      }, 1000);

      console.log('Success:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const clearAllFilters = () => {
    setSelectedIngredients([]);
    setSelectedCuisines([]);
    setSelectedCourse('');
    setSelectedCravings([]);
    setSearchTerm('');
    setIsVeg(false);
    setSearchResults([]);
  };

/*  const exampleRecipes = [
    {
      title: "Spaghetti Carbonara",
      description: "A classic Italian pasta dish with eggs, cheese, and pancetta",
      cookTime: 30,
      servings: 4,
      difficulty: "Medium",
      image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80"
    }
  ];
*/
  function RecipeCard({ id, title, description, cookTime, servings, difficulty, image, veg }) {
    return (
      <div className="w-full h-full m-auto bg-white border-2 border-slate-600 shadow-xl shadow-stone-400 rounded-lg flex flex-col">
        <div className="">
          <img
            src={image}
            alt="Recipe"
            className="w-full h-[250px] object-cover  rounded-tr-lg rounded-tl-lg rounded-b-none border-slate-800 mb-5" />
        </div>
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">{title}</h2>
          <p className="text-gray-600 mb-4">{description}</p>
        </div>
        <div className="px-4 flex-grow">
        {veg ? <p className="px-3 py-1 w-16 my-2 text-center text-m rounded-full font-semibold bg-green-300 text-green-800">Veg</p> : <p className="px-3 py-1 w-24 my-2 text-center rounded-full font-semibold bg-red-300 text-red-800">Non-Veg</p>}
          <div className="flex items-center mb-2">
            <Clock className="mr-2 text-gray-500" size={24} />
            <span className="text-sm text-gray-700">{cookTime}</span>
          </div>
          <div className="flex items-center mb-2">
            <Utensils className="mr-2 text-gray-500" size={24} />
            <span className="text-sm text-gray-700">{servings}</span>
          </div>
        </div>
        <div className="p-4 flex justify-between items-center border-t-2 border-gray-400">
          <span className={`px-2 py-1 text-s font-semibold rounded-full 
          ${difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
              difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'}`}>
            {difficulty}
          </span>
          <button type="button" class="w-1/2 bg-gray-800 text-white text-s py-3 px-4 rounded-full text-lg font-semibold hover:bg-gray-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50"
            onClick={() => handleClick(id)}>See Recipe</button>
        </div>
      </div>
    );
  }


  return (
    <>
      <div className="home flex flex-row bg-white">
        <div className="search-menu w-1/3 min-h-screen border-r-2 border-gray-600 shadow-xl shadow-gray-600 flex flex-col p-5 bg-white ">
          
          <h2 className="text-3xl p-1 font-bold mb-3 text-gray-800">What's for Dinner ?</h2>

          <div className="flex flex-row justify-start p-3">
              <p className='text-base font-semibold mx-2 mb-2 px-3 py-1 rounded-full bg-green-300 text-green-700'>Veg Mode</p>
              <div className='p-1'>
                <VegToggle initialState={isVeg} onChange={handleVegToggle}/>
              </div>
          </div>
          
          {/* Ingredients Section */}
          <div className="mb-8">
            <button
              className="flex items-center justify-between w-full p-3 bg-gray-300 rounded-lg text-lg font-semibold text-white-700 hover:bg-gray-200 transition duration-200"
              onClick={() => toggleSection('ingredients')}
            >
              <span>Ingredients</span>
              {expandedSections.ingredients ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </button>
            {expandedSections.ingredients && (
              <div className="mt-4">
                <div className="relative mb-4">
                  <input
                    type="text"
                    placeholder="Search ingredients..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full p-2 pl-10 pr-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
                </div>
                <div className="flex p-5 max-h-80 overflow-auto flex-wrap gap-2">
                  {filteredIngredients
                    .sort((a, b) => {
                      const aSelected = selectedIngredients.includes(a);
                      const bSelected = selectedIngredients.includes(b);
                      if (aSelected && !bSelected) return -1;
                      if (!aSelected && bSelected) return 1;
                      return 0;
                    })
                    .map(ingredient => (
                      <button
                        key={ingredient}
                        onClick={() => handleIngredientToggle(ingredient)}
                        className={`px-3 py-1 border-2 border-slate-500 rounded-full text-m font-medium transition duration-200 ${selectedIngredients.includes(ingredient)
                          ? 'bg-stone-700 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                          }`}
                      >
                        {ingredient}
                        {selectedIngredients.includes(ingredient) && (
                          <X size={14} className="inline-block ml-1" />
                        )}
                      </button>
                    ))}
                </div>
              </div>
            )}
          </div>

          {/* Cuisines Section */}
          <div className="mb-8">
            <button
              className="flex items-center justify-between w-full p-3 bg-gray-300 rounded-lg text-lg font-semibold text-white-700 hover:bg-gray-200 transition duration-200"
              onClick={() => toggleSection('cuisines')}
            >
              <span>Cuisines</span>
              {expandedSections.cuisines ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </button>
            {expandedSections.cuisines && (
              <div className="flex p-3 overflow-auto flex-wrap gap-2">
                {cuisines.map(cuisines => (
                  <button
                    key={cuisines}
                    onClick={() => handleCuisineChange(cuisines)}
                    className={`px-3 py-1 border-2 border-slate-500 rounded-full text-m font-medium transition duration-200 ${selectedCuisines.includes(cuisines)
                        ? 'bg-stone-700 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                  >
                    {cuisines}
                    {selectedCuisines.includes(cuisines) && (
                      <X size={14} className="inline-block ml-1" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Courses Section */}
          <div className="mb-8">
            <button
              className="flex items-center justify-between w-full p-3 bg-gray-300 rounded-lg text-lg font-semibold text-white-700 hover:bg-gray-200 transition duration-200"
              onClick={() => toggleSection('courses')}
            >
              <span>Courses</span>
              {expandedSections.courses ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </button>
            {expandedSections.courses && (
              <div className="mt-4 p-5 grid grid-cols-2 md:grid-cols-3 gap-2">
                {courses.map(course => (
                  <label key={course} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="radio"
                      name="course" // Add a name attribute to group radio buttons
                      checked={selectedCourse === course}
                      onChange={() => handleCourseChange(course)}
                      className={`form-radio h-5 w-5 text-blue-500 focus:ring-blue-400 `}
                    />
                    <span className="text-gray-700">{course}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          {/* Cravings Section */}
          <div className="mb-8">
            <button
              className="flex items-center justify-between w-full p-3 bg-gray-300 rounded-lg text-lg font-semibold text-white-700 hover:bg-gray-200 transition duration-200"
              onClick={() => toggleSection('cravings')}
            >
              <span>Cravings</span>
              {expandedSections.cravings ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </button>
            {expandedSections.cravings && (
              <div className="mt-4 p-5 flex gap-4">
                {cravings.map(craving => (
                  <label key={craving} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedCravings.includes(craving)}
                      onChange={() => handleCravingChange(craving)}
                      className="form-checkbox h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                    />
                    <span className="text-gray-700">{craving}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <div className='flex justify-between'>
          <button className="w-1/2 bg-gray-800 text-white py-3 px-4 rounded-full text-lg font-semibold hover:bg-gray-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50" onClick={handleSubmit}>
            Find Recipes
          </button>
          <button 
              className="w-1/3 bg-red-300 text-red-800 py-3 px-4 rounded-full text-lg font-semibold hover:bg-red-500 transition duration-200 border
              border-red-800 focus:ring-red-400"
              onClick={clearAllFilters}
            >
              Clear Filters ❌
          </button>

          </div>
        </div>

        <div className="result w-2/3 overflow-x-scroll p-5 bg-white-200">
          <div className="grid grid-cols-3 gap-7">
            {searchResults.length === 0 && loading === false ? (
              <h1 className="text-4xl w-full px-3 py-64 font-bold text-center mb-6">
                👈 Use the filters to get started
              </h1>
            ) : (
              <>
                {loading === true ? (
                  <div className="flex flex-row items-center justify-center w-[80em] h-screen">
                    <Loading/>
                  </div>
                ) : (
                  <>
                    <h1 className="text-4xl font-bold mb-6 border-b border-slate-800 pb-4 col-span-3">
                      Our Top Results 👇
                    </h1>
                    {searchResults.map((recipe) => (
                      <RecipeCard
                        key={recipe.id}
                        id={recipe.id}
                        title={recipe.title}
                        description={recipe.description}
                        cookTime={recipe.cooking_time}
                        servings={recipe.servings}
                        difficulty={recipe.difficulty}
                        image={recipe.image}
                        veg={recipe.veg}
                      />
                    ))}
                  </>
                )}
              </>
            )}
          </div>
        </div>

      </div>
    </>
  );
};

export default Home;