import requests

url = "http://localhost:5000/api/recommend"
data = {
    "ingredients": ["tomatoes",
    "onions",
    "garlic",
    "vegetable",
    "broth",
    "cream",
    "basil"],
    "course": "Main Course",
    "veg": True
}

response = requests.post(url, json=data)
print(response.json())