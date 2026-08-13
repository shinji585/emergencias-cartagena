import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';

interface Props {
  visible: boolean;
  onClose: () => void;
  onFotoTomada: (dataUri: string) => void;
}

export const CamaraModal: React.FC<Props> = ({
  visible,
  onClose,
  onFotoTomada,
}) => {
  const [permission, requestPermission] = useCameraPermissions();
  const [cargando, setCargando] = useState(false);

  const cameraRef = useRef<CameraView | null>(null);

  useEffect(() => {
    if (visible && !permission?.granted) {
      requestPermission();
    }
  }, [visible, permission?.granted]);

  if (!visible) {
    return null;
  }

  if (!permission) {
    return (
      <View style={styles.overlay}>
        <ActivityIndicator color="#FFF" />
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.overlay}>
        <Text style={styles.error}>
          Permiso de cámara denegado.
        </Text>

        <TouchableOpacity
          onPress={onClose}
          style={styles.closeBtn}
        >
          <Text style={styles.closeText}>Cerrar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleTake = async () => {
    if (!cameraRef.current || cargando) {
      return;
    }

    try {
      setCargando(true);

      const photo = await cameraRef.current.takePictureAsync({
        base64: true,
        quality: 0.7,
      });

      if (photo?.base64) {
        const dataUri = `data:image/jpeg;base64,${photo.base64}`;
        onFotoTomada(dataUri);
      }
    } catch (error) {
      console.error('Error tomando foto:', error);
    } finally {
      setCargando(false);
    }
  };

  return (
    <View style={styles.overlay}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing="back"
      />

      <View style={styles.controls}>
        <TouchableOpacity
          onPress={onClose}
          style={styles.cancelBtn}
          disabled={cargando}
        >
          <Text style={styles.cancelText}>
            Cancelar
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={handleTake}
          style={styles.shutterBtn}
          disabled={cargando}
        >
          {cargando ? (
            <ActivityIndicator color="#000" />
          ) : (
            <View style={styles.shutterInner} />
          )}
        </TouchableOpacity>

        <View style={{ width: 60 }} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
  },

  camera: {
    width: '100%',
    height: '80%',
  },

  controls: {
    width: '100%',
    height: '20%',
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },

  shutterBtn: {
    width: 70,
    height: 70,
    borderRadius: 35,
    borderWidth: 4,
    borderColor: '#FFF',
    justifyContent: 'center',
    alignItems: 'center',
  },

  shutterInner: {
    width: 46,
    height: 46,
    borderRadius: 23,
    backgroundColor: '#FFF',
  },

  cancelBtn: {
    padding: 10,
  },

  cancelText: {
    color: '#FFF',
    fontSize: 16,
  },

  closeBtn: {
    marginTop: 12,
    padding: 8,
    backgroundColor: '#1E293B',
    borderRadius: 8,
  },

  closeText: {
    color: '#FFF',
  },

  error: {
    color: '#F87171',
    fontSize: 16,
  },
});

export default CamaraModal;