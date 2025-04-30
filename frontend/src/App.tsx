// frontend/src/App.tsx
import React, { useEffect, useState } from 'react';
import Map from './Map'; // Le composant de la carte créé plus haut


// Définir les types pour les catégories et services
interface Category {
  id: number;
  name: string;
}

interface Service {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  address: string;
  phone: string;
  distanceKm?: number; // Optionnel
  category: Category;
}

interface Location {
  lat: number;
  lng: number;
}
// frontend/src/utils/distance.ts
export function haversineDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Rayon de la Terre en km
  const rad = Math.PI / 180;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  return distance;
}

const App: React.FC = () => {
  const [userLocation, setUserLocation] = useState<Location>({ lat: 48.8566, lng: 2.3522 }); // Position par défaut (Paris)
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);

  // Obtenir la position de l'utilisateur
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = position.coords;
          setUserLocation({ lat: coords.latitude, lng: coords.longitude });
          console.log("Position de l'utilisateur :", coords.latitude, coords.longitude);
        },
        (error) => {
          console.error("Erreur de géolocalisation :", error);
          // Si refus ou erreur, garder la position par défaut
        }
      );
    }
  }, []);

  // Récupérer la liste de tous les services depuis l'API Django
  useEffect(() => {
    fetch('/api/services/')
      .then((res) => res.json())
      .then((data: Service[]) => {
        setServices(data);
      })
      .catch((err) => console.error("Erreur API services :", err));
  }, []);

  // Filtrer les services et trouver le plus proche lorsque la catégorie est sélectionnée
  useEffect(() => {
    if (selectedCategory && services.length > 0) {
      const servicesFiltres = services.filter((s) => s.category.id === selectedCategory.id);

      if (servicesFiltres.length > 0) {
        let serviceLePlusProche: Service | null = null;
        let distanceMin = Infinity;

        servicesFiltres.forEach((s) => {
          const d = haversineDistance(userLocation.lat, userLocation.lng, s.latitude, s.longitude);
          if (d < distanceMin) {
            distanceMin = d;
            serviceLePlusProche = s;
          }
        });

        setSelectedService(serviceLePlusProche);
      } else {
        setSelectedService(null); // Aucun service trouvé
      }
    } else {
      setSelectedService(null); // Aucun service trouvé ou aucune catégorie sélectionnée
    }
  }, [selectedCategory, services, userLocation]);

  return (
    <div className="App">
      <h1>Services d’aide aux victimes</h1>
      {/* Composants Questionnaire ou CategorySelector imaginés */}
      <Map
        center={userLocation}
        services={
          selectedCategory ? services.filter((s) => s.category.id === selectedCategory.id) : services
        }
        selectedService={selectedService}
      />
      {selectedService && (
        <div className="info-service">
          <h2>Service le plus proche : {selectedService.name}</h2>
          <p>Catégorie : {selectedService.category.name}</p>
          <p>Adresse : {selectedService.address}</p>
          <p>Téléphone : {selectedService.phone}</p>
          <p>Distance : {selectedService.distanceKm?.toFixed(1)} km</p>
        </div>
      )}
    </div>
  );
};

export default App;
