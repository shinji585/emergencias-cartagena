import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { LISTA_EMERGENCIAS, OpciónEmergencia } from '../../constants/tiposEmergencia';
import { BotonTipoEmergencia } from '../../components/BotonTipoEmergencia';

interface Props {
  onSiguiente: (opcion: OpciónEmergencia) => void;
  onVerHistorial: () => void;
}

export const SeleccionarTipoEmergenciaScreen: React.FC<Props> = ({ onSiguiente, onVerHistorial }) => {
  const [seleccionada, setSeleccionada] = useState<OpciónEmergencia | null>(null);

  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>🚨 Emergencias Cartagena</Text>
      <Text style={styles.subtitle}>Selecciona el tipo de emergencia para reportar al instante:</Text>

      <ScrollView style={styles.scroll}>
        {LISTA_EMERGENCIAS.map(opcion => (
          <BotonTipoEmergencia
            key={opcion.id}
            opcion={opcion}
            seleccionado={seleccionada?.id === opcion.id}
            onSelect={setSeleccionada}
          />
        ))}
      </ScrollView>

      {seleccionada && (
        <TouchableOpacity
          style={[styles.botonContinuar, { backgroundColor: seleccionada.color }]}
          onPress={() => onSiguiente(seleccionada)}
        >
          <Text style={styles.textoBoton}>Continuar con {seleccionada.titulo} ➔</Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity style={styles.botonHistorial} onPress={onVerHistorial}>
        <Text style={styles.textoHistorial}>📋 Ver Mis Reportes Anteriores</Text>
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
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#F8FAFC',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 14,
    color: '#94A3B8',
    marginVertical: 10,
  },
  scroll: {
    flex: 1,
    marginVertical: 10,
  },
  botonContinuar: {
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 10,
  },
  textoBoton: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
  botonHistorial: {
    padding: 12,
    alignItems: 'center',
  },
  textoHistorial: {
    color: '#38BDF8',
    fontSize: 14,
  },
});
