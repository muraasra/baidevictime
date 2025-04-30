import requests

# URL de la ressource à mettre à jour
endpoints = "http://localhost:8000/api/services/2/"

# Données mises à jour
data = {
    "name": "Service Mis à Jour",
    "category_id": 1,
    "address": "Adresse Mise à Jour",
    "phone": "123456789",
    "latitude": 12.34,
    "longitude": 56.78
}

# Requête PUT
response = requests.put(endpoints, json=data)
# Vérification de la réponse
if response.status_code == 200:
    print("Mise à jour réussie !")



# Résultats
print(response.json())  # Réponse JSON du serveur
print(response.status_code)  # Code HTTP de la réponse
