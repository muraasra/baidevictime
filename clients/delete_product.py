import requests

endpoints = "http://localhost:8000/api/services/3/"


response = requests.delete(endpoints)

print(response)
print(response.status_code)
