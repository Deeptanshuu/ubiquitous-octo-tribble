import requests
import json
import time
import random


url = "http://localhost:5000/api/recommend"


data_list = [
    {
        "ingredients": ["chicken", "rice", "onion", "red Chili", "egg noodles ","rice noodles ","ginger ","tomatoes "],
        "cuisine": "Indian",
        "course": None,
        "craving": None,
        "veg": False
    },
]

data = data_list[0]
response = requests.post(url, json=data)

print("\nBert Approach Recommendations:")
for recipe in response.json():
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")