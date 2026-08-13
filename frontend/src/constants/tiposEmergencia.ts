import { TipoEmergencia, Organismo } from '../types/reporte';

export interface OpciónEmergencia {
  id: TipoEmergencia;
  titulo: string;
  descripcion: string;
  organismo: Organismo;
  icono: string;
  color: string;
}

export const LISTA_EMERGENCIAS: OpciónEmergencia[] = [
  {
    id: 'accidente',
    titulo: 'Accidente de Tránsito',
    descripcion: 'Choque, colisión o atropello vial con posibles lesionados',
    organismo: 'transito',
    icono: 'car-crash',
    color: '#EF4444' // Red
  },
  {
    id: 'robo_inseguridad',
    titulo: 'Robo / Inseguridad',
    descripcion: 'Hurto, atraco o situación de riesgo policial en curso',
    organismo: 'policia',
    icono: 'shield-alert',
    color: '#F59E0B' // Amber
  },
  {
    id: 'emergencia_medica',
    titulo: 'Emergencia Médica',
    descripcion: 'Persona desmayada, trauma severo o problema de salud grave',
    organismo: 'ambulancia',
    icono: 'medical-bag',
    color: '#10B981' // Emerald
  },
  {
    id: 'incidente_transito',
    titulo: 'Bloqueo / Vía Cerrada',
    descripcion: 'Vía obstaculizada, semáforo dañado o congestión severa',
    organismo: 'transito',
    icono: 'traffic-light',
    color: '#3B82F6' // Blue
  }
];
