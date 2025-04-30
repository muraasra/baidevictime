// frontend/src/Map.tsx
import React, { useEffect, useRef } from 'react';

// Définir les types pour les props
interface Service {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

interface MapProps {
  center: google.maps.LatLngLiteral;
  services: Service[];
  selectedService?: Service; // Peut être undefined si aucun service n'est sélectionné
}

const Map: React.FC<MapProps> = ({ center, services, selectedService }) => {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<google.maps.Map | null>(null);
  const markersRef = useRef<google.maps.Marker[]>([]);

  useEffect(() => {
    // Initialiser la carte Google Maps une fois que le composant est monté
    if (mapRef.current && !mapInstanceRef.current) {
      // Créer la carte centrée sur 'center'
      mapInstanceRef.current = new google.maps.Map(mapRef.current, {
        center: center,
        zoom: 13,
      });
    }
  }, [center]);

  useEffect(() => {
    // Mettre à jour les marqueurs dès que la liste des services change
    if (!mapInstanceRef.current) return;

    markersRef.current.forEach((marker) => marker.setMap(null));
    markersRef.current = [];

    services.forEach((service) => {
      const marker = new google.maps.Marker({
        position: { lat: service.latitude, lng: service.longitude },
        map: mapInstanceRef.current,
        title: service.name,
      });

      if (selectedService && service.id === selectedService.id) {
        marker.setAnimation(google.maps.Animation.BOUNCE);
      }

      markersRef.current.push(marker);
    });
  }, [services, selectedService]);

  return (
    <div ref={mapRef} style={{ width: '100%', height: '500px' }} />
  );
};

export default Map;
