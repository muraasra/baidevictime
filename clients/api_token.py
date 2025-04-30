
import requests

endpoints = "http://localhost:8000/api/api-token-auth/"

data = {
    "username": "tayou",
    "password": "6589",
    
}

response = requests.post(endpoints,json=data)

print(response.json())
print(response.status_code)
