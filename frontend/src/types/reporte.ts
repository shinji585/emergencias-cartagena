export type TipoEmergencia = 'accidente' | 'robo_inseguridad' | 'emergencia_medica' | 'incidente_transito';

export type Severidad = 'leve' | 'moderado' | 'grave';

export type EstadoReporte = 'pendiente' | 'en_atencion' | 'resuelto' | 'descartado';

export type Organismo = 'policia' | 'transito' | 'ambulancia';

export interface ReporteCreatePayload {
  tipo_emergencia: TipoEmergencia;
  ubicacion_lat: number;
  ubicacion_lng: number;
  foto_url?: string | null;
  descripcion?: string | null;
  organismo: Organismo;
  usuario_id?: string | null;
  usuario_nombre?: string | null;
  usuario_telefono?: string | null;
}

export interface ReporteResponse {
  id: string;
  tipo_emergencia: TipoEmergencia;
  ubicacion_lat: number;
  ubicacion_lng: number;
  foto_url?: string | null;
  organismo: Organismo;
  usuario_id: string;
  severidad: Severidad;
  estado: EstadoReporte;
  resumen_ia?: string | null;
  grupo_incidente_id?: string | null;
  created_at: string;
  updated_at?: string | null;
}

// Compatibilidad con nombres usados en servicios
export type ReporteCreate = ReporteCreatePayload;
export type ReportePublic = ReporteResponse;
