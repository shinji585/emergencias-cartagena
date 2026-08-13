import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, Alert } from 'react-native';
import { OpciónEmergencia } from '../../constants/tiposEmergencia';
import { useUbicacion } from '../../hooks/useUbicacion';
import { MapaUbicacion } from '../../components/MapaUbicacion';

interface Props {
  opcion: OpciónEmergencia;
  onAtras: () => void;
  onSiguiente: (datos: { lat: number; lng: number; fotoUrl: string | null; nombre: string; telefono: string }) => void;
}

export const CapturarUbicacionYFotoScreen: React.FC<Props> = ({ opcion, onAtras, onSiguiente }) => {
  const ubicacion = useUbicacion();
  const [fotoSimulada, setFotoSimulada] = useState<string | null>(null);
  const [nombre, setNombre] = useState<string>('');
  const [telefono, setTelefono] = useState<string>('');

  const handleTomarFotoMock = () => {
    setFotoSimulada('data:image/jpeg;base64,evidencia_fotografica_mock_cartagena');
    Alert.alert('Foto capturada', 'Evidencia fotográfica adjuntada correctamente.');
  };

  const handleContinuar = () => {
    if (!telefono || telefono.trim().length < 7) {
      Alert.alert('Teléfono requerido', 'Por favor ingresa tu número de teléfono para la trazabilidad del reporte.');
      return;
    }

    onSiguiente({
      lat: ubicacion.lat,
      lng: ubicacion.lng,
      fotoUrl: fotoSimulada,
      nombre: nombre.trim() || 'Ciudadano Cartagena',
      telefono: telefono.trim(),
    });
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backBtn} onPress={onAtras}>
        <Text style={styles.backText}>← Volver</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Detalles de {opcion.titulo}</Text>

      <MapaUbicacion lat={ubicacion.lat} lng={ubicacion.lng} cargando={ubicacion.cargando} />

      <View style={styles.cameraBox}>
        <Text style={styles.sectionLabel}>📷 Evidencia Fotográfica (Opcional)</Text>
        <TouchableOpacity style={styles.photoBtn} onPress={handleTomarFotoMock}>
          <Text style={styles.photoBtnText}>
            {fotoSimulada ? '✓ Foto Adjuntada (Tocar para cambiar)' : '📸 Tomar Foto del Lugar'}
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.userBox}>
        <Text style={styles.sectionLabel}>👤 Datos de Identidad y Trazabilidad</Text>
        <TextInput
          style={styles.input}
          placeholder="Nombre Completo"
          placeholderTextColor="#64748B"
          value={nombre}
          onChangeText={setNombre}
        />
        <TextInput
          style={styles.input}
          placeholder="Teléfono Celular (*Requerido)"
          placeholderTextColor="#64748B"
          keyboardType="phone-pad"
          value={telefono}
          onChangeText={setTelefono}
        />
      </View>

      <TouchableOpacity style={[styles.submitBtn, { backgroundColor: opcion.color }]} onPress={handleContinuar}>
        <Text style={styles.submitText}>Revisar y Confirmar Reporte ➔</Text>
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
    marginBottom: 10,
  },
  cameraBox: {
    marginVertical: 10,
  },
  sectionLabel: {
    color: '#CBD5E1',
    fontWeight: 'bold',
    fontSize: 13,
    marginBottom: 6,
  },
  photoBtn: {
    backgroundColor: '#1E293B',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#475569',
  },
  photoBtnText: {
    color: '#F8FAFC',
    fontWeight: '600',
  },
  userBox: {
    marginVertical: 10,
  },
  input: {
    backgroundColor: '#1E293B',
    color: '#F8FAFC',
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#334155',
  },
  submitBtn: {
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 'auto',
  },
  submitText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
