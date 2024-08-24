import requests
import json

url = "http://localhost:5000/api/recommend"
data = {
    "ingredients": ["chicken", "rice", "onion"],
    "cuisine": "Italian",
    "course": "Main Course",
    "veg": False
}


response = requests.post(url, json=data)
results = response.json()

# Print execution times
og_time = results['original']['execution_time']*100
bf_time = results['brute_force']['execution_time']*100

print(f"Original approach time: {og_time:.3f} ms")
print(f"Brute force approach time: {bf_time:.3f} ms")

print(f"Speed Factor: {(bf_time/og_time):.2f}x times FASATER than brute force approach")

print(data)
# Print recommendations from the original approach
print("\nTF-IDF vector Approach Recommendations:")
for recipe in results['original']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")

# Print recommendations from the brute force approach
print("\nBrute Force Approach Recommendations:")
for recipe in results['brute_force']['recommendations']:
    print(f"ID: {recipe['id']}, Title: {recipe['title']}")
