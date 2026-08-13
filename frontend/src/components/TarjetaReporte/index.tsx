import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { ReporteResponse } from '../../types/reporte';

interface Props {
  reporte: ReporteResponse;
}

export const TarjetaReporte: React.FC<Props> = ({ reporte }) => {
  const getSeveridadColor = (sev: string) => {
    switch (sev) {
      case 'grave': return '#EF4444';
      case 'moderado': return '#F59E0B';
      default: return '#10B981';
    }
  };

  return (
    <View style={styles.card}>
      <View style={styles.headerRow}>
        <Text style={styles.tipo}>{reporte.tipo_emergencia.replace('_', ' ').toUpperCase()}</Text>
        <View style={[styles.badge, { backgroundColor: getSeveridadColor(reporte.severidad) }]}>
          <Text style={styles.badgeText}>{reporte.severidad.toUpperCase()}</Text>
        </View>
      </View>
      <Text style={styles.organismo}>Organismo: {reporte.organismo.toUpperCase()}</Text>
      <Text style={styles.estado}>Estado: {reporte.estado.toUpperCase()}</Text>
      {reporte.resumen_ia && (
        <Text style={styles.resumen}>🤖 Resumen IA: {reporte.resumen_ia}</Text>
      )}
      <Text style={styles.fecha}>{new Date(reporte.created_at).toLocaleString()}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    padding: 14,
    borderRadius: 10,
    marginBottom: 10,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  tipo: {
    color: '#F8FAFC',
    fontWeight: 'bold',
    fontSize: 15,
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  badgeText: {
    color: '#FFF',
    fontSize: 10,
    fontWeight: 'bold',
  },
  organismo: {
    color: '#94A3B8',
    fontSize: 12,
  },
  estado: {
    color: '#38BDF8',
    fontSize: 12,
    marginTop: 2,
  },
  resumen: {
    color: '#CBD5E1',
    fontSize: 12,
    marginTop: 6,
    fontStyle: 'italic',
  },
  fecha: {
    color: '#64748B',
    fontSize: 10,
    marginTop: 6,
    textAlign: 'right',
  },
});
