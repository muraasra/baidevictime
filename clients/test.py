import requests

endpoints = "http://localhost:8000/api/services"

response = requests.get(endpoints)

print (response.json())
print (response.status_code)