/* eslint-disable react/no-unescaped-entities */
/* eslint-disable react/prop-types */
import  { useState, useEffect } from 'react';
import { X, ChevronDown, ChevronUp, Search, Menu } from 'lucide-react';
import { Clock, Utensils } from 'lucide-react';
import VegToggle from './VegToggle';
import Loading from './Loading';
import AIToggle from './AIToggle';

const Home = () => {
  const [loading, setLoading] = useState(false);
  //const [error, setError] = useState(null);
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
  const placeholderImage = 'https://via.placeholder.com/300x200.png?text=Placeholder+Image';
  const [customIngredients, setCustomIngredients] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [displayedIngredients, setDisplayedIngredients] = useState([]);
  const [isAI, setIsAI] = useState(true);
  const [executionTime, setExecutionTime] = useState(null);
  const [previousExecutionTime, setPreviousExecutionTime] = useState(null);
  const [previousMethod, setPreviousMethod] = useState(null);
  const [lastUsedMethod, setLastUsedMethod] = useState('AI Magic 🪄');
  const [isMenuVisible, setIsMenuVisible] = useState(false); // Start with the menu hidden on small screens

  const handleVegToggle = (newState) => {
    setIsVeg(newState);
  };
  

  function removeEmojis(str) {
    if (typeof str !== 'string') {
      return str;
    }
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

  useEffect(() => {
    const ingredientsWithIds = [
      'flour 🌾', 'sugar 🍬', 'eggs 🥚', 'chocolate 🍫', 'butter 🧈', 'vanilla extract 🌼',
      'rice noodles 🍜', 'tofu 🍶', 'bean sprouts 🌱', 'peanuts 🥜', 'lime 🍋', 'fish sauce 🐟',
      'tamarind paste 🌰', 'garlic 🧄', 'shallots 🧅', 'onions 🧅', 'tomatoes 🍅',
      'coconut milk 🥥', 'curry paste 🍛', 'ginger 🍂', 'cilantro 🌿', 'cocoa powder 🍫', 'milk 🥛',
      'vegetable oil 🌻', 'baking powder 🥄', 'salt 🧂',  'pasta 🍝', 'carrots 🥕',
      'celery 🌿', 'red wine 🍷' ,'noodles 🍜', 'thyme 🌿', 'parsley 🌿', 'apples 🍎',
      'cinnamon 🍂', 'nutmeg 🍂', 'lemon juice 🍋', 'mixed vegetables 🥗', 'vegetable broth 🥣',
      'sushi rice 🍚', 'nori 🍙', 'fish (salmon/tuna) 🐟', 'cucumber 🥒', 'avocado 🥑',
      'wasabi 🌶️', 'soy sauce 🍶', 'romaine lettuce 🥬', 'croutons 🥖', 'parmesan cheese 🧀', 'caesar dressing 🥗',
      'anchovies 🐟', 'cream 🥛', 'basil 🌿', 'taco shells 🌮', 'lettuce 🥬', 'cheese 🧀', 'sour cream 🍶',
      'taco seasoning 🌶️', 'sesame oil 🌻', 'rice 🍚', 'pie crust 🥧', 'lemons 🍋', 'cornstarch 🌽',
      'arborio rice 🍚', 'mushrooms 🍄', 'white wine 🍷', 'pork ribs 🍖', 'bbq sauce 🍖', 'brown sugar 🍬',
      'paprika 🌶️', 'garlic powder 🧄', 'onion powder 🧅', 'cucumbers 🥒', 'red onions 🧅', 'feta cheese 🧀',
      'olives 🫒', 'olive oil 🌿', 'oregano 🌿', 'yogurt 🥛', 'tomato sauce 🍅', 'garam masala 🌶️', 'bananas 🍌',
      'baking soda 🥄', 'egg noodles ', 'fresh mozzarella 🧀', 'balsamic vinegar 🍶',
      'chicken 🍗', 'herbs 🌿', 'chili 🌶️', 'star anise 🌟', 'ladyfingers 🍰', 'espresso ☕', 'mascarpone cheese 🧀',
      'chickpeas 🌱', 'cumin 🌿', 'coriander 🌿', 'corn tortillas 🌽', 'cheese 🧀', 'enchilada sauce 🌶️',
      'red onion 🧅', 'soya sauce 🍶', 'broccoli 🥦', 'red bell pepper 🌶️', 'potatoes 🥔', 'rice paper wrappers 🍚',
      'pork/shrimp/vegetables 🍖🍤🥗', 'vermicelli noodles 🍜', 'mint 🌿', 'eggplant 🍆', 'zucchini 🥒', 
      'assorted vegetables 🥗', 'sausage 🌭', 'shrimp 🍤', 'cajun seasoning 🌶️', 
      'kidney beans 🌱', 'black beans 🌱', 'chili powder 🌶️', 'beans 🌱',
      'meat (chicken, steak, carnitas) 🍗🥩', 'salsa 🌶️', 'guacamole 🥑', 'bacon 🥓', 'hard-boiled egg 🥚', 'cashews 🥜',
      'rice vinegar 🍚', 'chili paste 🌶️', 'nutritional yeast 🌾', 'black pepper 🌶️', 'vegetables (onion, bell pepper, spinach) 🧅🌶️🌿',
      'lentils 🌱', 'herbs (thyme, bay leaf) 🌿', 'salmon fillet 🐟', 'lemon slices 🍋', 'fresh herbs (dill, parsley) 🌿',
      'pepper 🌶️', 'quinoa 🍚', 'cherry tomatoes 🍅', 'chicken breast 🍗', 'breadcrumbs 🥖', 'mozzarella cheese 🧀',
      'lasagna noodles 🍜', 'ricotta cheese 🧀', 'spinach 🌿', 'chicken chuck 🥩', 'Guinness beer 🍺', 'dashi stock 🍲',
      'miso paste 🍲', 'wakame seaweed 🌿', 'chicken thighs 🍗', 'pita bread 🥖', 'turmeric 🌿',
      'basmati rice 🍚', 'biryani spices 🌿', 'saffron 🌼', 'white fish 🐟', 'tartar sauce 🐟', 'lemon wedges 🍋',
      'cauliflower 🥦', 'blue cheese dressing 🥗', 'chicken slices 🥩', 'pizza dough 🍕', 'tortillas 🌮', 'bell peppers 🌶️',
     'green onions 🧅', 'tempura batter 🍤', 'dipping sauce 🥣', 'clams 🐚', 'heavy cream 🥛',
      'phyllo dough 🥐', 'dill 🌿', 'mushroom duxelles 🍄', 'prosciutto 🥓', 'puff pastry 🥐',
      'dijon mustard 🌶️', 'maple syrup 🍁', 'almond milk 🥛'
    ].map((ing, index) => ({ id: `ing_${index}`, name: ing }));
    setIngredients(ingredientsWithIds);
    setDisplayedIngredients(ingredientsWithIds);
  }, []);

  const handleSearchChange = (e) => {
    const term = e.target.value;
    setSearchTerm(term);
    updateDisplayedIngredients(term);
  };

  const updateDisplayedIngredients = (term) => {
    if (term) {
      setDisplayedIngredients(ingredients.filter(ing => 
        ing.name.toLowerCase().includes(term.toLowerCase())
      ));
    } else {
      setDisplayedIngredients(ingredients);
    }
  };

  const selectIngredient = (ingredient) => {
    if (!selectedIngredients.find(sel => sel.id === ingredient.id)) {
      setSelectedIngredients([...selectedIngredients, ingredient]);
    }
    setSearchTerm("");
    updateDisplayedIngredients("");
  };

  const deselectIngredient = (ingredient) => {
    setSelectedIngredients(selectedIngredients.filter(sel => sel.id !== ingredient.id));
  };

  const handleAddCustomIngredient = () => {
    if (searchTerm && !ingredients.find(ing => ing.name.toLowerCase() === searchTerm.toLowerCase()) && !customIngredients.includes(searchTerm)) {
      setCustomIngredients([...customIngredients, searchTerm]);
      setSearchTerm("");
      updateDisplayedIngredients("");
    }
  };

  const removeCustomIngredient = (ingredient) => {
    setCustomIngredients(customIngredients.filter(ing => ing !== ingredient));
  };

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

  const handleAIToggle = (newState) => {
    setIsAI(newState);
  };

  //const cleanedIngredients = selectedIngredients.map(removeEmojis);
  const cleanedCuisines = selectedCuisines.map(removeEmojis);
  const cleanedCourses = removeEmojis(selectedCourse);
  //const cleanedCravings = selectedCravings.map(removeEmojis);

  const handleClick = (name) => {
    window.open('/recpie?name=' + name);
 
  }
  const handleSubmit = async () => {
    const cleanedIngredients = [...selectedIngredients.map(ing => removeEmojis(ing.name)), ...customIngredients];
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
      const endpoint = isAI ? '/api/recommend-ai' : '/api/recommend-brute-force';
      const currentMethod = isAI ? 'AI Magic 🪄' : 'Brute Force 🔨';
      const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      
      setTimeout(() => {
        setSearchResults(result.recommendations);
        setPreviousExecutionTime(executionTime);
        setPreviousMethod(lastUsedMethod);
        setExecutionTime(result.execution_time);
        setLastUsedMethod(currentMethod);
        // Remove this line: setCached(result.cached);
        setLoading(false);
      }, 100);

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
    setCustomIngredients([]);
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
  function RecipeCard({ title, description, cookTime, servings, difficulty, image, veg }) {
    return (
      <div className="w-full h-full m-auto bg-white border-2 border-slate-600 shadow-xl shadow-stone-400 rounded-lg flex flex-col">
        <div className="">
          <img
            src={image || placeholderImage}
            alt={placeholderImage}
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
            <span className="text-sm text-gray-700">{cookTime} minutes</span>
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
          <button type="button" className="w-1/2 bg-gray-800 text-white text-s py-3 px-4 rounded-full text-lg font-semibold hover:bg-gray-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50"
            onClick={() => handleClick(title)}>See Recipe</button>
        </div>
      </div>
    );
  }

  const toggleMenu = () => {
    setIsMenuVisible(!isMenuVisible);
  };

  useEffect(() => {
    const handleResize = () => {
      // Show the menu if the screen width is greater than or equal to 768px
      setIsMenuVisible(window.innerWidth >= 1000);
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Call it initially to set the correct state
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <>
      <div className="home flex flex-col md:flex-row bg-white relative">
        {/* Menu toggle button */}
        <button
          className="fixed top-6 left-4 z-50 bg-gray-800 text-white p-2 rounded-full shadow-lg"
          onClick={toggleMenu}
        >
          <Menu size={24} />
        </button>

    {/* Search menu */}
    <div
      className={`search-menu ${
        isMenuVisible ? 'w-full md:w-1/3' : 'w-0'
      } h-screen md:h-auto overflow-y-auto border-r-2 border-gray-600 shadow-xl shadow-gray-600 flex flex-col p-5 bg-white transition-all duration-300 ease-in-out fixed md:static top-0 left-0 z-40 ${
        isMenuVisible ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
          <button
            className="md:hidden absolute top-4 right-4 text-gray-600"
            onClick={toggleMenu}
          >
            <X size={24} />
          </button>

          <h2 className="text-3xl p-1 pl-10 font-bold mb-3 text-gray-800">What's for Dinner?</h2>

          <div className="flex flex-row justify-between p-3">
            <div className="flex items-center">
              <p className='text-base font-semibold mx-2 mb-2 px-3 py-1 rounded-full bg-green-300 text-green-700'>Veg Mode</p>
              <div className='p-1'>
                <VegToggle initialState={isVeg} onChange={handleVegToggle}/>
              </div>
            </div>
            <div className="flex items-center">
              <AIToggle initialState={isAI} onChange={handleAIToggle} />
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
                    onChange={handleSearchChange}
                    className="w-full p-2 pl-10 pr-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
                  {searchTerm && !ingredients.find(ing => ing.name.toLowerCase() === searchTerm.toLowerCase()) && !customIngredients.includes(searchTerm) && (
                    <button
                      onClick={handleAddCustomIngredient}
                      className="absolute right-2 top-2 px-2 py-1 bg-blue-500 text-white rounded-full text-sm"
                    >
                      Add
                    </button>
                  )}
                </div>
                <div className="flex p-5 max-h-80 overflow-auto flex-wrap gap-2">
                  {displayedIngredients
                    .sort((a, b) => {
                      const aSelected = selectedIngredients.some(sel => sel.id === a.id);
                      const bSelected = selectedIngredients.some(sel => sel.id === b.id);
                      if (aSelected && !bSelected) return -1;
                      if (!aSelected && bSelected) return 1;
                      return 0;
                    })
                    .map(ingredient => (
                      <button
                        key={ingredient.id}
                        onClick={() => selectedIngredients.find(sel => sel.id === ingredient.id) ? deselectIngredient(ingredient) : selectIngredient(ingredient)}
                        className={`px-3 py-1 border-2 border-slate-500 rounded-full text-m font-medium transition duration-200 ${
                          selectedIngredients.find(sel => sel.id === ingredient.id)
                            ? 'bg-stone-700 text-white'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {ingredient.name}
                        {selectedIngredients.find(sel => sel.id === ingredient.id) && (
                          <X size={14} className="inline-block ml-1" />
                        )}
                      </button>
                    ))}
                </div>
                {customIngredients.length > 0 && (
                  <div className="mt-4 px-5">
                    <h3 className="font-semibold mb-2 text-gray-700">Custom Ingredients:</h3>
                    <div className="flex flex-wrap gap-2">
                      {customIngredients.map((ingredient, index) => (
                        <button
                          key={index}
                          onClick={() => removeCustomIngredient(ingredient)}
                          className="px-3 py-1 border-2 border-blue-500 rounded-full text-sm font-medium bg-blue-100 text-blue-700 hover:bg-blue-200 transition duration-200 flex items-center"
                        >
                          {ingredient}
                          <X size={14} className="ml-1" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}
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

        <div className={`result ${isMenuVisible ? 'w-2/3' : 'w-screen'} transition-all duration-300 ease-in-out overflow-x-auto p-5 bg-white-200`}>
          <div className="md:grid md:grid-cols-3 md:gap-7 flex flex-col gap-10">
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
                    <h1 className="text-4xl font-bold mb-2 border-b border-slate-800 pb-4 col-span-3">
                      Our Top Results 👇
                    </h1>
                    <div className="bg-gray-100 rounded-lg p-3 mb-1 m-0 col-span-3">
                      <h2 className="text-lg font-semibold text-gray-700">Selected Filters:</h2>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {selectedIngredients.length > 0 && (
                          <div className="flex items-center bg-blue-200 text-blue-800 px-2 py-1 rounded-full">
                            <span>Ingredients:</span>
                            {selectedIngredients.map(ing => (
                              <span key={ing.id} className="ml-1">{ing.name}</span>
                            ))}
                          </div>
                        )}
                        {selectedCuisines.length > 0 && (
                          <div className="flex items-center bg-green-200 text-green-800 px-2 py-1 rounded-full">
                            <span>Cuisines:</span>
                            {selectedCuisines.map(cuisine => (
                              <span key={cuisine} className="ml-1">{cuisine}</span>
                            ))}
                          </div>
                        )}
                        {selectedCourse && (
                          <div className="flex items-center bg-yellow-200 text-yellow-800 px-2 py-1 rounded-full">
                            <span>Course:</span>
                            <span className="ml-1">{selectedCourse}</span>
                          </div>
                        )}
                        {selectedCravings.length > 0 && (
                          <div className="flex items-center bg-red-200 text-red-800 px-2 py-1 rounded-full">
                            <span>Cravings:</span>
                            {selectedCravings.map(craving => (
                              <span key={craving} className="ml-1">{craving}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                    {executionTime !== null && (
                      <div className="bg-gray-100 rounded-lg p-3 mb-4 col-span-3 flex items-center justify-between">
                        <div>
                          <p className="text-sm font-semibold text-gray-700">Execution Time</p>
                          <p className="text-2xl font-bold text-blue-600">{executionTime.toFixed(2)} ms</p>
                          {previousExecutionTime && (
                            <p className={`text-sm ${executionTime < previousExecutionTime ? 'text-green-600' : 'text-red-600'}`}>
                              {executionTime < previousExecutionTime ? '↓ ' : '↑ '}
                              {Math.abs(executionTime - previousExecutionTime).toFixed(2)} ms 
                              {executionTime < previousExecutionTime ? ' faster' : ' slower'} than {previousMethod}
                            </p>
                          )}
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-600">
                            Method: {lastUsedMethod}
                          </p>
                          <p className="text-sm text-gray-600">
                            {executionTime < 100 ? 'Lightning fast! ⚡' : executionTime < 500 ? 'Pretty quick! 🚀' : 'Not too shabby 👍'}
                          </p>
                        </div>
                      </div>
                    )}
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
