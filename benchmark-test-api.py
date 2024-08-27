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
    {
        "ingredients": ["tomato", "basil", "mozzarella", "olive oil"],
        "cuisine": "Italian",
        "course": "Appetizer",
        "craving": None,
        "veg": True
    },
    {
        "ingredients": ["onion", "potato", "carrot", "garlic"],
        "cuisine": "American",
        "course": "Main Course",
        "craving": None,
        "veg": False
    },
    {
        "ingredients": ["tofu", "soy sauce", "ginger", "scallion"],
        "craving": None,
        "cuisine": None,
        "craving": None,
        "veg": True
    },
    {
        "ingredients":["egg noodles ","rice noodles ","ginger ","tomatoes "],
        "craving": None,
        "cuisine": None,
        "craving": None,
        "veg": False
    },
    {   "ingredients":["flour ","chocolate ","butter ","sugar ","eggs "],
        "craving": None,
        "cuisine": None,
        "course": "Dessert",
        "veg": False
     }
]

total_og_time = 0
total_bf_time = 0

for _ in range(10):
    data = random.choice(data_list)  # Randomly select data
    start_time = time.time()
    response = requests.post(url, json=data)
    end_time = time.time()
    total_og_time += (end_time - start_time) * 100

    start_time = time.time()
    response = requests.post(url, json={**data, "brute_force": True})
    end_time = time.time()
    total_bf_time += (end_time - start_time) * 100

average_og_time = total_og_time / 10
average_bf_time = total_bf_time / 10

print(f"Average TF-IDF Vectorized approach time: {average_og_time:.3f} ms")
print(f"Average brute force approach time: {average_bf_time:.3f} ms")
print(f"Speed Factor: {(average_bf_time/average_og_time):.2f}x times FASTER than brute force approach")

#print(data_list)

# Print recommendations from the original approach
'''
print("\nTF-IDF vector Approach Recommendations:")
for recipe in response.json()['original']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")

# Print recommendations from the brute force approach
print("\nBrute Force Approach Recommendations:")
for recipe in response.json()['brute_force']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")
'''