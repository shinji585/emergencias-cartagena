import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface Props {
  lat: number;
  lng: number;
  cargando: boolean;
}

export const MapaUbicacion: React.FC<Props> = ({ lat, lng, cargando }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>📍 Ubicación GPS Capturada</Text>
      {cargando ? (
        <Text style={styles.texto}>Obteniendo coordenadas GPS...</Text>
      ) : (
        <View style={styles.coordsBox}>
          <Text style={styles.coordLabel}>Latitud: <Text style={styles.coordValue}>{lat.toFixed(6)}</Text></Text>
          <Text style={styles.coordLabel}>Longitud: <Text style={styles.coordValue}>{lng.toFixed(6)}</Text></Text>
        </View>
      )}
      <Text style={styles.nota}>Se adjuntará automáticamente a tu reporte.</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#0F172A',
    padding: 14,
    borderRadius: 10,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: '#334155',
  },
  header: {
    color: '#38BDF8',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  coordsBox: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 4,
  },
  coordLabel: {
    color: '#94A3B8',
    fontSize: 13,
  },
  coordValue: {
    color: '#F8FAFC',
    fontWeight: 'bold',
  },
  texto: {
    color: '#CBD5E1',
    fontSize: 13,
  },
  nota: {
    color: '#64748B',
    fontSize: 11,
    marginTop: 6,
    fontStyle: 'italic',
  },
});
