import requests

url = "http://localhost:5000/api/recommend"
data = {
    "ingredients": ["curry paste", "coconut milk", "vegetables", "chicken"],
    "course": "Main Course"
}

response = requests.post(url, json=data)
print(response.json())