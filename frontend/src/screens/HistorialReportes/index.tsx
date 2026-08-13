import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';
import { ReporteResponse } from '../../types/reporte';
import { obtenerHistorialUsuario } from '../../services/api/reportes';
import { TarjetaReporte } from '../../components/TarjetaReporte';

interface Props {
  onVolver: () => void;
}

export const HistorialReportesScreen: React.FC<Props> = ({ onVolver }) => {
  const [reportes, setReportes] = useState<ReporteResponse[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const datos = await obtenerHistorialUsuario('demo-user');
        setReportes(datos);
      } catch (err) {
        // Fallback demo array for offline mode UI check
        setReportes([]);
      } finally {
        setCargando(false);
      }
    })();
  }, []);

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backBtn} onPress={onVolver}>
        <Text style={styles.backText}>← Volver a Inicio</Text>
      </TouchableOpacity>

      <Text style={styles.title}>📋 Historial de Mis Reportes</Text>

      {cargando ? (
        <ActivityIndicator color="#38BDF8" style={{ marginTop: 40 }} />
      ) : reportes.length === 0 ? (
        <View style={styles.emptyBox}>
          <Text style={styles.emptyText}>No tienes reportes recientes registrados.</Text>
        </View>
      ) : (
        <FlatList
          data={reportes}
          keyExtractor={item => item.id}
          renderItem={({ item }) => <TarjetaReporte reporte={item} />}
          contentContainerStyle={{ paddingVertical: 10 }}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
    padding: 20,
  },
  backBtn: {
    marginTop: 10,
    marginBottom: 10,
  },
  backText: {
    color: '#38BDF8',
    fontSize: 14,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#F8FAFC',
    marginBottom: 10,
  },
  emptyBox: {
    marginTop: 50,
    alignItems: 'center',
  },
  emptyText: {
    color: '#64748B',
    fontSize: 14,
  },
});
