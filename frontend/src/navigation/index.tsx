import React, { useState } from 'react';
import { OpciónEmergencia } from '../constants/tiposEmergencia';
import { SeleccionarTipoEmergenciaScreen } from '../screens/SeleccionarTipoEmergencia';
import { CapturarUbicacionYFotoScreen } from '../screens/CapturarUbicacionYFoto';
import { ConfirmarReporteScreen } from '../screens/ConfirmarReporte';
import { HistorialReportesScreen } from '../screens/HistorialReportes';

type Pantalla = 'SELECCIONAR_TIPO' | 'CAPTURAR_DATOS' | 'CONFIRMAR' | 'HISTORIAL';

export const AppNavigator: React.FC = () => {
  const [pantallaActual, setPantallaActual] = useState<Pantalla>('SELECCIONAR_TIPO');
  const [emergenciaSeleccionada, setEmergenciaSeleccionada] = useState<OpciónEmergencia | null>(null);
  const [datosFormulario, setDatosFormulario] = useState<{
    lat: number;
    lng: number;
    fotoUrl: string | null;
    nombre: string;
    telefono: string;
    descripcion?: string | null;
  } | null>(null);

  const handleSeleccionarTipo = (opcion: OpciónEmergencia) => {
    setEmergenciaSeleccionada(opcion);
    setPantallaActual('CAPTURAR_DATOS');
  };

  const handleDatosCapturados = (datos: {
    lat: number;
    lng: number;
    fotoUrl: string | null;
    nombre: string;
    telefono: string;
    descripcion?: string | null;
  }) => {
    setDatosFormulario(datos);
    setPantallaActual('CONFIRMAR');
  };

  const handleReporteExitoso = () => {
    setPantallaActual('HISTORIAL');
  };

  switch (pantallaActual) {
    case 'SELECCIONAR_TIPO':
      return (
        <SeleccionarTipoEmergenciaScreen
          onSiguiente={handleSeleccionarTipo}
          onVerHistorial={() => setPantallaActual('HISTORIAL')}
        />
      );

    case 'CAPTURAR_DATOS':
      if (!emergenciaSeleccionada) return null;
      return (
        <CapturarUbicacionYFotoScreen
          opcion={emergenciaSeleccionada}
          onAtras={() => setPantallaActual('SELECCIONAR_TIPO')}
          onSiguiente={handleDatosCapturados}
        />
      );

    case 'CONFIRMAR':
      if (!emergenciaSeleccionada || !datosFormulario) return null;
      return (
        <ConfirmarReporteScreen
          opcion={emergenciaSeleccionada}
          datos={datosFormulario}
          onAtras={() => setPantallaActual('CAPTURAR_DATOS')}
          onExito={handleReporteExitoso}
        />
      );

    case 'HISTORIAL':
      return (
        <HistorialReportesScreen
          onVolver={() => setPantallaActual('SELECCIONAR_TIPO')}
        />
      );

    default:
      return null;
  }
};
