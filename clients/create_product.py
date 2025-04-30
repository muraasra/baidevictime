import requests

endpoints = "http://localhost:8000/api/services/"

data = {
    "name": "Blabla",
    "category_id": 1,
    "address": "Blabla Blabla",
    "phone": "65895",
    "latitude": 10.5,  # Utilisez None ici
    "longitude": 11.6  # Utilisez None ici
}

response = requests.post(endpoints,json=data)

print(response.json())
print(response.status_code)
