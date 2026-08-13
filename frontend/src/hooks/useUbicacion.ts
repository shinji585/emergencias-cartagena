import { useState, useEffect } from 'react';
import * as Location from 'expo-location';

export interface UbicacionEstado {
  lat: number;
  lng: number;
  cargando: boolean;
  error: string | null;
}

export function useUbicacion(): UbicacionEstado {
  const [estado, setEstado] = useState<UbicacionEstado>({
    lat: 10.399722, // Cartagena centro por defecto
    lng: -75.514444,
    cargando: true,
    error: null,
  });

  useEffect(() => {
    (async () => {
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          setEstado(prev => ({
            ...prev,
            cargando: false,
            error: 'Permiso de ubicación denegado. Usando ubicación estimada de Cartagena.',
          }));
          return;
        }

        const location = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.High,
        });

        setEstado({
          lat: location.coords.latitude,
          lng: location.coords.longitude,
          cargando: false,
          error: null,
        });
      } catch (err: any) {
        setEstado(prev => ({
          ...prev,
          cargando: false,
          error: 'No se pudo obtener la posición GPS actual.',
        }));
      }
    })();
  }, []);

  return estado;
}
