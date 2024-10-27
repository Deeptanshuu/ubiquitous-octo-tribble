import React, { useState, useEffect } from 'react';
import { Send, ChefHat, Search, X, ChevronDown, ChevronUp, Clock, Utensils } from 'lucide-react';
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Checkbox } from "@/components/ui/checkbox"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"

const UnifiedRecipeChatUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [selectedCuisines, setSelectedCuisines] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedCravings, setSelectedCravings] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isVeg, setIsVeg] = useState(false);
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  // Placeholder data (replace with your actual data)
  const ingredients = ['Chicken', 'Pasta', 'Tomatoes', 'Cheese'];
  const cuisines = ['Italian', 'Mexican', 'Chinese', 'Indian'];
  const courses = ['Appetizer', 'Main Course', 'Dessert'];
  const cravings = ['Sweet', 'Savory', 'Spicy'];

  const handleSend = async () => {
    if (input.trim() === '') return;

    setMessages(prev => [...prev, { type: 'user', content: input }]);

    // TODO: Integrate with your TF-IDF and LLaMA backend here
    const botResponse = "Based on your request, I recommend trying a delicious pasta primavera recipe. It's light and fresh, perfect for summer. Here are some suggestions:";

    setTimeout(() => {
      setMessages(prev => [...prev, { type: 'bot', content: botResponse }]);
      handleSubmit();
    }, 1000);

    setInput('');
  };

  const handleSubmit = async () => {
    setLoading(true);
    // TODO: Implement your recipe search logic here
    // For now, we'll just simulate a search with a timeout
    setTimeout(() => {
      setSearchResults([
        { id: 1, title: "Spaghetti Carbonara", description: "Classic Italian pasta dish", cooking_time: 30, servings: 4, difficulty: "Medium", image: "https://example.com/carbonara.jpg" },
        { id: 2, title: "Chicken Tikka Masala", description: "Creamy and spicy Indian curry", cooking_time: 45, servings: 6, difficulty: "Medium", image: "https://example.com/tikka-masala.jpg" },
        { id: 3, title: "Vegetable Stir Fry", description: "Quick and healthy Chinese-inspired dish", cooking_time: 20, servings: 4, difficulty: "Easy", image: "https://example.com/stir-fry.jpg" },
      ]);
      setLoading(false);
    }, 2000);
  };

  const handleIngredientToggle = (ingredient) => {
    setSelectedIngredients(prev =>
      prev.includes(ingredient)
        ? prev.filter(i => i !== ingredient)
        : [...prev, ingredient]
    );
  };

  useEffect(() => {
    // This effect will trigger a new search whenever the filters change
    handleSubmit();
  }, [selectedIngredients, selectedCuisines, selectedCourse, selectedCravings, isVeg]);

  return (
    <Card className="w-full max-w-7xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center">
          <ChefHat className="mr-2" />
          Recipe Chat and Recommendation
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Chat Section */}
          <div className="md:col-span-2">
            <ScrollArea className="h-[600px] pr-4 mb-4">
              {messages.map((message, index) => (
                <div key={index} className={`mb-4 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-2 rounded-lg ${message.type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
                    {message.content}
                  </div>
                  {message.type === 'bot' && searchResults.length > 0 && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                      {searchResults.map((recipe) => (
                        <Card key={recipe.id} className="overflow-hidden">
                          <img src={recipe.image || "/placeholder-image.jpg"} alt={recipe.title} className="w-full h-32 object-cover" />
                          <CardContent className="p-3">
                            <h3 className="text-sm font-semibold mb-1">{recipe.title}</h3>
                            <p className="text-xs text-gray-600 mb-1">{recipe.description}</p>
                            <div className="flex items-center text-xs mb-1">
                              <Clock className="mr-1 text-gray-500" size={12} />
                              <span>{recipe.cooking_time} min</span>
                              <Utensils className="ml-2 mr-1 text-gray-500" size={12} />
                              <span>{recipe.servings} servings</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
                                recipe.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                                recipe.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-red-100 text-red-800'
                              }`}>
                                {recipe.difficulty}
                              </span>
                              <Button size="sm" onClick={() => {/* Handle recipe click */}}>See Recipe</Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </ScrollArea>
            <div className="flex mt-4">
              <Input
                type="text"
                placeholder="Ask for a recipe recommendation..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                className="flex-grow mr-2"
              />
              <Button onClick={handleSend}>
                <Send size={20} />
              </Button>
            </div>
          </div>

          {/* Filters Section */}
          <div>
            <Collapsible open={isFilterOpen} onOpenChange={setIsFilterOpen}>
              <CollapsibleTrigger asChild>
                <Button variant="outline" className="w-full mb-4">
                  {isFilterOpen ? "Hide Filters" : "Show Filters"}
                  {isFilterOpen ? <ChevronUp className="ml-2" size={16} /> : <ChevronDown className="ml-2" size={16} />}
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <Card>
                  <CardHeader>
                    <CardTitle>Refine Your Search</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Ingredients */}
                      <div>
                        <Label>Ingredients</Label>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {ingredients.map(ingredient => (
                            <Button
                              key={ingredient}
                              variant={selectedIngredients.includes(ingredient) ? "secondary" : "outline"}
                              size="sm"
                              onClick={() => handleIngredientToggle(ingredient)}
                            >
                              {ingredient}
                            </Button>
                          ))}
                        </div>
                      </div>

                      {/* Cuisines */}
                      <div>
                        <Label>Cuisines</Label>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {cuisines.map(cuisine => (
                            <Button
                              key={cuisine}
                              variant={selectedCuisines.includes(cuisine) ? "secondary" : "outline"}
                              size="sm"
                              onClick={() => setSelectedCuisines(prev =>
                                prev.includes(cuisine) ? prev.filter(c => c !== cuisine) : [...prev, cuisine]
                              )}
                            >
                              {cuisine}
                            </Button>
                          ))}
                        </div>
                      </div>

                      {/* Course */}
                      <div>
                        <Label>Course</Label>
                        <RadioGroup onValueChange={setSelectedCourse} value={selectedCourse}>
                          {courses.map(course => (
                            <div key={course} className="flex items-center space-x-2">
                              <RadioGroupItem value={course} id={course} />
                              <Label htmlFor={course}>{course}</Label>
                            </div>
                          ))}
                        </RadioGroup>
                      </div>

                      {/* Cravings */}
                      <div>
                        <Label>Cravings</Label>
                        <div className="flex flex-wrap gap-4 mt-2">
                          {cravings.map(craving => (
                            <div key={craving} className="flex items-center space-x-2">
                              <Checkbox
                                id={craving}
                                checked={selectedCravings.includes(craving)}
                                onCheckedChange={(checked) => {
                                  if (checked) {
                                    setSelectedCravings(prev => [...prev, craving]);
                                  } else {
                                    setSelectedCravings(prev => prev.filter(c => c !== craving));
                                  }
                                }}
                              />
                              <label htmlFor={craving}>{craving}</label>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Veg Toggle */}
                      <div className="flex items-center space-x-2">
                        <Checkbox
                          id="veg"
                          checked={isVeg}
                          onCheckedChange={setIsVeg}
                        />
                        <label htmlFor="veg">Vegetarian Only</label>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </CollapsibleContent>
            </Collapsible>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default UnifiedRecipeChatUI;
