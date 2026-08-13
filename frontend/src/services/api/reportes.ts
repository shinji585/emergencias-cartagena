import { apiClient } from './client';
import { ReporteCreate, ReportePublic } from '../../types/reporte';

export async function crearReporte(payload: ReporteCreate): Promise<ReportePublic> {
  try {
    console.debug('[API] crearReporte payload:', payload);
    const res = await apiClient<ReportePublic>('/api/v1/reportes', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    console.debug('[API] crearReporte response:', res);
    return res;
  } catch (err: any) {
    console.error('[API] crearReporte error:', err);
    throw new Error(err?.message || 'Error desconocido al crear el reporte');
  }
}

export async function obtenerHistorialUsuario(usuarioId: string): Promise<ReportePublic[]> {
  try {
    return await apiClient<ReportePublic[]>(`/api/v1/reportes/usuario/${usuarioId}`);
  } catch (err: any) {
    console.error('[API] obtenerHistorialUsuario error:', err);
    throw err;
  }
}

export async function obtenerReporte(reporteId: string): Promise<ReportePublic> {
  try {
    return await apiClient<ReportePublic>(`/api/v1/reportes/${reporteId}`);
  } catch (err: any) {
    console.error('[API] obtenerReporte error:', err);
    throw err;
  }
}

export async function obtenerDespacho(reporteId: string): Promise<any> {
  try {
    return await apiClient<any>(`/api/v1/reportes/${reporteId}/despacho`);
  } catch (err: any) {
    console.error('[API] obtenerDespacho error:', err);
    throw err;
  }
}
