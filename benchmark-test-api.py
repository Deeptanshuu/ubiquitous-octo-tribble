import requests
import json
import time

url = "http://localhost:5000/api/recommend"
data = {
    "ingredients": ["chicken", "rice", "onion", "red Chili"],
    "cuisine": "Indian",
    "course": None,
    "veg": False
}

total_og_time = 0
total_bf_time = 0

for _ in range(10):
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

print(f"Average original approach time: {average_og_time:.3f} ms")
print(f"Average brute force approach time: {average_bf_time:.3f} ms")

print(f"Speed Factor: {(average_bf_time/average_og_time):.2f}x times FASATER than brute force approach")

print(data)
# Print recommendations from the original approach
print("\nTF-IDF vector Approach Recommendations:")
for recipe in response.json()['original']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")

# Print recommendations from the brute force approach
print("\nBrute Force Approach Recommendations:")
for recipe in response.json()['brute_force']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")

