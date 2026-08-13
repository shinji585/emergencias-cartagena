import React from 'react';
import { TouchableOpacity, Text, StyleSheet, View } from 'react-native';
import { OpciónEmergencia } from '../../constants/tiposEmergencia';

interface Props {
  opcion: OpciónEmergencia;
  seleccionado: boolean;
  onSelect: (opcion: OpciónEmergencia) => void;
}

export const BotonTipoEmergencia: React.FC<Props> = ({ opcion, seleccionado, onSelect }) => {
  return (
    <TouchableOpacity
      style={[
        styles.card,
        { borderColor: opcion.color },
        seleccionado && { backgroundColor: opcion.color + '22', borderWidth: 2 }
      ]}
      activeOpacity={0.8}
      onPress={() => onSelect(opcion)}
    >
      <View style={[styles.badge, { backgroundColor: opcion.color }]}>
        <Text style={styles.badgeText}>{opcion.organismo.toUpperCase()}</Text>
      </View>
      <Text style={styles.titulo}>{opcion.titulo}</Text>
      <Text style={styles.descripcion}>{opcion.descripcion}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
  },
  badge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    marginBottom: 8,
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: 'bold',
  },
  titulo: {
    color: '#F8FAFC',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  descripcion: {
    color: '#94A3B8',
    fontSize: 13,
  },
});
