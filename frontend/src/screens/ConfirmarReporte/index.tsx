import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { OpciónEmergencia } from '../../constants/tiposEmergencia';
import { crearReporte } from '../../services/api/reportes';

interface Props {
  opcion: OpciónEmergencia;
  datos: {
    lat: number;
    lng: number;
    fotoUrl: string | null;
    nombre: string;
    telefono: string;
  };
  onAtras: () => void;
  onExito: (reporteId: string) => void;
}

export const ConfirmarReporteScreen: React.FC<Props> = ({ opcion, datos, onAtras, onExito }) => {
  const [enviando, setEnviando] = useState(false);

  const handleEnviar = async () => {
    setEnviando(true);
    try {
      const respuesta = await crearReporte({
        tipo_emergencia: opcion.id,
        ubicacion_lat: datos.lat,
        ubicacion_lng: datos.lng,
        foto_url: datos.fotoUrl,
        organismo: opcion.organismo,
        usuario_nombre: datos.nombre,
        usuario_telefono: datos.telefono,
      });

      Alert.alert(
        '🚨 Reporte Recibido',
        `Tu reporte ha sido enviado al equipo de ${opcion.organismo.toUpperCase()}.\n\nSeveridad clasificada por IA: ${respuesta.severidad.toUpperCase()}\nID: ${respuesta.id.slice(0, 8)}`,
        [{ text: 'Entendido', onPress: () => onExito(respuesta.id) }]
      );
    } catch (err: any) {
      Alert.alert(
        'Atención',
        'No se pudo conectar con el servidor backend. Revisa que el backend en Docker esté activo.\n\nError: ' + err.message
      );
    } finally {
      setEnviando(false);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backBtn} onPress={onAtras} disabled={enviando}>
        <Text style={styles.backText}>← Modificar Datos</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Confirmar Envío de Emergencia</Text>

      <View style={styles.summaryCard}>
        <Text style={styles.summaryTipo}>{opcion.titulo}</Text>
        <Text style={styles.summaryItem}>🏛️ Destino: <Text style={styles.bold}>{opcion.organismo.toUpperCase()}</Text></Text>
        <Text style={styles.summaryItem}>📍 GPS: {datos.lat.toFixed(5)}, {datos.lng.toFixed(5)}</Text>
        <Text style={styles.summaryItem}>👤 Reportante: {datos.nombre} ({datos.telefono})</Text>
        <Text style={styles.summaryItem}>📸 Foto adjunta: {datos.fotoUrl ? 'Sí' : 'No'}</Text>
      </View>

      {/* Aviso legal explicito de trazabilidad exigido en seccion 1.4 */}
      <View style={styles.legalNotice}>
        <Text style={styles.legalTitle}>⚠️ AVISO LEGAL Y RESPONSABILIDAD</Text>
        <Text style={styles.legalBody}>
          Este reporte quedará registrado con tu ubicación GPS exacta, marca de tiempo e identidad ({datos.telefono}). 
          Las falsas alarmas o reportes mal intencionados constituyen un delito penado por la ley y serán remitidos a las autoridades competentes.
        </Text>
      </View>

      <TouchableOpacity
        style={[styles.sendBtn, { backgroundColor: opcion.color }, enviando && styles.disabledBtn]}
        onPress={handleEnviar}
        disabled={enviando}
      >
        {enviando ? (
          <ActivityIndicator color="#FFF" />
        ) : (
          <Text style={styles.sendBtnText}>ENVIAR REPORTE AHORA 🚨</Text>
        )}
      </TouchableOpacity>
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
    marginBottom: 16,
  },
  summaryCard: {
    backgroundColor: '#1E293B',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  summaryTipo: {
    color: '#38BDF8',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  summaryItem: {
    color: '#CBD5E1',
    fontSize: 14,
    marginBottom: 6,
  },
  bold: {
    fontWeight: 'bold',
    color: '#F8FAFC',
  },
  legalNotice: {
    backgroundColor: '#451A03',
    borderColor: '#F59E0B',
    borderWidth: 1,
    padding: 14,
    borderRadius: 10,
    marginBottom: 20,
  },
  legalTitle: {
    color: '#F59E0B',
    fontWeight: 'bold',
    fontSize: 12,
    marginBottom: 4,
  },
  legalBody: {
    color: '#FEF3C7',
    fontSize: 11,
    lineHeight: 16,
  },
  sendBtn: {
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 'auto',
  },
  disabledBtn: {
    opacity: 0.6,
  },
  sendBtnText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 18,
  },
});
